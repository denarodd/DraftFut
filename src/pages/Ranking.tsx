import { Search, Trophy, Users, TrendingUp, Crown } from "lucide-react";

const leaderboardData = [
  { rank: 1, name: "FootballKing", team: "The Winners", points: 2456, isTop3: true },
  { rank: 2, name: "ProManager", team: "Elite Squad", points: 2398, isTop3: true },
  { rank: 3, name: "TacticalGenius", team: "Master Class", points: 2367, isTop3: true },
  { rank: 4, name: "ChampionPlayer", team: "Victory FC", points: 2301, isTop3: false },
  { rank: 5, name: "TopStriker", team: "Goal Machine", points: 2256, isTop3: false },
  { rank: 6, name: "FantasyPro", team: "Dream Team", points: 2198, isTop3: false },
  { rank: 7, name: "BestManager", team: "Champions League", points: 2145, isTop3: false },
  { rank: 8, name: "StarPlayer", team: "All Stars FC", points: 2089, isTop3: false },
  { rank: 9, name: "WinnerMindset", team: "Never Give Up", points: 2034, isTop3: false },
  { rank: 10, name: "You", team: "Green Warriors", points: 1987, isTop3: false, isYou: true },
  { rank: 11, name: "FootballFan", team: "Fan Favorites", points: 1923, isTop3: false },
  { rank: 12, name: "GameChanger", team: "Game Changers", points: 1876, isTop3: false },
];

function getRankIcon(rank: number) {
  if (rank === 1) return <Crown className="w-6 h-6 text-yellow-500" />;
  if (rank === 2) return <Trophy className="w-6 h-6 text-slate-400" />;
  if (rank === 3) return <Trophy className="w-6 h-6 text-amber-700" />;
  return null;
}

function getRankDisplay(rank: number, isYou?: boolean) {
  if (rank <= 3) {
    return getRankIcon(rank);
  }
  return (
    <span className={`text-lg font-semibold ${isYou ? "text-green-400" : "text-slate-400"}`}>
      {rank}
    </span>
  );
}

export default function Ranking() {
  return (
    <div className="min-h-screen p-8">
      <div className="max-w-5xl">
        <h1 className="text-3xl font-bold text-green-400 mb-1">Global Ranking</h1>
        <p className="text-slate-400 mb-6">Compete with managers worldwide</p>

        {/* Stat Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          {/* Your Rank */}
          <div className="bg-slate-800/60 border border-slate-700/50 rounded-xl p-5 flex items-start justify-between">
            <div>
              <p className="text-slate-400 text-sm mb-1">Your Rank</p>
              <p className="text-3xl font-bold text-blue-400">#10</p>
              <p className="text-green-400 text-xs mt-1 flex items-center gap-1">
                <TrendingUp className="w-3 h-3" />
                +24 this week
              </p>
            </div>
            <div className="w-10 h-10 rounded-lg bg-slate-700/50 flex items-center justify-center">
              <Trophy className="w-5 h-5 text-green-400" />
            </div>
          </div>

          {/* Total Managers */}
          <div className="bg-slate-800/60 border border-slate-700/50 rounded-xl p-5 flex items-start justify-between">
            <div>
              <p className="text-slate-400 text-sm mb-1">Total Managers</p>
              <p className="text-3xl font-bold text-white">9.2M</p>
              <p className="text-slate-500 text-xs mt-1">Worldwide</p>
            </div>
            <div className="w-10 h-10 rounded-lg bg-slate-700/50 flex items-center justify-center">
              <Users className="w-5 h-5 text-blue-400" />
            </div>
          </div>

          {/* Points Behind Leader */}
          <div className="bg-slate-800/60 border border-slate-700/50 rounded-xl p-5 flex items-start justify-between">
            <div>
              <p className="text-slate-400 text-sm mb-1">Points Behind Leader</p>
              <p className="text-3xl font-bold text-orange-400">469</p>
              <p className="text-slate-500 text-xs mt-1">Catchable!</p>
            </div>
            <div className="w-10 h-10 rounded-lg bg-slate-700/50 flex items-center justify-center">
              <Crown className="w-5 h-5 text-yellow-500" />
            </div>
          </div>
        </div>

        {/* Search Bar */}
        <div className="bg-slate-800/60 border border-slate-700/50 rounded-xl p-4 mb-6 flex items-center gap-3">
          <Search className="w-5 h-5 text-slate-500" />
          <input
            type="text"
            placeholder="Search managers or teams..."
            className="bg-transparent text-slate-300 placeholder-slate-500 outline-none w-full text-sm"
          />
        </div>

        {/* Leaderboard */}
        <div className="bg-slate-800/60 border border-slate-700/50 rounded-xl overflow-hidden">
          <div className="p-5 border-b border-slate-700/50 flex items-center gap-2">
            <Trophy className="w-5 h-5 text-green-400" />
            <h2 className="text-white font-bold text-lg">Leaderboard</h2>
          </div>

          <div className="divide-y divide-slate-700/50">
            {leaderboardData.map((player) => (
              <div
                key={player.rank}
                className={`flex items-center px-5 py-4 transition-colors ${
                  player.isYou
                    ? "bg-green-500/10 border-l-4 border-green-500"
                    : "hover:bg-slate-700/30"
                }`}
              >
                {/* Rank */}
                <div className="w-12 flex items-center justify-center">
                  {getRankDisplay(player.rank, player.isYou)}
                </div>

                {/* Player Info */}
                <div className="flex-1 ml-4">
                  <div className="flex items-center gap-2">
                    <span className={`font-bold ${player.isYou ? "text-white" : "text-white"}`}>
                      {player.name}
                    </span>
                    {player.isTop3 && (
                      <span className="text-xs bg-green-500/20 text-green-400 px-2 py-0.5 rounded-full font-medium border border-green-500/30">
                        Top 3
                      </span>
                    )}
                    {player.isYou && (
                      <span className="text-xs bg-green-500 text-white px-2 py-0.5 rounded-full font-medium">
                        You
                      </span>
                    )}
                  </div>
                  <p className="text-slate-400 text-sm">{player.team}</p>
                </div>

                {/* Points */}
                <div className="text-right">
                  <p className={`text-xl font-bold ${player.isYou ? "text-green-400" : "text-white"}`}>
                    {player.points.toLocaleString("en-US", { minimumFractionDigits: 0 }).replace(",", ".")}
                  </p>
                  <p className="text-slate-500 text-xs">points</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Your Performance */}
        <div className="bg-slate-800/60 border border-slate-700/50 rounded-xl p-6 mt-6">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 rounded-lg bg-green-500/20 flex items-center justify-center">
              <TrendingUp className="w-5 h-5 text-green-400" />
            </div>
            <div>
              <h3 className="text-white font-bold text-lg">Your Performance</h3>
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
      </div>
    </div>
  );
}
