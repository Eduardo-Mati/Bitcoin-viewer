import { useEffect, useMemo, useState } from "react";
import styles from "./HistoricalChart.module.css";

const CHART_URL = "http://localhost:8000/crypto/chart";
const REFRESH_INTERVAL = 30000;

const buildChartUrl = (coinId) => `${CHART_URL}/${coinId}?t=${Date.now()}`;

export default function HistoricalChart({ coinId = "bitcoin", title }) {
  const displayTitle = useMemo(
    () => title ?? `${coinId.charAt(0).toUpperCase()}${coinId.slice(1)} history`,
    [coinId, title]
  );

  const [chartSrc, setChartSrc] = useState(() => buildChartUrl(coinId));

  useEffect(() => {
    const refreshChart = () => {
      setChartSrc(buildChartUrl(coinId));
    };

    refreshChart();
    const intervalId = setInterval(refreshChart, REFRESH_INTERVAL);

    return () => clearInterval(intervalId);
  }, [coinId]);

  return (
    <section className={styles.section}>
      <header className={styles.header}>
        <div className={styles.titleSection}>
          <p className={styles.label}>
            Historical chart
          </p>
          <h2 className={styles.title}>
            {displayTitle}
          </h2>
        </div>
        <span className={styles.badge}>
          Auto-refresh
        </span>
      </header>

      <div className={styles.chartContainer}>
        <img
          src={chartSrc}
          alt="Bitcoin price chart"
          className={styles.chartImage}
        />
      </div>
      <p className={styles.description}>
        Chart updates every 30 seconds with cache busting.
      </p>
    </section>
  );
}
