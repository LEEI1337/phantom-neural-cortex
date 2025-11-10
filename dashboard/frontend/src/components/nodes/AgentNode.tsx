import { Handle, Position } from 'reactflow'

interface NodeData {
  label: string
  status: 'active' | 'idle' | 'warning' | 'error'
  metrics: {
    activity: number
    health: number
    cost: number
    performance: number
  }
  config: any
}

const AGENT_CONFIG = {
  'Claude': { icon: '⚡', color: 'violet', specialization: 'Quality-First' },
  'Gemini': { icon: '💎', color: 'cyan', specialization: 'Cost-Optimized' },
  'Copilot': { icon: '🚀', color: 'blue', specialization: 'Code-Specialized' },
  'Cursor': { icon: '📐', color: 'amber', specialization: 'IDE-Integrated' },
  'Windsurf': { icon: '🌊', color: 'teal', specialization: 'Multi-Modal' },
}

const AgentNode = ({ data }: { data: NodeData }) => {
  const agentConfig = AGENT_CONFIG[data.label as keyof typeof AGENT_CONFIG] || {
    icon: '🤖',
    color: 'slate',
    specialization: 'General'
  }

  const borderColor = `border-${agentConfig.color}-500`
  const shadowColor = `shadow-${agentConfig.color}-500/25`
  const hoverShadowColor = `hover:shadow-${agentConfig.color}-500/40`
  const accentColor = `text-${agentConfig.color}-400`

  return (
    <div className={`relative bg-gradient-to-br from-slate-900 to-slate-800 border-2 ${
      data.status === 'active' ? borderColor : 'border-slate-600'
    } rounded-xl p-4 min-w-[180px] shadow-lg ${
      data.status === 'active' ? shadowColor : 'shadow-slate-800/25'
    } transition-all duration-300 ${
      data.status === 'active' ? hoverShadowColor : 'hover:shadow-slate-700/40'
    } hover:-translate-y-0.5 cursor-pointer`}>
      <Handle type="target" position={Position.Top} className={`w-3 h-3 ${
        data.status === 'active' ? `bg-${agentConfig.color}-500` : 'bg-slate-500'
      } border-2 border-slate-900`} />

      <div className="flex items-center gap-2 mb-3">
        <span className="text-2xl">{agentConfig.icon}</span>
        <div className="flex-1">
          <div className="font-semibold text-sm text-slate-100">{data.label}</div>
          <div className="text-xs text-slate-400">{agentConfig.specialization}</div>
        </div>
      </div>

      {data.status === 'active' ? (
        <>
          {/* Active state - show metrics */}
          <div className="space-y-2 text-xs">
            <div className="flex items-center justify-between">
              <span className="text-slate-400">Health:</span>
              <span className={accentColor + ' font-semibold'}>{data.metrics.health}%</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-slate-400">Cost/Task:</span>
              <span className={accentColor + ' font-semibold'}>${data.metrics.cost.toFixed(2)}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-slate-400">Performance:</span>
              <span className={accentColor + ' font-semibold'}>{data.metrics.performance}%</span>
            </div>
          </div>

          {/* Activity pulse indicator */}
          <div className="absolute top-3 right-3">
            <div className="relative w-2 h-2">
              <div className="absolute inset-0 bg-green-500 rounded-full animate-ping" />
              <div className="absolute inset-0 bg-green-500 rounded-full" />
            </div>
          </div>

          {/* Activity bar */}
          <div className="mt-3 h-1 bg-slate-700 rounded-full overflow-hidden">
            <div
              className={`h-full bg-gradient-to-r from-${agentConfig.color}-500 to-${agentConfig.color}-600 transition-all duration-500`}
              style={{ width: `${data.metrics.activity}%` }}
            />
          </div>
        </>
      ) : (
        <>
          {/* Idle state - minimal display */}
          <div className="py-4 text-center">
            <div className="text-slate-500 text-sm font-medium">Idle</div>
            <div className="text-slate-600 text-xs mt-1">Ready to activate</div>
          </div>

          {/* Idle indicator */}
          <div className="absolute top-3 right-3">
            <div className="w-2 h-2 bg-slate-600 rounded-full" />
          </div>
        </>
      )}

      <Handle type="source" position={Position.Bottom} className={`w-3 h-3 ${
        data.status === 'active' ? `bg-${agentConfig.color}-500` : 'bg-slate-500'
      } border-2 border-slate-900`} />
    </div>
  )
}

export default AgentNode
