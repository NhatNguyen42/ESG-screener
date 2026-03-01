"""
Pre-computed FinBERT-style sentiment analysis.
In production, this would call the HuggingFace Inference API.
For the demo, we use cached realistic results.
"""
from __future__ import annotations

import os
import httpx
from app.data.securities import SECURITIES

# ---------------------------------------------------------------------------
# Pre-computed sentiment cache (simulates FinBERT output)
# ---------------------------------------------------------------------------

SENTIMENT_CACHE: dict[str, dict] = {
    "MSFT": {
        "sentiment_score": 0.82,
        "label": "Bullish",
        "key_topics": ["AI cloud growth", "ESG leadership", "Carbon negative by 2030"],
        "controversy_flag": False,
        "summary": "Strong ESG positioning with industry-leading carbon negative commitment. AI investments driving revenue growth while maintaining responsible AI principles.",
    },
    "GOOGL": {
        "sentiment_score": 0.65,
        "label": "Moderately Bullish",
        "key_topics": ["AI dominance", "Data privacy concerns", "Renewable energy"],
        "controversy_flag": True,
        "summary": "Leading AI innovation with significant renewable energy investments, but faces ongoing scrutiny over data privacy practices and antitrust concerns.",
    },
    "TSLA": {
        "sentiment_score": 0.55,
        "label": "Neutral",
        "key_topics": ["EV market leader", "Governance concerns", "Green revenue"],
        "controversy_flag": True,
        "summary": "Dominant EV position with near-100% green revenue, but governance controversies and executive behavior weigh on ESG sentiment.",
    },
    "NVDA": {
        "sentiment_score": 0.78,
        "label": "Bullish",
        "key_topics": ["AI chip dominance", "Energy efficiency", "Supply chain"],
        "controversy_flag": False,
        "summary": "AI infrastructure backbone with improving energy efficiency per compute cycle. Strong growth trajectory with manageable ESG risks.",
    },
    "AAPL": {
        "sentiment_score": 0.75,
        "label": "Bullish",
        "key_topics": ["Carbon neutral products", "Supply chain scrutiny", "Privacy focus"],
        "controversy_flag": False,
        "summary": "Industry leader in product lifecycle carbon neutrality. Privacy-first approach differentiates positively, though supply chain labor practices face scrutiny.",
    },
    "XOM": {
        "sentiment_score": -0.35,
        "label": "Bearish",
        "key_topics": ["Fossil fuel exposure", "Greenwashing allegations", "Transition risk"],
        "controversy_flag": True,
        "summary": "Significant transition risk as energy landscape shifts. ESG funds increasingly excluding pure-play fossil fuel companies despite profitability.",
    },
    "CVX": {
        "sentiment_score": -0.25,
        "label": "Moderately Bearish",
        "key_topics": ["Oil dependency", "Hydrogen investments", "Climate litigation"],
        "controversy_flag": True,
        "summary": "Modest clean energy investments insufficient to offset core fossil fuel concerns. Faces growing climate-related litigation risk.",
    },
    "BLK": {
        "sentiment_score": 0.70,
        "label": "Bullish",
        "key_topics": ["ESG investing pioneer", "Aladdin platform", "Stewardship"],
        "controversy_flag": False,
        "summary": "World's largest asset manager with ESG integration across product suite. Aladdin platform increasingly embedding sustainability analytics.",
    },
    "NEE": {
        "sentiment_score": 0.85,
        "label": "Very Bullish",
        "key_topics": ["Largest renewable utility", "Clean energy transition", "Policy tailwinds"],
        "controversy_flag": False,
        "summary": "America's largest generator of renewable energy from wind and solar. Benefiting from IRA subsidies and accelerating grid decarbonization.",
    },
    "ENPH": {
        "sentiment_score": 0.72,
        "label": "Bullish",
        "key_topics": ["Solar microinverters", "Residential solar growth", "Margin pressure"],
        "controversy_flag": False,
        "summary": "Leading solar microinverter technology enabling residential clean energy adoption. Faces near-term margin pressure but long-term growth intact.",
    },
    "ICLN": {
        "sentiment_score": 0.68,
        "label": "Moderately Bullish",
        "key_topics": ["Clean energy basket", "Policy dependent", "Global diversification"],
        "controversy_flag": False,
        "summary": "Broad clean energy ETF offering diversified exposure to the green transition. Performance tied to policy support and interest rate environment.",
    },
    "LMT": {
        "sentiment_score": -0.15,
        "label": "Moderately Bearish",
        "key_topics": ["Defense spending", "ESG exclusion", "Weapons systems"],
        "controversy_flag": True,
        "summary": "Strong financials from defense contracts but increasingly excluded from ESG portfolios due to weapons manufacturing involvement.",
    },
    "JNJ": {
        "sentiment_score": 0.60,
        "label": "Moderately Bullish",
        "key_topics": ["Healthcare access", "Litigation overhang", "R&D pipeline"],
        "controversy_flag": True,
        "summary": "Solid ESG profile in healthcare access and R&D, but ongoing talc litigation creates governance risk.",
    },
    "COST": {
        "sentiment_score": 0.62,
        "label": "Moderately Bullish",
        "key_topics": ["Fair labor practices", "Sustainability packaging", "Organic growth"],
        "controversy_flag": False,
        "summary": "Above-average labor practices and expanding sustainable product lines. Growing organic and sustainable product offerings.",
    },
    "PLD": {
        "sentiment_score": 0.58,
        "label": "Moderately Bullish",
        "key_topics": ["Green buildings", "Solar installations", "E-commerce logistics"],
        "controversy_flag": False,
        "summary": "Leading industrial REIT with significant solar rooftop installations. Supporting e-commerce while investing in building efficiency.",
    },
    "PLUG": {
        "sentiment_score": 0.45,
        "label": "Neutral",
        "key_topics": ["Green hydrogen", "Cash burn", "Scaling challenges"],
        "controversy_flag": False,
        "summary": "Pure-play green hydrogen company with ambitious growth plans. High cash burn rate and execution risk temper otherwise strong ESG narrative.",
    },
    "CRWD": {
        "sentiment_score": 0.60,
        "label": "Moderately Bullish",
        "key_topics": ["Cybersecurity demand", "Data governance", "Digital infrastructure protection"],
        "controversy_flag": False,
        "summary": "Essential cybersecurity provider protecting digital infrastructure. Strong governance practices in data handling and incident response.",
    },
    "SPY": {
        "sentiment_score": 0.50,
        "label": "Neutral",
        "key_topics": ["Broad market exposure", "Mixed ESG profile", "Index benchmark"],
        "controversy_flag": False,
        "summary": "S&P 500 benchmark with inherently mixed ESG exposure across all sectors including fossil fuels and defense.",
    },
    "ESGU": {
        "sentiment_score": 0.75,
        "label": "Bullish",
        "key_topics": ["ESG screened US equities", "Low cost", "Broad exposure"],
        "controversy_flag": False,
        "summary": "iShares ESG Aware MSCI USA ETF providing broad US equity exposure with ESG screening. Low cost ESG integration.",
    },
    "NOVO-B.CO": {
        "sentiment_score": 0.80,
        "label": "Bullish",
        "key_topics": ["GLP-1 dominance", "Access to medicine", "Nordic governance"],
        "controversy_flag": False,
        "summary": "Global leader in diabetes/obesity treatment with strong Nordic governance standards. Expanding access to medicine initiatives across emerging markets.",
    },
}


