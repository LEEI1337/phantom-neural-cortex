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

const SwarmNode = ({ data }: { data: NodeData }) => {
  return (
    <div className="relative bg-gradient-to-br from-slate-900 to-slate-800 border-2 border-blue-500 rounded-xl p-4 min-w-[220px] shadow-lg shadow-blue-500/25 transition-all duration-300 hover:shadow-blue-500/40 hover:-translate-y-0.5 cursor-pointer">
      <Handle type="target" position={Position.Top} className="w-3 h-3 bg-blue-500 border-2 border-slate-900" />

      <div className="flex items-center gap-2 mb-3">
        <span className="text-2xl">🌊</span>
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

      <div className="space-y-2 text-xs">
        <div className="flex items-center justify-between">
          <span className="text-slate-400">Agent Pool:</span>
          <span className="text-blue-400 font-semibold">5 Agents</span>
        </div>
        <div className="flex items-center justify-between">
          <span className="text-slate-400">Active Tasks:</span>
          <span className="text-blue-400 font-semibold">{data.metrics.activity}%</span>
        </div>
        <div className="flex items-center justify-between">
          <span className="text-slate-400">Load Balance:</span>
          <span className="text-blue-400 font-semibold">Adaptive</span>
        </div>
      </div>

      {/* Performance indicator */}
      <div className="mt-3 grid grid-cols-2 gap-2">
        <div className="bg-slate-800/50 rounded px-2 py-1 text-center">
          <div className="text-xs text-slate-400">Health</div>
          <div className="text-sm font-semibold text-blue-400">{data.metrics.health}%</div>
        </div>
        <div className="bg-slate-800/50 rounded px-2 py-1 text-center">
          <div className="text-xs text-slate-400">Speed</div>
          <div className="text-sm font-semibold text-blue-400">{data.metrics.performance}%</div>
        </div>
      </div>

      {/* Activity waves */}
      {data.status === 'active' && (
        <div className="absolute -top-1 -right-1 w-4 h-4">
          <div className="absolute inset-0 bg-green-500 rounded-full animate-ping opacity-75" />
          <div className="absolute inset-0 bg-green-500 rounded-full" />
        </div>
      )}

      <Handle type="source" position={Position.Bottom} className="w-3 h-3 bg-blue-500 border-2 border-slate-900" />
    </div>
  )
}

export default SwarmNode
