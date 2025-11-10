/**
 * QualityTrends Component
 * Quality metrics over time with trend analysis
 */

import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Area,
  AreaChart,
} from 'recharts'
import { format, subDays } from 'date-fns'
import { api } from '@/lib/api'
import type { QualityTrendData } from '@/lib/types'

interface QualityTrendsProps {
  projectId?: string
}

export default function QualityTrends({ projectId }: QualityTrendsProps) {
  const [dateRange, setDateRange] = useState<{ start: string; end: string }>({
    start: format(subDays(new Date(), 30), 'yyyy-MM-dd'),
    end: format(new Date(), 'yyyy-MM-dd'),
  })

  const { data: trendsResponse, isLoading } = useQuery({
    queryKey: ['quality-trends', projectId, dateRange],
    queryFn: async () => {
      const result = await api.getQualityMetrics({
        project_id: projectId,
        start_date: dateRange.start,
        end_date: dateRange.end,
      })
      if (!result.success) throw new Error(result.error)
      return result.data!
    },
  })

  const trends = trendsResponse || []

  if (isLoading) {
    return <div className="p-8 text-center">Loading quality trends...</div>
  }

  // Calculate averages
  const avgQuality = trends.length > 0
    ? trends.reduce((sum, t) => sum + t.overall_quality, 0) / trends.length
    : 0

  const avgCoverage = trends.length > 0
    ? trends.reduce((sum, t) => sum + t.test_coverage, 0) / trends.length
    : 0

  const avgSecurity = trends.length > 0
    ? trends.reduce((sum, t) => sum + t.security_score, 0) / trends.length
    : 0

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold">Quality Trends</h2>
        <div className="flex gap-2">
          <button
            onClick={() =>
              setDateRange({
                start: format(subDays(new Date(), 7), 'yyyy-MM-dd'),
                end: format(new Date(), 'yyyy-MM-dd'),
              })
            }
            className="px-3 py-1 text-sm rounded bg-secondary hover:bg-secondary/80"
          >
            7 Days
          </button>
          <button
            onClick={() =>
              setDateRange({
                start: format(subDays(new Date(), 30), 'yyyy-MM-dd'),
                end: format(new Date(), 'yyyy-MM-dd'),
              })
            }
            className="px-3 py-1 text-sm rounded bg-secondary hover:bg-secondary/80"
          >
            30 Days
          </button>
          <button
            onClick={() =>
              setDateRange({
                start: format(subDays(new Date(), 90), 'yyyy-MM-dd'),
                end: format(new Date(), 'yyyy-MM-dd'),
              })
            }
            className="px-3 py-1 text-sm rounded bg-secondary hover:bg-secondary/80"
          >
            90 Days
          </button>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <StatCard
          title="Average Quality"
          value={`${(avgQuality * 100).toFixed(1)}%`}
          target={85}
          current={avgQuality * 100}
        />
        <StatCard
          title="Average Test Coverage"
          value={`${(avgCoverage * 100).toFixed(1)}%`}
          target={75}
          current={avgCoverage * 100}
        />
        <StatCard
          title="Average Security Score"
          value={`${(avgSecurity * 100).toFixed(1)}%`}
          target={90}
          current={avgSecurity * 100}
        />
      </div>

      {/* Main Quality Trend Chart */}
      <div className="border rounded-lg p-6 bg-card">
        <h3 className="text-lg font-semibold mb-4">Overall Quality Trend</h3>
        <ResponsiveContainer width="100%" height={300}>
          <AreaChart data={trends}>
            <defs>
              <linearGradient id="qualityGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.8} />
                <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis
              dataKey="date"
              tickFormatter={(value) => format(new Date(value), 'MMM dd')}
            />
            <YAxis domain={[0, 1]} tickFormatter={(value) => `${(value * 100).toFixed(0)}%`} />
            <Tooltip
              formatter={(value: number) => `${(value * 100).toFixed(1)}%`}
              labelFormatter={(label) => format(new Date(label), 'PPP')}
            />
            <Area
              type="monotone"
              dataKey="overall_quality"
              stroke="#3b82f6"
              fillOpacity={1}
              fill="url(#qualityGradient)"
              name="Overall Quality"
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>

      {/* Detailed Metrics Chart */}
      <div className="border rounded-lg p-6 bg-card">
        <h3 className="text-lg font-semibold mb-4">Detailed Metrics</h3>
        <ResponsiveContainer width="100%" height={350}>
          <LineChart data={trends}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis
              dataKey="date"
              tickFormatter={(value) => format(new Date(value), 'MMM dd')}
            />
            <YAxis domain={[0, 1]} tickFormatter={(value) => `${(value * 100).toFixed(0)}%`} />
            <Tooltip
              formatter={(value: number) => `${(value * 100).toFixed(1)}%`}
              labelFormatter={(label) => format(new Date(label), 'PPP')}
            />
            <Legend />
            <Line
              type="monotone"
              dataKey="overall_quality"
              stroke="#3b82f6"
              name="Overall Quality"
              strokeWidth={2}
            />
            <Line
              type="monotone"
              dataKey="test_coverage"
              stroke="#10b981"
              name="Test Coverage"
              strokeWidth={2}
            />
            <Line
              type="monotone"
              dataKey="security_score"
              stroke="#8b5cf6"
              name="Security Score"
              strokeWidth={2}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}

function StatCard({
  title,
  value,
  target,
  current,
}: {
  title: string
  value: string
  target: number
  current: number
}) {
  const percentage = (current / target) * 100
  const status =
    percentage >= 100 ? 'excellent' : percentage >= 90 ? 'good' : percentage >= 75 ? 'fair' : 'poor'

  const statusColors = {
    excellent: 'bg-green-100 text-green-800 border-green-200',
    good: 'bg-blue-100 text-blue-800 border-blue-200',
    fair: 'bg-yellow-100 text-yellow-800 border-yellow-200',
    poor: 'bg-red-100 text-red-800 border-red-200',
  }

  return (
    <div className={`border rounded-lg p-6 ${statusColors[status]}`}>
      <div className="text-sm font-medium opacity-80 mb-2">{title}</div>
      <div className="text-3xl font-bold mb-2">{value}</div>
      <div className="flex items-center justify-between text-sm">
        <span className="opacity-80">Target: {target}%</span>
        <span className="font-medium capitalize">{status}</span>
      </div>
    </div>
  )
}
