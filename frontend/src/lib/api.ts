/* ── API client for ESG Screener backend ─────────────── */

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8080";

async function fetchAPI<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
  });
  if (!res.ok) throw new Error(`API ${res.status}: ${res.statusText}`);
  return res.json();
}

/* ── Screener ──────────────────────────────────────────── */

export interface Security {
  ticker: string;
  name: string;
  asset_type: string;
  sector: string;
  region: string;
  market_cap_b: number;
  price: number;
  ytd_return: number;
  dividend_yield: number;
  esg_overall: number;
  esg_environmental: number;
  esg_social: number;
  esg_governance: number;
  carbon_intensity: number;
  green_revenue_pct: number;
  themes: string[];
  controversy_score: number;
  controversy_summary: string | null;
  expected_return?: number;
  volatility?: number;
}

export interface FilterOptions {
  sectors: string[];
  regions: string[];
  themes: { id: string; label: string }[];
  asset_types: string[];
}

export interface ScreenerFilters {
  search?: string;
  min_esg?: number;
  max_carbon?: number;
  sectors?: string[];
  regions?: string[];
  themes?: string[];
  asset_types?: string[];
  min_market_cap?: number;
  max_controversy?: number;
  sort_by?: string;
  sort_desc?: boolean;
}

export async function getSecurities(filters: ScreenerFilters = {}) {
  const params = new URLSearchParams();
  if (filters.search) params.set("search", filters.search);
  if (filters.min_esg != null) params.set("min_esg", String(filters.min_esg));
  if (filters.max_carbon != null) params.set("max_carbon", String(filters.max_carbon));
  if (filters.sectors?.length) params.set("sectors", filters.sectors.join(","));
  if (filters.regions?.length) params.set("regions", filters.regions.join(","));
  if (filters.themes?.length) params.set("themes", filters.themes.join(","));
  if (filters.asset_types?.length) params.set("asset_types", filters.asset_types.join(","));
  if (filters.min_market_cap != null) params.set("min_market_cap", String(filters.min_market_cap));
  if (filters.max_controversy != null) params.set("max_controversy", String(filters.max_controversy));
  if (filters.sort_by) params.set("sort_by", filters.sort_by);
  if (filters.sort_desc != null) params.set("sort_desc", String(filters.sort_desc));

  return fetchAPI<{ securities: Security[]; total: number }>(
    `/api/screener/securities?${params}`
  );
}

export async function getFilterOptions() {
  return fetchAPI<FilterOptions>("/api/screener/filters");
}

export async function compareTickers(tickers: string[]) {
  return fetchAPI<{
    securities: Security[];
    radar_data: { category: string; [ticker: string]: string | number }[];
    carbon_comparison: { ticker: string; name: string; carbon_intensity: number; green_revenue_pct: number }[];
    theme_overlap: Record<string, string[]>;
  }>("/api/screener/compare", {
    method: "POST",
    body: JSON.stringify(tickers),
  });
}

/* ── Optimizer ─────────────────────────────────────────── */

export interface OptimizerConstraints {
  tickers: string[];
  min_esg_score?: number;
  max_carbon_intensity?: number;
  max_single_weight?: number;
  max_sector_weight?: number;
  objective?: string;
}

export interface PortfolioAllocation {
  ticker: string;
  name: string;
  weight: number;
  sector: string;
  esg_score: number;
}

export interface OptimizedPortfolio {
  weights: PortfolioAllocation[];
  expected_return: number;
  volatility: number;
  sharpe_ratio: number;
  portfolio_esg_score: number;
  portfolio_carbon_intensity: number;
  efficient_frontier: { expected_return: number; volatility: number; is_optimal?: boolean }[];
  objective_used: string;
}

export async function optimizePortfolio(constraints: OptimizerConstraints) {
  return fetchAPI<OptimizedPortfolio>("/api/optimizer/optimize", {
    method: "POST",
    body: JSON.stringify(constraints),
  });
}

export async function downloadReport(constraints: OptimizerConstraints): Promise<Blob> {
  const res = await fetch(`${API_BASE}/api/optimizer/report`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(constraints),
  });
  if (!res.ok) throw new Error("Report generation failed");
  return res.blob();
}

/* ── ML Predictions ────────────────────────────────────── */

export interface Prediction {
  ticker: string;
  name: string;
  predicted_return_12m: number;
  confidence: number;
  current_esg: number;
  top_features: { feature: string; importance: number }[];
  volatility: number;
}

export async function getPredictions(tickers?: string[]) {
  const params = tickers ? `?tickers=${tickers.join(",")}` : "";
  return fetchAPI<{ predictions: Prediction[]; total: number }>(
    `/api/ml/predictions${params}`
  );
}

export async function getFeatureImportance() {
  return fetchAPI<{ features: { feature: string; importance: number }[] }>(
    "/api/ml/feature-importance"
  );
}

/* ── Sentiment ─────────────────────────────────────────── */

export interface SentimentData {
  ticker: string;
  sentiment_score: number;
  label: string;
  key_topics: string[];
  controversy_flag: boolean;
  summary: string;
}

export async function getSentiment(ticker: string) {
  return fetchAPI<SentimentData>(`/api/ml/sentiment/${ticker}`);
}

export async function getBatchSentiment(tickers: string[]) {
  return fetchAPI<{ sentiments: SentimentData[] }>("/api/ml/sentiment/batch", {
    method: "POST",
    body: JSON.stringify(tickers),
  });
}
