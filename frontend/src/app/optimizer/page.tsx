"use client";

import { useState, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import {
  optimizePortfolio,
  downloadReport,
  type OptimizerConstraints,
  type OptimizedPortfolio,
} from "@/lib/api";
import {
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Legend,
  PieLabelRenderProps,
} from "recharts";

const COLORS = [
  "#10b981", "#3b82f6", "#f59e0b", "#ef4444", "#8b5cf6",
  "#ec4899", "#06b6d4", "#84cc16", "#f97316", "#6366f1",
];

function OptimizerContent() {
  const searchParams = useSearchParams();
  const tickerParam = searchParams.get("tickers") || "";
  const [input, setInput] = useState(tickerParam);
  const [objective, setObjective] = useState("max_sharpe");
  const [minEsg, setMinEsg] = useState(50);
  const [maxCarbon, setMaxCarbon] = useState(200);
  const [maxWeight, setMaxWeight] = useState(0.3);
  const [maxSector, setMaxSector] = useState(0.4);
  const [result, setResult] = useState<OptimizedPortfolio | null>(null);
  const [loading, setLoading] = useState(false);
  const [downloading, setDownloading] = useState(false);

  const buildConstraints = (): OptimizerConstraints => ({
    tickers: input.split(",").map((s) => s.trim().toUpperCase()).filter(Boolean),
    objective,
    min_esg_score: minEsg,
    max_carbon_intensity: maxCarbon,
    max_single_weight: maxWeight,
    max_sector_weight: maxSector,
  });

  const handleOptimize = async () => {
    const c = buildConstraints();
    if (c.tickers.length < 2) return;
    setLoading(true);
    try {
      const res = await optimizePortfolio(c);
      setResult(res);
    } catch (e) {
      console.error(e);
    }
    setLoading(false);
  };

  const handleDownload = async () => {
    setDownloading(true);
    try {
      const blob = await downloadReport(buildConstraints());
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "esg_portfolio_report.pdf";
      a.click();
      URL.revokeObjectURL(url);
    } catch (e) {
      console.error(e);
    }
    setDownloading(false);
  };

  return (
    <div className="space-y-6">
      <div className="rounded-xl border border-gray-800 bg-gradient-to-br from-gray-900 to-gray-950 p-6">
        <h1 className="text-2xl font-bold">Build My Green Portfolio</h1>
        <p className="mt-1 text-sm text-gray-400">
          Mean-variance optimizer with ESG constraints. Select securities, set your preferences,
          and get an optimized allocation with efficient frontier visualization.
        </p>
      </div>

      {/* Controls */}
      <div className="grid gap-4 rounded-xl border border-gray-800 bg-gray-900/50 p-4 md:grid-cols-2 lg:grid-cols-3">
        <div className="md:col-span-2 lg:col-span-3">
          <label className="mb-1 block text-xs font-medium text-gray-400">
            Tickers (comma-separated, min 2)
          </label>
          <input
            type="text"
            placeholder="MSFT, GOOGL, NVDA, NEE, ENPH, ICLN, BLK"
            className="w-full rounded-lg border border-gray-700 bg-gray-800 px-4 py-2 text-sm focus:border-emerald-500 focus:outline-none"
            value={input}
            onChange={(e) => setInput(e.target.value)}
          />
        </div>

        <div>
          <label className="mb-1 block text-xs font-medium text-gray-400">Objective</label>
          <select
            className="w-full rounded-lg border border-gray-700 bg-gray-800 p-2 text-sm"
            value={objective}
            onChange={(e) => setObjective(e.target.value)}
          >
            <option value="max_sharpe">Maximize Sharpe Ratio</option>
            <option value="min_variance">Minimize Variance</option>
            <option value="max_esg">Maximize ESG Score</option>
          </select>
        </div>

        <div>
          <label className="mb-1 block text-xs font-medium text-gray-400">
            Min ESG Score: {minEsg}
          </label>
          <input
            type="range"
            min={0}
            max={90}
            value={minEsg}
            onChange={(e) => setMinEsg(Number(e.target.value))}
            className="w-full accent-emerald-500"
          />
        </div>

        <div>
          <label className="mb-1 block text-xs font-medium text-gray-400">
            Max Carbon: {maxCarbon}
          </label>
          <input
            type="range"
            min={10}
            max={500}
            step={10}
            value={maxCarbon}
            onChange={(e) => setMaxCarbon(Number(e.target.value))}
            className="w-full accent-emerald-500"
          />
        </div>

        <div>
          <label className="mb-1 block text-xs font-medium text-gray-400">
            Max Single Weight: {(maxWeight * 100).toFixed(0)}%
          </label>
          <input
            type="range"
            min={5}
            max={100}
            value={maxWeight * 100}
            onChange={(e) => setMaxWeight(Number(e.target.value) / 100)}
            className="w-full accent-emerald-500"
          />
        </div>

        <div>
          <label className="mb-1 block text-xs font-medium text-gray-400">
            Max Sector Weight: {(maxSector * 100).toFixed(0)}%
          </label>
          <input
            type="range"
            min={10}
            max={100}
            value={maxSector * 100}
            onChange={(e) => setMaxSector(Number(e.target.value) / 100)}
            className="w-full accent-emerald-500"
          />
        </div>

        <div className="flex items-end gap-3 md:col-span-2 lg:col-span-1">
          <button
            onClick={handleOptimize}
            disabled={loading}
            className="flex-1 rounded-lg bg-emerald-600 px-4 py-2 text-sm font-semibold hover:bg-emerald-700 disabled:opacity-50"
          >
            {loading ? "Optimizing..." : "Optimize Portfolio"}
          </button>
        </div>
      </div>

      {/* Results */}
      {result && (
        <div className="space-y-6">
          {/* KPI Cards */}
          <div className="grid grid-cols-2 gap-4 lg:grid-cols-5">
            {[
              { label: "Expected Return", value: `${(result.expected_return * 100).toFixed(1)}%`, color: "text-emerald-400" },
              { label: "Volatility", value: `${(result.volatility * 100).toFixed(1)}%`, color: "text-yellow-400" },
              { label: "Sharpe Ratio", value: result.sharpe_ratio.toFixed(2), color: "text-blue-400" },
              { label: "ESG Score", value: result.portfolio_esg_score.toFixed(1), color: "text-emerald-400" },
              { label: "Carbon Intensity", value: result.portfolio_carbon_intensity.toFixed(0), color: "text-orange-400" },
            ].map((kpi) => (
              <div key={kpi.label} className="rounded-xl border border-gray-800 bg-gray-900/50 p-4">
                <p className="text-xs text-gray-500">{kpi.label}</p>
                <p className={`mt-1 text-2xl font-bold ${kpi.color}`}>{kpi.value}</p>
              </div>
            ))}
          </div>

          <div className="grid gap-6 lg:grid-cols-2">
            {/* Pie Chart: Allocation */}
            <div className="rounded-xl border border-gray-800 bg-gray-900/50 p-4">
              <h2 className="mb-4 text-lg font-semibold">Portfolio Allocation</h2>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={result.weights}
                    dataKey="weight"
                    nameKey="ticker"
                    cx="50%"
                    cy="50%"
                    outerRadius={110}
                    label={(props: PieLabelRenderProps) =>
                      `${props.name ?? ""} ${((props.value as number) * 100).toFixed(0)}%`
                    }
                    labelLine={{ stroke: "#6b7280" }}
                  >
                    {result.weights.map((_, i) => (
                      <Cell key={i} fill={COLORS[i % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip
                    formatter={(val: number | undefined) => val != null ? `${(val * 100).toFixed(1)}%` : ""}
                    contentStyle={{ background: "#1f2937", border: "1px solid #374151", borderRadius: 8 }}
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>

            {/* Efficient Frontier */}
            <div className="rounded-xl border border-gray-800 bg-gray-900/50 p-4">
              <h2 className="mb-4 text-lg font-semibold">Efficient Frontier</h2>
              <ResponsiveContainer width="100%" height={300}>
                <ScatterChart>
                  <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                  <XAxis
                    dataKey="volatility"
                    name="Volatility"
                    tickFormatter={(v: number) => `${(v * 100).toFixed(0)}%`}
                    tick={{ fill: "#9ca3af", fontSize: 11 }}
                    label={{ value: "Volatility", position: "bottom", fill: "#6b7280", fontSize: 11 }}
                  />
                  <YAxis
                    dataKey="expected_return"
                    name="Return"
                    tickFormatter={(v: number) => `${(v * 100).toFixed(0)}%`}
                    tick={{ fill: "#9ca3af", fontSize: 11 }}
                    label={{ value: "Return", angle: -90, position: "left", fill: "#6b7280", fontSize: 11 }}
                  />
                  <Tooltip
                    formatter={(val: number | undefined) => val != null ? `${(val * 100).toFixed(2)}%` : ""}
                    contentStyle={{ background: "#1f2937", border: "1px solid #374151", borderRadius: 8 }}
                    labelStyle={{ color: "#f3f4f6" }}
                  />
                  <Scatter
                    name="Frontier"
                    data={result.efficient_frontier.filter((p) => !p.is_optimal)}
                    fill="#3b82f6"
                    line={{ stroke: "#3b82f6", strokeWidth: 2 }}
                    lineType="fitting"
                  />
                  <Scatter
                    name="Optimal"
                    data={result.efficient_frontier.filter((p) => p.is_optimal)}
                    fill="#10b981"
                    shape="star"
                  />
                </ScatterChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Allocation table */}
          <div className="overflow-x-auto rounded-xl border border-gray-800">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-gray-800 bg-gray-900/70 text-left text-xs uppercase text-gray-500">
                  <th className="p-3">Ticker</th>
                  <th className="p-3">Name</th>
                  <th className="p-3">Weight</th>
                  <th className="p-3">Sector</th>
                  <th className="p-3">ESG Score</th>
                </tr>
              </thead>
              <tbody>
                {result.weights.map((w, i) => (
                  <tr key={w.ticker} className="border-b border-gray-800/50">
                    <td className="p-3 font-mono font-semibold text-emerald-400">{w.ticker}</td>
                    <td className="p-3">{w.name}</td>
                    <td className="p-3">
                      <div className="flex items-center gap-2">
                        <div
                          className="h-2 rounded-full"
                          style={{
                            width: `${w.weight * 200}px`,
                            background: COLORS[i % COLORS.length],
                          }}
                        />
                        <span className="text-xs">{(w.weight * 100).toFixed(1)}%</span>
                      </div>
                    </td>
                    <td className="p-3 text-gray-400">{w.sector}</td>
                    <td className="p-3">{w.esg_score}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Download button */}
          <button
            onClick={handleDownload}
            disabled={downloading}
            className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium hover:bg-blue-700 disabled:opacity-50"
          >
            {downloading ? "Generating PDF..." : "Download PDF Report"}
          </button>
        </div>
      )}
    </div>
  );
}

export default function OptimizerPage() {
  return (
    <Suspense fallback={<p className="text-center text-gray-500 p-8">Loading...</p>}>
      <OptimizerContent />
    </Suspense>
  );
}
