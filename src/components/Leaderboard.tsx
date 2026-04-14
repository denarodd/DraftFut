import { Trophy } from "lucide-react";

interface Player {
  rank: number;
  name: string;
  team: string;
  points: string;
  isTop3: boolean;
  isYou: boolean;
}

const players: Player[] = [
  { rank: 1, name: "FootballKing", team: "The Winners", points: "2.456", isTop3: true, isYou: false },
  { rank: 2, name: "ProManager", team: "Elite Squad", points: "2.398", isTop3: true, isYou: false },
  { rank: 3, name: "TacticalGenius", team: "Master Class", points: "2.367", isTop3: true, isYou: false },
  { rank: 4, name: "ChampionPlayer", team: "Victory FC", points: "2.301", isTop3: false, isYou: false },
  { rank: 5, name: "GoalMachine", team: "Striker United", points: "2.245", isTop3: false, isYou: false },
  { rank: 6, name: "FantasyPro", team: "Dream Team", points: "2.198", isTop3: false, isYou: false },
  { rank: 7, name: "BestManager", team: "Champions League", points: "2.145", isTop3: false, isYou: false },
  { rank: 8, name: "StarPlayer", team: "All Stars FC", points: "2.089", isTop3: false, isYou: false },
  { rank: 9, name: "WinnerMindset", team: "Never Give Up", points: "2.034", isTop3: false, isYou: false },
  { rank: 10, name: "You", team: "Green Warriors", points: "1.987", isTop3: false, isYou: true },
  { rank: 11, name: "FootballFan", team: "Fan Favorites", points: "1.923", isTop3: false, isYou: false },
  { rank: 12, name: "GameChanger", team: "Game Changers", points: "1.876", isTop3: false, isYou: false },
];

function getTrophyColor(rank: number): string {
  if (rank === 1) return "text-yellow-400";
  if (rank === 2) return "text-slate-300";
  if (rank === 3) return "text-orange-400";
  return "text-slate-500";
}

export default function Leaderboard() {
  return (
    <div className="bg-slate-800/60 border border-slate-700/50 rounded-xl overflow-hidden mb-6">
      <div className="flex items-center gap-2 px-6 py-4 border-b border-slate-700/50">
        <Trophy size={20} className="text-green-400" />
        <h2 className="text-white font-semibold text-lg">Leaderboard</h2>
      </div>

      <div className="divide-y divide-slate-700/30">
        {players.map((player) => (
          <div
            key={player.rank}
            className={`flex items-center px-6 py-4 transition-colors ${
              player.isYou
                ? "bg-green-500/10 border-l-4 border-green-500"
                : "hover:bg-slate-700/20"
            }`}
          >
            {/* Rank */}
            <div className="w-12 flex-shrink-0 text-center">
              {player.isTop3 ? (
                <Trophy size={22} className={getTrophyColor(player.rank)} />
              ) : (
                <span className={`text-lg font-medium ${player.isYou ? "text-green-400" : "text-slate-400"}`}>
                  {player.rank}
                </span>
              )}
            </div>

            {/* Player Info */}
            <div className="flex-1 ml-4">
              <div className="flex items-center gap-2">
                <span className={`font-semibold ${player.isYou ? "text-white" : "text-white"}`}>
                  {player.name}
                </span>
                {player.isTop3 && (
                  <span className="bg-yellow-500/20 text-yellow-400 text-xs px-2 py-0.5 rounded-md font-medium border border-yellow-500/30">
                    Top 3
                  </span>
                )}
                {player.isYou && (
                  <span className="bg-green-500/20 text-green-400 text-xs px-2 py-0.5 rounded-md font-medium border border-green-500/30">
                    You
                  </span>
                )}
              </div>
              <p className="text-slate-500 text-sm">{player.team}</p>
            </div>

            {/* Points */}
            <div className="text-right">
              <span className={`text-xl font-bold ${player.isYou ? "text-green-400" : "text-white"}`}>
                {player.points}
              </span>
              <p className="text-slate-500 text-xs">points</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
