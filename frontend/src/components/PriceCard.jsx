import { useEffect, useMemo, useState } from "react";

const PRICE_URL = "http://localhost:8000/crypto/price";
const REFRESH_INTERVAL = 30000;

const formatUSD = new Intl.NumberFormat("en-US", {
  style: "currency",
  currency: "USD",
  maximumFractionDigits: 2
});

export default function PriceCard({ coinId = "bitcoin", label }) {
  const [price, setPrice] = useState(null);
  const [status, setStatus] = useState("loading");

  const displayLabel = useMemo(
    () => label ?? `${coinId.charAt(0).toUpperCase()}${coinId.slice(1)}`,
    [coinId, label]
  );

  useEffect(() => {
    let isMounted = true;
    const url = `${PRICE_URL}/${coinId}`;

    const fetchPrice = async () => {
      try {
        setStatus((current) => (current === "ready" ? "ready" : "loading"));
        const response = await fetch(url);
        if (!response.ok) {
          throw new Error("Failed to fetch price");
        }
        const data = await response.json();
        if (isMounted) {
          setPrice(data?.usd_price ?? null);
          setStatus("ready");
        }
      } catch (error) {
        if (isMounted) {
          setStatus("error");
        }
      }
    };

    fetchPrice();
    const intervalId = setInterval(fetchPrice, REFRESH_INTERVAL);

    return () => {
      isMounted = false;
      clearInterval(intervalId);
    };
  }, [coinId]);

  return (
    <section className="rounded-3xl border border-slate-800 bg-slate-900/70 p-6 shadow-glow">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm uppercase tracking-[0.2em] text-slate-400">
            Price
          </p>
          <h2 className="mt-2 text-2xl font-semibold text-white">
            {displayLabel}
          </h2>
        </div>
        <span className="rounded-full border border-blue-500/40 bg-blue-500/10 px-3 py-1 text-xs uppercase tracking-[0.25em] text-blue-200">
          Live
        </span>
      </div>

      <div className="mt-6">
        {status === "error" ? (
          <p className="text-sm text-rose-300">
            Unable to load price for {coinId}.
          </p>
        ) : (
          <p className="text-4xl font-semibold text-white">
            {price !== null ? formatUSD.format(price) : "--"}
          </p>
        )}
        <p className="mt-3 text-sm text-slate-400">
          Updated every 30 seconds from your local backend.
        </p>
      </div>
    </section>
  );
}
