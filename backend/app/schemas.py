"""Pydantic schemas for the ESG Screener API."""
from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, Field


# ── Security / ETF ─────────────────────────────────────────
class Security(BaseModel):
    ticker: str
    name: str
    asset_type: str = Field(description="stock | etf")
    sector: str
    region: str
    market_cap_b: float = Field(description="Market cap in billions USD")
    price: float
    ytd_return: float
    dividend_yield: float

    # ESG scores (0-100)
    esg_overall: float
    esg_environmental: float
    esg_social: float
    esg_governance: float

    # Carbon metrics
    carbon_intensity: float = Field(description="tCO2e per $M revenue")
    green_revenue_pct: float = Field(description="% revenue from green activities")

    # Thematic tags
    themes: list[str] = Field(default_factory=list)

    # Controversy
    controversy_score: float = Field(description="0 (none) to 5 (severe)")
    controversy_summary: Optional[str] = None


class SecurityFilters(BaseModel):
    min_esg: Optional[float] = None
    max_carbon: Optional[float] = None
    sectors: Optional[list[str]] = None
    regions: Optional[list[str]] = None
    themes: Optional[list[str]] = None
    asset_types: Optional[list[str]] = None
    min_market_cap: Optional[float] = None
    max_controversy: Optional[float] = None
    search: Optional[str] = None
    sort_by: Optional[str] = "esg_overall"
    sort_desc: bool = True


# ── Portfolio Optimizer ────────────────────────────────────
class OptimizerConstraints(BaseModel):
    tickers: list[str] = Field(min_length=2)
    min_esg_score: float = Field(default=50.0, ge=0, le=100)
    max_carbon_intensity: float = Field(default=200.0, ge=0)
    max_single_weight: float = Field(default=0.30, ge=0.05, le=1.0)
    min_single_weight: float = Field(default=0.02, ge=0, le=0.5)
    max_sector_weight: float = Field(default=0.40, ge=0.1, le=1.0)
    target_return: Optional[float] = None
    objective: str = Field(default="max_sharpe", description="max_sharpe | min_variance | max_esg")


class OptimizedPortfolio(BaseModel):
    weights: list[dict]  # [{ticker, name, weight, sector, esg_score}, ...]
    expected_return: float
    volatility: float
    sharpe_ratio: float
    portfolio_esg_score: float
    portfolio_carbon_intensity: float
    efficient_frontier: list[dict]
    objective_used: str


# ── ML Predictions ─────────────────────────────────────────
class ReturnPrediction(BaseModel):
    ticker: str
    predicted_return_12m: float
    confidence: float
    top_features: list[dict]


class SentimentResult(BaseModel):
    ticker: str
    company_name: str
    sentiment_score: float = Field(description="-1 (negative) to 1 (positive)")
    sentiment_label: str
    key_topics: list[str]
    controversy_flag: bool
    summary: str


# ── Comparison ─────────────────────────────────────────────
class ComparisonRequest(BaseModel):
    tickers: list[str] = Field(min_length=2, max_length=6)


class ComparisonResult(BaseModel):
    securities: list[Security]
    radar_data: list[dict]
    carbon_comparison: list[dict]
    theme_overlap: dict[str, list[str]]
