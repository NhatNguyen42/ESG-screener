"""
Optimizer routes — portfolio construction with ESG constraints.
"""
from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import Response

from app.schemas import OptimizerConstraints
from app.services.optimizer import optimize_portfolio
from app.services.screener import get_securities_by_tickers
from app.services.report import generate_portfolio_report

router = APIRouter(prefix="/api/optimizer", tags=["optimizer"])


@router.post("/optimize")
async def run_optimizer(constraints: OptimizerConstraints):
    """Run mean-variance optimization with ESG constraints."""
    if len(constraints.tickers) < 2:
        return {"error": "Provide at least 2 tickers"}
    if len(constraints.tickers) > 30:
        return {"error": "Maximum 30 tickers supported"}

    result = optimize_portfolio(constraints)
    return result.model_dump()


@router.post("/report")
async def download_report(constraints: OptimizerConstraints):
    """Generate and download PDF report for optimized portfolio."""
    result = optimize_portfolio(constraints)
    securities = get_securities_by_tickers(constraints.tickers)
    sec_dicts = [s.model_dump() for s in securities]

    pdf_bytes = generate_portfolio_report(result.model_dump(), sec_dicts)

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=esg_portfolio_report.pdf"},
    )
