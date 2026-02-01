import { useState } from "react";
import { Link, Navigate, useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import styles from "./Register.module.css";

export default function Register() {
  const { register, loading, error, isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const [name, setName] = useState("");
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

    if (!name || !email || !password) {
      setLocalError("Preencha todos os campos");
      return;
    }

    if (password.length < 3) {
      setLocalError("A senha deve ter pelo menos 3 caracteres");
      return;
    }

    const result = await register(name, email, password);
    if (result.success) {
      navigate("/login");
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
              Novo acesso
            </p>
            <h1 className={styles.title}>Cadastro</h1>
            <p className={styles.description}>
              Crie sua conta para salvar preferências e alertas de preço.
            </p>
          </div>

          {(error || localError) && (
            <div className={styles.errorBox}>
              {localError || error}
            </div>
          )}

          <form className={styles.form} onSubmit={handleSubmit}>
            <label className={styles.label}>
              Nome completo
              <input
                type="text"
                placeholder="Seu nome"
                value={name}
                onChange={(e) => setName(e.target.value)}
                className={styles.input}
              />
            </label>
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
                placeholder="Crie uma senha"
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
              {loading ? "Criando conta..." : "Criar conta"}
            </button>
          </form>

          <div className={styles.linkSection}>
            Já tem conta?{" "}
            <Link to="/login" className={styles.link}>
              Fazer login
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
