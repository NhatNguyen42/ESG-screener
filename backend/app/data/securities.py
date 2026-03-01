"""
Curated ESG dataset — ~100 securities with realistic ESG scores,
carbon metrics, thematic tags, and controversy data.

Based on publicly available ESG rating ranges from MSCI, Sustainalytics,
and BlackRock's iShares sustainable ETF methodologies.
"""
from __future__ import annotations

SECURITIES = [
    # ── Clean Energy & Climate ────────────────────────────────
    {"ticker": "ICLN", "name": "iShares Global Clean Energy ETF", "asset_type": "etf", "sector": "Clean Energy", "region": "Global", "market_cap_b": 3.2, "price": 16.80, "ytd_return": 0.08, "dividend_yield": 0.012, "esg_overall": 88, "esg_environmental": 95, "esg_social": 78, "esg_governance": 82, "carbon_intensity": 45, "green_revenue_pct": 92, "themes": ["clean_energy", "climate_transition"], "controversy_score": 0.5, "controversy_summary": None},
    {"ticker": "QCLN", "name": "First Trust NASDAQ Clean Edge ETF", "asset_type": "etf", "sector": "Clean Energy", "region": "US", "market_cap_b": 1.8, "price": 38.50, "ytd_return": 0.12, "dividend_yield": 0.005, "esg_overall": 85, "esg_environmental": 92, "esg_social": 76, "esg_governance": 80, "carbon_intensity": 52, "green_revenue_pct": 88, "themes": ["clean_energy", "ev"], "controversy_score": 0.8, "controversy_summary": None},
    {"ticker": "TAN", "name": "Invesco Solar ETF", "asset_type": "etf", "sector": "Clean Energy", "region": "Global", "market_cap_b": 1.5, "price": 42.30, "ytd_return": 0.15, "dividend_yield": 0.003, "esg_overall": 86, "esg_environmental": 94, "esg_social": 74, "esg_governance": 78, "carbon_intensity": 38, "green_revenue_pct": 95, "themes": ["clean_energy", "solar"], "controversy_score": 0.6, "controversy_summary": None},
    {"ticker": "ENPH", "name": "Enphase Energy Inc", "asset_type": "stock", "sector": "Clean Energy", "region": "US", "market_cap_b": 22.5, "price": 125.40, "ytd_return": 0.22, "dividend_yield": 0.0, "esg_overall": 82, "esg_environmental": 90, "esg_social": 72, "esg_governance": 76, "carbon_intensity": 28, "green_revenue_pct": 100, "themes": ["clean_energy", "solar"], "controversy_score": 1.0, "controversy_summary": "Minor supply chain concerns"},
    {"ticker": "SEDG", "name": "SolarEdge Technologies", "asset_type": "stock", "sector": "Clean Energy", "region": "Israel", "market_cap_b": 4.8, "price": 68.20, "ytd_return": -0.05, "dividend_yield": 0.0, "esg_overall": 78, "esg_environmental": 88, "esg_social": 68, "esg_governance": 72, "carbon_intensity": 35, "green_revenue_pct": 100, "themes": ["clean_energy", "solar"], "controversy_score": 1.2, "controversy_summary": "Revenue decline concerns"},
    {"ticker": "NEE", "name": "NextEra Energy Inc", "asset_type": "stock", "sector": "Utilities", "region": "US", "market_cap_b": 155.0, "price": 78.90, "ytd_return": 0.10, "dividend_yield": 0.028, "esg_overall": 80, "esg_environmental": 85, "esg_social": 75, "esg_governance": 78, "carbon_intensity": 120, "green_revenue_pct": 65, "themes": ["clean_energy", "climate_transition"], "controversy_score": 0.8, "controversy_summary": None},
    {"ticker": "PLUG", "name": "Plug Power Inc", "asset_type": "stock", "sector": "Clean Energy", "region": "US", "market_cap_b": 2.1, "price": 3.45, "ytd_return": -0.15, "dividend_yield": 0.0, "esg_overall": 72, "esg_environmental": 85, "esg_social": 60, "esg_governance": 62, "carbon_intensity": 55, "green_revenue_pct": 100, "themes": ["clean_energy", "hydrogen"], "controversy_score": 2.5, "controversy_summary": "Persistent losses, auditor concerns"},
    {"ticker": "FSLR", "name": "First Solar Inc", "asset_type": "stock", "sector": "Clean Energy", "region": "US", "market_cap_b": 24.0, "price": 195.30, "ytd_return": 0.18, "dividend_yield": 0.0, "esg_overall": 84, "esg_environmental": 91, "esg_social": 74, "esg_governance": 80, "carbon_intensity": 32, "green_revenue_pct": 100, "themes": ["clean_energy", "solar", "us_manufacturing"], "controversy_score": 0.5, "controversy_summary": None},

    # ── AI & Technology ───────────────────────────────────────
    {"ticker": "MSFT", "name": "Microsoft Corp", "asset_type": "stock", "sector": "Technology", "region": "US", "market_cap_b": 3100.0, "price": 445.20, "ytd_return": 0.14, "dividend_yield": 0.007, "esg_overall": 82, "esg_environmental": 78, "esg_social": 82, "esg_governance": 88, "carbon_intensity": 42, "green_revenue_pct": 15, "themes": ["ai_infrastructure", "cloud", "cybersecurity"], "controversy_score": 1.0, "controversy_summary": "Antitrust scrutiny in EU"},
    {"ticker": "GOOGL", "name": "Alphabet Inc", "asset_type": "stock", "sector": "Technology", "region": "US", "market_cap_b": 2200.0, "price": 185.60, "ytd_return": 0.11, "dividend_yield": 0.004, "esg_overall": 76, "esg_environmental": 72, "esg_social": 70, "esg_governance": 85, "carbon_intensity": 55, "green_revenue_pct": 10, "themes": ["ai_infrastructure", "cloud", "autonomous_vehicles"], "controversy_score": 2.0, "controversy_summary": "Privacy and antitrust lawsuits"},
    {"ticker": "NVDA", "name": "NVIDIA Corp", "asset_type": "stock", "sector": "Technology", "region": "US", "market_cap_b": 2800.0, "price": 142.80, "ytd_return": 0.25, "dividend_yield": 0.001, "esg_overall": 74, "esg_environmental": 65, "esg_social": 75, "esg_governance": 82, "carbon_intensity": 68, "green_revenue_pct": 5, "themes": ["ai_infrastructure", "semiconductors", "data_centers"], "controversy_score": 1.5, "controversy_summary": "Export control issues, energy consumption of AI training"},
    {"ticker": "AAPL", "name": "Apple Inc", "asset_type": "stock", "sector": "Technology", "region": "US", "market_cap_b": 3400.0, "price": 235.40, "ytd_return": 0.08, "dividend_yield": 0.005, "esg_overall": 78, "esg_environmental": 82, "esg_social": 68, "esg_governance": 84, "carbon_intensity": 38, "green_revenue_pct": 8, "themes": ["consumer_tech", "privacy"], "controversy_score": 1.8, "controversy_summary": "Supply chain labor practices in Asia"},
    {"ticker": "CRM", "name": "Salesforce Inc", "asset_type": "stock", "sector": "Technology", "region": "US", "market_cap_b": 275.0, "price": 290.10, "ytd_return": 0.06, "dividend_yield": 0.006, "esg_overall": 80, "esg_environmental": 76, "esg_social": 82, "esg_governance": 82, "carbon_intensity": 25, "green_revenue_pct": 12, "themes": ["ai_infrastructure", "cloud"], "controversy_score": 0.8, "controversy_summary": None},
    {"ticker": "ADBE", "name": "Adobe Inc", "asset_type": "stock", "sector": "Technology", "region": "US", "market_cap_b": 195.0, "price": 440.80, "ytd_return": 0.04, "dividend_yield": 0.0, "esg_overall": 81, "esg_environmental": 74, "esg_social": 84, "esg_governance": 86, "carbon_intensity": 22, "green_revenue_pct": 5, "themes": ["ai_infrastructure", "digital_transformation"], "controversy_score": 0.5, "controversy_summary": None},
    {"ticker": "ARTY", "name": "iShares Future AI & Tech ETF", "asset_type": "etf", "sector": "Technology", "region": "Global", "market_cap_b": 0.8, "price": 32.40, "ytd_return": 0.18, "dividend_yield": 0.003, "esg_overall": 72, "esg_environmental": 62, "esg_social": 74, "esg_governance": 80, "carbon_intensity": 72, "green_revenue_pct": 8, "themes": ["ai_infrastructure", "robotics"], "controversy_score": 1.2, "controversy_summary": None},
    {"ticker": "BAI", "name": "iShares A.I. Innovation and Tech ETF", "asset_type": "etf", "sector": "Technology", "region": "US", "market_cap_b": 0.5, "price": 28.90, "ytd_return": 0.20, "dividend_yield": 0.002, "esg_overall": 70, "esg_environmental": 60, "esg_social": 72, "esg_governance": 78, "carbon_intensity": 78, "green_revenue_pct": 6, "themes": ["ai_infrastructure", "semiconductors"], "controversy_score": 1.4, "controversy_summary": None},
    {"ticker": "AMD", "name": "Advanced Micro Devices", "asset_type": "stock", "sector": "Technology", "region": "US", "market_cap_b": 220.0, "price": 155.30, "ytd_return": 0.16, "dividend_yield": 0.0, "esg_overall": 72, "esg_environmental": 64, "esg_social": 74, "esg_governance": 78, "carbon_intensity": 48, "green_revenue_pct": 3, "themes": ["ai_infrastructure", "semiconductors"], "controversy_score": 0.8, "controversy_summary": None},
    {"ticker": "TSM", "name": "Taiwan Semiconductor", "asset_type": "stock", "sector": "Technology", "region": "Asia", "market_cap_b": 780.0, "price": 178.50, "ytd_return": 0.20, "dividend_yield": 0.014, "esg_overall": 75, "esg_environmental": 68, "esg_social": 76, "esg_governance": 80, "carbon_intensity": 85, "green_revenue_pct": 4, "themes": ["ai_infrastructure", "semiconductors", "us_manufacturing"], "controversy_score": 1.0, "controversy_summary": "Water usage concerns in Taiwan"},

    # ── Healthcare & Biotech ──────────────────────────────────
    {"ticker": "JNJ", "name": "Johnson & Johnson", "asset_type": "stock", "sector": "Healthcare", "region": "US", "market_cap_b": 395.0, "price": 162.50, "ytd_return": 0.05, "dividend_yield": 0.032, "esg_overall": 74, "esg_environmental": 72, "esg_social": 70, "esg_governance": 80, "carbon_intensity": 65, "green_revenue_pct": 5, "themes": ["healthcare", "aging_population"], "controversy_score": 3.5, "controversy_summary": "Talc litigation, opioid settlements"},
    {"ticker": "UNH", "name": "UnitedHealth Group", "asset_type": "stock", "sector": "Healthcare", "region": "US", "market_cap_b": 510.0, "price": 550.20, "ytd_return": 0.07, "dividend_yield": 0.015, "esg_overall": 68, "esg_environmental": 55, "esg_social": 72, "esg_governance": 78, "carbon_intensity": 18, "green_revenue_pct": 2, "themes": ["healthcare", "aging_population"], "controversy_score": 2.0, "controversy_summary": "DOJ antitrust probe"},
    {"ticker": "LLY", "name": "Eli Lilly & Co", "asset_type": "stock", "sector": "Healthcare", "region": "US", "market_cap_b": 720.0, "price": 810.40, "ytd_return": 0.22, "dividend_yield": 0.006, "esg_overall": 76, "esg_environmental": 70, "esg_social": 78, "esg_governance": 82, "carbon_intensity": 42, "green_revenue_pct": 3, "themes": ["healthcare", "biotech"], "controversy_score": 1.2, "controversy_summary": "Drug pricing criticism"},
    {"ticker": "ISRG", "name": "Intuitive Surgical", "asset_type": "stock", "sector": "Healthcare", "region": "US", "market_cap_b": 175.0, "price": 520.80, "ytd_return": 0.15, "dividend_yield": 0.0, "esg_overall": 79, "esg_environmental": 72, "esg_social": 82, "esg_governance": 84, "carbon_intensity": 22, "green_revenue_pct": 8, "themes": ["healthcare", "robotics"], "controversy_score": 0.5, "controversy_summary": None},
    {"ticker": "IBB", "name": "iShares Biotechnology ETF", "asset_type": "etf", "sector": "Healthcare", "region": "US", "market_cap_b": 7.5, "price": 138.60, "ytd_return": 0.09, "dividend_yield": 0.002, "esg_overall": 70, "esg_environmental": 62, "esg_social": 74, "esg_governance": 76, "carbon_intensity": 35, "green_revenue_pct": 5, "themes": ["healthcare", "biotech"], "controversy_score": 1.5, "controversy_summary": None},

    # ── ESG / Sustainable ETFs ────────────────────────────────
    {"ticker": "ESGU", "name": "iShares ESG Aware MSCI USA ETF", "asset_type": "etf", "sector": "Multi-Sector", "region": "US", "market_cap_b": 12.5, "price": 112.30, "ytd_return": 0.11, "dividend_yield": 0.013, "esg_overall": 78, "esg_environmental": 74, "esg_social": 78, "esg_governance": 82, "carbon_intensity": 95, "green_revenue_pct": 18, "themes": ["esg_core", "broad_market"], "controversy_score": 1.0, "controversy_summary": None},
    {"ticker": "ESGD", "name": "iShares ESG Aware MSCI EAFE ETF", "asset_type": "etf", "sector": "Multi-Sector", "region": "International", "market_cap_b": 8.2, "price": 78.40, "ytd_return": 0.08, "dividend_yield": 0.022, "esg_overall": 80, "esg_environmental": 78, "esg_social": 80, "esg_governance": 82, "carbon_intensity": 88, "green_revenue_pct": 20, "themes": ["esg_core", "international"], "controversy_score": 0.8, "controversy_summary": None},
    {"ticker": "ESGE", "name": "iShares ESG Aware MSCI EM ETF", "asset_type": "etf", "sector": "Multi-Sector", "region": "Emerging", "market_cap_b": 5.8, "price": 35.20, "ytd_return": 0.06, "dividend_yield": 0.025, "esg_overall": 68, "esg_environmental": 62, "esg_social": 68, "esg_governance": 72, "carbon_intensity": 145, "green_revenue_pct": 12, "themes": ["esg_core", "emerging_markets"], "controversy_score": 1.8, "controversy_summary": None},
    {"ticker": "SUSL", "name": "iShares ESG MSCI USA Leaders ETF", "asset_type": "etf", "sector": "Multi-Sector", "region": "US", "market_cap_b": 3.4, "price": 82.10, "ytd_return": 0.12, "dividend_yield": 0.012, "esg_overall": 85, "esg_environmental": 82, "esg_social": 84, "esg_governance": 88, "carbon_intensity": 68, "green_revenue_pct": 22, "themes": ["esg_core", "esg_leaders"], "controversy_score": 0.5, "controversy_summary": None},
    {"ticker": "DSI", "name": "iShares MSCI KLD 400 Social ETF", "asset_type": "etf", "sector": "Multi-Sector", "region": "US", "market_cap_b": 4.1, "price": 95.60, "ytd_return": 0.10, "dividend_yield": 0.011, "esg_overall": 83, "esg_environmental": 80, "esg_social": 85, "esg_governance": 84, "carbon_intensity": 72, "green_revenue_pct": 20, "themes": ["esg_core", "social_impact"], "controversy_score": 0.6, "controversy_summary": None},

    # ── EV & Autonomous ───────────────────────────────────────
    {"ticker": "TSLA", "name": "Tesla Inc", "asset_type": "stock", "sector": "Automotive", "region": "US", "market_cap_b": 850.0, "price": 280.50, "ytd_return": 0.30, "dividend_yield": 0.0, "esg_overall": 62, "esg_environmental": 78, "esg_social": 42, "esg_governance": 45, "carbon_intensity": 55, "green_revenue_pct": 85, "themes": ["ev", "clean_energy", "autonomous_vehicles"], "controversy_score": 4.0, "controversy_summary": "Governance concerns, workplace safety, CEO controversies"},
    {"ticker": "RIVN", "name": "Rivian Automotive", "asset_type": "stock", "sector": "Automotive", "region": "US", "market_cap_b": 18.5, "price": 18.20, "ytd_return": 0.05, "dividend_yield": 0.0, "esg_overall": 72, "esg_environmental": 82, "esg_social": 68, "esg_governance": 62, "carbon_intensity": 85, "green_revenue_pct": 100, "themes": ["ev", "us_manufacturing"], "controversy_score": 1.5, "controversy_summary": "Cash burn rate concerns"},
    {"ticker": "LI", "name": "Li Auto Inc", "asset_type": "stock", "sector": "Automotive", "region": "Asia", "market_cap_b": 32.0, "price": 28.90, "ytd_return": 0.18, "dividend_yield": 0.0, "esg_overall": 58, "esg_environmental": 68, "esg_social": 50, "esg_governance": 48, "carbon_intensity": 110, "green_revenue_pct": 75, "themes": ["ev", "emerging_markets"], "controversy_score": 1.8, "controversy_summary": "Chinese regulatory environment"},
    {"ticker": "DRIV", "name": "Global X Autonomous & EV ETF", "asset_type": "etf", "sector": "Automotive", "region": "Global", "market_cap_b": 1.2, "price": 25.80, "ytd_return": 0.14, "dividend_yield": 0.005, "esg_overall": 68, "esg_environmental": 72, "esg_social": 62, "esg_governance": 68, "carbon_intensity": 92, "green_revenue_pct": 55, "themes": ["ev", "autonomous_vehicles", "robotics"], "controversy_score": 1.5, "controversy_summary": None},

    # ── Defense & Security ────────────────────────────────────
    {"ticker": "LMT", "name": "Lockheed Martin Corp", "asset_type": "stock", "sector": "Defense", "region": "US", "market_cap_b": 130.0, "price": 545.20, "ytd_return": 0.12, "dividend_yield": 0.025, "esg_overall": 55, "esg_environmental": 48, "esg_social": 52, "esg_governance": 72, "carbon_intensity": 145, "green_revenue_pct": 2, "themes": ["defense", "cybersecurity"], "controversy_score": 3.0, "controversy_summary": "Weapons manufacturing ethical concerns"},
    {"ticker": "RTX", "name": "RTX Corp (Raytheon)", "asset_type": "stock", "sector": "Defense", "region": "US", "market_cap_b": 155.0, "price": 122.40, "ytd_return": 0.09, "dividend_yield": 0.021, "esg_overall": 52, "esg_environmental": 45, "esg_social": 50, "esg_governance": 68, "carbon_intensity": 160, "green_revenue_pct": 3, "themes": ["defense", "cybersecurity"], "controversy_score": 3.2, "controversy_summary": "Weapons sales to conflict zones"},
    {"ticker": "ITA", "name": "iShares U.S. Aerospace & Defense ETF", "asset_type": "etf", "sector": "Defense", "region": "US", "market_cap_b": 5.8, "price": 145.80, "ytd_return": 0.10, "dividend_yield": 0.008, "esg_overall": 50, "esg_environmental": 42, "esg_social": 48, "esg_governance": 65, "carbon_intensity": 155, "green_revenue_pct": 2, "themes": ["defense"], "controversy_score": 2.8, "controversy_summary": None},

    # ── Financials ────────────────────────────────────────────
    {"ticker": "BLK", "name": "BlackRock Inc", "asset_type": "stock", "sector": "Financials", "region": "US", "market_cap_b": 145.0, "price": 980.50, "ytd_return": 0.13, "dividend_yield": 0.021, "esg_overall": 78, "esg_environmental": 72, "esg_social": 78, "esg_governance": 85, "carbon_intensity": 12, "green_revenue_pct": 25, "themes": ["esg_leaders", "digital_transformation"], "controversy_score": 1.5, "controversy_summary": "ESG backlash from some US states"},
    {"ticker": "JPM", "name": "JPMorgan Chase & Co", "asset_type": "stock", "sector": "Financials", "region": "US", "market_cap_b": 620.0, "price": 225.80, "ytd_return": 0.10, "dividend_yield": 0.022, "esg_overall": 65, "esg_environmental": 55, "esg_social": 68, "esg_governance": 75, "carbon_intensity": 18, "green_revenue_pct": 8, "themes": ["digital_transformation"], "controversy_score": 2.5, "controversy_summary": "Fossil fuel financing criticism"},
    {"ticker": "GS", "name": "Goldman Sachs Group", "asset_type": "stock", "sector": "Financials", "region": "US", "market_cap_b": 175.0, "price": 520.30, "ytd_return": 0.15, "dividend_yield": 0.020, "esg_overall": 62, "esg_environmental": 50, "esg_social": 65, "esg_governance": 72, "carbon_intensity": 15, "green_revenue_pct": 10, "themes": ["digital_transformation"], "controversy_score": 2.2, "controversy_summary": "1MDB settlement legacy"},
    {"ticker": "XLF", "name": "Financial Select Sector SPDR", "asset_type": "etf", "sector": "Financials", "region": "US", "market_cap_b": 42.0, "price": 45.80, "ytd_return": 0.09, "dividend_yield": 0.016, "esg_overall": 64, "esg_environmental": 52, "esg_social": 66, "esg_governance": 74, "carbon_intensity": 20, "green_revenue_pct": 8, "themes": ["broad_market"], "controversy_score": 1.8, "controversy_summary": None},

    # ── Consumer / Retail ─────────────────────────────────────
    {"ticker": "COST", "name": "Costco Wholesale", "asset_type": "stock", "sector": "Consumer", "region": "US", "market_cap_b": 405.0, "price": 920.50, "ytd_return": 0.12, "dividend_yield": 0.005, "esg_overall": 76, "esg_environmental": 70, "esg_social": 80, "esg_governance": 78, "carbon_intensity": 55, "green_revenue_pct": 8, "themes": ["consumer_staples"], "controversy_score": 0.8, "controversy_summary": None},
    {"ticker": "PG", "name": "Procter & Gamble Co", "asset_type": "stock", "sector": "Consumer", "region": "US", "market_cap_b": 390.0, "price": 168.20, "ytd_return": 0.06, "dividend_yield": 0.024, "esg_overall": 79, "esg_environmental": 78, "esg_social": 80, "esg_governance": 80, "carbon_intensity": 48, "green_revenue_pct": 15, "themes": ["consumer_staples", "circular_economy"], "controversy_score": 1.0, "controversy_summary": "Deforestation supply chain links"},
    {"ticker": "NKE", "name": "Nike Inc", "asset_type": "stock", "sector": "Consumer", "region": "US", "market_cap_b": 135.0, "price": 95.40, "ytd_return": -0.08, "dividend_yield": 0.016, "esg_overall": 72, "esg_environmental": 74, "esg_social": 65, "esg_governance": 76, "carbon_intensity": 42, "green_revenue_pct": 20, "themes": ["circular_economy"], "controversy_score": 2.0, "controversy_summary": "Overseas labor practices"},
    {"ticker": "SBUX", "name": "Starbucks Corp", "asset_type": "stock", "sector": "Consumer", "region": "US", "market_cap_b": 105.0, "price": 92.80, "ytd_return": -0.04, "dividend_yield": 0.026, "esg_overall": 74, "esg_environmental": 72, "esg_social": 70, "esg_governance": 78, "carbon_intensity": 38, "green_revenue_pct": 12, "themes": ["circular_economy", "social_impact"], "controversy_score": 1.8, "controversy_summary": "Unionization disputes"},

    # ── Energy Transition / Traditional → Green ───────────────
    {"ticker": "XOM", "name": "Exxon Mobil Corp", "asset_type": "stock", "sector": "Energy", "region": "US", "market_cap_b": 480.0, "price": 112.50, "ytd_return": 0.04, "dividend_yield": 0.034, "esg_overall": 38, "esg_environmental": 25, "esg_social": 45, "esg_governance": 55, "carbon_intensity": 420, "green_revenue_pct": 2, "themes": ["energy_transition"], "controversy_score": 4.5, "controversy_summary": "Climate change litigation, lobbying against emissions regulation"},
    {"ticker": "CVX", "name": "Chevron Corp", "asset_type": "stock", "sector": "Energy", "region": "US", "market_cap_b": 290.0, "price": 155.20, "ytd_return": 0.02, "dividend_yield": 0.038, "esg_overall": 40, "esg_environmental": 28, "esg_social": 48, "esg_governance": 58, "carbon_intensity": 395, "green_revenue_pct": 3, "themes": ["energy_transition"], "controversy_score": 4.2, "controversy_summary": "Ecuador Lago Agrio case, climate disinformation allegations"},
    {"ticker": "TTE", "name": "TotalEnergies SE", "asset_type": "stock", "sector": "Energy", "region": "Europe", "market_cap_b": 155.0, "price": 65.80, "ytd_return": 0.03, "dividend_yield": 0.048, "esg_overall": 48, "esg_environmental": 38, "esg_social": 52, "esg_governance": 62, "carbon_intensity": 350, "green_revenue_pct": 12, "themes": ["energy_transition", "clean_energy"], "controversy_score": 3.5, "controversy_summary": "Mozambique gas project human rights concerns"},
    {"ticker": "SHEL", "name": "Shell PLC", "asset_type": "stock", "sector": "Energy", "region": "Europe", "market_cap_b": 210.0, "price": 68.40, "ytd_return": 0.01, "dividend_yield": 0.040, "esg_overall": 45, "esg_environmental": 32, "esg_social": 50, "esg_governance": 60, "carbon_intensity": 380, "green_revenue_pct": 8, "themes": ["energy_transition"], "controversy_score": 4.0, "controversy_summary": "Dutch court climate ruling, Niger Delta pollution"},

    # ── Industrials & Infrastructure ──────────────────────────
    {"ticker": "CAT", "name": "Caterpillar Inc", "asset_type": "stock", "sector": "Industrials", "region": "US", "market_cap_b": 185.0, "price": 385.20, "ytd_return": 0.08, "dividend_yield": 0.016, "esg_overall": 64, "esg_environmental": 58, "esg_social": 65, "esg_governance": 72, "carbon_intensity": 135, "green_revenue_pct": 10, "themes": ["infrastructure", "us_manufacturing"], "controversy_score": 1.5, "controversy_summary": "Tax avoidance allegations"},
    {"ticker": "DE", "name": "Deere & Co", "asset_type": "stock", "sector": "Industrials", "region": "US", "market_cap_b": 120.0, "price": 432.50, "ytd_return": 0.06, "dividend_yield": 0.014, "esg_overall": 72, "esg_environmental": 68, "esg_social": 72, "esg_governance": 76, "carbon_intensity": 95, "green_revenue_pct": 15, "themes": ["precision_agriculture", "autonomous_vehicles"], "controversy_score": 1.0, "controversy_summary": None},
    {"ticker": "PAVE", "name": "Global X US Infrastructure ETF", "asset_type": "etf", "sector": "Industrials", "region": "US", "market_cap_b": 6.8, "price": 38.90, "ytd_return": 0.07, "dividend_yield": 0.008, "esg_overall": 62, "esg_environmental": 55, "esg_social": 64, "esg_governance": 70, "carbon_intensity": 125, "green_revenue_pct": 12, "themes": ["infrastructure", "us_manufacturing"], "controversy_score": 1.2, "controversy_summary": None},
    {"ticker": "WM", "name": "Waste Management Inc", "asset_type": "stock", "sector": "Industrials", "region": "US", "market_cap_b": 88.0, "price": 218.40, "ytd_return": 0.09, "dividend_yield": 0.015, "esg_overall": 78, "esg_environmental": 82, "esg_social": 74, "esg_governance": 76, "carbon_intensity": 180, "green_revenue_pct": 35, "themes": ["circular_economy", "climate_transition"], "controversy_score": 1.0, "controversy_summary": None},

    # ── Water & Agriculture ───────────────────────────────────
    {"ticker": "XYL", "name": "Xylem Inc", "asset_type": "stock", "sector": "Water", "region": "US", "market_cap_b": 32.0, "price": 132.80, "ytd_return": 0.10, "dividend_yield": 0.011, "esg_overall": 84, "esg_environmental": 90, "esg_social": 78, "esg_governance": 82, "carbon_intensity": 42, "green_revenue_pct": 80, "themes": ["water", "climate_transition"], "controversy_score": 0.3, "controversy_summary": None},
    {"ticker": "AWK", "name": "American Water Works", "asset_type": "stock", "sector": "Water", "region": "US", "market_cap_b": 28.0, "price": 145.60, "ytd_return": 0.05, "dividend_yield": 0.022, "esg_overall": 82, "esg_environmental": 88, "esg_social": 76, "esg_governance": 80, "carbon_intensity": 55, "green_revenue_pct": 90, "themes": ["water", "infrastructure"], "controversy_score": 0.5, "controversy_summary": None},
    {"ticker": "PHO", "name": "Invesco Water Resources ETF", "asset_type": "etf", "sector": "Water", "region": "US", "market_cap_b": 2.1, "price": 62.40, "ytd_return": 0.08, "dividend_yield": 0.005, "esg_overall": 80, "esg_environmental": 86, "esg_social": 74, "esg_governance": 78, "carbon_intensity": 48, "green_revenue_pct": 75, "themes": ["water"], "controversy_score": 0.5, "controversy_summary": None},

    # ── Materials & Mining ────────────────────────────────────
    {"ticker": "LIN", "name": "Linde PLC", "asset_type": "stock", "sector": "Materials", "region": "Global", "market_cap_b": 215.0, "price": 460.20, "ytd_return": 0.07, "dividend_yield": 0.012, "esg_overall": 76, "esg_environmental": 72, "esg_social": 76, "esg_governance": 82, "carbon_intensity": 165, "green_revenue_pct": 25, "themes": ["hydrogen", "climate_transition"], "controversy_score": 0.8, "controversy_summary": None},
    {"ticker": "ALB", "name": "Albemarle Corp", "asset_type": "stock", "sector": "Materials", "region": "US", "market_cap_b": 12.5, "price": 95.40, "ytd_return": -0.10, "dividend_yield": 0.018, "esg_overall": 60, "esg_environmental": 52, "esg_social": 62, "esg_governance": 68, "carbon_intensity": 210, "green_revenue_pct": 45, "themes": ["ev", "clean_energy"], "controversy_score": 2.0, "controversy_summary": "Lithium mining environmental impact in Chile"},
    {"ticker": "FCX", "name": "Freeport-McMoRan", "asset_type": "stock", "sector": "Materials", "region": "US", "market_cap_b": 68.0, "price": 48.20, "ytd_return": 0.08, "dividend_yield": 0.014, "esg_overall": 48, "esg_environmental": 35, "esg_social": 52, "esg_governance": 62, "carbon_intensity": 280, "green_revenue_pct": 20, "themes": ["ev", "infrastructure"], "controversy_score": 3.5, "controversy_summary": "Grasberg mine environmental devastation in Indonesia"},

    # ── Real Estate / REITs ───────────────────────────────────
    {"ticker": "PLD", "name": "Prologis Inc", "asset_type": "stock", "sector": "Real Estate", "region": "US", "market_cap_b": 115.0, "price": 128.40, "ytd_return": 0.09, "dividend_yield": 0.030, "esg_overall": 80, "esg_environmental": 82, "esg_social": 76, "esg_governance": 80, "carbon_intensity": 35, "green_revenue_pct": 30, "themes": ["green_buildings", "infrastructure"], "controversy_score": 0.5, "controversy_summary": None},
    {"ticker": "EQIX", "name": "Equinix Inc", "asset_type": "stock", "sector": "Real Estate", "region": "US", "market_cap_b": 82.0, "price": 880.50, "ytd_return": 0.11, "dividend_yield": 0.019, "esg_overall": 78, "esg_environmental": 75, "esg_social": 78, "esg_governance": 82, "carbon_intensity": 95, "green_revenue_pct": 20, "themes": ["data_centers", "green_buildings"], "controversy_score": 0.8, "controversy_summary": "Energy consumption of data centers"},

    # ── Telecom ───────────────────────────────────────────────
    {"ticker": "T", "name": "AT&T Inc", "asset_type": "stock", "sector": "Telecom", "region": "US", "market_cap_b": 155.0, "price": 22.80, "ytd_return": 0.03, "dividend_yield": 0.058, "esg_overall": 60, "esg_environmental": 52, "esg_social": 62, "esg_governance": 68, "carbon_intensity": 75, "green_revenue_pct": 5, "themes": ["digital_transformation"], "controversy_score": 1.5, "controversy_summary": "Lead cable contamination lawsuits"},
    {"ticker": "VZ", "name": "Verizon Communications", "asset_type": "stock", "sector": "Telecom", "region": "US", "market_cap_b": 175.0, "price": 42.50, "ytd_return": 0.02, "dividend_yield": 0.065, "esg_overall": 64, "esg_environmental": 56, "esg_social": 66, "esg_governance": 72, "carbon_intensity": 68, "green_revenue_pct": 6, "themes": ["digital_transformation"], "controversy_score": 1.0, "controversy_summary": None},

    # ── European ESG Leaders ──────────────────────────────────
    {"ticker": "NESN.SW", "name": "Nestle SA", "asset_type": "stock", "sector": "Consumer", "region": "Europe", "market_cap_b": 260.0, "price": 88.50, "ytd_return": 0.02, "dividend_yield": 0.032, "esg_overall": 75, "esg_environmental": 72, "esg_social": 74, "esg_governance": 80, "carbon_intensity": 65, "green_revenue_pct": 18, "themes": ["consumer_staples", "water"], "controversy_score": 2.5, "controversy_summary": "Water extraction controversies, infant formula marketing"},
    {"ticker": "OR.PA", "name": "L'Oreal SA", "asset_type": "stock", "sector": "Consumer", "region": "Europe", "market_cap_b": 240.0, "price": 385.20, "ytd_return": 0.05, "dividend_yield": 0.015, "esg_overall": 82, "esg_environmental": 80, "esg_social": 82, "esg_governance": 84, "carbon_intensity": 22, "green_revenue_pct": 25, "themes": ["circular_economy", "social_impact"], "controversy_score": 0.8, "controversy_summary": None},
    {"ticker": "ASML", "name": "ASML Holding NV", "asset_type": "stock", "sector": "Technology", "region": "Europe", "market_cap_b": 350.0, "price": 885.40, "ytd_return": 0.12, "dividend_yield": 0.006, "esg_overall": 84, "esg_environmental": 78, "esg_social": 84, "esg_governance": 90, "carbon_intensity": 18, "green_revenue_pct": 10, "themes": ["semiconductors", "ai_infrastructure"], "controversy_score": 0.5, "controversy_summary": None},
    {"ticker": "SAP", "name": "SAP SE", "asset_type": "stock", "sector": "Technology", "region": "Europe", "market_cap_b": 280.0, "price": 232.50, "ytd_return": 0.14, "dividend_yield": 0.010, "esg_overall": 86, "esg_environmental": 82, "esg_social": 86, "esg_governance": 90, "carbon_intensity": 15, "green_revenue_pct": 12, "themes": ["cloud", "digital_transformation"], "controversy_score": 0.5, "controversy_summary": None},
    {"ticker": "NOVO-B.CO", "name": "Novo Nordisk A/S", "asset_type": "stock", "sector": "Healthcare", "region": "Europe", "market_cap_b": 480.0, "price": 720.40, "ytd_return": 0.08, "dividend_yield": 0.012, "esg_overall": 85, "esg_environmental": 82, "esg_social": 86, "esg_governance": 88, "carbon_intensity": 25, "green_revenue_pct": 5, "themes": ["healthcare", "social_impact"], "controversy_score": 0.8, "controversy_summary": "Drug pricing in US market"},

    # ── Cybersecurity ─────────────────────────────────────────
    {"ticker": "CRWD", "name": "CrowdStrike Holdings", "asset_type": "stock", "sector": "Technology", "region": "US", "market_cap_b": 85.0, "price": 352.40, "ytd_return": 0.18, "dividend_yield": 0.0, "esg_overall": 74, "esg_environmental": 62, "esg_social": 78, "esg_governance": 82, "carbon_intensity": 15, "green_revenue_pct": 3, "themes": ["cybersecurity", "cloud"], "controversy_score": 1.5, "controversy_summary": "July 2024 global IT outage"},
    {"ticker": "PANW", "name": "Palo Alto Networks", "asset_type": "stock", "sector": "Technology", "region": "US", "market_cap_b": 125.0, "price": 385.20, "ytd_return": 0.15, "dividend_yield": 0.0, "esg_overall": 72, "esg_environmental": 60, "esg_social": 76, "esg_governance": 80, "carbon_intensity": 12, "green_revenue_pct": 2, "themes": ["cybersecurity", "cloud"], "controversy_score": 0.5, "controversy_summary": None},
    {"ticker": "CIBR", "name": "First Trust NASDAQ Cybersecurity ETF", "asset_type": "etf", "sector": "Technology", "region": "US", "market_cap_b": 7.2, "price": 58.40, "ytd_return": 0.14, "dividend_yield": 0.002, "esg_overall": 72, "esg_environmental": 60, "esg_social": 76, "esg_governance": 80, "carbon_intensity": 18, "green_revenue_pct": 3, "themes": ["cybersecurity"], "controversy_score": 0.8, "controversy_summary": None},

    # ── Broad Market / Benchmark ──────────────────────────────
    {"ticker": "SPY", "name": "SPDR S&P 500 ETF Trust", "asset_type": "etf", "sector": "Multi-Sector", "region": "US", "market_cap_b": 550.0, "price": 528.40, "ytd_return": 0.10, "dividend_yield": 0.013, "esg_overall": 62, "esg_environmental": 55, "esg_social": 64, "esg_governance": 70, "carbon_intensity": 130, "green_revenue_pct": 12, "themes": ["broad_market"], "controversy_score": 1.5, "controversy_summary": None},
    {"ticker": "QQQ", "name": "Invesco QQQ Trust", "asset_type": "etf", "sector": "Technology", "region": "US", "market_cap_b": 280.0, "price": 485.20, "ytd_return": 0.15, "dividend_yield": 0.005, "esg_overall": 68, "esg_environmental": 60, "esg_social": 70, "esg_governance": 76, "carbon_intensity": 72, "green_revenue_pct": 10, "themes": ["broad_market", "ai_infrastructure"], "controversy_score": 1.2, "controversy_summary": None},
    {"ticker": "VTI", "name": "Vanguard Total Stock Market ETF", "asset_type": "etf", "sector": "Multi-Sector", "region": "US", "market_cap_b": 420.0, "price": 275.80, "ytd_return": 0.09, "dividend_yield": 0.014, "esg_overall": 60, "esg_environmental": 52, "esg_social": 62, "esg_governance": 68, "carbon_intensity": 138, "green_revenue_pct": 11, "themes": ["broad_market"], "controversy_score": 1.5, "controversy_summary": None},

    # ── Thematic: Robotics & Innovation ───────────────────────
    {"ticker": "BOTZ", "name": "Global X Robotics & AI ETF", "asset_type": "etf", "sector": "Technology", "region": "Global", "market_cap_b": 2.5, "price": 32.80, "ytd_return": 0.16, "dividend_yield": 0.003, "esg_overall": 70, "esg_environmental": 62, "esg_social": 72, "esg_governance": 76, "carbon_intensity": 65, "green_revenue_pct": 8, "themes": ["robotics", "ai_infrastructure"], "controversy_score": 1.0, "controversy_summary": None},
    {"ticker": "ARKK", "name": "ARK Innovation ETF", "asset_type": "etf", "sector": "Multi-Sector", "region": "US", "market_cap_b": 6.8, "price": 52.40, "ytd_return": 0.20, "dividend_yield": 0.0, "esg_overall": 58, "esg_environmental": 52, "esg_social": 60, "esg_governance": 62, "carbon_intensity": 85, "green_revenue_pct": 18, "themes": ["biotech", "ai_infrastructure", "ev"], "controversy_score": 2.0, "controversy_summary": "Concentrated positions, high volatility"},

    # ── Additional diversified picks ──────────────────────────
    {"ticker": "V", "name": "Visa Inc", "asset_type": "stock", "sector": "Financials", "region": "US", "market_cap_b": 580.0, "price": 295.40, "ytd_return": 0.08, "dividend_yield": 0.007, "esg_overall": 76, "esg_environmental": 68, "esg_social": 78, "esg_governance": 84, "carbon_intensity": 8, "green_revenue_pct": 5, "themes": ["digital_transformation", "financial_inclusion"], "controversy_score": 1.0, "controversy_summary": "Antitrust fee litigation"},
    {"ticker": "MA", "name": "Mastercard Inc", "asset_type": "stock", "sector": "Financials", "region": "US", "market_cap_b": 440.0, "price": 485.20, "ytd_return": 0.10, "dividend_yield": 0.006, "esg_overall": 78, "esg_environmental": 72, "esg_social": 80, "esg_governance": 84, "carbon_intensity": 6, "green_revenue_pct": 6, "themes": ["digital_transformation", "financial_inclusion"], "controversy_score": 0.8, "controversy_summary": None},
    {"ticker": "DIS", "name": "Walt Disney Co", "asset_type": "stock", "sector": "Consumer", "region": "US", "market_cap_b": 205.0, "price": 115.40, "ytd_return": 0.06, "dividend_yield": 0.008, "esg_overall": 70, "esg_environmental": 65, "esg_social": 72, "esg_governance": 74, "carbon_intensity": 32, "green_revenue_pct": 5, "themes": ["digital_transformation"], "controversy_score": 1.5, "controversy_summary": "Political controversies, content moderation debates"},
    {"ticker": "AMZN", "name": "Amazon.com Inc", "asset_type": "stock", "sector": "Technology", "region": "US", "market_cap_b": 2100.0, "price": 205.80, "ytd_return": 0.12, "dividend_yield": 0.0, "esg_overall": 64, "esg_environmental": 62, "esg_social": 55, "esg_governance": 72, "carbon_intensity": 48, "green_revenue_pct": 10, "themes": ["ai_infrastructure", "cloud", "ev"], "controversy_score": 2.8, "controversy_summary": "Worker conditions, antitrust, delivery carbon footprint"},
    {"ticker": "META", "name": "Meta Platforms Inc", "asset_type": "stock", "sector": "Technology", "region": "US", "market_cap_b": 1500.0, "price": 585.20, "ytd_return": 0.18, "dividend_yield": 0.003, "esg_overall": 55, "esg_environmental": 52, "esg_social": 42, "esg_governance": 68, "carbon_intensity": 58, "green_revenue_pct": 4, "themes": ["ai_infrastructure", "digital_transformation"], "controversy_score": 3.8, "controversy_summary": "Privacy violations, misinformation, teen mental health impact"},
]


