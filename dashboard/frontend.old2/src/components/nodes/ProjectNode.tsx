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

const ProjectNode = ({ data }: { data: NodeData }) => {
  return (
    <div className="relative bg-gradient-to-br from-slate-900 to-slate-800 border-2 border-cyan-500 rounded-xl p-4 min-w-[200px] shadow-lg shadow-cyan-500/25 transition-all duration-300 hover:shadow-cyan-500/40 hover:-translate-y-0.5 cursor-pointer">
      <div className="flex items-center gap-2 mb-3">
        <span className="text-2xl">📁</span>
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
        <div className="flex justify-between items-center">
          <span className="text-slate-400">Activity:</span>
          <span className="text-cyan-400 font-semibold">{data.metrics.activity}%</span>
        </div>
        <div className="flex justify-between items-center">
          <span className="text-slate-400">Health:</span>
          <span className="text-cyan-400 font-semibold">{data.metrics.health}%</span>
        </div>
        <div className="flex justify-between items-center">
          <span className="text-slate-400">Cost:</span>
          <span className="text-cyan-400 font-semibold">${data.metrics.cost.toFixed(2)}/hr</span>
        </div>
        <div className="flex justify-between items-center">
          <span className="text-slate-400">Performance:</span>
          <span className="text-cyan-400 font-semibold">{data.metrics.performance}%</span>
        </div>
      </div>

      {/* Progress bar */}
      <div className="mt-3 h-1 bg-slate-700 rounded-full overflow-hidden">
        <div
          className="h-full bg-gradient-to-r from-cyan-500 to-blue-500 transition-all duration-300"
          style={{ width: `${data.metrics.health}%` }}
        />
      </div>

      <Handle type="source" position={Position.Bottom} className="w-3 h-3 bg-cyan-500 border-2 border-slate-900" />
    </div>
  )
}

export default ProjectNode
