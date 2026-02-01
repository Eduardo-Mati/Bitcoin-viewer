import PriceCard from "../components/PriceCard";
import HistoricalChart from "../components/HistoricalChart";
import styles from "./Dashboard.module.css";

export default function Dashboard() {
  return (
    <div className={styles.container}>
      <header className={styles.header}>
        <p className={styles.label}>
          Bitcoin Viewer
        </p>
        <h1 className={styles.title}>
          Dashboard
        </h1>
        <p className={styles.description}>
          Live price updates and charts refreshed every 30 seconds.
        </p>
      </header>

      <div className={styles.grid}>
        <PriceCard coinId="bitcoin" label="Bitcoin (BTC)" />
        <HistoricalChart coinId="bitcoin" title="Last 24 hours" />
      </div>
    </div>
  );
}
