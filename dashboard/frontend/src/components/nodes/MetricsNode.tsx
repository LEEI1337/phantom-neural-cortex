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

const MetricsNode = ({ data }: { data: NodeData }) => {
  return (
    <div className="relative bg-gradient-to-br from-slate-900 to-slate-800 border-2 border-green-500 rounded-xl p-4 min-w-[200px] shadow-lg shadow-green-500/25 transition-all duration-300 hover:shadow-green-500/40 hover:-translate-y-0.5 cursor-pointer">
      <Handle type="target" position={Position.Top} className="w-3 h-3 bg-green-500 border-2 border-slate-900" />

      <div className="flex items-center gap-2 mb-3">
        <span className="text-2xl">📊</span>
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

      {/* Export status */}
      <div className="mb-3">
        <div className="text-xs text-slate-400 mb-1">Export Status</div>
        <div className="flex items-center gap-2">
          {data.status === 'active' ? (
            <>
              <div className="relative">
                <div className="w-2 h-2 bg-green-500 rounded-full animate-ping absolute" />
                <div className="w-2 h-2 bg-green-500 rounded-full" />
              </div>
              <span className="text-xs text-green-400 font-semibold">Exporting Live</span>
            </>
          ) : (
            <>
              <div className="w-2 h-2 bg-slate-600 rounded-full" />
              <span className="text-xs text-slate-500 font-semibold">Paused</span>
            </>
          )}
        </div>
      </div>

      {/* Metrics exported */}
      <div className="space-y-2 text-xs">
        <div className="flex items-center justify-between">
          <span className="text-slate-400">Requests/min:</span>
          <span className="text-green-400 font-semibold">142</span>
        </div>
        <div className="flex items-center justify-between">
          <span className="text-slate-400">Avg Latency:</span>
          <span className="text-green-400 font-semibold">78ms</span>
        </div>
        <div className="flex items-center justify-between">
          <span className="text-slate-400">Error Rate:</span>
          <span className="text-green-400 font-semibold">0.2%</span>
        </div>
      </div>

      {/* Export interval */}
      <div className="mt-3 p-2 bg-slate-800/50 rounded text-center">
        <div className="text-xs text-slate-400">Export Interval</div>
        <div className="text-sm font-semibold text-green-400">15s</div>
      </div>

      {/* Prometheus indicator */}
      <div className="mt-2 flex items-center justify-center gap-2 text-xs">
        <div className="flex items-center gap-1 px-2 py-1 bg-green-500/10 rounded border border-green-500/30">
          <span className="text-green-400">🔥</span>
          <span className="text-green-400 font-semibold">Prometheus</span>
        </div>
      </div>

      {/* Data flow animation */}
      {data.status === 'active' && (
        <div className="absolute inset-0 pointer-events-none overflow-hidden rounded-xl">
          <div className="absolute top-0 left-0 w-full h-0.5 bg-gradient-to-r from-transparent via-green-500 to-transparent animate-pulse" />
        </div>
      )}

      <Handle type="source" position={Position.Bottom} className="w-3 h-3 bg-green-500 border-2 border-slate-900" />
    </div>
  )
}

export default MetricsNode
