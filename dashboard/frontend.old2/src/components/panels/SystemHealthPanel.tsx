import React, { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card'
import { Button } from '../ui/button'

export interface SystemHealthPanelProps {}

interface SystemComponent {
  name: string
  status: 'connected' | 'running' | 'healthy' | 'warning' | 'error'
  metrics: {
    [key: string]: string | number
  }
}

interface CacheInfo {
  name: string
  size: string
  entries: number
  hitRate: number
}

const SYSTEM_COMPONENTS: SystemComponent[] = [
  {
    name: 'Database (PostgreSQL)',
    status: 'connected',
    metrics: {
      latency: '12ms',
      pool: '8/20',
      connections: 8
    }
  },
  {
    name: 'Cache (Redis)',
    status: 'connected',
    metrics: {
      hitRate: '87%',
      memory: '45%',
      uptime: '24h'
    }
  },
  {
    name: 'WebSocket Server',
    status: 'running',
    metrics: {
      connections: 12,
      events: 340,
      uptime: '24h'
    }
  },
  {
    name: 'Backend API',
    status: 'healthy',
    metrics: {
      rps: 45,
      avgLatency: '78ms',
      errorRate: '0.2%'
    }
  }
]

const CACHES: CacheInfo[] = [
  {
    name: 'Guideline Cache',
    size: '145MB',
    entries: 2340,
    hitRate: 87
  },
  {
    name: 'GitHub API Cache',
    size: '89MB',
    entries: 1203,
    hitRate: 92
  },
  {
    name: 'Quality Pattern Cache',
    size: '56MB',
    entries: 890,
    hitRate: 88
  }
]

const METRICS = {
  requestsPerSecond: 45.3,
  avgResponseTime: 78,
  errorRate: 0.2,
  cpuUsage: 34,
  memoryUsage: 58
}

export const SystemHealthPanel: React.FC<SystemHealthPanelProps> = () => {
  const [clearing, setClearing] = useState<string | null>(null)

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'connected':
      case 'running':
      case 'healthy':
        return '🟢'
      case 'warning':
        return '🟡'
      case 'error':
        return '🔴'
      default:
        return '⚪'
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'connected':
      case 'running':
      case 'healthy':
        return 'text-green-400'
      case 'warning':
        return 'text-yellow-400'
      case 'error':
        return 'text-red-400'
      default:
        return 'text-slate-400'
    }
  }

  const clearCache = async (cacheName: string) => {
    setClearing(cacheName)
    // Simulate API call
    await new Promise((resolve) => setTimeout(resolve, 1000))
    setClearing(null)
  }

  const clearAllCaches = async () => {
    setClearing('all')
    // Simulate API call
    await new Promise((resolve) => setTimeout(resolve, 1500))
    setClearing(null)
  }

  return (
    <div className="space-y-6">
      {/* Overall Status */}
      <Card className="bg-gradient-to-br from-slate-900 to-slate-800 border-cyan-500/30">
        <CardHeader>
          <CardTitle className="text-cyan-400 flex items-center gap-2">
            <span className="text-2xl">🏥</span>
            System Health & Infrastructure
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center gap-2">
            <span className="text-2xl">🟢</span>
            <span className="text-lg text-green-400 font-semibold">All Systems Operational</span>
          </div>
        </CardContent>
      </Card>

      {/* Components */}
      <Card className="bg-gradient-to-br from-slate-900 to-slate-800 border-cyan-500/30">
        <CardHeader>
          <CardTitle className="text-cyan-400 text-lg">Components</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {SYSTEM_COMPONENTS.map((component) => (
              <div key={component.name} className="p-4 bg-slate-950/50 rounded border border-cyan-500/20">
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-2">
                    <span className="text-xl">{getStatusIcon(component.status)}</span>
                    <span className="font-semibold text-slate-200">{component.name}</span>
                  </div>
                  <span className={`text-sm ${getStatusColor(component.status)}`}>
                    {component.status.charAt(0).toUpperCase() + component.status.slice(1)}
                  </span>
                </div>
                <div className="flex flex-wrap gap-4 text-sm">
                  {Object.entries(component.metrics).map(([key, value]) => (
                    <div key={key} className="text-slate-400">
                      <span className="capitalize">{key.replace(/([A-Z])/g, ' $1').trim()}: </span>
                      <span className="text-cyan-400">{value}</span>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Cache Management */}
      <Card className="bg-gradient-to-br from-slate-900 to-slate-800 border-cyan-500/30">
        <CardHeader>
          <CardTitle className="text-cyan-400 text-lg">Cache Management</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {CACHES.map((cache) => (
              <div key={cache.name} className="p-4 bg-slate-950/50 rounded border border-cyan-500/20">
                <div className="flex items-center justify-between mb-2">
                  <div>
                    <div className="font-semibold text-slate-200">{cache.name}</div>
                    <div className="text-sm text-slate-400 mt-1">
                      Size: <span className="text-cyan-400">{cache.size}</span>
                      {' | '}
                      Entries: <span className="text-cyan-400">{cache.entries.toLocaleString()}</span>
                      {' | '}
                      Hit Rate: <span className="text-cyan-400">{cache.hitRate}%</span>
                    </div>
                  </div>
                  <Button
                    onClick={() => clearCache(cache.name)}
                    disabled={clearing === cache.name}
                    size="sm"
                    variant="outline"
                    className="border-red-500/50 text-red-400 hover:bg-red-500/10"
                  >
                    {clearing === cache.name ? 'Clearing...' : 'Clear Cache'}
                  </Button>
                </div>
                <div className="mt-2">
                  <div className="w-full h-2 bg-slate-700 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-gradient-to-r from-cyan-500 to-blue-500"
                      style={{ width: `${cache.hitRate}%` }}
                    />
                  </div>
                </div>
              </div>
            ))}

            <div className="pt-4 border-t border-cyan-500/20">
              <Button
                onClick={clearAllCaches}
                disabled={clearing === 'all'}
                variant="outline"
                className="w-full border-red-500/50 text-red-400 hover:bg-red-500/10"
              >
                {clearing === 'all' ? 'Clearing All Caches...' : 'Clear All Caches'}
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Real-time Metrics */}
      <Card className="bg-gradient-to-br from-slate-900 to-slate-800 border-cyan-500/30">
        <CardHeader>
          <CardTitle className="text-cyan-400 text-lg">Real-time Metrics</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-slate-300">Requests per Second</span>
                <span className="text-cyan-400 font-bold">{METRICS.requestsPerSecond}</span>
              </div>
              <div className="w-full h-2 bg-slate-700 rounded-full overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-green-500 to-emerald-500"
                  style={{ width: `${(METRICS.requestsPerSecond / 100) * 100}%` }}
                />
              </div>
            </div>

            <div>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-slate-300">Avg Response Time</span>
                <span className="text-cyan-400 font-bold">{METRICS.avgResponseTime}ms</span>
              </div>
              <div className="w-full h-2 bg-slate-700 rounded-full overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-cyan-500 to-blue-500"
                  style={{ width: `${(METRICS.avgResponseTime / 200) * 100}%` }}
                />
              </div>
            </div>

            <div>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-slate-300">Error Rate</span>
                <span className="text-green-400 font-bold">{METRICS.errorRate}%</span>
              </div>
              <div className="w-full h-2 bg-slate-700 rounded-full overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-green-500 to-emerald-500"
                  style={{ width: `${METRICS.errorRate * 10}%` }}
                />
              </div>
            </div>

            <div>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-slate-300">CPU Usage</span>
                <span className="text-cyan-400 font-bold">{METRICS.cpuUsage}%</span>
              </div>
              <div className="w-full h-2 bg-slate-700 rounded-full overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-cyan-500 to-blue-500"
                  style={{ width: `${METRICS.cpuUsage}%` }}
                />
              </div>
            </div>

            <div>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-slate-300">Memory Usage</span>
                <span className="text-yellow-400 font-bold">{METRICS.memoryUsage}%</span>
              </div>
              <div className="w-full h-2 bg-slate-700 rounded-full overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-yellow-500 to-orange-500"
                  style={{ width: `${METRICS.memoryUsage}%` }}
                />
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Action Buttons */}
      <div className="flex gap-3">
        <Button
          variant="outline"
          className="flex-1 border-cyan-500/50 text-cyan-400 hover:bg-cyan-500/10"
        >
          View Logs
        </Button>
        <Button
          variant="outline"
          className="flex-1 border-cyan-500/50 text-cyan-400 hover:bg-cyan-500/10"
        >
          Download Report
        </Button>
        <Button
          variant="outline"
          className="flex-1 border-cyan-500/50 text-cyan-400 hover:bg-cyan-500/10"
        >
          Configure Alerts
        </Button>
      </div>
    </div>
  )
}
