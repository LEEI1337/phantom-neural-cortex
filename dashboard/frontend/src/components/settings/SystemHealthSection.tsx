import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Trash2, RefreshCw } from 'lucide-react'
import { api } from '@/lib/api'

export function SystemHealthSection() {
  const queryClient = useQueryClient()

  const { data: healthResponse } = useQuery({
    queryKey: ['system-health'],
    queryFn: async () => {
      const result = await api.getSystemHealth()
      if (!result.success) throw new Error(result.error)
      return result.data!
    },
    refetchInterval: 10000,
  })

  const { data: cacheStatsResponse } = useQuery({
    queryKey: ['cache-stats'],
    queryFn: async () => {
      const result = await api.getCacheStatistics()
      if (!result.success) throw new Error(result.error)
      return result.data!
    },
  })

  const clearCacheMutation = useMutation({
    mutationFn: async (layer?: 'guideline' | 'github' | 'quality') => {
      const result = await api.clearCache(layer)
      if (!result.success) throw new Error(result.error)
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['cache-stats'] })
    },
  })

  const health = healthResponse
  const cacheStats = cacheStatsResponse

  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-3xl font-bold">System & Cache</h2>
        <p className="text-muted-foreground mt-1">Monitor system health and manage caches</p>
      </div>

      {/* System Health */}
      <div className="border rounded-lg p-6 bg-card">
        <h3 className="text-xl font-semibold mb-4">System Health</h3>
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-muted-foreground">Status</span>
            <span
              className={`px-3 py-1 rounded-full text-sm font-medium ${
                health?.status === 'healthy'
                  ? 'bg-green-100 text-green-800'
                  : health?.status === 'degraded'
                  ? 'bg-yellow-100 text-yellow-800'
                  : 'bg-red-100 text-red-800'
              }`}
            >
              {health?.status?.toUpperCase() || 'UNKNOWN'}
            </span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-muted-foreground">Uptime</span>
            <span className="font-medium">
              {health ? formatUptime(health.uptime_seconds) : 'N/A'}
            </span>
          </div>
        </div>

        {health?.components && (
          <div className="mt-6">
            <h4 className="font-medium mb-3">Components</h4>
            <div className="space-y-2">
              {Object.entries(health.components).map(([name, status]) => (
                <div key={name} className="flex items-center justify-between">
                  <span className="text-sm">{name}</span>
                  <div
                    className={`w-3 h-3 rounded-full ${
                      status ? 'bg-green-500' : 'bg-red-500'
                    }`}
                  />
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Cache Management */}
      <div className="border rounded-lg p-6 bg-card">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-xl font-semibold">Cache Management</h3>
          <button
            onClick={() => clearCacheMutation.mutate()}
            disabled={clearCacheMutation.isPending}
            className="flex items-center gap-2 px-4 py-2 bg-destructive text-destructive-foreground rounded-lg hover:opacity-90 disabled:opacity-50"
          >
            <Trash2 size={16} />
            Clear All Caches
          </button>
        </div>

        {cacheStats && (
          <div className="space-y-4">
            <CacheLayerCard
              name="Guideline Cache"
              stats={cacheStats.guideline_cache}
              onClear={() => clearCacheMutation.mutate('guideline')}
            />
            <CacheLayerCard
              name="GitHub API Cache"
              stats={cacheStats.github_cache}
              onClear={() => clearCacheMutation.mutate('github')}
            />
            <CacheLayerCard
              name="Quality Pattern Cache"
              stats={cacheStats.quality_pattern_cache}
              onClear={() => clearCacheMutation.mutate('quality')}
            />
          </div>
        )}
      </div>
    </div>
  )
}

function CacheLayerCard({
  name,
  stats,
  onClear,
}: {
  name: string
  stats: any
  onClear: () => void
}) {
  const hitRate = stats?.hit_rate ? (stats.hit_rate * 100).toFixed(1) : '0.0'

  return (
    <div className="border rounded-lg p-4 bg-muted/30">
      <div className="flex items-center justify-between mb-3">
        <h4 className="font-medium">{name}</h4>
        <button
          onClick={onClear}
          className="text-sm text-destructive hover:underline flex items-center gap-1"
        >
          <RefreshCw size={14} />
          Clear
        </button>
      </div>
      <div className="grid grid-cols-4 gap-4 text-sm">
        <div>
          <div className="text-muted-foreground">Size</div>
          <div className="font-medium">{stats?.size || 0}</div>
        </div>
        <div>
          <div className="text-muted-foreground">Hits</div>
          <div className="font-medium">{stats?.hits || 0}</div>
        </div>
        <div>
          <div className="text-muted-foreground">Misses</div>
          <div className="font-medium">{stats?.misses || 0}</div>
        </div>
        <div>
          <div className="text-muted-foreground">Hit Rate</div>
          <div className="font-medium">{hitRate}%</div>
        </div>
      </div>
    </div>
  )
}

function formatUptime(seconds: number): string {
  const days = Math.floor(seconds / 86400)
  const hours = Math.floor((seconds % 86400) / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)

  if (days > 0) return `${days}d ${hours}h`
  if (hours > 0) return `${hours}h ${minutes}m`
  return `${minutes}m`
}
