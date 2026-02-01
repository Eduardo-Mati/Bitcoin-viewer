import { NavLink, Link, useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";

const baseLink =
  "rounded-full px-4 py-2 text-sm font-semibold transition-all duration-300";
const activeLink =
  "bg-gradient-to-r from-blue-500/80 via-indigo-500/80 to-purple-500/80 text-white shadow-glow";
const idleLink =
  "border border-slate-800 bg-slate-900/40 text-slate-300 hover:border-slate-600 hover:text-white";

export default function TopNav() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <nav className="flex flex-col gap-4 rounded-3xl border border-slate-800 bg-slate-900/60 p-4 backdrop-blur lg:flex-row lg:items-center lg:justify-between">
      <Link to="/" className="group inline-flex items-center gap-3">
        <span className="flex h-10 w-10 items-center justify-center rounded-2xl bg-gradient-to-br from-amber-400 via-orange-400 to-rose-400 text-xl font-semibold text-slate-950 shadow-glow">
          ₿
        </span>
        <div>
          <p className="text-sm uppercase tracking-[0.3em] text-slate-400">
            Bitcoin Viewer
          </p>
          <p className="text-lg font-semibold text-white">
            Crypto Command Center
          </p>
        </div>
      </Link>

      <div className="flex flex-wrap items-center gap-3">
        <NavLink
          to="/"
          end
          className={({ isActive }) =>
            `${baseLink} ${isActive ? activeLink : idleLink}`
          }
        >
          Dashboard
        </NavLink>
        <NavLink
          to="/charts/bitcoin"
          className={({ isActive }) =>
            `${baseLink} ${isActive ? activeLink : idleLink}`
          }
        >
          Charts
        </NavLink>

        {/* User info and logout */}
        <div className="ml-2 flex items-center gap-3 border-l border-slate-700 pl-4">
          <span className="text-sm text-slate-400">
            {user?.email}
          </span>
          <button
            onClick={handleLogout}
            className="rounded-full border border-rose-500/40 bg-rose-500/10 px-4 py-2 text-sm font-semibold text-rose-300 transition-all duration-300 hover:bg-rose-500/20"
          >
            Sair
          </button>
        </div>
      </div>
    </nav>
  );
}
