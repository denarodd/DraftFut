import {
  Home,
  Users,
  BarChart3,
  Trophy,
  Crown,
  LogOut,
} from "lucide-react";

interface NavItem {
  icon: React.ReactNode;
  label: string;
  active?: boolean;
}

const navItems: NavItem[] = [
  { icon: <Home size={20} />, label: "Dashboard" },
  { icon: <Users size={20} />, label: "Build Team" },
  { icon: <BarChart3 size={20} />, label: "Points" },
  { icon: <Trophy size={20} />, label: "Ranking", active: true },
  { icon: <Crown size={20} />, label: "Leagues" },
];

export default function Sidebar() {
  return (
    <aside className="fixed left-0 top-0 h-screen w-52 bg-slate-900 border-r border-slate-700/50 flex flex-col z-50">
      <div className="flex items-center gap-2 px-5 py-5">
        <div className="w-8 h-8 rounded-lg bg-green-500 flex items-center justify-center">
          <Trophy size={18} className="text-white" />
        </div>
        <span className="text-green-400 font-bold text-xl">DraftFut</span>
      </div>

      <nav className="flex-1 mt-4">
        {navItems.map((item) => (
          <a
            key={item.label}
            href="#"
            className={`flex items-center gap-3 px-5 py-3 text-sm transition-colors ${
              item.active
                ? "bg-green-500 text-white font-semibold border-l-4 border-green-400"
                : "text-slate-400 hover:text-white hover:bg-slate-800"
            }`}
          >
            {item.icon}
            {item.label}
          </a>
        ))}
      </nav>

      <div className="border-t border-slate-700/50 p-4">
        <a
          href="#"
          className="flex items-center gap-3 text-slate-400 hover:text-white text-sm transition-colors"
        >
          <LogOut size={20} />
          Logout
        </a>
      </div>
    </aside>
  );
}
