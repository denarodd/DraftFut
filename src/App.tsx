import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Sidebar from "./components/Sidebar";
import Dashboard from "./pages/Dashboard";
import BuildTeam from "./pages/BuildTeam";
import Points from "./pages/Points";
import Ranking from "./pages/Ranking";
import Leagues from "./pages/Leagues";
import "./App.css";

function App() {
  return (
    <BrowserRouter>
      <div className="flex min-h-screen bg-slate-950 text-white">
        <Sidebar />
        <main className="flex-1 ml-52">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/build-team" element={<BuildTeam />} />
            <Route path="/points" element={<Points />} />
            <Route path="/ranking" element={<Ranking />} />
            <Route path="/leagues" element={<Leagues />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
