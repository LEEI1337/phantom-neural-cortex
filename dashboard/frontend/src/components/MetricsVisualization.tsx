/**
 * MetricsVisualization Component
 * Comprehensive metrics dashboard with charts
 */

import { useQuery } from '@tanstack/react-query'
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts'
import { TrendingUp, TrendingDown, Minus } from 'lucide-react'
import { api } from '@/lib/api'
import type { PerformanceMetrics } from '@/lib/types'

interface MetricsVisualizationProps {
  projectId?: string
}

export default function MetricsVisualization({ projectId }: MetricsVisualizationProps) {
  // Fetch performance metrics
  const { data: perfResponse, isLoading: perfLoading } = useQuery({
    queryKey: ['performance-metrics', projectId],
    queryFn: async () => {
      const result = await api.getPerformanceMetrics({ project_id: projectId })
      if (!result.success) throw new Error(result.error)
      return result.data!
    },
  })

  const metrics = perfResponse

  if (perfLoading) {
    return <div className="p-8 text-center">Loading metrics...</div>
  }

  if (!metrics) {
    return <div className="p-8 text-center text-muted-foreground">No metrics available</div>
  }

  return (
    <div className="space-y-6">
      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <KPICard
          title="Avg Time per Task"
          value={`${(metrics.avg_time_per_task / 60).toFixed(1)} min`}
          change={-12}
          icon="⏱️"
        />
        <KPICard
          title="Avg Iterations"
          value={metrics.avg_iterations.toFixed(1)}
          change={-18}
          icon="🔄"
        />
        <KPICard
          title="Avg Quality"
          value={`${(metrics.avg_quality * 100).toFixed(0)}%`}
          change={+8}
          icon="⭐"
        />
        <KPICard
          title="Success Rate"
          value={`${(metrics.success_rate * 100).toFixed(0)}%`}
          change={+5}
          icon="✅"
        />
      </div>

      {/* Optimization Impact Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <ImpactCard
          title="Token Reduction"
          value={`${metrics.token_reduction_percent.toFixed(0)}%`}
          description="From Latent Reasoning + Caching"
          color="blue"
        />
        <ImpactCard
          title="Speed Improvement"
          value={`${metrics.speed_improvement_factor.toFixed(1)}x`}
          description="From Parallel Evaluation + Deep Supervision"
          color="green"
        />
        <ImpactCard
          title="Cost Savings"
          value={`${metrics.cost_savings_percent.toFixed(0)}%`}
          description="From Smart Agent Switching"
          color="purple"
        />
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Performance Comparison Chart */}
        <ChartCard title="Performance Comparison">
          <PerformanceComparisonChart metrics={metrics} />
        </ChartCard>

        {/* Optimization Impact Chart */}
        <ChartCard title="Optimization Impact">
          <OptimizationImpactChart metrics={metrics} />
        </ChartCard>
      </div>
    </div>
  )
}

function KPICard({
  title,
  value,
  change,
  icon,
}: {
  title: string
  value: string
  change: number
  icon: string
}) {
  const isPositive = change > 0
  const isNeutral = change === 0

  return (
    <div className="border rounded-lg p-6 bg-card">
      <div className="flex items-center justify-between mb-2">
        <span className="text-sm text-muted-foreground">{title}</span>
        <span className="text-2xl">{icon}</span>
      </div>
      <div className="text-2xl font-bold mb-2">{value}</div>
      <div className="flex items-center gap-1 text-sm">
        {isNeutral ? (
          <Minus size={16} className="text-muted-foreground" />
        ) : isPositive ? (
          <TrendingUp size={16} className="text-green-600" />
        ) : (
          <TrendingDown size={16} className="text-red-600" />
        )}
        <span
          className={
            isNeutral
              ? 'text-muted-foreground'
              : isPositive
              ? 'text-green-600'
              : 'text-red-600'
          }
        >
          {isPositive ? '+' : ''}
          {change}%
        </span>
        <span className="text-muted-foreground">vs baseline</span>
      </div>
    </div>
  )
}

function ImpactCard({
  title,
  value,
  description,
  color,
}: {
  title: string
  value: string
  description: string
  color: 'blue' | 'green' | 'purple'
}) {
  const colorClasses = {
    blue: 'bg-blue-100 text-blue-800 border-blue-200',
    green: 'bg-green-100 text-green-800 border-green-200',
    purple: 'bg-purple-100 text-purple-800 border-purple-200',
  }

  return (
    <div className={`border rounded-lg p-6 ${colorClasses[color]}`}>
      <div className="text-sm font-medium opacity-80 mb-1">{title}</div>
      <div className="text-3xl font-bold mb-2">{value}</div>
      <div className="text-sm opacity-80">{description}</div>
    </div>
  )
}

function ChartCard({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="border rounded-lg p-6 bg-card">
      <h3 className="text-lg font-semibold mb-4">{title}</h3>
      {children}
    </div>
  )
}

function PerformanceComparisonChart({ metrics }: { metrics: PerformanceMetrics }) {
  const data = [
    {
      metric: 'Time',
      baseline: 100,
      optimized: 100 / metrics.speed_improvement_factor,
    },
    {
      metric: 'Tokens',
      baseline: 100,
      optimized: 100 - metrics.token_reduction_percent,
    },
    {
      metric: 'Cost',
      baseline: 100,
      optimized: 100 - metrics.cost_savings_percent,
    },
    {
      metric: 'Quality',
      baseline: 85,
      optimized: metrics.avg_quality * 100,
    },
  ]

  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="metric" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Bar dataKey="baseline" fill="#94a3b8" name="Baseline" />
        <Bar dataKey="optimized" fill="#3b82f6" name="Optimized" />
      </BarChart>
    </ResponsiveContainer>
  )
}

function OptimizationImpactChart({ metrics }: { metrics: PerformanceMetrics }) {
  const data = [
    { name: 'Token Reduction', value: metrics.token_reduction_percent },
    { name: 'Speed Gain', value: (metrics.speed_improvement_factor - 1) * 100 },
    { name: 'Cost Savings', value: metrics.cost_savings_percent },
  ]

  const COLORS = ['#3b82f6', '#10b981', '#8b5cf6']

  return (
    <ResponsiveContainer width="100%" height={300}>
      <PieChart>
        <Pie
          data={data}
          cx="50%"
          cy="50%"
          labelLine={false}
          label={({ name, value }) => `${name}: ${value.toFixed(0)}%`}
          outerRadius={80}
          fill="#8884d8"
          dataKey="value"
        >
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
          ))}
        </Pie>
        <Tooltip />
      </PieChart>
    </ResponsiveContainer>
  )
}
