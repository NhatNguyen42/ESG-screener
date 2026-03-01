"""
Illustrative ML predictions — Random Forest on ESG features.
This demonstrates the concept; in production you'd train on real return data.
"""
from __future__ import annotations

import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from app.data.securities import SECURITIES


# ---------------------------------------------------------------------------
# Feature engineering
# ---------------------------------------------------------------------------

FEATURE_NAMES = [
    "esg_overall",
    "esg_environmental",
    "esg_social",
    "esg_governance",
    "carbon_intensity",
    "green_revenue_pct",
    "controversy_score",
    "market_cap_b",
    "volatility",
]

_model_cache: dict | None = None


def _build_features() -> tuple[np.ndarray, np.ndarray, list[str]]:
    """Build feature matrix and target vector from securities data."""
    X, y, tickers = [], [], []
    for s in SECURITIES:
        features = [s.get(f, 0) for f in FEATURE_NAMES]
        X.append(features)
        y.append(s.get("expected_return", 0.10))
        tickers.append(s["ticker"])
    return np.array(X), np.array(y), tickers


def _get_model():
    """Train (or return cached) Random Forest model."""
    global _model_cache
    if _model_cache is not None:
        return _model_cache

    X, y, tickers = _build_features()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=6,
        random_state=42,
        n_jobs=-1,
    )
    model.fit(X_scaled, y)

    _model_cache = {
        "model": model,
        "scaler": scaler,
        "tickers": tickers,
        "X": X,
        "y": y,
    }
    return _model_cache


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def predict_returns(tickers: list[str] | None = None) -> list[dict]:
    """Predict 12-month returns for given tickers (or all)."""
    cache = _get_model()
    model = cache["model"]
    scaler = cache["scaler"]

    sec_map = {s["ticker"]: s for s in SECURITIES}
    target_tickers = tickers or list(sec_map.keys())

    results = []
    for ticker in target_tickers:
        s = sec_map.get(ticker)
        if s is None:
            continue
        features = np.array([[s.get(f, 0) for f in FEATURE_NAMES]])
        features_scaled = scaler.transform(features)

        # Get prediction from all trees for confidence estimation
        tree_preds = np.array([t.predict(features_scaled)[0] for t in model.estimators_])
        predicted = float(tree_preds.mean())
        std = float(tree_preds.std())

        # Feature importance for this prediction
        importances = model.feature_importances_
        top_indices = np.argsort(importances)[::-1][:5]
        top_features = [
            {"feature": FEATURE_NAMES[i], "importance": round(float(importances[i]), 3)}
            for i in top_indices
        ]

        # Confidence: inverse of coefficient of variation
        confidence = max(0.3, min(0.95, 1 - std / max(abs(predicted), 0.01)))

        results.append({
            "ticker": ticker,
            "name": s["name"],
            "predicted_return_12m": round(predicted, 4),
            "confidence": round(confidence, 3),
            "current_esg": s["esg_overall"],
            "top_features": top_features,
            "volatility": s.get("volatility", 0.20),
        })

    results.sort(key=lambda x: x["predicted_return_12m"], reverse=True)
    return results


def get_feature_importance() -> list[dict]:
    """Get global feature importance from the model."""
    cache = _get_model()
    importances = cache["model"].feature_importances_
    result = [
        {"feature": FEATURE_NAMES[i], "importance": round(float(importances[i]), 3)}
        for i in range(len(FEATURE_NAMES))
    ]
    result.sort(key=lambda x: x["importance"], reverse=True)
    return result
