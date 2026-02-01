import { NavLink, useParams } from "react-router-dom";
import HistoricalChart from "../components/HistoricalChart";
import PriceCard from "../components/PriceCard";

const coins = [
  { id: "bitcoin", label: "Bitcoin (BTC)", tone: "from-amber-400 to-orange-500" },
  { id: "ethereum", label: "Ethereum (ETH)", tone: "from-indigo-400 to-purple-500" },
  { id: "solana", label: "Solana (SOL)", tone: "from-emerald-400 to-teal-500" }
];

export default function Charts() {
  const { coinId } = useParams();
  const active = coins.find((coin) => coin.id === coinId) ?? coins[0];

  return (
    <div className="flex w-full flex-col gap-6">
      <header className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
        <div className="space-y-2">
          <p className="text-sm uppercase tracking-[0.3em] text-slate-400">
            Charts
          </p>
          <h1 className="text-3xl font-semibold text-white md:text-4xl">
            Market history
          </h1>
          <p className="text-slate-400">
            Explore refreshed charts by coin with cache-busting updates.
          </p>
        </div>
        <div className="flex flex-wrap gap-3">
          {coins.map((coin) => (
            <NavLink
              key={coin.id}
              to={`/charts/${coin.id}`}
              className={({ isActive }) =>
                `rounded-full border px-4 py-2 text-sm font-semibold transition-all duration-300 ${
                  isActive
                    ? `border-transparent bg-gradient-to-r ${coin.tone} text-slate-950 shadow-glow`
                    : "border-slate-800 bg-slate-900/40 text-slate-300 hover:border-slate-600 hover:text-white"
                }`
              }
            >
              {coin.label}
            </NavLink>
          ))}
        </div>
      </header>

      <div className="grid gap-6 lg:grid-cols-[1.05fr_1.95fr]">
        <PriceCard coinId={active.id} label={active.label} />
        <HistoricalChart
          coinId={active.id}
          title={`${active.label} · last 24h`}
        />
      </div>
    </div>
  );
}
