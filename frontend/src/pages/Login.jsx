import { useState } from "react";
import { Link, Navigate, useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";

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
    <div className="relative min-h-screen overflow-hidden bg-slate-950 text-slate-100">
      <div className="pointer-events-none absolute -left-24 top-10 h-80 w-80 rounded-full bg-blue-500/30 blur-[140px]" />
      <div className="pointer-events-none absolute right-0 bottom-10 h-72 w-72 rounded-full bg-purple-500/30 blur-[140px]" />

      <div className="relative mx-auto flex min-h-screen w-full max-w-5xl flex-col items-center justify-center px-6 py-12">
        <div className="w-full max-w-md rounded-3xl border border-slate-800 bg-slate-900/70 p-8 shadow-glow">
          {/* Logo */}
          <div className="mb-6 flex justify-center">
            <span className="flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-amber-400 via-orange-400 to-rose-400 text-3xl font-bold text-slate-950 shadow-glow">
              ₿
            </span>
          </div>

          <div className="space-y-2 text-center">
            <p className="text-sm uppercase tracking-[0.3em] text-slate-400">
              Bem-vindo
            </p>
            <h1 className="text-3xl font-semibold text-white">Login</h1>
            <p className="text-slate-400">
              Entre para acompanhar seus ativos favoritos em tempo real.
            </p>
          </div>

          {(error || localError) && (
            <div className="mt-4 rounded-2xl border border-rose-500/40 bg-rose-500/10 px-4 py-3 text-center text-sm text-rose-300">
              {localError || error}
            </div>
          )}

          <form className="mt-8 space-y-4" onSubmit={handleSubmit}>
            <label className="flex flex-col gap-2 text-sm text-slate-300">
              Email
              <input
                type="email"
                placeholder="voce@email.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="rounded-2xl border border-slate-800 bg-slate-950/70 px-4 py-3 text-white outline-none transition focus:border-blue-500"
              />
            </label>
            <label className="flex flex-col gap-2 text-sm text-slate-300">
              Senha
              <input
                type="password"
                placeholder="********"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="rounded-2xl border border-slate-800 bg-slate-950/70 px-4 py-3 text-white outline-none transition focus:border-blue-500"
              />
            </label>
            <button
              type="submit"
              disabled={loading}
              className="w-full rounded-2xl bg-gradient-to-r from-blue-500 via-indigo-500 to-purple-500 px-4 py-3 text-sm font-semibold text-white shadow-glow transition hover:opacity-90 disabled:opacity-50"
            >
              {loading ? "Entrando..." : "Entrar agora"}
            </button>
          </form>

          <div className="mt-6 text-center text-sm text-slate-400">
            Ainda não tem conta?{" "}
            <Link to="/register" className="text-blue-300 hover:text-blue-200">
              Criar cadastro
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
