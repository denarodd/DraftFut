import { NavLink } from "react-router-dom";
import {
  Home,
  Users,
  BarChart3,
  Trophy,
  Shield,
  LogOut,
} from "lucide-react";

const navItems = [
  { to: "/", icon: Home, label: "Dashboard" },
  { to: "/build-team", icon: Users, label: "Build Team" },
  { to: "/points", icon: BarChart3, label: "Points" },
  { to: "/ranking", icon: Trophy, label: "Ranking" },
  { to: "/leagues", icon: Shield, label: "Leagues" },
];

export default function Sidebar() {
  return (
    <aside className="fixed left-0 top-0 h-screen w-52 bg-slate-900 border-r border-slate-700/50 flex flex-col z-50">
      <div className="flex items-center gap-2 px-5 py-6">
        <div className="w-8 h-8 rounded-full bg-green-500 flex items-center justify-center">
          <Trophy className="w-4 h-4 text-white" />
        </div>
        <span className="text-green-400 font-bold text-lg">DraftFut</span>
      </div>

      <nav className="flex-1 flex flex-col gap-1 px-3 mt-2">
        {navItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                isActive
                  ? "bg-green-500 text-white"
                  : "text-slate-400 hover:text-white hover:bg-slate-800"
              }`
            }
          >
            <item.icon className="w-5 h-5" />
            {item.label}
          </NavLink>
        ))}
      </nav>

      <div className="px-3 pb-6">
        <button className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium text-slate-400 hover:text-white hover:bg-slate-800 transition-colors w-full">
          <LogOut className="w-5 h-5" />
          Logout
        </button>
      </div>
    </aside>
  );
}
