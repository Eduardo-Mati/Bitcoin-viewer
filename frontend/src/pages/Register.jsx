import { useState } from "react";
import { Link, Navigate, useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";

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
    <div className="relative min-h-screen overflow-hidden bg-slate-950 text-slate-100">
      <div className="pointer-events-none absolute left-0 top-16 h-80 w-80 rounded-full bg-emerald-400/25 blur-[140px]" />
      <div className="pointer-events-none absolute right-0 bottom-10 h-72 w-72 rounded-full bg-amber-400/25 blur-[140px]" />

      <div className="relative mx-auto flex min-h-screen w-full max-w-5xl flex-col items-center justify-center px-6 py-12">
        <div className="w-full max-w-md rounded-3xl border border-slate-800 bg-slate-900/70 p-8 shadow-glow">
          {/* Logo */}
          <div className="mb-6 flex justify-center">
            <span className="flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-emerald-400 via-teal-400 to-cyan-400 text-3xl font-bold text-slate-950 shadow-glow">
              ₿
            </span>
          </div>

          <div className="space-y-2 text-center">
            <p className="text-sm uppercase tracking-[0.3em] text-slate-400">
              Novo acesso
            </p>
            <h1 className="text-3xl font-semibold text-white">Cadastro</h1>
            <p className="text-slate-400">
              Crie sua conta para salvar preferências e alertas de preço.
            </p>
          </div>

          {(error || localError) && (
            <div className="mt-4 rounded-2xl border border-rose-500/40 bg-rose-500/10 px-4 py-3 text-center text-sm text-rose-300">
              {localError || error}
            </div>
          )}

          <form className="mt-8 space-y-4" onSubmit={handleSubmit}>
            <label className="flex flex-col gap-2 text-sm text-slate-300">
              Nome completo
              <input
                type="text"
                placeholder="Seu nome"
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="rounded-2xl border border-slate-800 bg-slate-950/70 px-4 py-3 text-white outline-none transition focus:border-emerald-400"
              />
            </label>
            <label className="flex flex-col gap-2 text-sm text-slate-300">
              Email
              <input
                type="email"
                placeholder="voce@email.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="rounded-2xl border border-slate-800 bg-slate-950/70 px-4 py-3 text-white outline-none transition focus:border-emerald-400"
              />
            </label>
            <label className="flex flex-col gap-2 text-sm text-slate-300">
              Senha
              <input
                type="password"
                placeholder="Crie uma senha"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="rounded-2xl border border-slate-800 bg-slate-950/70 px-4 py-3 text-white outline-none transition focus:border-emerald-400"
              />
            </label>
            <button
              type="submit"
              disabled={loading}
              className="w-full rounded-2xl bg-gradient-to-r from-emerald-400 via-teal-500 to-cyan-500 px-4 py-3 text-sm font-semibold text-slate-950 shadow-glow transition hover:opacity-90 disabled:opacity-50"
            >
              {loading ? "Criando conta..." : "Criar conta"}
            </button>
          </form>

          <div className="mt-6 text-center text-sm text-slate-400">
            Já tem conta?{" "}
            <Link to="/login" className="text-emerald-300 hover:text-emerald-200">
              Fazer login
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
