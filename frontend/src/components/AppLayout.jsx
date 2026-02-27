import { Outlet } from "react-router-dom";
import TopNav from "./TopNav";
import styles from "./AppLayout.module.css";

export default function AppLayout() {
  return (
    <div className={styles.container}>
      <div className={styles.blurBlue} />
      <div className={styles.blurPurple} />
      <div className={styles.blurAmber} />

      <div className={styles.content}>
        <TopNav />
        <main className={styles.main}>
          <Outlet />
        </main>
      </div>
    </div>
  );
}
