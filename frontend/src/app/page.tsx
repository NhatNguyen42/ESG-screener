"use client";

import { useState, useEffect, useCallback } from "react";
import {
  getSecurities,
  getFilterOptions,
  type Security,
  type FilterOptions,
  type ScreenerFilters,
} from "@/lib/api";
import { Search, SlidersHorizontal, ArrowUpDown, Leaf, Factory, AlertTriangle } from "lucide-react";

/* ── Helper: ESG badge color ──────────────────────────── */
function esgColor(score: number) {
  if (score >= 80) return "bg-emerald-600/20 text-emerald-400 border-emerald-600/40";
  if (score >= 65) return "bg-green-600/20 text-green-400 border-green-600/40";
  if (score >= 50) return "bg-yellow-600/20 text-yellow-400 border-yellow-600/40";
  return "bg-red-600/20 text-red-400 border-red-600/40";
}

function carbonColor(val: number) {
  if (val <= 50) return "text-emerald-400";
  if (val <= 150) return "text-yellow-400";
  return "text-red-400";
}

export default function ScreenerPage() {
  const [securities, setSecurities] = useState<Security[]>([]);
  const [filterOpts, setFilterOpts] = useState<FilterOptions | null>(null);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState<ScreenerFilters>({ sort_by: "esg_overall", sort_desc: true });
  const [showFilters, setShowFilters] = useState(false);
  const [selected, setSelected] = useState<Set<string>>(new Set());

  const fetchData = useCallback(async () => {
    setLoading(true);
    try {
      const [secRes, optRes] = await Promise.all([
        getSecurities(filters),
        filterOpts ? Promise.resolve(filterOpts) : getFilterOptions(),
      ]);
      setSecurities(secRes.securities);
      if (!filterOpts) setFilterOpts(optRes as FilterOptions);
    } catch (e) {
      console.error("Fetch error:", e);
    }
    setLoading(false);
  }, [filters, filterOpts]);

  useEffect(() => { fetchData(); }, [fetchData]);

  const toggleSort = (col: string) => {
    setFilters((f) => ({
      ...f,
      sort_by: col,
      sort_desc: f.sort_by === col ? !f.sort_desc : true,
    }));
  };

  const toggleSelect = (ticker: string) => {
    setSelected((prev) => {
      const next = new Set(prev);
      next.has(ticker) ? next.delete(ticker) : next.add(ticker);
      return next;
    });
  };

  return (
    <div className="space-y-4">
      {/* Hero */}
      <div className="rounded-xl border border-gray-800 bg-gradient-to-br from-gray-900 to-gray-950 p-6">
        <h1 className="text-2xl font-bold">ESG Investment Screener</h1>
        <p className="mt-1 text-sm text-gray-400">
          Screen {securities.length} securities by ESG score, carbon intensity, sector, theme & more.
          Select securities to compare or build an optimized portfolio.
        </p>
      </div>

      {/* Search & Filter bar */}
      <div className="flex flex-wrap items-center gap-3">
        <div className="relative flex-1 min-w-[240px]">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-500" />
          <input
            type="text"
            placeholder="Search ticker, name, or sector..."
            className="w-full rounded-lg border border-gray-700 bg-gray-900 py-2 pl-10 pr-3 text-sm focus:border-emerald-500 focus:outline-none"
            value={filters.search || ""}
            onChange={(e) => setFilters((f) => ({ ...f, search: e.target.value }))}
          />
        </div>
        <button
          onClick={() => setShowFilters(!showFilters)}
          className="flex items-center gap-2 rounded-lg border border-gray-700 bg-gray-900 px-3 py-2 text-sm hover:bg-gray-800"
        >
          <SlidersHorizontal className="h-4 w-4" />
          Filters
        </button>
        {selected.size >= 2 && (
          <>
            <a
              href={`/compare?tickers=${[...selected].join(",")}`}
              className="rounded-lg bg-blue-600 px-3 py-2 text-sm font-medium hover:bg-blue-700"
            >
              Compare ({selected.size})
            </a>
            <a
              href={`/optimizer?tickers=${[...selected].join(",")}`}
              className="rounded-lg bg-emerald-600 px-3 py-2 text-sm font-medium hover:bg-emerald-700"
            >
              Optimize ({selected.size})
            </a>
          </>
        )}
      </div>

      {/* Filter panel */}
      {showFilters && filterOpts && (
        <div className="grid grid-cols-2 gap-4 rounded-xl border border-gray-800 bg-gray-900/50 p-4 md:grid-cols-4">
          <div>
            <label className="mb-1 block text-xs font-medium text-gray-400">Min ESG Score</label>
            <input
              type="range"
              min={0}
              max={100}
              value={filters.min_esg ?? 0}
              onChange={(e) => setFilters((f) => ({ ...f, min_esg: Number(e.target.value) || undefined }))}
              className="w-full accent-emerald-500"
            />
            <span className="text-xs text-gray-500">{filters.min_esg ?? 0}</span>
          </div>
          <div>
            <label className="mb-1 block text-xs font-medium text-gray-400">Max Carbon (tCO2e/$M)</label>
            <input
              type="range"
              min={0}
              max={500}
              value={filters.max_carbon ?? 500}
              onChange={(e) =>
                setFilters((f) => ({
                  ...f,
                  max_carbon: Number(e.target.value) < 500 ? Number(e.target.value) : undefined,
                }))
              }
              className="w-full accent-emerald-500"
            />
            <span className="text-xs text-gray-500">{filters.max_carbon ?? "Any"}</span>
          </div>
          <div>
            <label className="mb-1 block text-xs font-medium text-gray-400">Sector</label>
            <select
              className="w-full rounded border border-gray-700 bg-gray-800 p-1.5 text-xs"
              value={filters.sectors?.[0] ?? ""}
              onChange={(e) =>
                setFilters((f) => ({ ...f, sectors: e.target.value ? [e.target.value] : undefined }))
              }
            >
              <option value="">All Sectors</option>
              {filterOpts.sectors.map((s) => (
                <option key={s} value={s}>
                  {s}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="mb-1 block text-xs font-medium text-gray-400">Theme</label>
            <select
              className="w-full rounded border border-gray-700 bg-gray-800 p-1.5 text-xs"
              value={filters.themes?.[0] ?? ""}
              onChange={(e) =>
                setFilters((f) => ({ ...f, themes: e.target.value ? [e.target.value] : undefined }))
              }
            >
              <option value="">All Themes</option>
              {filterOpts.themes.map((t) => (
                <option key={t.id} value={t.id}>
                  {t.label}
                </option>
              ))}
            </select>
          </div>
        </div>
      )}

      {/* Table */}
      <div className="overflow-x-auto rounded-xl border border-gray-800">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-gray-800 bg-gray-900/70 text-left text-xs uppercase text-gray-500">
              <th className="p-3 w-10">
                <input
                  type="checkbox"
                  className="accent-emerald-500"
                  checked={selected.size === securities.length && securities.length > 0}
                  onChange={() =>
                    setSelected(
                      selected.size === securities.length
                        ? new Set()
                        : new Set(securities.map((s) => s.ticker))
                    )
                  }
                />
              </th>
              {[
                { key: "ticker", label: "Ticker" },
                { key: "name", label: "Name" },
                { key: "sector", label: "Sector" },
                { key: "esg_overall", label: "ESG Score" },
                { key: "esg_environmental", label: "E" },
                { key: "esg_social", label: "S" },
                { key: "esg_governance", label: "G" },
                { key: "carbon_intensity", label: "Carbon" },
                { key: "green_revenue_pct", label: "Green Rev %" },
                { key: "ytd_return", label: "YTD" },
                { key: "controversy_score", label: "Controversy" },
              ].map((col) => (
                <th
                  key={col.key}
                  className="cursor-pointer p-3 hover:text-gray-300"
                  onClick={() => toggleSort(col.key)}
                >
                  <span className="flex items-center gap-1">
                    {col.label}
                    {filters.sort_by === col.key && (
                      <ArrowUpDown className="h-3 w-3 text-emerald-400" />
                    )}
                  </span>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr>
                <td colSpan={12} className="p-8 text-center text-gray-500">
                  Loading securities...
                </td>
              </tr>
            ) : securities.length === 0 ? (
              <tr>
                <td colSpan={12} className="p-8 text-center text-gray-500">
                  No securities match your filters.
                </td>
              </tr>
            ) : (
              securities.map((sec) => (
                <tr
                  key={sec.ticker}
                  className="border-b border-gray-800/50 transition hover:bg-gray-900/50"
                >
                  <td className="p-3">
                    <input
                      type="checkbox"
                      className="accent-emerald-500"
                      checked={selected.has(sec.ticker)}
                      onChange={() => toggleSelect(sec.ticker)}
                    />
                  </td>
                  <td className="p-3 font-mono font-semibold text-emerald-400">
                    {sec.ticker}
                  </td>
                  <td className="p-3 max-w-[160px] truncate">{sec.name}</td>
                  <td className="p-3 text-gray-400">{sec.sector}</td>
                  <td className="p-3">
                    <span
                      className={`inline-flex items-center rounded-full border px-2 py-0.5 text-xs font-semibold ${esgColor(
                        sec.esg_overall
                      )}`}
                    >
                      <Leaf className="mr-1 h-3 w-3" />
                      {sec.esg_overall}
                    </span>
                  </td>
                  <td className="p-3 text-xs text-gray-400">{sec.esg_environmental}</td>
                  <td className="p-3 text-xs text-gray-400">{sec.esg_social}</td>
                  <td className="p-3 text-xs text-gray-400">{sec.esg_governance}</td>
                  <td className={`p-3 text-xs font-medium ${carbonColor(sec.carbon_intensity)}`}>
                    <Factory className="mr-1 inline h-3 w-3" />
                    {sec.carbon_intensity}
                  </td>
                  <td className="p-3 text-xs">{sec.green_revenue_pct}%</td>
                  <td
                    className={`p-3 text-xs font-medium ${
                      sec.ytd_return >= 0 ? "text-emerald-400" : "text-red-400"
                    }`}
                  >
                    {(sec.ytd_return * 100).toFixed(1)}%
                  </td>
                  <td className="p-3">
                    {sec.controversy_score >= 3 ? (
                      <span className="inline-flex items-center gap-1 text-xs text-red-400" title={sec.controversy_summary || ""}>
                        <AlertTriangle className="h-3 w-3" />
                        {sec.controversy_score}
                      </span>
                    ) : (
                      <span className="text-xs text-gray-500">{sec.controversy_score}</span>
                    )}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
