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

const HRMNode = ({ data }: { data: NodeData }) => {
  return (
    <div className="relative bg-gradient-to-br from-slate-900 to-slate-800 border-2 border-purple-500 rounded-xl p-4 min-w-[200px] shadow-lg shadow-purple-500/25 transition-all duration-300 hover:shadow-purple-500/40 hover:-translate-y-0.5 cursor-pointer">
      <Handle type="target" position={Position.Top} className="w-3 h-3 bg-purple-500 border-2 border-slate-900" />

      <div className="flex items-center gap-2 mb-3">
        <span className="text-2xl">🧠</span>
        <span className="flex-1 font-semibold text-sm text-slate-100">{data.label}</span>
        <span className={`text-xs ${
          data.status === 'active' ? 'text-green-500 animate-pulse' :
          data.status === 'warning' ? 'text-amber-500' :
          data.status === 'error' ? 'text-red-500' :
          'text-slate-500'
        }`}>
          ●
        </span>
      </div>

      <div className="mb-3 space-y-1">
        <div className="text-xs text-slate-300 font-medium">12 Optimizations</div>
        <div className="text-xs text-purple-400">Balanced Preset</div>
      </div>

      <div className="flex items-center justify-around gap-3 text-xs">
        <div className="flex items-center gap-1">
          <span className="text-base">⚡</span>
          <span className="text-purple-400 font-semibold">{data.metrics.performance}%</span>
        </div>
        <div className="h-6 w-px bg-slate-700" />
        <div className="flex items-center gap-1">
          <span className="text-base">💰</span>
          <span className="text-purple-400 font-semibold">${data.metrics.cost.toFixed(2)}</span>
        </div>
      </div>

      {/* Activity indicator */}
      {data.status === 'active' && (
        <div className="absolute top-2 right-2">
          <div className="relative">
            <div className="w-2 h-2 bg-green-500 rounded-full animate-ping absolute" />
            <div className="w-2 h-2 bg-green-500 rounded-full" />
          </div>
        </div>
      )}

      <Handle type="source" position={Position.Bottom} className="w-3 h-3 bg-purple-500 border-2 border-slate-900" />
    </div>
  )
}

export default HRMNode
