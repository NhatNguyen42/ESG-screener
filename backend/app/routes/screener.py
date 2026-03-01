"""
Screener routes — browse, filter, compare securities.
"""
from __future__ import annotations

from fastapi import APIRouter, Query
from typing import Optional

from app.schemas import SecurityFilters
from app.services.screener import (
    filter_securities,
    get_all_securities,
    get_securities_by_tickers,
    compare_securities,
    get_filter_options,
)

router = APIRouter(prefix="/api/screener", tags=["screener"])


@router.get("/securities")
async def list_securities(
    search: Optional[str] = None,
    min_esg: Optional[float] = None,
    max_carbon: Optional[float] = None,
    sectors: Optional[str] = None,       # comma-separated
    regions: Optional[str] = None,       # comma-separated
    themes: Optional[str] = None,        # comma-separated
    asset_types: Optional[str] = None,   # comma-separated
    min_market_cap: Optional[float] = None,
    max_controversy: Optional[int] = None,
    sort_by: Optional[str] = "esg_overall",
    sort_desc: bool = True,
):
    """List & filter securities."""
    filters = SecurityFilters(
        search=search,
        min_esg=min_esg,
        max_carbon=max_carbon,
        sectors=sectors.split(",") if sectors else None,
        regions=regions.split(",") if regions else None,
        themes=themes.split(",") if themes else None,
        asset_types=asset_types.split(",") if asset_types else None,
        min_market_cap=min_market_cap,
        max_controversy=max_controversy,
        sort_by=sort_by,
        sort_desc=sort_desc,
    )
    securities = filter_securities(filters)
    return {"securities": [s.model_dump() for s in securities], "total": len(securities)}


@router.get("/securities/{ticker}")
async def get_security(ticker: str):
    """Get a single security by ticker."""
    results = get_securities_by_tickers([ticker])
    if not results:
        return {"error": f"Ticker {ticker} not found"}
    return results[0].model_dump()


@router.get("/filters")
async def list_filters():
    """Get available filter options."""
    return get_filter_options()


@router.post("/compare")
async def compare(tickers: list[str]):
    """Compare 2-6 securities side by side."""
    if len(tickers) < 2 or len(tickers) > 6:
        return {"error": "Provide 2-6 tickers for comparison"}
    return compare_securities(tickers)
