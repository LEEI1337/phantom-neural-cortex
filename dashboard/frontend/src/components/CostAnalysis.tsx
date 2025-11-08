/**
 * CostAnalysis Component
 * Detailed cost breakdown and projections
 */

import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import {
  BarChart,
  Bar,
  LineChart,
  Line,
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
import { DollarSign, TrendingDown, AlertCircle } from 'lucide-react'
import { api } from '@/lib/api'
import type { CostMetrics } from '@/lib/types'

interface CostAnalysisProps {
  projectId?: string
}

export default function CostAnalysis({ projectId }: CostAnalysisProps) {
  const [period, setPeriod] = useState<'7d' | '30d' | '90d' | 'all'>('30d')

  const { data: costResponse, isLoading } = useQuery({
    queryKey: ['cost-metrics', projectId, period],
    queryFn: async () => {
      const result = await api.getCostMetrics({ project_id: projectId, period })
      if (!result.success) throw new Error(result.error)
      return result.data!
    },
  })

  const cost = costResponse

  if (isLoading) {
    return <div className="p-8 text-center">Loading cost data...</div>
  }

  if (!cost) {
    return <div className="p-8 text-center text-muted-foreground">No cost data available</div>
  }

  const totalCost = cost.total_cost
  const monthlyCost = cost.monthly_projection
  const savings = cost.savings_vs_all_claude

  return (
    <div className="space-y-6">
      {/* Period Selector */}
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold">Cost Analysis</h2>
        <div className="flex gap-2">
          {(['7d', '30d', '90d', 'all'] as const).map((p) => (
            <button
              key={p}
              onClick={() => setPeriod(p)}
              className={`px-4 py-2 rounded-lg text-sm font-medium ${
                period === p
                  ? 'bg-primary text-primary-foreground'
                  : 'bg-secondary text-secondary-foreground hover:bg-secondary/80'
              }`}
            >
              {p === 'all' ? 'All Time' : p.toUpperCase()}
            </button>
          ))}
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <CostCard
          title="Total Cost"
          value={`$${totalCost.toFixed(2)}`}
          subtitle={`${period === 'all' ? 'All time' : `Last ${period}`}`}
          icon={<DollarSign />}
          color="blue"
        />
        <CostCard
          title="Monthly Projection"
          value={`$${monthlyCost.toFixed(2)}`}
          subtitle="Based on current usage"
          icon={<TrendingDown />}
          color="green"
        />
        <CostCard
          title="Avg Cost per Task"
          value={`$${cost.avg_cost_per_task.toFixed(3)}`}
          subtitle="All agents combined"
          icon={<DollarSign />}
          color="purple"
        />
        <CostCard
          title="Savings vs Claude-Only"
          value={`$${savings.toFixed(2)}`}
          subtitle={`${((savings / (totalCost + savings)) * 100).toFixed(0)}% reduction`}
          icon={<TrendingDown />}
          color="green"
          highlight
        />
      </div>

      {/* Cost Breakdown */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* By Agent */}
        <ChartCard title="Cost by Agent">
          <AgentCostPieChart costByAgent={cost.cost_by_agent} />
        </ChartCard>

        {/* Comparison */}
        <ChartCard title="Cost Comparison">
          <CostComparisonChart cost={cost} />
        </ChartCard>
      </div>

      {/* Detailed Breakdown Table */}
      <div className="border rounded-lg p-6 bg-card">
        <h3 className="text-lg font-semibold mb-4">Agent Cost Breakdown</h3>
        <CostBreakdownTable costByAgent={cost.cost_by_agent} totalCost={totalCost} />
      </div>

      {/* Budget Alert */}
      {monthlyCost > 30 && (
        <div className="border-l-4 border-yellow-500 bg-yellow-50 p-4 rounded">
          <div className="flex items-center gap-2">
            <AlertCircle className="text-yellow-600" size={20} />
            <p className="text-sm text-yellow-800">
              <strong>Budget Alert:</strong> Monthly projection (${monthlyCost.toFixed(2)})
              exceeds recommended budget of $30/month. Consider increasing Gemini usage.
            </p>
          </div>
        </div>
      )}
    </div>
  )
}

function CostCard({
  title,
  value,
  subtitle,
  icon,
  color,
  highlight = false,
}: {
  title: string
  value: string
  subtitle: string
  icon: React.ReactNode
  color: 'blue' | 'green' | 'purple'
  highlight?: boolean
}) {
  const colorClasses = {
    blue: 'text-blue-600 bg-blue-50',
    green: 'text-green-600 bg-green-50',
    purple: 'text-purple-600 bg-purple-50',
  }

  return (
    <div className={`border rounded-lg p-6 bg-card ${highlight ? 'ring-2 ring-green-500' : ''}`}>
      <div className="flex items-center justify-between mb-3">
        <span className="text-sm text-muted-foreground">{title}</span>
        <div className={`p-2 rounded-lg ${colorClasses[color]}`}>{icon}</div>
      </div>
      <div className="text-2xl font-bold mb-1">{value}</div>
      <div className="text-sm text-muted-foreground">{subtitle}</div>
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

function AgentCostPieChart({
  costByAgent,
}: {
  costByAgent: { gemini: number; claude: number; copilot: number }
}) {
  const data = [
    { name: 'Gemini (Free)', value: costByAgent.gemini || 0.01, color: '#10b981' },
    { name: 'Claude', value: costByAgent.claude || 0.01, color: '#3b82f6' },
    { name: 'Copilot', value: costByAgent.copilot || 0.01, color: '#8b5cf6' },
  ]

  return (
    <ResponsiveContainer width="100%" height={300}>
      <PieChart>
        <Pie
          data={data}
          cx="50%"
          cy="50%"
          labelLine={false}
          label={({ name, value, percent }) =>
            `${name}: $${value.toFixed(2)} (${(percent * 100).toFixed(0)}%)`
          }
          outerRadius={80}
          fill="#8884d8"
          dataKey="value"
        >
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={entry.color} />
          ))}
        </Pie>
        <Tooltip formatter={(value: number) => `$${value.toFixed(2)}`} />
      </PieChart>
    </ResponsiveContainer>
  )
}

