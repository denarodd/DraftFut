import { Home, TrendingUp, Trophy, Users } from "lucide-react";

export default function Dashboard() {
  return (
    <div className="min-h-screen p-8">
      <div className="max-w-5xl">
        <h1 className="text-3xl font-bold text-green-400 mb-1">Dashboard</h1>
        <p className="text-slate-400 mb-6">Welcome back, Manager!</p>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          <div className="bg-slate-800/60 border border-slate-700/50 rounded-xl p-5">
            <div className="flex items-center justify-between mb-3">
              <p className="text-slate-400 text-sm">Team Rating</p>
              <div className="w-9 h-9 rounded-lg bg-slate-700/50 flex items-center justify-center">
                <Trophy className="w-4 h-4 text-yellow-500" />
              </div>
            </div>
            <p className="text-2xl font-bold text-white">87</p>
            <p className="text-green-400 text-xs mt-1">+2 this week</p>
          </div>

          <div className="bg-slate-800/60 border border-slate-700/50 rounded-xl p-5">
            <div className="flex items-center justify-between mb-3">
              <p className="text-slate-400 text-sm">Total Points</p>
              <div className="w-9 h-9 rounded-lg bg-slate-700/50 flex items-center justify-center">
                <TrendingUp className="w-4 h-4 text-green-400" />
              </div>
            </div>
            <p className="text-2xl font-bold text-white">1,987</p>
            <p className="text-green-400 text-xs mt-1">+124 this week</p>
          </div>

          <div className="bg-slate-800/60 border border-slate-700/50 rounded-xl p-5">
            <div className="flex items-center justify-between mb-3">
              <p className="text-slate-400 text-sm">Global Rank</p>
              <div className="w-9 h-9 rounded-lg bg-slate-700/50 flex items-center justify-center">
                <Home className="w-4 h-4 text-blue-400" />
              </div>
            </div>
            <p className="text-2xl font-bold text-white">#10</p>
            <p className="text-green-400 text-xs mt-1">+24 positions</p>
          </div>

          <div className="bg-slate-800/60 border border-slate-700/50 rounded-xl p-5">
            <div className="flex items-center justify-between mb-3">
              <p className="text-slate-400 text-sm">Squad Size</p>
              <div className="w-9 h-9 rounded-lg bg-slate-700/50 flex items-center justify-center">
                <Users className="w-4 h-4 text-purple-400" />
              </div>
            </div>
            <p className="text-2xl font-bold text-white">23</p>
            <p className="text-slate-500 text-xs mt-1">Players</p>
          </div>
        </div>

        <div className="bg-slate-800/60 border border-slate-700/50 rounded-xl p-6">
          <h2 className="text-white font-bold text-lg mb-4">Recent Activity</h2>
          <div className="space-y-3">
            <div className="flex items-center gap-3 text-sm">
              <div className="w-2 h-2 rounded-full bg-green-400" />
              <span className="text-slate-300">Won draft match vs EliteManager</span>
              <span className="text-slate-500 ml-auto">2h ago</span>
            </div>
            <div className="flex items-center gap-3 text-sm">
              <div className="w-2 h-2 rounded-full bg-blue-400" />
              <span className="text-slate-300">Signed Mbappé to your squad</span>
              <span className="text-slate-500 ml-auto">5h ago</span>
            </div>
            <div className="flex items-center gap-3 text-sm">
              <div className="w-2 h-2 rounded-full bg-yellow-400" />
              <span className="text-slate-300">Reached Top 10 in Global Ranking</span>
              <span className="text-slate-500 ml-auto">1d ago</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
