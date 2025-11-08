import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom'
import { Home, FolderKanban, TrendingUp, DollarSign, Settings, Activity } from 'lucide-react'
import Dashboard from './pages/Dashboard'
import Projects from './pages/Projects'
import Analytics from './pages/Analytics'
import SettingsPage from './pages/Settings'

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-background relative overflow-hidden">
        {/* Cyberpunk Grid Background */}
        <div className="absolute inset-0 bg-cyber-grid bg-cyber-grid opacity-20 pointer-events-none" />

        {/* Animated Glow Orbs */}
        <div className="absolute top-20 left-20 w-96 h-96 bg-neon-cyan rounded-full blur-3xl opacity-10 animate-pulse-slow pointer-events-none" />
        <div className="absolute bottom-20 right-20 w-96 h-96 bg-neon-purple rounded-full blur-3xl opacity-10 animate-pulse-slow pointer-events-none" style={{ animationDelay: '1.5s' }} />

        <Sidebar />
        <main className="ml-64 p-8 relative z-10">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/projects" element={<Projects />} />
            <Route path="/analytics" element={<Analytics />} />
            <Route path="/settings" element={<SettingsPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

function Sidebar() {
  const location = useLocation()

  const navItems = [
    { path: '/', icon: Home, label: 'Dashboard' },
    { path: '/projects', icon: FolderKanban, label: 'Projects' },
    { path: '/analytics', icon: TrendingUp, label: 'Analytics' },
    { path: '/settings', icon: Settings, label: 'Settings' },
  ]

  return (
    <aside className="fixed left-0 top-0 h-screen w-64 border-r border-primary/20 bg-card/80 backdrop-blur-xl p-6 shadow-neon-cyan z-20">
      <div className="mb-8">
        <h1 className="text-2xl font-bold flex items-center gap-2 text-primary animate-glow">
          <span className="text-3xl">👻🧠</span>
          <span className="bg-gradient-to-r from-neon-cyan via-neon-purple to-neon-pink bg-clip-text text-transparent">
            Phantom Neural Cortex
          </span>
        </h1>
        <p className="text-sm text-neon-cyan/70 mt-2 font-mono">The Mind Behind The Machine</p>
      </div>

      <nav className="space-y-2">
        {navItems.map((item) => {
          const isActive = location.pathname === item.path
          const Icon = item.icon

          return (
            <Link
              key={item.path}
              to={item.path}
              className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-300 border ${
                isActive
                  ? 'bg-primary/10 text-primary border-primary shadow-neon-cyan animate-glow'
                  : 'hover:bg-primary/5 text-foreground border-transparent hover:border-primary/30 hover:shadow-neon-cyan/50'
              }`}
            >
              <Icon size={20} />
              <span className="font-medium">{item.label}</span>
            </Link>
          )
        })}
      </nav>

      <div className="absolute bottom-6 left-6 right-6">
        <div className="border-t border-primary/20 pt-4">
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <Activity size={16} className="text-neon-cyan" />
            <span className="font-mono">System Status</span>
          </div>
          <div className="mt-2 flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-neon-green shadow-[0_0_10px_rgba(57,255,20,0.8)] animate-pulse" />
            <span className="text-sm font-medium text-neon-green">Neural Cortex Active</span>
          </div>
        </div>
      </div>
    </aside>
  )
}

export default App
