import { useQuery } from '@tanstack/react-query'
import { Activity, Zap, CheckCircle, DollarSign } from 'lucide-react'
import { api } from '@/lib/api'
import RealTimeMonitor from '@/components/RealTimeMonitor'
import MetricsVisualization from '@/components/MetricsVisualization'

export default function Dashboard() {
  const { data: statsResponse, isLoading } = useQuery({
    queryKey: ['dashboard-stats'],
    queryFn: async () => {
      const result = await api.getDashboardStats()
      if (!result.success) throw new Error(result.error)
      return result.data!
    },
    refetchInterval: 30000, // Refresh every 30s
  })

  const stats = statsResponse

  if (isLoading) {
    return <div className="text-center py-12">Loading dashboard...</div>
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold bg-gradient-to-r from-neon-cyan via-neon-purple to-neon-pink bg-clip-text text-transparent">
          Dashboard
        </h1>
        <p className="text-neon-cyan/70 mt-1 font-mono">Real-time overview of your AI development orchestration</p>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Total Projects"
          value={stats?.total_projects || 0}
          icon={<Activity />}
          color="blue"
        />
        <StatCard
          title="Active Tasks"
          value={stats?.active_tasks || 0}
          icon={<Zap />}
          color="yellow"
        />
        <StatCard
          title="Completed Today"
          value={stats?.completed_today || 0}
          icon={<CheckCircle />}
          color="green"
        />
        <StatCard
          title="Cost Today"
          value={`$${(stats?.total_cost_today || 0).toFixed(2)}`}
          icon={<DollarSign />}
          color="purple"
        />
      </div>

      {/* Real-Time Monitor */}
      <RealTimeMonitor />

      {/* Performance Overview */}
      <MetricsVisualization />
    </div>
  )
}

function StatCard({
  title,
  value,
  icon,
  color,
}: {
  title: string
  value: string | number
  icon: React.ReactNode
  color: 'blue' | 'yellow' | 'green' | 'purple'
}) {
  const colorClasses = {
    blue: 'bg-neon-cyan/10 text-neon-cyan border-neon-cyan/30 shadow-neon-cyan',
    yellow: 'bg-neon-yellow/10 text-neon-yellow border-neon-yellow/30',
    green: 'bg-neon-green/10 text-neon-green border-neon-green/30',
    purple: 'bg-neon-purple/10 text-neon-purple border-neon-purple/30 shadow-neon-purple',
  }

  return (
    <div className="border border-primary/20 rounded-lg p-6 bg-card/60 backdrop-blur-md shadow-cyber-card hover:shadow-neon-cyan transition-all duration-300 hover:border-primary/40 group">
      <div className="flex items-center justify-between mb-4">
        <span className="text-sm text-muted-foreground font-mono">{title}</span>
        <div className={`p-2 rounded-lg border transition-all duration-300 group-hover:scale-110 ${colorClasses[color]}`}>{icon}</div>
      </div>
      <div className="text-3xl font-bold text-foreground">{value}</div>
    </div>
  )
}
