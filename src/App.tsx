import './App.css'
import Sidebar from './components/Sidebar'
import StatsCards from './components/StatsCards'
import SearchBar from './components/SearchBar'
import Leaderboard from './components/Leaderboard'
import YourPerformance from './components/YourPerformance'

function App() {
  return (
    <div className="flex min-h-screen bg-slate-950 text-white">
      <Sidebar />
      <main className="ml-52 flex-1 p-8">
        <div className="max-w-5xl">
          <h1 className="text-3xl font-bold text-green-400 mb-1">
            Global Ranking
          </h1>
          <p className="text-slate-400 mb-6">
            Compete with managers worldwide
          </p>

          <StatsCards />
          <SearchBar />
          <Leaderboard />
          <YourPerformance />
        </div>
      </main>
    </div>
  )
}

export default App
