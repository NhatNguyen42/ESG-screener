"""
ML & Sentiment routes — predictions and sentiment analysis.
"""
from __future__ import annotations

from fastapi import APIRouter
from typing import Optional

from app.services.ml_predictions import predict_returns, get_feature_importance
from app.services.sentiment import get_sentiment, get_batch_sentiment

router = APIRouter(prefix="/api/ml", tags=["ml"])


@router.get("/predictions")
async def predictions(tickers: Optional[str] = None):
    """Get ML return predictions. Pass comma-separated tickers or omit for all."""
    ticker_list = tickers.split(",") if tickers else None
    results = predict_returns(ticker_list)
    return {"predictions": results, "total": len(results)}


@router.get("/feature-importance")
async def feature_importance():
    """Get global feature importance from the Random Forest model."""
    return {"features": get_feature_importance()}


@router.get("/sentiment/{ticker}")
async def sentiment(ticker: str):
    """Get ESG sentiment for a single ticker."""
    result = await get_sentiment(ticker)
    return result


@router.post("/sentiment/batch")
async def batch_sentiment(tickers: list[str]):
    """Get sentiment for multiple tickers."""
    results = await get_batch_sentiment(tickers)
    return {"sentiments": results}
