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

const CacheNode = ({ data }: { data: NodeData }) => {
  const hitRate = data.metrics.activity
  const hitRateColor =
    hitRate >= 85 ? 'text-green-400' :
    hitRate >= 70 ? 'text-blue-400' :
    hitRate >= 50 ? 'text-amber-400' : 'text-red-400'

  return (
    <div className="relative bg-gradient-to-br from-slate-900 to-slate-800 border-2 border-indigo-500 rounded-xl p-4 min-w-[200px] shadow-lg shadow-indigo-500/25 transition-all duration-300 hover:shadow-indigo-500/40 hover:-translate-y-0.5 cursor-pointer">
      <Handle type="target" position={Position.Top} className="w-3 h-3 bg-indigo-500 border-2 border-slate-900" />

      <div className="flex items-center gap-2 mb-3">
        <span className="text-2xl">💾</span>
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

      {/* Cache Hit Rate - Large Display */}
      <div className="mb-3 text-center">
        <div className={`text-2xl font-bold ${hitRateColor}`}>{hitRate}%</div>
        <div className="text-xs text-slate-400">Hit Rate</div>
      </div>

      {/* Cache Layers */}
      <div className="space-y-2 text-xs">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 bg-green-500 rounded-full" />
            <span className="text-slate-400">Memory:</span>
          </div>
          <span className="text-indigo-400 font-semibold">145MB</span>
        </div>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 bg-green-500 rounded-full" />
            <span className="text-slate-400">Disk:</span>
          </div>
          <span className="text-indigo-400 font-semibold">2.3GB</span>
        </div>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 bg-slate-600 rounded-full" />
            <span className="text-slate-400">Remote:</span>
          </div>
          <span className="text-slate-500 font-semibold">Disabled</span>
        </div>
      </div>

      {/* Cache efficiency bar */}
      <div className="mt-3">
        <div className="flex items-center justify-between text-xs mb-1">
          <span className="text-slate-400">Efficiency</span>
          <span className="text-indigo-400 font-semibold">{data.metrics.performance}%</span>
        </div>
        <div className="h-1.5 bg-slate-700 rounded-full overflow-hidden">
          <div
            className="h-full bg-gradient-to-r from-indigo-500 to-purple-500 transition-all duration-300"
            style={{ width: `${data.metrics.performance}%` }}
          />
        </div>
      </div>

      {/* Entry count */}
      <div className="mt-2 text-xs text-center text-slate-500">
        4,433 entries cached
      </div>

      <Handle type="source" position={Position.Bottom} className="w-3 h-3 bg-indigo-500 border-2 border-slate-900" />
    </div>
  )
}

export default CacheNode
