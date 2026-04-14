import { Shield, Users, Trophy, ChevronRight } from "lucide-react";

const leagues = [
  { name: "Premier League", members: 1240, rank: 3, badge: "bg-purple-500/20 text-purple-400" },
  { name: "Champions Cup", members: 856, rank: 7, badge: "bg-blue-500/20 text-blue-400" },
  { name: "Brazil Masters", members: 2100, rank: 1, badge: "bg-green-500/20 text-green-400" },
  { name: "Global Elite", members: 5600, rank: 15, badge: "bg-yellow-500/20 text-yellow-400" },
];

export default function Leagues() {
  return (
    <div className="min-h-screen p-8">
      <div className="max-w-5xl">
        <h1 className="text-3xl font-bold text-green-400 mb-1">Leagues</h1>
        <p className="text-slate-400 mb-6">Join and compete in leagues</p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
          <div className="bg-slate-800/60 border border-slate-700/50 rounded-xl p-5 flex items-start justify-between">
            <div>
              <p className="text-slate-400 text-sm mb-1">Active Leagues</p>
              <p className="text-3xl font-bold text-white">4</p>
              <p className="text-slate-500 text-xs mt-1">Competing in</p>
            </div>
            <div className="w-10 h-10 rounded-lg bg-slate-700/50 flex items-center justify-center">
              <Shield className="w-5 h-5 text-green-400" />
            </div>
          </div>

          <div className="bg-slate-800/60 border border-slate-700/50 rounded-xl p-5 flex items-start justify-between">
            <div>
              <p className="text-slate-400 text-sm mb-1">Best League Rank</p>
              <p className="text-3xl font-bold text-green-400">#1</p>
              <p className="text-slate-500 text-xs mt-1">Brazil Masters</p>
            </div>
            <div className="w-10 h-10 rounded-lg bg-slate-700/50 flex items-center justify-center">
              <Trophy className="w-5 h-5 text-yellow-500" />
            </div>
          </div>
        </div>

        <div className="bg-slate-800/60 border border-slate-700/50 rounded-xl overflow-hidden">
          <div className="p-5 border-b border-slate-700/50 flex items-center gap-2">
            <Shield className="w-5 h-5 text-green-400" />
            <h2 className="text-white font-bold text-lg">Your Leagues</h2>
          </div>

          <div className="divide-y divide-slate-700/50">
            {leagues.map((league) => (
              <div
                key={league.name}
                className="flex items-center px-5 py-4 hover:bg-slate-700/30 transition-colors cursor-pointer"
              >
                <div className={`w-10 h-10 rounded-lg ${league.badge} flex items-center justify-center`}>
                  <Shield className="w-5 h-5" />
                </div>
                <div className="flex-1 ml-4">
                  <p className="text-white font-semibold">{league.name}</p>
                  <p className="text-slate-400 text-sm flex items-center gap-1">
                    <Users className="w-3 h-3" />
                    {league.members.toLocaleString()} members
                  </p>
                </div>
                <div className="text-right mr-3">
                  <p className="text-white font-bold">#{league.rank}</p>
                  <p className="text-slate-500 text-xs">Your Rank</p>
                </div>
                <ChevronRight className="w-5 h-5 text-slate-500" />
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
