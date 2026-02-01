import { Outlet } from "react-router-dom";
import TopNav from "./TopNav";

export default function AppLayout() {
  return (
    <div className="relative min-h-screen overflow-hidden bg-slate-950 text-slate-100">
      <div className="pointer-events-none absolute -left-32 top-0 h-96 w-96 rounded-full bg-blue-500/20 blur-[140px]" />
      <div className="pointer-events-none absolute right-0 top-40 h-80 w-80 rounded-full bg-purple-500/20 blur-[140px]" />
      <div className="pointer-events-none absolute bottom-0 left-1/3 h-72 w-72 rounded-full bg-amber-400/20 blur-[140px]" />

      <div className="relative mx-auto flex w-full max-w-6xl flex-col gap-8 px-6 py-10">
        <TopNav />
        <main className="flex w-full flex-col gap-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
