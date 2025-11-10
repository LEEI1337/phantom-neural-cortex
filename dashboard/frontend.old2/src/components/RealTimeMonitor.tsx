/**
 * RealTimeMonitor Component
 * Live task monitoring with WebSocket updates
 */

import { useState, useEffect } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Activity, Zap, AlertCircle, CheckCircle, Clock } from 'lucide-react'
import { formatDistanceToNow } from 'date-fns'
import { ws } from '@/lib/websocket'
import { api } from '@/lib/api'
import type { Task, RealTimeTaskUpdate, FeedbackLoopUpdate } from '@/lib/types'

export default function RealTimeMonitor() {
  const [activeTasks, setActiveTasks] = useState<Task[]>([])
  const [liveUpdates, setLiveUpdates] = useState<RealTimeTaskUpdate[]>([])
  const [feedbackUpdates, setFeedbackUpdates] = useState<FeedbackLoopUpdate[]>([])
  const [isConnected, setIsConnected] = useState(false)

  // Fetch active tasks initially
  const { data: tasksResponse } = useQuery({
    queryKey: ['active-tasks'],
    queryFn: async () => {
      const result = await api.getTasks({ status: 'in_progress' })
      if (!result.success) throw new Error(result.error)
      return result.data!
    },
    refetchInterval: 10000, // Fallback polling every 10s
  })

  useEffect(() => {
    if (tasksResponse?.items) {
      setActiveTasks(tasksResponse.items)
    }
  }, [tasksResponse])

  // WebSocket subscriptions
  useEffect(() => {
    // Connection status
    const unsubStatus = ws.on('connection_status', (data: { connected: boolean }) => {
      setIsConnected(data.connected)
    })

    // Task updates
    const unsubTask = ws.subscribeToAllTasks((update) => {
      setLiveUpdates((prev) => [update, ...prev].slice(0, 20)) // Keep last 20

      // Update active tasks
      setActiveTasks((prev) => {
        const existing = prev.find((t) => t.id === update.task_id)
        if (existing) {
          return prev.map((t) =>
            t.id === update.task_id
              ? {
                  ...t,
                  status: update.status,
                  current_iteration: update.iteration,
                  current_quality: update.quality,
                  assigned_agent: update.agent as any,
                }
              : t
          )
        }
        return prev
      })
    })

    // Feedback loop updates
    const unsubFeedback = ws.subscribeToFeedbackLoop((update) => {
      setFeedbackUpdates((prev) => [update, ...prev].slice(0, 10))
    })

    return () => {
      unsubStatus()
      unsubTask()
      unsubFeedback()
    }
  }, [])

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <h2 className="text-2xl font-bold">Real-Time Monitor</h2>
          <ConnectionStatus isConnected={isConnected} />
        </div>
        <div className="text-sm text-muted-foreground">
          {activeTasks.length} active task{activeTasks.length !== 1 ? 's' : ''}
        </div>
      </div>

      {/* Active Tasks */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {activeTasks.map((task) => (
          <ActiveTaskCard key={task.id} task={task} />
        ))}

        {activeTasks.length === 0 && (
          <div className="col-span-2 text-center py-12 border-2 border-dashed rounded-lg">
            <Activity className="mx-auto mb-3 text-muted-foreground" size={48} />
            <p className="text-lg text-muted-foreground">No active tasks</p>
            <p className="text-sm text-muted-foreground mt-1">
              Tasks will appear here when running
            </p>
          </div>
        )}
      </div>

      {/* Live Update Stream */}
      <div className="border rounded-lg p-6 bg-card">
        <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
          <Zap size={20} />
          Live Updates
        </h3>
        <div className="space-y-2 max-h-96 overflow-y-auto">
          {liveUpdates.map((update, idx) => (
            <LiveUpdateItem key={idx} update={update} />
          ))}

          {liveUpdates.length === 0 && (
            <p className="text-sm text-muted-foreground text-center py-8">
              Waiting for updates...
            </p>
          )}
        </div>
      </div>

      {/* Feedback Loop Monitor */}
      {feedbackUpdates.length > 0 && (
        <div className="border rounded-lg p-6 bg-card">
          <h3 className="text-lg font-semibold mb-4">Feedback Loop Activity</h3>
          <div className="space-y-3">
            {feedbackUpdates.map((update, idx) => (
              <FeedbackLoopItem key={idx} update={update} />
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

function ConnectionStatus({ isConnected }: { isConnected: boolean }) {
  return (
    <div className="flex items-center gap-2">
      <div
        className={`w-2 h-2 rounded-full ${
          isConnected ? 'bg-green-500 animate-pulse' : 'bg-red-500'
        }`}
      />
      <span className="text-sm text-muted-foreground">
        {isConnected ? 'Connected' : 'Disconnected'}
      </span>
    </div>
  )
}

function ActiveTaskCard({ task }: { task: Task }) {
  const statusColors = {
    in_progress: 'border-blue-500 bg-blue-50',
    pending: 'border-yellow-500 bg-yellow-50',
    completed: 'border-green-500 bg-green-50',
    failed: 'border-red-500 bg-red-50',
  }

  const agentEmoji = {
    gemini: '🟢',
    claude: '🔵',
    copilot: '🟣',
  }

  const progress = (task.current_iteration / task.max_iterations) * 100

  return (
    <div className={`border-l-4 rounded-lg p-5 ${statusColors[task.status]}`}>
      <div className="flex items-start justify-between mb-3">
        <div className="flex-1">
          <h4 className="font-semibold mb-1">{task.title}</h4>
          <p className="text-sm text-muted-foreground">#{task.issue_number}</p>
        </div>
        <span className="text-2xl">{agentEmoji[task.assigned_agent]}</span>
      </div>

      <div className="space-y-3">
        {/* Progress Bar */}
        <div>
          <div className="flex justify-between text-sm mb-1">
            <span className="text-muted-foreground">
              Iteration {task.current_iteration}/{task.max_iterations}
            </span>
            <span className="text-muted-foreground">{progress.toFixed(0)}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-blue-600 h-2 rounded-full transition-all"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>

        {/* Quality Badge */}
        {task.current_quality > 0 && (
          <div className="flex items-center justify-between text-sm">
            <span className="text-muted-foreground">Current Quality</span>
            <span className="font-medium">{(task.current_quality * 100).toFixed(0)}%</span>
          </div>
        )}

        {/* Agent Switches */}
        {task.agent_switches > 0 && (
          <div className="text-xs text-muted-foreground">
            🔄 {task.agent_switches} agent switch{task.agent_switches !== 1 ? 'es' : ''}
          </div>
        )}

        {/* Timestamp */}
        {task.started_at && (
          <div className="text-xs text-muted-foreground flex items-center gap-1">
            <Clock size={12} />
            Started {formatDistanceToNow(new Date(task.started_at), { addSuffix: true })}
          </div>
        )}
      </div>
    </div>
  )
}

function LiveUpdateItem({ update }: { update: RealTimeTaskUpdate }) {
  const statusIcons = {
    in_progress: <Activity size={16} className="text-blue-600" />,
    pending: <Clock size={16} className="text-yellow-600" />,
    completed: <CheckCircle size={16} className="text-green-600" />,
    failed: <AlertCircle size={16} className="text-red-600" />,
  }

  return (
    <div className="flex items-start gap-3 p-3 bg-muted/50 rounded-lg text-sm">
      <div className="mt-0.5">{statusIcons[update.status]}</div>
      <div className="flex-1">
        <div className="flex items-center justify-between mb-1">
          <span className="font-medium">
            Task #{update.task_id.slice(0, 8)} • Iteration {update.iteration}
          </span>
          <span className="text-xs text-muted-foreground">
            {formatDistanceToNow(new Date(update.timestamp), { addSuffix: true })}
          </span>
        </div>
        <p className="text-muted-foreground">{update.message}</p>
        {update.quality > 0 && (
          <div className="mt-1 text-xs">
            Quality: {(update.quality * 100).toFixed(0)}% • Agent: {update.agent}
          </div>
        )}
      </div>
    </div>
  )
}

function FeedbackLoopItem({ update }: { update: FeedbackLoopUpdate }) {
  const decisionColors = {
    continue: 'bg-blue-100 text-blue-800',
    halt: 'bg-green-100 text-green-800',
  }

  return (
    <div className="border rounded-lg p-4 bg-muted/30">
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-2">
          <span className="font-medium">Iteration {update.iteration}</span>
          <span className={`px-2 py-1 rounded text-xs font-medium ${decisionColors[update.decision]}`}>
            {update.decision.toUpperCase()}
          </span>
        </div>
        <span className="text-xs text-muted-foreground">
          {formatDistanceToNow(new Date(update.timestamp), { addSuffix: true })}
        </span>
      </div>

      <div className="grid grid-cols-2 gap-2 text-sm mb-2">
        <div>
          <span className="text-muted-foreground">H-Module Quality: </span>
          <span className="font-medium">{(update.h_module_quality * 100).toFixed(0)}%</span>
        </div>
        <div>
          <span className="text-muted-foreground">L-Module: </span>
          <span className="font-medium">{update.l_module_status}</span>
        </div>
      </div>

      {update.warnings.length > 0 && (
        <div className="text-xs space-y-1">
          {update.warnings.map((warning, idx) => (
            <div key={idx} className="text-yellow-700">
              ⚠️ {warning}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
