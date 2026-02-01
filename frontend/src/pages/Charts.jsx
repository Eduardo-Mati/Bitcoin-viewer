import { NavLink, useParams } from "react-router-dom";
import HistoricalChart from "../components/HistoricalChart";
import PriceCard from "../components/PriceCard";
import styles from "./Charts.module.css";

const coins = [
  { id: "bitcoin", label: "Bitcoin (BTC)"},
  { id: "ethereum", label: "Ethereum (ETH)"},
  { id: "solana", label: "Solana (SOL)"}
];

export default function Charts() {
  const { coinId } = useParams();
  const active = coins.find((coin) => coin.id === coinId) ?? coins[0];

  return (
    <div className={styles.container}>
      <header className={styles.header}>
        <div className={styles.titleSection}>
          <p className={styles.label}>
            Charts
          </p>
          <h1 className={styles.title}>
            Market history
          </h1>
          <p className={styles.description}>
            Explore refreshed charts by coin with cache-busting updates.
          </p>
        </div>
        <div className={styles.buttonGroup}>
          {coins.map((coin) => (
            <NavLink
              key={coin.id}
              to={`/charts/${coin.id}`}
              className={({ isActive }) =>
                isActive ? `${styles.coinButton} ${styles.active} ${styles[coin.id]}` : `${styles.coinButton} ${styles.inactive}`
              }
            >
              {coin.label}
            </NavLink>
          ))}
        </div>
      </header>

      <div className={styles.grid}>
        <PriceCard coinId={active.id} label={active.label} />
        <HistoricalChart
          coinId={active.id}
          title={`${active.label} · last 24h`}
        />
      </div>
    </div>
  );
}