# ── Available themes ──────────────────────────────────────
THEMES = {
    "clean_energy": "Clean Energy",
    "solar": "Solar",
    "ev": "Electric Vehicles",
    "hydrogen": "Hydrogen Economy",
    "water": "Water Resources",
    "climate_transition": "Climate Transition",
    "ai_infrastructure": "AI Infrastructure",
    "semiconductors": "Semiconductors",
    "cloud": "Cloud Computing",
    "cybersecurity": "Cybersecurity",
    "robotics": "Robotics & Automation",
    "autonomous_vehicles": "Autonomous Vehicles",
    "healthcare": "Healthcare Innovation",
    "biotech": "Biotechnology",
    "aging_population": "Aging Population",
    "defense": "Defense & Security",
    "infrastructure": "Infrastructure",
    "us_manufacturing": "US Manufacturing",
    "circular_economy": "Circular Economy",
    "green_buildings": "Green Buildings",
    "digital_transformation": "Digital Transformation",
    "social_impact": "Social Impact",
    "financial_inclusion": "Financial Inclusion",
    "esg_core": "ESG Core",
    "esg_leaders": "ESG Leaders",
    "broad_market": "Broad Market",
    "consumer_staples": "Consumer Staples",
    "precision_agriculture": "Precision Agriculture",
    "data_centers": "Data Centers",
    "emerging_markets": "Emerging Markets",
    "international": "International Developed",
    "consumer_tech": "Consumer Technology",
    "privacy": "Privacy & Data Protection",
    "energy_transition": "Energy Transition",
}

