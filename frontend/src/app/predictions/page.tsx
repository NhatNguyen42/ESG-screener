"use client";

import { useState, useEffect } from "react";
import {
  getPredictions,
  getFeatureImportance,
  type Prediction,
} from "@/lib/api";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ScatterChart,
  Scatter,
  Cell,
} from "recharts";
import { Brain, TrendingUp, AlertTriangle } from "lucide-react";

const RETURN_COLORS = (val: number) => {
  if (val >= 0.15) return "#10b981";
  if (val >= 0.08) return "#3b82f6";
  if (val >= 0) return "#f59e0b";
  return "#ef4444";
};

export default function PredictionsPage() {
  const [predictions, setPredictions] = useState<Prediction[]>([]);
  const [features, setFeatures] = useState<{ feature: string; importance: number }[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([getPredictions(), getFeatureImportance()])
      .then(([predRes, featRes]) => {
        setPredictions(predRes.predictions);
        setFeatures(featRes.features);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <p className="p-8 text-center text-gray-500">Training ML model & generating predictions...</p>;
  }

  // Risk-return scatter data
  const scatterData = predictions.map((p) => ({
    ticker: p.ticker,
    predicted_return: p.predicted_return_12m,
    volatility: p.volatility,
    esg: p.current_esg,
    confidence: p.confidence,
  }));

  // Top 10 / bottom 5
  const top10 = predictions.slice(0, 10);
  const bottom5 = [...predictions].reverse().slice(0, 5).reverse();

  return (
    <div className="space-y-6">
      <div className="rounded-xl border border-gray-800 bg-gradient-to-br from-gray-900 to-gray-950 p-6">
        <div className="flex items-center gap-3">
          <Brain className="h-8 w-8 text-purple-400" />
          <div>
            <h1 className="text-2xl font-bold">ML Return Predictions</h1>
            <p className="mt-1 text-sm text-gray-400">
              Random Forest model trained on ESG features predicting 12-month returns.
              Feature importance shows which ESG factors drive predictions.
            </p>
          </div>
        </div>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        {/* Feature Importance */}
        <div className="rounded-xl border border-gray-800 bg-gray-900/50 p-4">
          <h2 className="mb-4 text-lg font-semibold">Feature Importance (Random Forest)</h2>
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={features} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
              <XAxis type="number" tick={{ fill: "#9ca3af", fontSize: 11 }} />
              <YAxis
                dataKey="feature"
                type="category"
                tick={{ fill: "#9ca3af", fontSize: 10 }}
                width={120}
              />
              <Tooltip
                contentStyle={{ background: "#1f2937", border: "1px solid #374151", borderRadius: 8 }}
                labelStyle={{ color: "#f3f4f6" }}
              />
              <Bar dataKey="importance" fill="#8b5cf6" radius={[0, 6, 6, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Risk-Return Scatter */}
        <div className="rounded-xl border border-gray-800 bg-gray-900/50 p-4">
          <h2 className="mb-4 text-lg font-semibold">Predicted Risk vs. Return</h2>
          <ResponsiveContainer width="100%" height={280}>
            <ScatterChart>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
              <XAxis
                dataKey="volatility"
                name="Volatility"
                tickFormatter={(v: number) => `${(v * 100).toFixed(0)}%`}
                tick={{ fill: "#9ca3af", fontSize: 11 }}
              />
              <YAxis
                dataKey="predicted_return"
                name="Predicted Return"
                tickFormatter={(v: number) => `${(v * 100).toFixed(0)}%`}
                tick={{ fill: "#9ca3af", fontSize: 11 }}
              />
              <Tooltip
                content={({ payload }) => {
                  if (!payload?.length) return null;
                  const d = payload[0].payload;
                  return (
                    <div className="rounded-lg border border-gray-700 bg-gray-800 p-2 text-xs">
                      <p className="font-bold text-emerald-400">{d.ticker}</p>
                      <p>Return: {(d.predicted_return * 100).toFixed(1)}%</p>
                      <p>Vol: {(d.volatility * 100).toFixed(1)}%</p>
                      <p>ESG: {d.esg}</p>
                      <p>Confidence: {(d.confidence * 100).toFixed(0)}%</p>
                    </div>
                  );
                }}
              />
              <Scatter data={scatterData}>
                {scatterData.map((entry, i) => (
                  <Cell key={i} fill={RETURN_COLORS(entry.predicted_return)} />
                ))}
              </Scatter>
            </ScatterChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Top Predictions Table */}
      <div className="grid gap-6 lg:grid-cols-2">
        <div className="rounded-xl border border-gray-800 bg-gray-900/50 p-4">
          <h2 className="mb-3 flex items-center gap-2 text-lg font-semibold">
            <TrendingUp className="h-5 w-5 text-emerald-400" />
            Top 10 Predicted Returns
          </h2>
          <div className="space-y-2">
            {top10.map((p, i) => (
              <div
                key={p.ticker}
                className="flex items-center justify-between rounded-lg border border-gray-800/50 bg-gray-800/30 px-3 py-2"
              >
                <div className="flex items-center gap-3">
                  <span className="text-xs text-gray-500 w-5">{i + 1}</span>
                  <span className="font-mono font-semibold text-emerald-400">{p.ticker}</span>
                  <span className="text-xs text-gray-400 max-w-[100px] truncate">{p.name}</span>
                </div>
                <div className="flex items-center gap-4">
                  <span className="text-sm font-bold text-emerald-400">
                    {(p.predicted_return_12m * 100).toFixed(1)}%
                  </span>
                  <span className="text-xs text-gray-500">
                    conf: {(p.confidence * 100).toFixed(0)}%
                  </span>
                  <span className="rounded bg-emerald-600/20 px-1.5 py-0.5 text-xs text-emerald-400">
                    ESG {p.current_esg}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="rounded-xl border border-gray-800 bg-gray-900/50 p-4">
          <h2 className="mb-3 flex items-center gap-2 text-lg font-semibold">
            <AlertTriangle className="h-5 w-5 text-red-400" />
            Bottom 5 Predicted Returns
          </h2>
          <div className="space-y-2">
            {bottom5.map((p) => (
              <div
                key={p.ticker}
                className="flex items-center justify-between rounded-lg border border-gray-800/50 bg-gray-800/30 px-3 py-2"
              >
                <div className="flex items-center gap-3">
                  <span className="font-mono font-semibold text-red-400">{p.ticker}</span>
                  <span className="text-xs text-gray-400 max-w-[120px] truncate">{p.name}</span>
                </div>
                <div className="flex items-center gap-4">
                  <span className="text-sm font-bold text-red-400">
                    {(p.predicted_return_12m * 100).toFixed(1)}%
                  </span>
                  <span className="text-xs text-gray-500">
                    conf: {(p.confidence * 100).toFixed(0)}%
                  </span>
                  <span className="rounded bg-red-600/20 px-1.5 py-0.5 text-xs text-red-400">
                    ESG {p.current_esg}
                  </span>
                </div>
              </div>
            ))}
          </div>

          {/* Model disclaimer */}
          <div className="mt-4 rounded-lg border border-gray-700/50 bg-gray-800/50 p-3">
            <p className="text-xs text-gray-500">
              <strong className="text-gray-400">Model Details:</strong> Random Forest Regressor
              (100 trees, max depth 6) trained on 9 ESG-related features.
              Predictions are illustrative and should not be used for actual investment decisions.
            </p>
          </div>
        </div>
      </div>

      {/* Individual Prediction Cards — top features breakdown */}
      <div>
        <h2 className="mb-4 text-lg font-semibold">Prediction Details — Top Feature Drivers</h2>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {predictions.slice(0, 9).map((p) => (
            <div
              key={p.ticker}
              className="rounded-xl border border-gray-800 bg-gray-900/50 p-4 space-y-3"
            >
              <div className="flex items-center justify-between">
                <span className="font-mono text-lg font-bold text-emerald-400">{p.ticker}</span>
                <span
                  className={`text-lg font-bold ${
                    p.predicted_return_12m >= 0.08 ? "text-emerald-400" : p.predicted_return_12m >= 0 ? "text-yellow-400" : "text-red-400"
                  }`}
                >
                  {(p.predicted_return_12m * 100).toFixed(1)}%
                </span>
              </div>
              <p className="text-xs text-gray-400 truncate">{p.name}</p>
              <div className="space-y-1.5">
                {p.top_features.slice(0, 4).map((f) => (
                  <div key={f.feature} className="flex items-center gap-2">
                    <span className="text-xs text-gray-500 w-28 truncate">{f.feature}</span>
                    <div className="flex-1 h-1.5 rounded-full bg-gray-800">
                      <div
                        className="h-1.5 rounded-full bg-purple-500"
                        style={{ width: `${f.importance * 400}%` }}
                      />
                    </div>
                    <span className="text-xs text-gray-500">{(f.importance * 100).toFixed(0)}%</span>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
