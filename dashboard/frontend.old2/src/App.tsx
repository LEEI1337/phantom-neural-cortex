import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { CollapsableSidebar } from './components/CollapsableSidebar'
import Dashboard from './pages/Dashboard'
import Projects from './pages/Projects'
import Analytics from './pages/Analytics'
import UnifiedSettings from './pages/UnifiedSettings'
import SwarmVisualization from './pages/SwarmVisualization'
import UnifiedSwarm from './pages/UnifiedSwarm'

// Import all CSS files
import './styles/matrix.css'
import './styles/nodes.css'
import './styles/panels.css'
import './styles/animations.css'
import './styles/graph.css'
import './styles/unified-swarm.css'
import 'reactflow/dist/style.css'

function App() {
  return (
    <Router>
      <div className="flex min-h-screen bg-background">
        <CollapsableSidebar />
        <main className="flex-1 p-8">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/projects" element={<Projects />} />
            <Route path="/analytics" element={<Analytics />} />
            <Route path="/swarm" element={<UnifiedSwarm />} />
            <Route path="/swarm-old" element={<SwarmVisualization />} />
            <Route path="/hrm" element={<UnifiedSettings />} />
            <Route path="/settings" element={<UnifiedSettings />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App
