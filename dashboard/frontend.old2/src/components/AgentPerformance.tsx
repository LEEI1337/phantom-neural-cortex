/**
 * AgentPerformance Component
 * Comparative analysis of AI agent performance
 */

import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import {
  BarChart,
  Bar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Cell,
} from 'recharts'
import { api } from '@/lib/api'
import type { AgentPerformanceData } from '@/lib/types'

interface AgentPerformanceProps {
  projectId?: string
}

export default function AgentPerformance({ projectId }: AgentPerformanceProps) {
  const [period, setPeriod] = useState<'7d' | '30d' | '90d' | 'all'>('30d')

  const { data: agentsResponse, isLoading } = useQuery({
    queryKey: ['agent-performance', projectId, period],
    queryFn: async () => {
      const result = await api.getAgentPerformance({ project_id: projectId, period })
      if (!result.success) throw new Error(result.error)
      return result.data!
    },
  })

  const agents = agentsResponse || []

  if (isLoading) {
    return <div className="p-8 text-center">Loading agent performance...</div>
  }

  // Find best performer in each category
  const bestQuality = agents.reduce((best, agent) =>
    agent.avg_quality > (best?.avg_quality || 0) ? agent : best
  , agents[0])

  const bestCost = agents.reduce((best, agent) =>
    agent.avg_cost < (best?.avg_cost || Infinity) ? agent : best
  , agents[0])

  const bestSpeed = agents.reduce((best, agent) =>
    agent.avg_time < (best?.avg_time || Infinity) ? agent : best
  , agents[0])

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold">Agent Performance</h2>
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

      {/* Best Performers */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <BestPerformerCard
          title="Best Quality"
          agent={bestQuality}
          metric="avg_quality"
          format={(v) => `${(v * 100).toFixed(0)}%`}
        />
        <BestPerformerCard
          title="Most Cost-Effective"
          agent={bestCost}
          metric="avg_cost"
          format={(v) => `$${v.toFixed(3)}`}
        />
        <BestPerformerCard
          title="Fastest"
          agent={bestSpeed}
          metric="avg_time"
          format={(v) => `${(v / 60).toFixed(1)} min`}
        />
      </div>

      {/* Comparison Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Quality Comparison */}
        <ChartCard title="Quality Comparison">
          <QualityComparisonChart agents={agents} />
        </ChartCard>

        {/* Cost vs Quality */}
        <ChartCard title="Cost vs Quality">
          <CostQualityChart agents={agents} />
        </ChartCard>
      </div>

      {/* Radar Chart - Overall Comparison */}
      <div className="border rounded-lg p-6 bg-card">
        <h3 className="text-lg font-semibold mb-4">Overall Comparison</h3>
        <ResponsiveContainer width="100%" height={400}>
          <RadarChart data={prepareRadarData(agents)}>
            <PolarGrid />
            <PolarAngleAxis dataKey="metric" />
            <PolarRadiusAxis domain={[0, 100]} />
            <Radar
              name="Gemini"
              dataKey="gemini"
              stroke="#10b981"
              fill="#10b981"
              fillOpacity={0.3}
            />
            <Radar
              name="Claude"
              dataKey="claude"
              stroke="#3b82f6"
              fill="#3b82f6"
              fillOpacity={0.3}
            />
            <Radar
              name="Copilot"
              dataKey="copilot"
              stroke="#8b5cf6"
              fill="#8b5cf6"
              fillOpacity={0.3}
            />
            <Legend />
            <Tooltip />
          </RadarChart>
        </ResponsiveContainer>
      </div>

      {/* Detailed Table */}
      <div className="border rounded-lg p-6 bg-card">
        <h3 className="text-lg font-semibold mb-4">Detailed Metrics</h3>
        <AgentComparisonTable agents={agents} />
      </div>
    </div>
  )
}