async def get_sentiment(ticker: str) -> dict:
    """Get sentiment for a ticker - cached or via HuggingFace API."""
    # Check cache first
    if ticker in SENTIMENT_CACHE:
        return {"ticker": ticker, **SENTIMENT_CACHE[ticker]}

    # Try HuggingFace API if token available
    hf_token = os.getenv("HF_API_TOKEN")
    if hf_token and os.getenv("AI_PROVIDER", "mock") != "mock":
        try:
            return await _call_hf_sentiment(ticker, hf_token)
        except Exception:
            pass

    # Fallback: generate from security data
    return _generate_fallback_sentiment(ticker)


def _generate_fallback_sentiment(ticker: str) -> dict:
    """Generate reasonable sentiment from security ESG data."""
    sec_map = {s["ticker"]: s for s in SECURITIES}
    s = sec_map.get(ticker)

    if s is None:
        return {
            "ticker": ticker,
            "sentiment_score": 0.0,
            "label": "Unknown",
            "key_topics": [],
            "controversy_flag": False,
            "summary": f"No data available for {ticker}.",
        }

    esg = s["esg_overall"]
    controversy = s["controversy_score"]

    # Score: normalize ESG to [-1, 1] range, with controversy penalty
    score = (esg - 50) / 50 - controversy * 0.1
    score = max(-1, min(1, score))

    if score > 0.5:
        label = "Bullish"
    elif score > 0.2:
        label = "Moderately Bullish"
    elif score > -0.2:
        label = "Neutral"
    elif score > -0.5:
        label = "Moderately Bearish"
    else:
        label = "Bearish"

    topics = []
    if esg >= 70:
        topics.append("Strong ESG profile")
    if s["green_revenue_pct"] > 50:
        topics.append("High green revenue")
    if s["carbon_intensity"] > 200:
        topics.append("High carbon exposure")
    if controversy >= 3:
        topics.append("Controversy concerns")
    topics.append(s["sector"])

    return {
        "ticker": ticker,
        "sentiment_score": round(score, 2),
        "label": label,
        "key_topics": topics[:4],
        "controversy_flag": controversy >= 3,
        "summary": f"{s['name']} ({ticker}) has an ESG score of {esg}/100 with "
                   f"{'low' if s['carbon_intensity'] < 50 else 'moderate' if s['carbon_intensity'] < 150 else 'high'} "
                   f"carbon intensity at {s['carbon_intensity']} tCO2e/$M revenue.",
    }


async def _call_hf_sentiment(ticker: str, token: str) -> dict:
    """Call HuggingFace Inference API with FinBERT."""
    sec_map = {s["ticker"]: s for s in SECURITIES}
    s = sec_map.get(ticker, {"name": ticker})
    text = f"{s.get('name', ticker)} ESG sustainability investment analysis"

    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.post(
            "https://api-inference.huggingface.co/models/ProsusAI/finbert",
            headers={"Authorization": f"Bearer {token}"},
            json={"inputs": text},
        )
        resp.raise_for_status()
        data = resp.json()

    # Parse FinBERT output
    if isinstance(data, list) and len(data) > 0:
        results = data[0] if isinstance(data[0], list) else data
        score_map = {r["label"]: r["score"] for r in results}
        pos = score_map.get("positive", 0)
        neg = score_map.get("negative", 0)
        sentiment = pos - neg
    else:
        sentiment = 0.0

    fallback = _generate_fallback_sentiment(ticker)
    fallback["sentiment_score"] = round(sentiment, 2)
    return fallback


async def get_batch_sentiment(tickers: list[str]) -> list[dict]:
    """Get sentiment for multiple tickers."""
    results = []
    for t in tickers:
        r = await get_sentiment(t)
        results.append(r)
    return results
