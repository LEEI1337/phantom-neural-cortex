import React, { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card'
import { Button } from '../ui/button'
import { Switch } from '../ui/switch'

export interface AgentConfigPanelProps {
  projectId?: string
}

interface AgentConfig {
  id: string
  name: string
  icon: string
  provider: string
  model: string
  status: 'active' | 'idle' | 'disabled'
  apiKey: {
    value: string
    valid: boolean
  }
  rateLimit: {
    requestsPerMinute: number
    currentUsage: number
  }
  specializations: {
    name: string
    strength: number
  }[]
  routingRules: {
    qualityThreshold: boolean
    complexityThreshold: boolean
    securityCritical: boolean
    costCeilingExceeded: boolean
  }
  fallbackAgent: string
  performance: {
    tasksCompleted: number
    successRate: number
    avgQuality: number
    avgCost: number
    avgDuration: number
  }
}

const MOCK_AGENTS: AgentConfig[] = [
  {
    id: 'claude',
    name: 'Claude',
    icon: '⚡',
    provider: 'Anthropic',
    model: 'claude-sonnet-4-5',
    status: 'active',
    apiKey: { value: 'sk-ant-***************abc', valid: true },
    rateLimit: { requestsPerMinute: 1000, currentUsage: 142 },
    specializations: [
      { name: 'Complex Reasoning', strength: 95 },
      { name: 'Code Quality', strength: 92 },
      { name: 'Documentation', strength: 90 },
      { name: 'Speed', strength: 65 },
      { name: 'Cost Efficiency', strength: 40 }
    ],
    routingRules: {
      qualityThreshold: true,
      complexityThreshold: true,
      securityCritical: true,
      costCeilingExceeded: false
    },
    fallbackAgent: 'gemini',
    performance: {
      tasksCompleted: 342,
      successRate: 96.5,
      avgQuality: 94,
      avgCost: 3.20,
      avgDuration: 285
    }
  },
  {
    id: 'gemini',
    name: 'Gemini',
    icon: '💎',
    provider: 'Google',
    model: 'gemini-2.0-flash-exp',
    status: 'active',
    apiKey: { value: 'FREE', valid: true },
    rateLimit: { requestsPerMinute: 500, currentUsage: 89 },
    specializations: [
      { name: 'Cost Efficiency', strength: 100 },
      { name: 'Speed', strength: 88 },
      { name: 'Code Generation', strength: 85 },
      { name: 'Complex Reasoning', strength: 72 },
      { name: 'Documentation', strength: 70 }
    ],
    routingRules: {
      qualityThreshold: false,
      complexityThreshold: false,
      securityCritical: false,
      costCeilingExceeded: true
    },
    fallbackAgent: 'claude',
    performance: {
      tasksCompleted: 498,
      successRate: 89.2,
      avgQuality: 82,
      avgCost: 0.00,
      avgDuration: 198
    }
  },
  {
    id: 'copilot',
    name: 'Copilot',
    icon: '🚀',
    provider: 'GitHub',
    model: 'gpt-4',
    status: 'idle',
    apiKey: { value: 'Not configured', valid: false },
    rateLimit: { requestsPerMinute: 800, currentUsage: 0 },
    specializations: [
      { name: 'Code Generation', strength: 92 },
      { name: 'GitHub Integration', strength: 95 },
      { name: 'Speed', strength: 75 },
      { name: 'Cost Efficiency', strength: 60 },
      { name: 'Complex Reasoning', strength: 78 }
    ],
    routingRules: {
      qualityThreshold: false,
      complexityThreshold: false,
      securityCritical: false,
      costCeilingExceeded: false
    },
    fallbackAgent: 'claude',
    performance: {
      tasksCompleted: 0,
      successRate: 0,
      avgQuality: 0,
      avgCost: 0,
      avgDuration: 0
    }
  },
  {
    id: 'cursor',
    name: 'Cursor',
    icon: '📐',
    provider: 'Cursor',
    model: 'cursor-small',
    status: 'idle',
    apiKey: { value: 'Not configured', valid: false },
    rateLimit: { requestsPerMinute: 600, currentUsage: 0 },
    specializations: [
      { name: 'IDE Integration', strength: 98 },
      { name: 'Code Generation', strength: 88 },
      { name: 'Refactoring', strength: 90 },
      { name: 'Speed', strength: 82 },
      { name: 'Cost Efficiency', strength: 70 }
    ],
    routingRules: {
      qualityThreshold: false,
      complexityThreshold: false,
      securityCritical: false,
      costCeilingExceeded: false
    },
    fallbackAgent: 'claude',
    performance: {
      tasksCompleted: 0,
      successRate: 0,
      avgQuality: 0,
      avgCost: 0,
      avgDuration: 0
    }
  },
  {
    id: 'windsurf',
    name: 'Windsurf',
    icon: '🌊',
    provider: 'Codeium',
    model: 'windsurf-cascade',
    status: 'idle',
    apiKey: { value: 'Not configured', valid: false },
    rateLimit: { requestsPerMinute: 500, currentUsage: 0 },
    specializations: [
      { name: 'Multi-Modal', strength: 92 },
      { name: 'Context Awareness', strength: 94 },
      { name: 'Code Generation', strength: 86 },
      { name: 'Speed', strength: 80 },
      { name: 'Cost Efficiency', strength: 75 }
    ],
    routingRules: {
      qualityThreshold: false,
      complexityThreshold: false,
      securityCritical: false,
      costCeilingExceeded: false
    },
    fallbackAgent: 'claude',
    performance: {
      tasksCompleted: 0,
      successRate: 0,
      avgQuality: 0,
      avgCost: 0,
      avgDuration: 0
    }
  }
]

export const AgentConfigPanel: React.FC<AgentConfigPanelProps> = ({ projectId }) => {
  const [selectedAgentId, setSelectedAgentId] = useState<string>('claude')
  const [agents, setAgents] = useState<AgentConfig[]>(MOCK_AGENTS)

  const selectedAgent = agents.find((a) => a.id === selectedAgentId)

  if (!selectedAgent) {
    return <div>Agent not found</div>
  }

  const updateRoutingRule = (rule: keyof AgentConfig['routingRules'], value: boolean) => {
    setAgents(
      agents.map((a) =>
        a.id === selectedAgentId
          ? { ...a, routingRules: { ...a.routingRules, [rule]: value } }
          : a
      )
    )
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'text-green-400'
      case 'idle':
        return 'text-slate-400'
      case 'disabled':
        return 'text-red-400'
      default:
        return 'text-slate-400'
    }
  }

  const getStatusDot = (status: string) => {
    switch (status) {
      case 'active':
        return '🟢'
      case 'idle':
        return '⚪'
      case 'disabled':
        return '🔴'
      default:
        return '⚪'
    }
  }

  return (
    <div className="space-y-6">
      {/* Agent Selector */}
      <Card className="bg-gradient-to-br from-slate-900 to-slate-800 border-cyan-500/30">
        <CardHeader>
          <CardTitle className="text-cyan-400 flex items-center gap-2">
            <span className="text-2xl">🤖</span>
            Agent Configuration
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-5 gap-2">
            {agents.map((agent) => (
              <Button
                key={agent.id}
                onClick={() => setSelectedAgentId(agent.id)}
                variant={selectedAgentId === agent.id ? 'default' : 'outline'}
                size="sm"
                className={`${
                  selectedAgentId === agent.id
                    ? 'bg-cyan-500 text-slate-900'
                    : 'border-cyan-500/30 text-cyan-400'
                }`}
              >
                <span className="mr-1">{agent.icon}</span>
                {agent.name}
              </Button>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Agent Details */}
      <Card className="bg-gradient-to-br from-slate-900 to-slate-800 border-cyan-500/30">
        <CardHeader>
          <CardTitle className="text-cyan-400 flex items-center gap-2">
            <span className="text-2xl">{selectedAgent.icon}</span>
            {selectedAgent.name}
            <span className={`text-sm ml-2 ${getStatusColor(selectedAgent.status)}`}>
              {getStatusDot(selectedAgent.status)} {selectedAgent.status.charAt(0).toUpperCase() + selectedAgent.status.slice(1)}
            </span>
            <span className="text-sm text-slate-400 ml-auto">Quality Tier: Premium</span>
          </CardTitle>
        </CardHeader>
      </Card>

      {/* Performance Metrics */}
      <Card className="bg-gradient-to-br from-slate-900 to-slate-800 border-cyan-500/30">
        <CardHeader>
          <CardTitle className="text-cyan-400 text-lg">Performance Metrics</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
            <div className="p-3 bg-slate-950/50 rounded border border-cyan-500/20">
              <div className="text-xs text-slate-400 mb-1">Tasks</div>
              <div className="text-lg font-bold text-cyan-400">
                {selectedAgent.performance.tasksCompleted}
              </div>
            </div>
            <div className="p-3 bg-slate-950/50 rounded border border-cyan-500/20">
              <div className="text-xs text-slate-400 mb-1">Success Rate</div>
              <div className="text-lg font-bold text-cyan-400">
                {selectedAgent.performance.successRate.toFixed(1)}%
              </div>
            </div>
            <div className="p-3 bg-slate-950/50 rounded border border-cyan-500/20">
              <div className="text-xs text-slate-400 mb-1">Avg Quality</div>
              <div className="text-lg font-bold text-cyan-400">
                {selectedAgent.performance.avgQuality}%
              </div>
            </div>
            <div className="p-3 bg-slate-950/50 rounded border border-cyan-500/20">
              <div className="text-xs text-slate-400 mb-1">Avg Cost</div>
              <div className="text-lg font-bold text-cyan-400">
                ${selectedAgent.performance.avgCost.toFixed(2)}
              </div>
            </div>
            <div className="p-3 bg-slate-950/50 rounded border border-cyan-500/20">
              <div className="text-xs text-slate-400 mb-1">Avg Duration</div>
              <div className="text-lg font-bold text-cyan-400">
                {selectedAgent.performance.avgDuration}s
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Specializations */}
      <Card className="bg-gradient-to-br from-slate-900 to-slate-800 border-cyan-500/30">
        <CardHeader>
          <CardTitle className="text-cyan-400 text-lg">Specializations</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {selectedAgent.specializations.map((spec) => (
              <div key={spec.name}>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-slate-300">{spec.name}</span>
                  <span className={`font-bold ${spec.strength >= 90 ? 'text-green-400' : spec.strength >= 70 ? 'text-cyan-400' : 'text-yellow-400'}`}>
                    {spec.strength}%
                  </span>
                </div>
                <div className="w-full h-2 bg-slate-700 rounded-full overflow-hidden">
                  <div
                    className={`h-full ${
                      spec.strength >= 90
                        ? 'bg-gradient-to-r from-green-500 to-emerald-500'
                        : spec.strength >= 70
                        ? 'bg-gradient-to-r from-cyan-500 to-blue-500'
                        : 'bg-gradient-to-r from-yellow-500 to-orange-500'
                    }`}
                    style={{ width: `${spec.strength}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* API Configuration */}
      <Card className="bg-gradient-to-br from-slate-900 to-slate-800 border-cyan-500/30">
        <CardHeader>
          <CardTitle className="text-cyan-400 text-lg">API Configuration</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <div className="text-xs text-slate-400 mb-1">Provider</div>
                <div className="text-sm text-slate-200">{selectedAgent.provider}</div>
              </div>
              <div>
                <div className="text-xs text-slate-400 mb-1">Model</div>
                <div className="text-sm text-slate-200">{selectedAgent.model}</div>
              </div>
            </div>

            <div>
              <div className="text-xs text-slate-400 mb-1">API Key</div>
              <div className="flex items-center gap-2">
                <input
                  type="password"
                  value={selectedAgent.apiKey.value}
                  readOnly
                  className="flex-1 px-3 py-2 bg-slate-900 border border-cyan-500/30 rounded text-sm text-slate-200"
                />
                {selectedAgent.apiKey.valid ? (
                  <span className="text-green-400 text-sm">✅ Valid</span>
                ) : (
                  <span className="text-red-400 text-sm">❌ Invalid</span>
                )}
              </div>
            </div>

            <div>
              <div className="text-xs text-slate-400 mb-1">Rate Limit</div>
              <div className="text-sm text-slate-200 mb-2">
                {selectedAgent.rateLimit.requestsPerMinute}/min
              </div>
              <div className="text-xs text-slate-500 mb-1">
                Current Usage: {selectedAgent.rateLimit.currentUsage}/{selectedAgent.rateLimit.requestsPerMinute} ({((selectedAgent.rateLimit.currentUsage / selectedAgent.rateLimit.requestsPerMinute) * 100).toFixed(0)}%)
              </div>
              <div className="w-full h-2 bg-slate-700 rounded-full overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-cyan-500 to-blue-500"
                  style={{ width: `${(selectedAgent.rateLimit.currentUsage / selectedAgent.rateLimit.requestsPerMinute) * 100}%` }}
                />
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Routing Rules */}
      <Card className="bg-gradient-to-br from-slate-900 to-slate-800 border-cyan-500/30">
        <CardHeader>
          <CardTitle className="text-cyan-400 text-lg">Routing Rules</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3 mb-4">
            <div className="text-sm text-slate-400 mb-3">
              Use {selectedAgent.name} when:
            </div>

            <label className="flex items-center justify-between text-sm text-slate-300">
              <span>Quality threshold &gt; 90%</span>
              <Switch
                checked={selectedAgent.routingRules.qualityThreshold}
                onCheckedChange={(checked) => updateRoutingRule('qualityThreshold', checked)}
              />
            </label>

            <label className="flex items-center justify-between text-sm text-slate-300">
              <span>Task complexity &gt; 8.0</span>
              <Switch
                checked={selectedAgent.routingRules.complexityThreshold}
                onCheckedChange={(checked) => updateRoutingRule('complexityThreshold', checked)}
              />
            </label>

            <label className="flex items-center justify-between text-sm text-slate-300">
              <span>Security critical = true</span>
              <Switch
                checked={selectedAgent.routingRules.securityCritical}
                onCheckedChange={(checked) => updateRoutingRule('securityCritical', checked)}
              />
            </label>

            <label className="flex items-center justify-between text-sm text-slate-300">
              <span>Cost ceiling exceeded</span>
              <Switch
                checked={selectedAgent.routingRules.costCeilingExceeded}
                onCheckedChange={(checked) => updateRoutingRule('costCeilingExceeded', checked)}
              />
            </label>
          </div>

          <div className="pt-3 border-t border-cyan-500/20">
            <div className="text-xs text-slate-400 mb-2">Fallback Agent</div>
            <select
              value={selectedAgent.fallbackAgent}
              onChange={(e) => {
                setAgents(
                  agents.map((a) =>
                    a.id === selectedAgentId ? { ...a, fallbackAgent: e.target.value } : a
                  )
                )
              }}
              className="w-full p-2 bg-slate-900 border border-cyan-500/30 rounded text-sm text-slate-200"
            >
              {agents
                .filter((a) => a.id !== selectedAgentId)
                .map((a) => (
                  <option key={a.id} value={a.id}>
                    {a.icon} {a.name}
                  </option>
                ))}
            </select>
          </div>
        </CardContent>
      </Card>

      {/* Action Buttons */}
      <div className="flex gap-3">
        <Button
          variant="outline"
          className="flex-1 border-cyan-500/50 text-cyan-400 hover:bg-cyan-500/10"
        >
          Edit Routing
        </Button>
        <Button
          variant="outline"
          className="flex-1 border-cyan-500/50 text-cyan-400 hover:bg-cyan-500/10"
        >
          Test Connection
        </Button>
        <Button
          variant="outline"
          className="flex-1 border-cyan-500/50 text-cyan-400 hover:bg-cyan-500/10"
        >
          View Logs
        </Button>
      </div>
    </div>
  )
}