function BestPerformerCard({
  title,
  agent,
  metric,
  format,
}: {
  title: string
  agent: AgentPerformanceData
  metric: keyof AgentPerformanceData
  format: (value: number) => string
}) {
  const agentIcons = {
    gemini: '🟢',
    claude: '🔵',
    copilot: '🟣',
  }

  return (
    <div className="border rounded-lg p-6 bg-card">
      <div className="text-sm text-muted-foreground mb-2">{title}</div>
      <div className="flex items-center gap-3 mb-3">
        <span className="text-3xl">{agentIcons[agent.agent]}</span>
        <div>
          <div className="text-lg font-bold capitalize">{agent.agent}</div>
          <div className="text-2xl font-bold text-primary">
            {format(agent[metric] as number)}
          </div>
        </div>
      </div>
      <div className="text-sm text-muted-foreground">
        {agent.total_tasks} tasks • {(agent.success_rate * 100).toFixed(0)}% success
      </div>
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

function QualityComparisonChart({ agents }: { agents: AgentPerformanceData[] }) {
  const COLORS = ['#10b981', '#3b82f6', '#8b5cf6']

  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={agents}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="agent" tickFormatter={(v) => v.charAt(0).toUpperCase() + v.slice(1)} />
        <YAxis domain={[0, 1]} tickFormatter={(v) => `${(v * 100).toFixed(0)}%`} />
        <Tooltip
          formatter={(value: number) => `${(value * 100).toFixed(1)}%`}
          labelFormatter={(label) => label.charAt(0).toUpperCase() + label.slice(1)}
        />
        <Legend />
        <Bar dataKey="avg_quality" name="Average Quality">
          {agents.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  )
}

function CostQualityChart({ agents }: { agents: AgentPerformanceData[] }) {
  const COLORS = ['#10b981', '#3b82f6', '#8b5cf6']

  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={agents}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="agent" tickFormatter={(v) => v.charAt(0).toUpperCase() + v.slice(1)} />
        <YAxis />
        <Tooltip
          formatter={(value: number, name: string) =>
            name === 'avg_cost' ? `$${value.toFixed(3)}` : `${(value * 100).toFixed(0)}%`
          }
          labelFormatter={(label) => label.charAt(0).toUpperCase() + label.slice(1)}
        />
        <Legend />
        <Bar dataKey="avg_cost" name="Avg Cost ($)">
          {agents.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  )
}

function prepareRadarData(agents: AgentPerformanceData[]) {
  const byAgent = agents.reduce((acc, agent) => {
    acc[agent.agent] = agent
    return acc
  }, {} as Record<string, AgentPerformanceData>)

  // Normalize metrics to 0-100 scale
  return [
    {
      metric: 'Quality',
      gemini: (byAgent.gemini?.avg_quality || 0) * 100,
      claude: (byAgent.claude?.avg_quality || 0) * 100,
      copilot: (byAgent.copilot?.avg_quality || 0) * 100,
    },
    {
      metric: 'Success Rate',
      gemini: (byAgent.gemini?.success_rate || 0) * 100,
      claude: (byAgent.claude?.success_rate || 0) * 100,
      copilot: (byAgent.copilot?.success_rate || 0) * 100,
    },
    {
      metric: 'Cost Efficiency',
      gemini: 100, // Free = best
      claude: Math.max(0, 100 - (byAgent.claude?.avg_cost || 0) * 200),
      copilot: Math.max(0, 100 - (byAgent.copilot?.avg_cost || 0) * 500),
    },
    {
      metric: 'Speed',
      gemini: Math.max(0, 100 - ((byAgent.gemini?.avg_time || 0) / 1800) * 100),
      claude: Math.max(0, 100 - ((byAgent.claude?.avg_time || 0) / 1800) * 100),
      copilot: Math.max(0, 100 - ((byAgent.copilot?.avg_time || 0) / 1800) * 100),
    },
  ]
}

function AgentComparisonTable({ agents }: { agents: AgentPerformanceData[] }) {
  return (
    <table className="w-full">
      <thead>
        <tr className="border-b text-left">
          <th className="pb-3 font-medium">Agent</th>
          <th className="pb-3 font-medium text-right">Tasks</th>
          <th className="pb-3 font-medium text-right">Success Rate</th>
          <th className="pb-3 font-medium text-right">Avg Quality</th>
          <th className="pb-3 font-medium text-right">Avg Cost</th>
          <th className="pb-3 font-medium text-right">Avg Time</th>
        </tr>
      </thead>
      <tbody>
        {agents.map((agent) => (
          <tr key={agent.agent} className="border-b last:border-0">
            <td className="py-3 font-medium capitalize">{agent.agent}</td>
            <td className="py-3 text-right">{agent.total_tasks}</td>
            <td className="py-3 text-right">{(agent.success_rate * 100).toFixed(0)}%</td>
            <td className="py-3 text-right">{(agent.avg_quality * 100).toFixed(0)}%</td>
            <td className="py-3 text-right">${agent.avg_cost.toFixed(3)}</td>
            <td className="py-3 text-right">{(agent.avg_time / 60).toFixed(1)} min</td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}
