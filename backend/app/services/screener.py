"""
ESG data screener service — filtering, sorting, comparisons.
"""
from __future__ import annotations

from app.data.securities import SECURITIES, THEMES, SECTORS, REGIONS
from app.schemas import Security, SecurityFilters


def get_all_securities() -> list[Security]:
    return [Security(**s) for s in SECURITIES]


def filter_securities(filters: SecurityFilters) -> list[Security]:
    """Apply filters and return matching securities."""
    results = SECURITIES.copy()

    if filters.search:
        q = filters.search.lower()
        results = [
            s for s in results
            if q in s["ticker"].lower()
            or q in s["name"].lower()
            or q in s["sector"].lower()
        ]

    if filters.min_esg is not None:
        results = [s for s in results if s["esg_overall"] >= filters.min_esg]

    if filters.max_carbon is not None:
        results = [s for s in results if s["carbon_intensity"] <= filters.max_carbon]

    if filters.sectors:
        results = [s for s in results if s["sector"] in filters.sectors]

    if filters.regions:
        results = [s for s in results if s["region"] in filters.regions]

    if filters.themes:
        results = [
            s for s in results
            if any(t in s["themes"] for t in filters.themes)
        ]

    if filters.asset_types:
        results = [s for s in results if s["asset_type"] in filters.asset_types]

    if filters.min_market_cap is not None:
        results = [
            s for s in results if s["market_cap_b"] >= filters.min_market_cap
        ]

    if filters.max_controversy is not None:
        results = [
            s for s in results
            if s["controversy_score"] <= filters.max_controversy
        ]

    # Sort
    sort_key = filters.sort_by or "esg_overall"
    if sort_key in SECURITIES[0]:
        results.sort(key=lambda s: s.get(sort_key, 0), reverse=filters.sort_desc)

    return [Security(**s) for s in results]


def get_securities_by_tickers(tickers: list[str]) -> list[Security]:
    """Get specific securities by ticker."""
    ticker_set = {t.upper() for t in tickers}
    return [
        Security(**s)
        for s in SECURITIES
        if s["ticker"].upper() in ticker_set
    ]


def compare_securities(tickers: list[str]) -> dict:
    """Generate comparison data for 2-6 securities."""
    securities = get_securities_by_tickers(tickers)

    # Radar chart data
    radar_data = []
    for category in ["Environmental", "Social", "Governance"]:
        entry = {"category": category}
        for sec in securities:
            key = f"esg_{category.lower()}"
            entry[sec.ticker] = getattr(sec, key)
        radar_data.append(entry)

    # Carbon comparison
    carbon_data = [
        {
            "ticker": sec.ticker,
            "name": sec.name,
            "carbon_intensity": sec.carbon_intensity,
            "green_revenue_pct": sec.green_revenue_pct,
        }
        for sec in securities
    ]

    # Theme overlap
    all_themes: dict[str, list[str]] = {}
    for sec in securities:
        for t in sec.themes:
            label = THEMES.get(t, t)
            if label not in all_themes:
                all_themes[label] = []
            all_themes[label].append(sec.ticker)

    return {
        "securities": [s.model_dump() for s in securities],
        "radar_data": radar_data,
        "carbon_comparison": carbon_data,
        "theme_overlap": all_themes,
    }


def get_filter_options() -> dict:
    """Return available filter options."""
    return {
        "sectors": SECTORS,
        "regions": REGIONS,
        "themes": [{"id": k, "label": v} for k, v in THEMES.items()],
        "asset_types": ["stock", "etf"],
    }
