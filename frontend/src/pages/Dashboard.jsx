import PriceCard from "../components/PriceCard";
import HistoricalChart from "../components/HistoricalChart";

export default function Dashboard() {
  return (
    <div className="flex w-full flex-col gap-6">
      <header className="space-y-2">
        <p className="text-sm uppercase tracking-[0.3em] text-slate-400">
          Bitcoin Viewer
        </p>
        <h1 className="text-3xl font-semibold text-white md:text-4xl">
          Dashboard
        </h1>
        <p className="text-slate-400">
          Live price updates and charts refreshed every 30 seconds.
        </p>
      </header>

      <div className="grid gap-6 lg:grid-cols-[1.1fr_1.9fr]">
        <PriceCard coinId="bitcoin" label="Bitcoin (BTC)" />
        <HistoricalChart coinId="bitcoin" title="Last 24 hours" />
      </div>
    </div>
  );
}
