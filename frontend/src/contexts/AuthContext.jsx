import { createContext, useContext, useState, useEffect, useMemo } from "react";

const AuthContext = createContext(null);

const TOKEN_COOKIE = "btc_viewer_token";
const USER_COOKIE = "btc_viewer_user";

function getCookie(name) {
  const match = document.cookie.match(new RegExp("(^| )" + name + "=([^;]+)"));
  return match ? decodeURIComponent(match[2]) : null;
}

function setCookie(name, value, days = 1) {
  const expires = new Date(Date.now() + days * 864e5).toUTCString();
  document.cookie = `${name}=${encodeURIComponent(value)}; expires=${expires}; path=/; SameSite=Lax`;
}

function removeCookie(name) {
  document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
}

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => getCookie(TOKEN_COOKIE));
  const [user, setUser] = useState(() => {
    const saved = getCookie(USER_COOKIE);
    return saved ? JSON.parse(saved) : null;
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const isAuthenticated = Boolean(token);

  const login = async (email, password) => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch("http://localhost:8000/api/user/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
      });

      const data = await res.json();
      
      if (!res.ok) {
        throw new Error(data.detail || "Falha no login");
      }

      setCookie(TOKEN_COOKIE, data.access_token, 1);
      setCookie(USER_COOKIE, JSON.stringify({ email: data.email }), 1);
      setToken(data.access_token);
      setUser({ email: data.email });

      return { success: true };
    } catch (err) {
      const errorMessage = typeof err.message === 'string' ? err.message : "Falha no login";
      setError(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setLoading(false);
    }
  };

  const register = async (name, email, password) => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch("http://localhost:8000/api/user/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, password })
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.detail || "Falha no cadastro");
      }

      return { success: true };
    } catch (err) {
      const errorMessage = typeof err.message === 'string' ? err.message : "Falha no cadastro";
      setError(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    removeCookie(TOKEN_COOKIE);
    removeCookie(USER_COOKIE);
    setToken(null);
    setUser(null);
  };

  const value = useMemo(
    () => ({
      token,
      user,
      isAuthenticated,
      loading,
      error,
      login,
      register,
      logout
    }),
    [token, user, isAuthenticated, loading, error]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
