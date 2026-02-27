import { useEffect, useMemo, useState } from "react";
import styles from "./PriceCard.module.css";
import api from "../services/api";

const PRICE_URL = `${api.baseUrl}/crypto/price`;
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
    <section className={styles.section}>
      <div className={styles.header}>
        <div className={styles.titleSection}>
          <p className={styles.label}>
            Price
          </p>
          <h2 className={styles.title}>
            {displayLabel}
          </h2>
        </div>
        <span className={styles.badge}>
          Live
        </span>
      </div>

      <div className={styles.content}>
        {status === "error" ? (
          <p className={styles.errorMessage}>
            Unable to load price for {coinId}.
          </p>
        ) : (
          <p className={styles.priceValue}>
            {price !== null ? formatUSD.format(price) : "--"}
          </p>
        )}
        <p className={styles.description}>
          Updated every 30 seconds from your local backend.
        </p>
      </div>
    </section>
  );
}
