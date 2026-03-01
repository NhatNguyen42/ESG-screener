"""
ESG & Thematic Investment Screener + Optimizer
FastAPI Backend — Main Application
Created by Nhat Nguyen (Nhatmn114@gmail.com)
"""
from __future__ import annotations

import os
import re
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: pre-warm the ML model
    from app.services.ml_predictions import _get_model
    _get_model()
    print("ML model pre-warmed.")
    yield


app = FastAPI(
    title="ESG & Thematic Investment Screener",
    version="1.0.0",
    description="Portfolio screening, ESG-constrained optimization, ML predictions & sentiment analysis.",
    lifespan=lifespan,
)

# ---------------------------------------------------------------------------
# CORS — allow Vercel frontend + local dev
# ---------------------------------------------------------------------------
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")

origins = [
    frontend_url,
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# Also allow any Vercel preview deployments
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
from app.routes.screener import router as screener_router
from app.routes.optimizer import router as optimizer_router
from app.routes.ml import router as ml_router

app.include_router(screener_router)
app.include_router(optimizer_router)
app.include_router(ml_router)


@app.get("/")
async def root():
    return {
        "app": "ESG & Thematic Investment Screener",
        "version": "1.0.0",
        "author": "Nhat Nguyen",
        "endpoints": {
            "screener": "/api/screener/securities",
            "filters": "/api/screener/filters",
            "compare": "/api/screener/compare",
            "optimize": "/api/optimizer/optimize",
            "report": "/api/optimizer/report",
            "predictions": "/api/ml/predictions",
            "feature_importance": "/api/ml/feature-importance",
            "sentiment": "/api/ml/sentiment/{ticker}",
        },
    }


@app.get("/api/health")
async def health():
    return {"status": "ok", "service": "esg-screener-backend"}


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8080"))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
