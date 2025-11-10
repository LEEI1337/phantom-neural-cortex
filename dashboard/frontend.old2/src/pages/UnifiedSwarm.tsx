import { useState, useEffect } from 'react'
import MatrixRainbow from '../components/MatrixRainbow'
import MatrixText from '../components/MatrixText'
import SwarmGraph from '../components/SwarmGraph'
import { ControlPanel } from '../components/panels'
import { useSwarmStore } from '../lib/swarmStore'

const UnifiedSwarm = () => {
  const [matrixRainActive, setMatrixRainActive] = useState(false)
  const [partyMode, setPartyMode] = useState(false)
  const [showPanel, setShowPanel] = useState(true)
  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null)

  const swarmStore = useSwarmStore()

  // Konami Code Easter Egg
  useEffect(() => {
    const KONAMI_CODE = [
      'ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown',
      'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight',
      'b', 'a'
    ]

    let konamiIndex = 0

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === KONAMI_CODE[konamiIndex]) {
        konamiIndex++

        if (konamiIndex === KONAMI_CODE.length) {
          // PARTY MODE ACTIVATED! 🎉
          setPartyMode(true)
          setMatrixRainActive(true)

          // Show achievement toast
          const toast = document.createElement('div')
          toast.className = 'achievement-toast party-mode'
          toast.innerHTML = `
            <div class="achievement-content">
              <div class="achievement-icon">🎮</div>
              <div>
                <div class="achievement-title">Achievement Unlocked!</div>
                <div class="achievement-name">Konami Master</div>
                <div class="achievement-description">You activated party mode! 🎉</div>
              </div>
            </div>
          `
          document.body.appendChild(toast)

          setTimeout(() => toast.remove(), 5000)

          // Auto-disable after 10 seconds
          setTimeout(() => {
            setPartyMode(false)
            setMatrixRainActive(false)
          }, 10000)

          konamiIndex = 0
        }
      } else {
        konamiIndex = 0
      }
    }

    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [])

  // Logo triple-click handler
  const [logoClickCount, setLogoClickCount] = useState(0)
  const [lastLogoClick, setLastLogoClick] = useState(0)

  const handleLogoClick = () => {
    const now = Date.now()

    if (now - lastLogoClick < 500) {
      setLogoClickCount(prev => prev + 1)

      if (logoClickCount === 2) {
        // Triple click! Rainbow confetti
        if (typeof window !== 'undefined' && (window as any).confetti) {
          (window as any).confetti({
            particleCount: 200,
            spread: 180,
            origin: { y: 0.3 },
            colors: ['#06b6d4', '#3b82f6', '#8b5cf6', '#ec4899', '#f59e0b']
          })
        }

        // Show achievement
        const toast = document.createElement('div')
        toast.className = 'achievement-toast rainbow'
        toast.innerHTML = `
          <div class="achievement-content">
            <div class="achievement-icon">🌈</div>
            <div>
              <div class="achievement-title">Achievement Unlocked!</div>
              <div class="achievement-name">Rainbow Hunter</div>
              <div class="achievement-description">You found the rainbow! ✨</div>
            </div>
          </div>
        `
        document.body.appendChild(toast)
        setTimeout(() => toast.remove(), 5000)

        setLogoClickCount(0)
      }
    } else {
      setLogoClickCount(1)
    }

    setLastLogoClick(now)
  }

  // Handle node selection
  const handleNodeClick = (nodeId: string) => {
    setSelectedNodeId(nodeId)
    setShowPanel(true)
  }

  // Determine panel mode based on selected node
  const getPanelMode = () => {
    if (!selectedNodeId) return 'overview'

    if (selectedNodeId.includes('hrm')) return 'hrm'
    if (selectedNodeId.includes('swarm')) return 'swarm'
    if (selectedNodeId.includes('agent')) return 'agent'
    if (selectedNodeId.includes('cache') || selectedNodeId.includes('metrics')) return 'health'

    return 'overview'
  }

  // Expose to console for easter eggs
  useEffect(() => {
    (window as any).phantomCommands = {
      rainbow: () => {
        setMatrixRainActive(true)
        setTimeout(() => setMatrixRainActive(false), 10000)
        console.log('🌈 Rainbow mode activated for 10 seconds!')
      },

      matrix: () => {
        setMatrixRainActive(!matrixRainActive)
        console.log(`💻 Matrix rain ${!matrixRainActive ? 'activated' : 'deactivated'}!`)
      },

      hackThePlanet: () => {
        setMatrixRainActive(true)
        setPartyMode(true)

        console.log(`
╔═══════════════════════════════════════╗
║  🌈 HACK THE PLANET ACTIVATED! 🌈    ║
║                                       ║
║  You are now a certified hackerman    ║
║  Badge: 💻 Elite Hacker               ║
║                                       ║
╚═══════════════════════════════════════╝
        `)

        setTimeout(() => {
          setMatrixRainActive(false)
          setPartyMode(false)
        }, 15000)
      },

      help: () => {
        console.log(`
🌈 PHANTOM NEURAL CORTEX - Secret Commands
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

phantomCommands.rainbow()        - Activate rainbow mode
phantomCommands.matrix()         - Toggle matrix rain
phantomCommands.hackThePlanet()  - Full terminal takeover
phantomCommands.help()           - Show this help

Easter Eggs:
• Konami Code: ↑↑↓↓←→←→BA
• Triple-click logo
        `)
      }
    }
  }, [matrixRainActive])

  return (
    <div className={`unified-swarm-page ${partyMode ? 'party-mode' : ''}`}>
      {/* Subtle Matrix Background (always on) */}
      <MatrixRainbow active={true} opacity={0.05} speed={0.5} />

      {/* Full Matrix Rain (easter egg) */}
      <MatrixRainbow active={matrixRainActive} opacity={0.3} speed={1} />

      {/* Header */}
      <header className="swarm-header">
        <h1 className="logo-text" onClick={handleLogoClick}>
          <MatrixText text="🧠 PHANTOM NEURAL CORTEX" duration={50} />
        </h1>

        <div className="header-actions">
          <button className="header-btn">
            <span>🔔</span>
          </button>
          <button className="header-btn">
            <span>👤</span>
          </button>
        </div>
      </header>

      {/* Main Content */}
      <div className="swarm-content">
        {/* Sidebar */}
        <aside className="swarm-sidebar">
          <button className="sidebar-btn active" title="Home">
            🏠
          </button>
          <button className="sidebar-btn" title="Global Settings">
            🌐
          </button>
          <button className="sidebar-btn" title="Projects">
            📁
          </button>
          <button className="sidebar-btn" title="Analytics">
            📊
          </button>
          <button className="sidebar-btn" title="Settings">
            ⚙️
          </button>
        </aside>

        {/* Graph Area */}
        <div className="swarm-graph-area">
          <SwarmGraph onNodeClick={handleNodeClick} />
        </div>

        {/* Control Panel */}
        {showPanel && (
          <div className="swarm-panel-area">
            <ControlPanel
              initialMode={getPanelMode() as any}
              projectId="projekt-a"
              onClose={() => setShowPanel(false)}
            />
          </div>
        )}
      </div>

      {/* Bottom Status Bar */}
      <footer className="swarm-footer">
        <div className="footer-item">
          <span className="status-dot active"></span>
          All Systems Operational
        </div>
        <div className="footer-item">
          5 Agents Active
        </div>
        <div className="footer-item">
          $2.50/hr
        </div>
      </footer>
    </div>
  )
}

export default UnifiedSwarm
