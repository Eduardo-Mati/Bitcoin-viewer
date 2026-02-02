import { useEffect, useMemo, useState } from "react";
import styles from "./HistoricalChart.module.css";
import api from "../services/api";

const CHART_URL = `${api.baseUrl}/crypto/chart`;
const REFRESH_INTERVAL = 30000;

const buildChartUrl = (coinId) => `${CHART_URL}/${coinId}?t=${Date.now()}`;

export default function HistoricalChart({ coinId = "bitcoin", title }) {
  const displayTitle = useMemo(
    () => title ?? `${coinId.charAt(0).toUpperCase()}${coinId.slice(1)} history`,
    [coinId, title]
  );

  const [chartSrc, setChartSrc] = useState(() => buildChartUrl(coinId));
  const [analysis, setAnalysis] = useState("");
  const [loadingAI, setLoadingAI] = useState(false);

  useEffect(() => {
    const refreshChart = () => {
      setChartSrc(buildChartUrl(coinId));
    };

    refreshChart();
    const intervalId = setInterval(refreshChart, REFRESH_INTERVAL);

    return () => clearInterval(intervalId);
  }, [coinId]);

  useEffect(() => {
    setAnalysis("");
    setLoadingAI(false);
  }, [coinId]);

  const handleAskAI = async (coin) => {
    setLoadingAI(true);
    setAnalysis("Consultando o Gemini...");
    try {
      const response = await fetch(`${api.baseUrl}/crypto/analyze/${coin}`);
      if (!response.ok) {
        throw new Error("Request failed");
      }
      const data = await response.json();
      setAnalysis(data?.analysis ?? "Sem análise disponível.");
    } catch (error) {
      setAnalysis("Erro ao consultar IA.");
    } finally {
      setLoadingAI(false);
    }
  };

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
          alt={`${displayTitle} price chart`}
          className={styles.chartImage}
        />
      </div>
      <p className={styles.description}>
        Chart updates every 30 seconds with cache busting.
      </p>

      <button
        type="button"
        onClick={() => handleAskAI(coinId)}
        className={styles.aiButton}
        disabled={loadingAI}
      >
        {loadingAI ? "Analisando..." : "✨ Pedir Análise da IA"}
      </button>

      {analysis && (
        <div className={styles.analysisBox}>
          🤖 {analysis}
        </div>
      )}
    </section>
  );
}
