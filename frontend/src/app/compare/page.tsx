"use client";

import { useState, useEffect, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import { compareTickers, getSentiment, type Security, type SentimentData } from "@/lib/api";
import {
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  Legend,
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from "recharts";

const COLORS = ["#10b981", "#3b82f6", "#f59e0b", "#ef4444", "#8b5cf6", "#ec4899"];

function CompareContent() {
  const searchParams = useSearchParams();
  const tickerParam = searchParams.get("tickers") || "";
  const [tickers, setTickers] = useState<string[]>(tickerParam ? tickerParam.split(",") : []);
  const [input, setInput] = useState(tickerParam);
  const [data, setData] = useState<{
    securities: Security[];
    radar_data: { category: string; [k: string]: string | number }[];
    carbon_comparison: { ticker: string; name: string; carbon_intensity: number; green_revenue_pct: number }[];
    theme_overlap: Record<string, string[]>;
  } | null>(null);
  const [sentiments, setSentiments] = useState<Record<string, SentimentData>>({});
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (tickers.length < 2) return;
    setLoading(true);
    compareTickers(tickers)
      .then((res) => {
        setData(res);
        // Fetch sentiments in parallel
        Promise.all(tickers.map((t) => getSentiment(t).catch(() => null))).then(
          (results) => {
            const map: Record<string, SentimentData> = {};
            results.forEach((r) => { if (r) map[r.ticker] = r; });
            setSentiments(map);
          }
        );
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [tickers]);

  const handleCompare = () => {
    const t = input.split(",").map((s) => s.trim().toUpperCase()).filter(Boolean);
    if (t.length >= 2) setTickers(t);
  };

  return (
    <div className="space-y-6">
      <div className="rounded-xl border border-gray-800 bg-gradient-to-br from-gray-900 to-gray-950 p-6">
        <h1 className="text-2xl font-bold">Security Comparison</h1>
        <p className="mt-1 text-sm text-gray-400">
          Compare 2-6 securities side by side: ESG radar, carbon metrics, themes & sentiment.
        </p>
      </div>

      {/* Input */}
      <div className="flex items-center gap-3">
        <input
          type="text"
          placeholder="e.g. MSFT, GOOGL, TSLA, NEE"
          className="flex-1 rounded-lg border border-gray-700 bg-gray-900 px-4 py-2 text-sm focus:border-emerald-500 focus:outline-none"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleCompare()}
        />
        <button
          onClick={handleCompare}
          className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium hover:bg-blue-700"
        >
          Compare
        </button>
      </div>

      {loading && <p className="text-center text-gray-500">Loading comparison...</p>}

      {data && (
        <div className="space-y-6">
          {/* ESG Radar Chart */}
          <div className="rounded-xl border border-gray-800 bg-gray-900/50 p-4">
            <h2 className="mb-4 text-lg font-semibold">ESG Score Radar</h2>
            <ResponsiveContainer width="100%" height={350}>
              <RadarChart data={data.radar_data}>
                <PolarGrid stroke="#374151" />
                <PolarAngleAxis dataKey="category" tick={{ fill: "#9ca3af", fontSize: 12 }} />
                <PolarRadiusAxis domain={[0, 100]} tick={{ fill: "#6b7280", fontSize: 10 }} />
                {tickers.map((t, i) => (
                  <Radar
                    key={t}
                    name={t}
                    dataKey={t}
                    stroke={COLORS[i % COLORS.length]}
                    fill={COLORS[i % COLORS.length]}
                    fillOpacity={0.15}
                    strokeWidth={2}
                  />
                ))}
                <Legend />
              </RadarChart>
            </ResponsiveContainer>
          </div>

          {/* Carbon Comparison Bar Chart */}
          <div className="grid gap-6 md:grid-cols-2">
            <div className="rounded-xl border border-gray-800 bg-gray-900/50 p-4">
              <h2 className="mb-4 text-lg font-semibold">Carbon Intensity (tCO2e/$M)</h2>
              <ResponsiveContainer width="100%" height={250}>
                <BarChart data={data.carbon_comparison}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                  <XAxis dataKey="ticker" tick={{ fill: "#9ca3af", fontSize: 11 }} />
                  <YAxis tick={{ fill: "#9ca3af", fontSize: 11 }} />
                  <Tooltip
                    contentStyle={{ background: "#1f2937", border: "1px solid #374151", borderRadius: 8 }}
                    labelStyle={{ color: "#f3f4f6" }}
                  />
                  <Bar dataKey="carbon_intensity" fill="#ef4444" radius={[6, 6, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>

            <div className="rounded-xl border border-gray-800 bg-gray-900/50 p-4">
              <h2 className="mb-4 text-lg font-semibold">Green Revenue %</h2>
              <ResponsiveContainer width="100%" height={250}>
                <BarChart data={data.carbon_comparison}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                  <XAxis dataKey="ticker" tick={{ fill: "#9ca3af", fontSize: 11 }} />
                  <YAxis domain={[0, 100]} tick={{ fill: "#9ca3af", fontSize: 11 }} />
                  <Tooltip
                    contentStyle={{ background: "#1f2937", border: "1px solid #374151", borderRadius: 8 }}
                    labelStyle={{ color: "#f3f4f6" }}
                  />
                  <Bar dataKey="green_revenue_pct" fill="#10b981" radius={[6, 6, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Details table */}
          <div className="overflow-x-auto rounded-xl border border-gray-800">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-gray-800 bg-gray-900/70 text-left text-xs uppercase text-gray-500">
                  <th className="p-3">Metric</th>
                  {data.securities.map((s) => (
                    <th key={s.ticker} className="p-3 text-center">
                      {s.ticker}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {[
                  { label: "ESG Overall", key: "esg_overall" },
                  { label: "Environmental", key: "esg_environmental" },
                  { label: "Social", key: "esg_social" },
                  { label: "Governance", key: "esg_governance" },
                  { label: "Carbon Intensity", key: "carbon_intensity" },
                  { label: "Green Rev %", key: "green_revenue_pct" },
                  { label: "YTD Return", key: "ytd_return", pct: true },
                  { label: "Controversy", key: "controversy_score" },
                  { label: "Sector", key: "sector" },
                ].map((row) => (
                  <tr key={row.key} className="border-b border-gray-800/50">
                    <td className="p-3 text-gray-400">{row.label}</td>
                    {data.securities.map((s) => {
                      const val = (s as unknown as Record<string, unknown>)[row.key];
                      return (
                        <td key={s.ticker} className="p-3 text-center">
                          {row.pct
                            ? `${((val as number) * 100).toFixed(1)}%`
                            : String(val)}
                        </td>
                      );
                    })}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Sentiment Cards */}
          {Object.keys(sentiments).length > 0 && (
            <div>
              <h2 className="mb-4 text-lg font-semibold">ESG Sentiment Analysis</h2>
              <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                {tickers.map((t) => {
                  const s = sentiments[t];
                  if (!s) return null;
                  return (
                    <div
                      key={t}
                      className="rounded-xl border border-gray-800 bg-gray-900/50 p-4 space-y-2"
                    >
                      <div className="flex items-center justify-between">
                        <span className="font-mono font-bold text-emerald-400">{t}</span>
                        <span
                          className={`rounded-full px-2 py-0.5 text-xs font-semibold ${
                            s.sentiment_score > 0.3
                              ? "bg-emerald-600/20 text-emerald-400"
                              : s.sentiment_score > -0.3
                              ? "bg-yellow-600/20 text-yellow-400"
                              : "bg-red-600/20 text-red-400"
                          }`}
                        >
                          {s.label} ({s.sentiment_score.toFixed(2)})
                        </span>
                      </div>
                      <p className="text-xs text-gray-400">{s.summary}</p>
                      <div className="flex flex-wrap gap-1">
                        {s.key_topics.map((topic) => (
                          <span
                            key={topic}
                            className="rounded bg-gray-800 px-1.5 py-0.5 text-xs text-gray-300"
                          >
                            {topic}
                          </span>
                        ))}
                      </div>
                      {s.controversy_flag && (
                        <p className="text-xs text-red-400">⚠ Controversy flagged</p>
                      )}
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {/* Theme overlap */}
          <div className="rounded-xl border border-gray-800 bg-gray-900/50 p-4">
            <h2 className="mb-3 text-lg font-semibold">Theme Overlap</h2>
            <div className="flex flex-wrap gap-2">
              {Object.entries(data.theme_overlap).map(([theme, tickerList]) => (
                <div key={theme} className="rounded-lg border border-gray-700 bg-gray-800/70 px-3 py-2">
                  <span className="text-xs font-medium text-gray-300">{theme}</span>
                  <div className="mt-1 flex gap-1">
                    {tickerList.map((t) => (
                      <span
                        key={t}
                        className="rounded bg-emerald-600/20 px-1.5 py-0.5 text-xs font-mono text-emerald-400"
                      >
                        {t}
                      </span>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default function ComparePage() {
  return (
    <Suspense fallback={<p className="text-center text-gray-500 p-8">Loading...</p>}>
      <CompareContent />
    </Suspense>
  );
}
