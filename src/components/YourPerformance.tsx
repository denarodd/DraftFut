import { TrendingUp } from "lucide-react";

export default function YourPerformance() {
  return (
    <div className="bg-slate-800/60 border border-slate-700/50 rounded-xl p-6">
      <div className="flex items-center gap-3 mb-2">
        <div className="w-10 h-10 rounded-lg bg-green-600/20 flex items-center justify-center">
          <TrendingUp size={20} className="text-green-400" />
        </div>
        <div>
          <h2 className="text-white font-semibold text-lg">Your Performance</h2>
          <p className="text-slate-400 text-sm">
            You're in the top <span className="text-green-400 font-bold">0.0001%</span> of all managers worldwide!
          </p>
        </div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mt-5">
        <div>
          <p className="text-slate-500 text-xs mb-1">Country Rank</p>
          <p className="text-white text-2xl font-bold">#3</p>
        </div>
        <div>
          <p className="text-slate-500 text-xs mb-1">Region Rank</p>
          <p className="text-white text-2xl font-bold">#1</p>
        </div>
        <div>
          <p className="text-slate-500 text-xs mb-1">League Avg Rank</p>
          <p className="text-white text-2xl font-bold">#2</p>
        </div>
        <div>
          <p className="text-slate-500 text-xs mb-1">Best Rank</p>
          <p className="text-green-400 text-2xl font-bold">#4</p>
        </div>
      </div>
    </div>
  );
}
