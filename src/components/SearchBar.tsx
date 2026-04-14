import { Search } from "lucide-react";

export default function SearchBar() {
  return (
    <div className="relative mb-6">
      <Search
        size={18}
        className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500"
      />
      <input
        type="text"
        placeholder="Search managers or teams..."
        className="w-full bg-slate-800/60 border border-slate-700/50 rounded-xl py-3 pl-11 pr-4 text-slate-300 placeholder-slate-500 text-sm focus:outline-none focus:border-green-500/50 transition-colors"
      />
    </div>
  );
}
