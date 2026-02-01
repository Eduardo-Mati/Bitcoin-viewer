import { NavLink, Link, useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import styles from "./TopNav.module.css";

export default function TopNav() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <nav className={styles.nav}>
      <Link to="/" className={styles.logo}>
        <span className={styles.logoBadge}>
          ₿
        </span>
        <div className={styles.logoText}>
          <p className={styles.logoSubtext}>
            Bitcoin Viewer
          </p>
          <p className={styles.logoTitle}>
            Crypto Command Center
          </p>
        </div>
      </Link>

      <div className={styles.navLinks}>
        <NavLink
          to="/"
          end
          className={({ isActive }) =>
            `${styles.navLinkBase} ${isActive ? styles.navLinkActive : styles.navLinkIdle}`
          }
        >
          Dashboard
        </NavLink>
        <NavLink
          to="/charts/bitcoin"
          className={({ isActive }) =>
            `${styles.navLinkBase} ${isActive ? styles.navLinkActive : styles.navLinkIdle}`
          }
        >
          Charts
        </NavLink>

        {/* User info and logout */}
        <div className={styles.userSection}>
          <span className={styles.userEmail}>
            {user?.email}
          </span>
          <button
            onClick={handleLogout}
            className={styles.logoutButton}
          >
            Sair
          </button>
        </div>
      </div>
    </nav>
  );
}
