import { Users, Plus } from "lucide-react";

const positions = [
  { id: "gk", label: "GK", top: "80%", left: "50%" },
  { id: "lb", label: "LB", top: "60%", left: "15%" },
  { id: "cb1", label: "CB", top: "62%", left: "38%" },
  { id: "cb2", label: "CB", top: "62%", left: "62%" },
  { id: "rb", label: "RB", top: "60%", left: "85%" },
  { id: "cm1", label: "CM", top: "40%", left: "30%" },
  { id: "cm2", label: "CM", top: "38%", left: "50%" },
  { id: "cm3", label: "CM", top: "40%", left: "70%" },
  { id: "lw", label: "LW", top: "18%", left: "20%" },
  { id: "st", label: "ST", top: "12%", left: "50%" },
  { id: "rw", label: "RW", top: "18%", left: "80%" },
];

export default function BuildTeam() {
  return (
    <div className="min-h-screen p-8">
      <div className="max-w-5xl">
        <h1 className="text-3xl font-bold text-green-400 mb-1">Build Team</h1>
        <p className="text-slate-400 mb-6">Create your ultimate squad</p>

        <div className="bg-slate-800/60 border border-slate-700/50 rounded-xl p-6">
          <div className="flex items-center gap-2 mb-6">
            <Users className="w-5 h-5 text-green-400" />
            <h2 className="text-white font-bold text-lg">Formation 4-3-3</h2>
          </div>

          <div className="relative w-full bg-gradient-to-b from-green-900/40 to-green-800/20 border border-green-700/30 rounded-xl overflow-hidden" style={{ paddingBottom: "60%" }}>
            {/* Field lines */}
            <div className="absolute inset-0">
              <div className="absolute top-1/2 left-0 right-0 h-px bg-green-600/30" />
              <div className="absolute top-1/2 left-1/2 w-24 h-24 border border-green-600/30 rounded-full -translate-x-1/2 -translate-y-1/2" />
            </div>

            {positions.map((pos) => (
              <div
                key={pos.id}
                className="absolute -translate-x-1/2 -translate-y-1/2 flex flex-col items-center gap-1"
                style={{ top: pos.top, left: pos.left }}
              >
                <div className="w-12 h-12 rounded-full bg-slate-700/80 border-2 border-dashed border-slate-500 flex items-center justify-center cursor-pointer hover:border-green-400 hover:bg-slate-600/80 transition-colors group">
                  <Plus className="w-5 h-5 text-slate-400 group-hover:text-green-400" />
                </div>
                <span className="text-xs text-slate-400 font-medium">{pos.label}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