function CostComparisonChart({ cost }: { cost: CostMetrics }) {
  const data = [
    {
      scenario: 'All Claude',
      cost: cost.total_cost + cost.savings_vs_all_claude,
    },
    {
      scenario: 'Smart Routing',
      cost: cost.total_cost,
    },
  ]

  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="scenario" />
        <YAxis />
        <Tooltip formatter={(value: number) => `$${value.toFixed(2)}`} />
        <Legend />
        <Bar dataKey="cost" fill="#3b82f6" name="Total Cost ($)" />
      </BarChart>
    </ResponsiveContainer>
  )
}

function CostBreakdownTable({
  costByAgent,
  totalCost,
}: {
  costByAgent: { gemini: number; claude: number; copilot: number }
  totalCost: number
}) {
  const agents = [
    { name: 'Gemini', cost: costByAgent.gemini, tier: 'FREE (1000 req/day)' },
    { name: 'Claude', cost: costByAgent.claude, tier: '$20/month Pro' },
    { name: 'Copilot', cost: costByAgent.copilot, tier: '$10/month' },
  ]

  return (
    <table className="w-full">
      <thead>
        <tr className="border-b text-left">
          <th className="pb-3 font-medium">Agent</th>
          <th className="pb-3 font-medium">Tier</th>
          <th className="pb-3 font-medium text-right">Cost</th>
          <th className="pb-3 font-medium text-right">Percentage</th>
        </tr>
      </thead>
      <tbody>
        {agents.map((agent) => {
          const percentage = totalCost > 0 ? (agent.cost / totalCost) * 100 : 0
          return (
            <tr key={agent.name} className="border-b last:border-0">
              <td className="py-3 font-medium">{agent.name}</td>
              <td className="py-3 text-sm text-muted-foreground">{agent.tier}</td>
              <td className="py-3 text-right font-medium">${agent.cost.toFixed(2)}</td>
              <td className="py-3 text-right text-sm text-muted-foreground">
                {percentage.toFixed(1)}%
              </td>
            </tr>
          )
        })}
        <tr className="font-bold">
          <td className="pt-3" colSpan={2}>
            Total
          </td>
          <td className="pt-3 text-right">${totalCost.toFixed(2)}</td>
          <td className="pt-3 text-right">100%</td>
        </tr>
      </tbody>
    </table>
  )
}