SECTORS = sorted(set(s["sector"] for s in SECURITIES))
REGIONS = sorted(set(s["region"] for s in SECURITIES))


# ── Derived fields: expected_return & volatility ──────────
# Computed from fundamentals so the ML model has real signal to learn from.
import math as _math, hashlib as _hashlib

for _s in SECURITIES:
    # Expected return: start from ytd, adjust for ESG momentum, sector, size
    _base = _s["ytd_return"] * 0.6  # partial mean reversion
    _esg_bonus = (_s["esg_overall"] - 60) * 0.0012  # ESG alpha
    _size_adj = -0.005 * _math.log10(max(_s["market_cap_b"], 0.1))  # small cap premium
    _green_adj = _s["green_revenue_pct"] * 0.0003  # green premium
    _carbon_drag = -_s["carbon_intensity"] * 0.00005  # carbon penalty
    _controversy_drag = -_s["controversy_score"] * 0.008

    _seed = int(_hashlib.md5(_s["ticker"].encode()).hexdigest()[:8], 16)
    _noise = ((_seed % 1000) / 1000 - 0.5) * 0.04  # deterministic +-2%

    _s["expected_return"] = round(
        max(-0.10, min(0.35, 0.08 + _base + _esg_bonus + _size_adj + _green_adj + _carbon_drag + _controversy_drag + _noise)),
        4,
    )

    # Volatility: base from sector, adjust for size and controversy
    _sector_vol = {
        "Clean Energy": 0.32, "Technology": 0.25, "Healthcare": 0.22,
        "Multi-Sector": 0.16, "Automotive": 0.35, "Defense": 0.20,
        "Financials": 0.22, "Consumer": 0.18, "Energy": 0.28,
        "Industrials": 0.21, "Water": 0.20, "Materials": 0.28,
        "Real Estate": 0.22, "Telecom": 0.18, "Utilities": 0.18,
    }.get(_s["sector"], 0.22)
    _size_vol = 0.05 / max(_math.log10(max(_s["market_cap_b"], 0.1)), 0.1)
    _type_adj = -0.05 if _s["asset_type"] == "etf" else 0.0
    _noise_vol = ((_seed % 500) / 500 - 0.5) * 0.04

    _s["volatility"] = round(
        max(0.10, min(0.55, _sector_vol + _size_vol + _type_adj + _noise_vol)),
        4,
    )
