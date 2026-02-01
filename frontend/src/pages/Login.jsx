import { useState } from "react";
import { Link, Navigate, useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import styles from "./Login.module.css";

export default function Login() {
  const { login, loading, error, isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [localError, setLocalError] = useState("");

  // Se já estiver autenticado, redireciona para home
  if (isAuthenticated) {
    return <Navigate to="/" replace />;
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLocalError("");

    if (!email || !password) {
      setLocalError("Preencha todos os campos");
      return;
    }

    const result = await login(email, password);
    if (result.success) {
      navigate("/");
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.blurLeft} />
      <div className={styles.blurRight} />

      <div className={styles.contentWrapper}>
        <div className={styles.card}>
          {/* Logo */}
          <div className={styles.logoContainer}>
            <span className={styles.logoBadge}>
              ₿
            </span>
          </div>

          <div className={styles.titleSection}>
            <p className={styles.subtitle}>
              Bem-vindo
            </p>
            <h1 className={styles.title}>Login</h1>
            <p className={styles.description}>
              Entre para acompanhar seus ativos favoritos em tempo real.
            </p>
          </div>

          {(error || localError) && (
            <div className={styles.errorBox}>
              {localError || error}
            </div>
          )}

          <form className={styles.form} onSubmit={handleSubmit}>
            <label className={styles.label}>
              Email
              <input
                type="email"
                placeholder="voce@email.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className={styles.input}
              />
            </label>
            <label className={styles.label}>
              Senha
              <input
                type="password"
                placeholder="********"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className={styles.input}
              />
            </label>
            <button
              type="submit"
              disabled={loading}
              className={styles.submitButton}
            >
              {loading ? "Entrando..." : "Entrar agora"}
            </button>
          </form>

          <div className={styles.linkSection}>
            Ainda não tem conta?{" "}
            <Link to="/register" className={styles.link}>
              Criar cadastro
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
