import { Trophy, Users, Award } from "lucide-react";

export default function StatsCards() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
      {/* Your Rank */}
      <div className="bg-slate-800/60 border border-slate-700/50 rounded-xl p-5 flex items-start justify-between">
        <div>
          <p className="text-slate-400 text-sm mb-1">Your Rank</p>
          <p className="text-blue-400 text-3xl font-bold">#10</p>
          <p className="text-green-400 text-xs mt-1 flex items-center gap-1">
            <span className="inline-block">~</span> +24 this week
          </p>
        </div>
        <div className="w-10 h-10 rounded-lg bg-green-600/20 flex items-center justify-center">
          <Trophy size={20} className="text-green-400" />
        </div>
      </div>

      {/* Total Managers */}
      <div className="bg-slate-800/60 border border-slate-700/50 rounded-xl p-5 flex items-start justify-between">
        <div>
          <p className="text-slate-400 text-sm mb-1">Total Managers</p>
          <p className="text-white text-3xl font-bold">9.2M</p>
          <p className="text-slate-500 text-xs mt-1">Worldwide</p>
        </div>
        <div className="w-10 h-10 rounded-lg bg-slate-700/50 flex items-center justify-center">
          <Users size={20} className="text-slate-400" />
        </div>
      </div>

      {/* Points Behind Leader */}
      <div className="bg-slate-800/60 border border-slate-700/50 rounded-xl p-5 flex items-start justify-between">
        <div>
          <p className="text-slate-400 text-sm mb-1">Points Behind Leader</p>
          <p className="text-orange-400 text-3xl font-bold">469</p>
          <p className="text-slate-500 text-xs mt-1">Catchable!</p>
        </div>
        <div className="w-10 h-10 rounded-lg bg-slate-700/50 flex items-center justify-center">
          <Award size={20} className="text-yellow-500" />
        </div>
      </div>
    </div>
  );
}
