/**
 * AgentTierConfiguration Component
 * Configure individual agent pricing tiers for accurate cost statistics
 */

import { useState } from 'react'
import { DollarSign, Zap, Save, Plus, Trash2 } from 'lucide-react'

interface AgentTier {
  id: string
  name: string
  icon: string
  tierType: 'free' | 'monthly' | 'pay-per-use'
  monthlyCost?: number
  rateLimit?: number
  rateLimitPeriod?: string
  costPerToken?: number
  enabled: boolean
}

const DEFAULT_AGENTS: AgentTier[] = [
  {
    id: 'gemini',
    name: 'Google Gemini',
    icon: '✨',
    tierType: 'free',
    rateLimit: 1000,
    rateLimitPeriod: 'day',
    enabled: true,
  },
  {
    id: 'claude',
    name: 'Anthropic Claude',
    icon: '🧠',
    tierType: 'monthly',
    monthlyCost: 20,
    enabled: true,
  },
  {
    id: 'copilot',
    name: 'GitHub Copilot',
    icon: '🤖',
    tierType: 'monthly',
    monthlyCost: 10,
    enabled: true,
  },
  {
    id: 'openai',
    name: 'OpenAI GPT',
    icon: '🔮',
    tierType: 'pay-per-use',
    costPerToken: 0.00002,
    enabled: true,
  },
  {
    id: 'cohere',
    name: 'Cohere',
    icon: '🔷',
    tierType: 'pay-per-use',
    costPerToken: 0.00001,
    enabled: false,
  },
  {
    id: 'mistral',
    name: 'Mistral AI',
    icon: '🌊',
    tierType: 'pay-per-use',
    costPerToken: 0.000015,
    enabled: false,
  },
  {
    id: 'ollama',
    name: 'Ollama (Local)',
    icon: '🦙',
    tierType: 'free',
    rateLimit: 999999,
    rateLimitPeriod: 'day',
    enabled: true,
  },
]

