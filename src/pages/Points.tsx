import { BarChart3, TrendingUp, Calendar, Award } from "lucide-react";

const weeklyData = [
  { week: "Week 1", points: 156 },
  { week: "Week 2", points: 189 },
  { week: "Week 3", points: 203 },
  { week: "Week 4", points: 178 },
  { week: "Week 5", points: 245 },
  { week: "Week 6", points: 212 },
  { week: "Week 7", points: 267 },
  { week: "Week 8", points: 234 },
];

const maxPoints = Math.max(...weeklyData.map((d) => d.points));

export default function Points() {
  return (
    <div className="min-h-screen p-8">
      <div className="max-w-5xl">
        <h1 className="text-3xl font-bold text-green-400 mb-1">Points</h1>
        <p className="text-slate-400 mb-6">Track your scoring history</p>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div className="bg-slate-800/60 border border-slate-700/50 rounded-xl p-5 flex items-start justify-between">
            <div>
              <p className="text-slate-400 text-sm mb-1">Total Points</p>
              <p className="text-3xl font-bold text-white">1,987</p>
              <p className="text-green-400 text-xs mt-1">Season 2024/25</p>
            </div>
            <div className="w-10 h-10 rounded-lg bg-slate-700/50 flex items-center justify-center">
              <BarChart3 className="w-5 h-5 text-green-400" />
            </div>
          </div>

          <div className="bg-slate-800/60 border border-slate-700/50 rounded-xl p-5 flex items-start justify-between">
            <div>
              <p className="text-slate-400 text-sm mb-1">This Week</p>
              <p className="text-3xl font-bold text-blue-400">234</p>
              <p className="text-green-400 text-xs mt-1 flex items-center gap-1">
                <TrendingUp className="w-3 h-3" />
                +18% vs last week
              </p>
            </div>
            <div className="w-10 h-10 rounded-lg bg-slate-700/50 flex items-center justify-center">
              <Calendar className="w-5 h-5 text-blue-400" />
            </div>
          </div>

          <div className="bg-slate-800/60 border border-slate-700/50 rounded-xl p-5 flex items-start justify-between">
            <div>
              <p className="text-slate-400 text-sm mb-1">Best Week</p>
              <p className="text-3xl font-bold text-yellow-400">267</p>
              <p className="text-slate-500 text-xs mt-1">Week 7</p>
            </div>
            <div className="w-10 h-10 rounded-lg bg-slate-700/50 flex items-center justify-center">
              <Award className="w-5 h-5 text-yellow-500" />
            </div>
          </div>
        </div>

        <div className="bg-slate-800/60 border border-slate-700/50 rounded-xl p-6">
          <h2 className="text-white font-bold text-lg mb-6">Weekly Points</h2>
          <div className="flex items-end gap-3 h-48">
            {weeklyData.map((d) => (
              <div key={d.week} className="flex-1 flex flex-col items-center gap-2">
                <span className="text-xs text-slate-400">{d.points}</span>
                <div
                  className="w-full bg-green-500/60 hover:bg-green-500/80 rounded-t-md transition-colors"
                  style={{ height: `${(d.points / maxPoints) * 100}%` }}
                />
                <span className="text-xs text-slate-500">{d.week.replace("Week ", "W")}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
