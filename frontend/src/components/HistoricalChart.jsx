import { useEffect, useState } from "react";

const CHART_URL = "http://localhost:8000/crypto/chart";
const REFRESH_INTERVAL = 30000;

const buildChartUrl = () => `${CHART_URL}?t=${Date.now()}`;

export default function HistoricalChart() {
  const [chartSrc, setChartSrc] = useState(buildChartUrl());

  useEffect(() => {
    const refreshChart = () => {
      setChartSrc(buildChartUrl());
    };

    const intervalId = setInterval(refreshChart, REFRESH_INTERVAL);

    return () => clearInterval(intervalId);
  }, []);

  return (
    <section className="rounded-3xl border border-slate-800 bg-slate-900/70 p-6 shadow-glow">
      <header className="flex items-center justify-between">
        <div>
          <p className="text-sm uppercase tracking-[0.2em] text-slate-400">
            Historical chart
          </p>
          <h2 className="mt-2 text-2xl font-semibold text-white">
            Last 24 hours
          </h2>
        </div>
        <span className="rounded-full border border-emerald-400/40 bg-emerald-400/10 px-3 py-1 text-xs uppercase tracking-[0.25em] text-emerald-200">
          Auto-refresh
        </span>
      </header>

      <div className="mt-6 overflow-hidden rounded-2xl border border-slate-800 bg-slate-950/60 p-4">
        <img
          src={chartSrc}
          alt="Bitcoin price chart"
          className="h-72 w-full rounded-xl object-cover"
        />
      </div>
      <p className="mt-3 text-sm text-slate-400">
        Chart updates every 30 seconds with cache busting.
      </p>
    </section>
  );
}