export default function AgentTierConfiguration() {
  const [agents, setAgents] = useState<AgentTier[]>(DEFAULT_AGENTS)
  const [editingAgent, setEditingAgent] = useState<string | null>(null)
  const [showAddForm, setShowAddForm] = useState(false)

  const updateAgent = (id: string, updates: Partial<AgentTier>) => {
    setAgents((prev) =>
      prev.map((agent) => (agent.id === id ? { ...agent, ...updates } : agent))
    )
  }

  const deleteAgent = (id: string) => {
    setAgents((prev) => prev.filter((agent) => agent.id !== id))
  }

  const addAgent = () => {
    const newAgent: AgentTier = {
      id: `custom-${Date.now()}`,
      name: 'Custom Agent',
      icon: '🔧',
      tierType: 'pay-per-use',
      costPerToken: 0.00001,
      enabled: true,
    }
    setAgents((prev) => [...prev, newAgent])
    setEditingAgent(newAgent.id)
    setShowAddForm(false)
  }

  const calculateMonthlyCost = (agent: AgentTier) => {
    if (agent.tierType === 'free') return 0
    if (agent.tierType === 'monthly') return agent.monthlyCost || 0
    // For pay-per-use, we can't know until usage happens
    return null
  }

  const saveConfiguration = () => {
    // TODO: Save to backend API
    alert('Agent tier configuration saved!')
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold">Agent Tier Configuration</h2>
          <p className="text-muted-foreground mt-1">
            Configure individual agent pricing tiers for accurate cost tracking
          </p>
        </div>
        <div className="flex gap-3">
          <button
            onClick={() => setShowAddForm(true)}
            className="flex items-center gap-2 px-4 py-2 bg-neon-cyan/20 text-neon-cyan border border-neon-cyan/50 rounded-lg hover:bg-neon-cyan/30 transition-all"
          >
            <Plus size={16} />
            Add Agent
          </button>
          <button
            onClick={saveConfiguration}
            className="flex items-center gap-2 px-4 py-2 bg-neon-green/20 text-neon-green border border-neon-green/50 rounded-lg hover:bg-neon-green/30 transition-all"
          >
            <Save size={16} />
            Save Configuration
          </button>
        </div>
      </div>

      {/* Agent List */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {agents.map((agent) => (
          <AgentTierCard
            key={agent.id}
            agent={agent}
            isEditing={editingAgent === agent.id}
            onEdit={() => setEditingAgent(agent.id)}
            onStopEdit={() => setEditingAgent(null)}
            onUpdate={(updates) => updateAgent(agent.id, updates)}
            onDelete={() => deleteAgent(agent.id)}
          />
        ))}
      </div>

      {/* Cost Summary */}
      <div className="border rounded-lg p-6 bg-card/60 backdrop-blur-md">
        <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
          <DollarSign className="text-neon-green" size={20} />
          Monthly Cost Summary
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="border rounded-lg p-4 bg-muted/30">
            <div className="text-sm text-muted-foreground mb-1">Total Fixed Cost</div>
            <div className="text-2xl font-bold text-neon-green">
              $
              {agents
                .filter((a) => a.enabled && a.tierType === 'monthly')
                .reduce((sum, a) => sum + (a.monthlyCost || 0), 0)
                .toFixed(2)}
              <span className="text-sm text-muted-foreground">/month</span>
            </div>
          </div>
          <div className="border rounded-lg p-4 bg-muted/30">
            <div className="text-sm text-muted-foreground mb-1">Free Agents</div>
            <div className="text-2xl font-bold text-neon-cyan">
              {agents.filter((a) => a.enabled && a.tierType === 'free').length}
            </div>
          </div>
          <div className="border rounded-lg p-4 bg-muted/30">
            <div className="text-sm text-muted-foreground mb-1">Pay-Per-Use Agents</div>
            <div className="text-2xl font-bold text-neon-purple">
              {agents.filter((a) => a.enabled && a.tierType === 'pay-per-use').length}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

function AgentTierCard({
  agent,
  isEditing,
  onEdit,
  onStopEdit,
  onUpdate,
  onDelete,
}: {
  agent: AgentTier
  isEditing: boolean
  onEdit: () => void
  onStopEdit: () => void
  onUpdate: (updates: Partial<AgentTier>) => void
  onDelete: () => void
}) {
  return (
    <div
      className={`border rounded-lg p-5 bg-card/60 backdrop-blur-md transition-all ${
        isEditing ? 'border-neon-cyan shadow-neon-cyan' : ''
      } ${!agent.enabled ? 'opacity-60' : ''}`}
    >
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <span className="text-3xl">{agent.icon}</span>
          <div>
            {isEditing ? (
              <input
                type="text"
                value={agent.name}
                onChange={(e) => onUpdate({ name: e.target.value })}
                className="px-2 py-1 bg-background border border-border rounded text-sm font-medium"
              />
            ) : (
              <h3 className="font-semibold">{agent.name}</h3>
            )}
            <div className="text-sm text-muted-foreground">ID: {agent.id}</div>
          </div>
        </div>
        <div className="flex gap-2">
          <button
            onClick={isEditing ? onStopEdit : onEdit}
            className={`px-3 py-1 rounded text-xs transition-all ${
              isEditing
                ? 'bg-neon-green/20 text-neon-green border border-neon-green/50'
                : 'bg-neon-cyan/20 text-neon-cyan border border-neon-cyan/50'
            }`}
          >
            {isEditing ? 'Done' : 'Edit'}
          </button>
          {!agent.id.startsWith('gemini') &&
            !agent.id.startsWith('claude') &&
            !agent.id.startsWith('copilot') && (
              <button
                onClick={onDelete}
                className="px-3 py-1 rounded text-xs bg-red-500/20 text-red-500 border border-red-500/50 hover:bg-red-500/30"
              >
                <Trash2 size={12} />
              </button>
            )}
        </div>
      </div>

      {/* Tier Type Selection */}
      <div className="space-y-3">
        <div>
          <label className="text-sm text-muted-foreground block mb-2">Tier Type</label>
          <select
            value={agent.tierType}
            onChange={(e) =>
              onUpdate({ tierType: e.target.value as AgentTier['tierType'] })
            }
            disabled={!isEditing}
            className="w-full px-3 py-2 bg-background border border-border rounded text-sm disabled:opacity-50"
          >
            <option value="free">FREE (Rate Limited)</option>
            <option value="monthly">Monthly Subscription</option>
            <option value="pay-per-use">Pay-Per-Use (Per Token)</option>
          </select>
        </div>

        {/* Conditional Fields Based on Tier Type */}
        {agent.tierType === 'free' && (
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="text-sm text-muted-foreground block mb-2">
                Rate Limit
              </label>
              <input
                type="number"
                value={agent.rateLimit || 0}
                onChange={(e) => onUpdate({ rateLimit: parseInt(e.target.value) })}
                disabled={!isEditing}
                className="w-full px-3 py-2 bg-background border border-border rounded text-sm disabled:opacity-50"
              />
            </div>
            <div>
              <label className="text-sm text-muted-foreground block mb-2">Period</label>
              <select
                value={agent.rateLimitPeriod || 'day'}
                onChange={(e) => onUpdate({ rateLimitPeriod: e.target.value })}
                disabled={!isEditing}
                className="w-full px-3 py-2 bg-background border border-border rounded text-sm disabled:opacity-50"
              >
                <option value="hour">Per Hour</option>
                <option value="day">Per Day</option>
                <option value="month">Per Month</option>
              </select>
            </div>
          </div>
        )}

        {agent.tierType === 'monthly' && (
          <div>
            <label className="text-sm text-muted-foreground block mb-2">
              Monthly Cost (USD)
            </label>
            <input
              type="number"
              step="0.01"
              value={agent.monthlyCost || 0}
              onChange={(e) => onUpdate({ monthlyCost: parseFloat(e.target.value) })}
              disabled={!isEditing}
              className="w-full px-3 py-2 bg-background border border-border rounded text-sm disabled:opacity-50"
            />
          </div>
        )}

        {agent.tierType === 'pay-per-use' && (
          <div>
            <label className="text-sm text-muted-foreground block mb-2">
              Cost Per Token (USD)
            </label>
            <input
              type="number"
              step="0.0000001"
              value={agent.costPerToken || 0}
              onChange={(e) => onUpdate({ costPerToken: parseFloat(e.target.value) })}
              disabled={!isEditing}
              className="w-full px-3 py-2 bg-background border border-border rounded text-sm disabled:opacity-50"
            />
          </div>
        )}

        {/* Enable/Disable Toggle */}
        <div className="flex items-center gap-2 pt-2 border-t border-border">
          <input
            type="checkbox"
            id={`enabled-${agent.id}`}
            checked={agent.enabled}
            onChange={(e) => onUpdate({ enabled: e.target.checked })}
            className="w-4 h-4"
          />
          <label htmlFor={`enabled-${agent.id}`} className="text-sm">
            Enable agent for cost tracking
          </label>
        </div>
      </div>

      {/* Cost Display */}
      <div className="mt-4 pt-4 border-t border-border">
        <div className="flex items-center justify-between">
          <span className="text-sm text-muted-foreground">Monthly Cost:</span>
          <span className="font-bold text-neon-green">
            {agent.tierType === 'free' && '$0.00'}
            {agent.tierType === 'monthly' && `$${(agent.monthlyCost || 0).toFixed(2)}`}
            {agent.tierType === 'pay-per-use' && 'Variable'}
          </span>
        </div>
        {agent.tierType === 'free' && (
          <div className="flex items-center justify-between mt-1">
            <span className="text-xs text-muted-foreground">Limit:</span>
            <span className="text-xs">
              {agent.rateLimit} req/{agent.rateLimitPeriod}
            </span>
          </div>
        )}
      </div>
    </div>
  )
}
