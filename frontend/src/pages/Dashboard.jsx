import PriceCard from "../components/PriceCard";
import HistoricalChart from "../components/HistoricalChart";

export default function Dashboard() {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <div className="mx-auto flex w-full max-w-6xl flex-col gap-6 px-6 py-10">
        <header className="space-y-2">
          <p className="text-sm uppercase tracking-[0.3em] text-slate-400">
            Bitcoin Viewer
          </p>
          <h1 className="text-3xl font-semibold text-white md:text-4xl">
            Dashboard
          </h1>
          <p className="text-slate-400">
            Live price updates and a historical chart refreshed every 30 seconds.
          </p>
        </header>

        <div className="grid gap-6 lg:grid-cols-[1.1fr_1.9fr]">
          <PriceCard />
          <HistoricalChart />
        </div>
      </div>
    </div>
  );
}
