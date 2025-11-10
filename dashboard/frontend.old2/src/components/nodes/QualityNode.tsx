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

const QualityNode = ({ data }: { data: NodeData }) => {
  const qualityLevel = data.metrics.performance
  const qualityColor =
    qualityLevel >= 90 ? 'emerald' :
    qualityLevel >= 75 ? 'blue' :
    qualityLevel >= 60 ? 'amber' : 'red'

  return (
    <div className={`relative bg-gradient-to-br from-slate-900 to-slate-800 border-2 border-${qualityColor}-500 rounded-xl p-4 min-w-[200px] shadow-lg shadow-${qualityColor}-500/25 transition-all duration-300 hover:shadow-${qualityColor}-500/40 hover:-translate-y-0.5 cursor-pointer`}>
      <Handle type="target" position={Position.Top} className={`w-3 h-3 bg-${qualityColor}-500 border-2 border-slate-900`} />

      <div className="flex items-center gap-2 mb-3">
        <span className="text-2xl">🎯</span>
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

      {/* Quality Score - Large Display */}
      <div className="mb-3 text-center">
        <div className="text-3xl font-bold text-emerald-400">{data.metrics.performance}%</div>
        <div className="text-xs text-slate-400">Overall Quality</div>
      </div>

      {/* Quality Dimensions */}
      <div className="space-y-1.5 text-xs">
        <div className="flex items-center gap-2">
          <span className="text-slate-400 w-20">Accuracy:</span>
          <div className="flex-1 h-1.5 bg-slate-700 rounded-full overflow-hidden">
            <div className="h-full bg-gradient-to-r from-emerald-500 to-green-500" style={{ width: '95%' }} />
          </div>
          <span className="text-emerald-400 font-semibold w-8 text-right">95%</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-slate-400 w-20">Completeness:</span>
          <div className="flex-1 h-1.5 bg-slate-700 rounded-full overflow-hidden">
            <div className="h-full bg-gradient-to-r from-emerald-500 to-green-500" style={{ width: '92%' }} />
          </div>
          <span className="text-emerald-400 font-semibold w-8 text-right">92%</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-slate-400 w-20">Reliability:</span>
          <div className="flex-1 h-1.5 bg-slate-700 rounded-full overflow-hidden">
            <div className="h-full bg-gradient-to-r from-emerald-500 to-green-500" style={{ width: '88%' }} />
          </div>
          <span className="text-emerald-400 font-semibold w-8 text-right">88%</span>
        </div>
      </div>

      {/* Checkpoints indicator */}
      <div className="mt-3 flex items-center justify-between text-xs">
        <span className="text-slate-400">Checkpoints:</span>
        <div className="flex gap-1">
          <span className="w-2 h-2 bg-green-500 rounded-full" title="33% Complete" />
          <span className="w-2 h-2 bg-green-500 rounded-full" title="66% Complete" />
          <span className="w-2 h-2 bg-green-500 rounded-full" title="100% Complete" />
        </div>
      </div>

      <Handle type="source" position={Position.Bottom} className={`w-3 h-3 bg-${qualityColor}-500 border-2 border-slate-900`} />
    </div>
  )
}

export default QualityNode
