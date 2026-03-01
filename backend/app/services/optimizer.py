"""
Mean-Variance Optimizer with ESG constraints.
Uses scipy.optimize for portfolio construction.
"""
from __future__ import annotations

import numpy as np
from scipy.optimize import minimize
from app.data.securities import SECURITIES
from app.schemas import OptimizerConstraints, OptimizedPortfolio


# ---------------------------------------------------------------------------
# Simulated return / covariance helpers  (deterministic seed per ticker set)
# ---------------------------------------------------------------------------

def _build_expected_returns(tickers: list[str]) -> np.ndarray:
    """Generate realistic expected annual returns based on the security data."""
    sec_map = {s["ticker"]: s for s in SECURITIES}
    returns = []
    for t in tickers:
        s = sec_map.get(t)
        if s is None:
            returns.append(0.08)
            continue
        # Higher-ESG securities get a slight return premium (illustrative)
        base = s.get("expected_return", 0.10)
        esg_bonus = (s["esg_overall"] - 50) * 0.0005
        returns.append(base + esg_bonus)
    return np.array(returns)


def _build_covariance_matrix(tickers: list[str]) -> np.ndarray:
    """Build a synthetic but positive-definite covariance matrix."""
    n = len(tickers)
    rng = np.random.RandomState(sum(ord(c) for t in tickers for c in t))
    # Random correlation base
    A = rng.randn(n, max(n, 10))
    cov = A @ A.T / A.shape[1]
    # Scale to realistic volatilities (12-35%)
    sec_map = {s["ticker"]: s for s in SECURITIES}
    vols = []
    for t in tickers:
        s = sec_map.get(t)
        vols.append(s.get("volatility", 0.20) if s else 0.20)
    vols = np.array(vols)
    # Convert correlation → covariance
    stds = np.sqrt(np.diag(cov))
    corr = cov / np.outer(stds, stds)
    cov = corr * np.outer(vols, vols)
    return cov


# ---------------------------------------------------------------------------
# Optimizer
# ---------------------------------------------------------------------------

RISK_FREE_RATE = 0.05  # 5% for 2024-era rates


def optimize_portfolio(constraints: OptimizerConstraints) -> OptimizedPortfolio:
    tickers = constraints.tickers
    n = len(tickers)
    mu = _build_expected_returns(tickers)
    cov = _build_covariance_matrix(tickers)
    sec_map = {s["ticker"]: s for s in SECURITIES}

    # Helper lambdas
    port_return = lambda w: float(w @ mu)
    port_vol = lambda w: float(np.sqrt(w @ cov @ w))
    port_sharpe = lambda w: (port_return(w) - RISK_FREE_RATE) / max(port_vol(w), 1e-9)

    # ESG & carbon lookups
    esg_scores = np.array([sec_map.get(t, {}).get("esg_overall", 50) for t in tickers])
    carbon_vals = np.array([sec_map.get(t, {}).get("carbon_intensity", 100) for t in tickers])

    # Bounds
    max_w = constraints.max_single_weight
    bounds = [(0, max_w) for _ in range(n)]

    # Constraints list
    cons: list[dict] = [
        {"type": "eq", "fun": lambda w: np.sum(w) - 1.0},  # fully invested
    ]

    if constraints.min_esg_score is not None:
        min_esg = constraints.min_esg_score
        cons.append({"type": "ineq", "fun": lambda w: float(w @ esg_scores) - min_esg})

    if constraints.max_carbon_intensity is not None:
        max_carb = constraints.max_carbon_intensity
        cons.append({"type": "ineq", "fun": lambda w: max_carb - float(w @ carbon_vals)})

    # Sector weight caps
    if constraints.max_sector_weight is not None:
        sectors_arr = [sec_map.get(t, {}).get("sector", "Unknown") for t in tickers]
        unique_sectors = set(sectors_arr)
        for sect in unique_sectors:
            mask = np.array([1 if s == sect else 0 for s in sectors_arr], dtype=float)
            cap = constraints.max_sector_weight
            cons.append({"type": "ineq", "fun": lambda w, m=mask, c=cap: c - float(w @ m)})

    # Objective function
    if constraints.objective == "max_sharpe":
        obj = lambda w: -port_sharpe(w)
    elif constraints.objective == "max_esg":
        obj = lambda w: -float(w @ esg_scores)
    else:  # min_variance
        obj = lambda w: port_vol(w)

    x0 = np.ones(n) / n
    result = minimize(obj, x0, method="SLSQP", bounds=bounds, constraints=cons,
                      options={"maxiter": 1000, "ftol": 1e-12})

    weights = result.x if result.success else x0
    weights = np.maximum(weights, 0)
    weights /= weights.sum()  # renormalize

    # Build efficient frontier (20 points)
    frontier = _build_frontier(tickers, mu, cov, bounds, cons, weights)

    portfolio_esg = float(weights @ esg_scores)
    portfolio_carbon = float(weights @ carbon_vals)

    allocation = []
    for i, t in enumerate(tickers):
        if weights[i] > 0.001:
            s = sec_map.get(t, {})
            allocation.append({
                "ticker": t,
                "name": s.get("name", t),
                "weight": round(float(weights[i]), 4),
                "sector": s.get("sector", "Unknown"),
                "esg_score": s.get("esg_overall", 50),
            })
    allocation.sort(key=lambda x: x["weight"], reverse=True)

    return OptimizedPortfolio(
        weights=allocation,
        expected_return=round(port_return(weights), 4),
        volatility=round(port_vol(weights), 4),
        sharpe_ratio=round(port_sharpe(weights), 4),
        portfolio_esg_score=round(portfolio_esg, 1),
        portfolio_carbon_intensity=round(portfolio_carbon, 1),
        efficient_frontier=frontier,
        objective_used=constraints.objective,
    )


def _build_frontier(
    tickers: list[str],
    mu: np.ndarray,
    cov: np.ndarray,
    bounds: list,
    extra_cons: list,
    optimal_w: np.ndarray,
) -> list[dict]:
    """Generate ~20 points on the efficient frontier."""
    n = len(tickers)
    points = []
    target_returns = np.linspace(float(mu.min()) * 0.6, float(mu.max()) * 1.1, 20)

    for tr in target_returns:
        cons = extra_cons.copy()
        cons.append({"type": "eq", "fun": lambda w, t=tr: float(w @ mu) - t})
        obj = lambda w: float(np.sqrt(w @ cov @ w))
        x0 = np.ones(n) / n
        res = minimize(obj, x0, method="SLSQP", bounds=bounds, constraints=cons,
                       options={"maxiter": 500, "ftol": 1e-10})
        if res.success:
            w = np.maximum(res.x, 0)
            w /= w.sum()
            points.append({
                "expected_return": round(float(w @ mu), 4),
                "volatility": round(float(np.sqrt(w @ cov @ w)), 4),
            })

    # Add the optimal portfolio point
    points.append({
        "expected_return": round(float(optimal_w @ mu), 4),
        "volatility": round(float(np.sqrt(optimal_w @ cov @ optimal_w)), 4),
        "is_optimal": True,
    })

    points.sort(key=lambda p: p["volatility"])
    return points
