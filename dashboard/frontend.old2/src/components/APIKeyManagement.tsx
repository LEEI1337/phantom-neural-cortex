import { useState } from 'react'
import { Plus, Trash2, Edit2, Eye, EyeOff, Check, X } from 'lucide-react'

interface APIKey {
  id: string
  provider: string
  key_name: string
  key_preview: string
  weight: number
  enabled: boolean
  status: string
  usage_stats: {
    total_requests: number
    total_cost: number
  }
}

const PROVIDERS = [
  { id: 'anthropic', name: 'Anthropic (Claude)', icon: '🧠' },
  { id: 'openai', name: 'OpenAI (GPT)', icon: '🤖' },
  { id: 'google', name: 'Google (Gemini)', icon: '✨' },
  { id: 'cohere', name: 'Cohere', icon: '🔷' },
  { id: 'mistral', name: 'Mistral AI', icon: '🌊' },
  { id: 'ollama', name: 'Ollama (Local)', icon: '🦙' },
]

export default function APIKeyManagement() {
  const [keys, setKeys] = useState<APIKey[]>([])
  const [showAddModal, setShowAddModal] = useState(false)
  const [newKey, setNewKey] = useState({
    provider: 'anthropic',
    key_name: '',
    api_key: '',
    weight: 100,
  })

  const handleAddKey = async () => {
    // Mock API call
    const mockKey: APIKey = {
      id: Math.random().toString(36).substr(2, 9),
      provider: newKey.provider,
      key_name: newKey.key_name,
      key_preview: `****${newKey.api_key.slice(-4)}`,
      weight: newKey.weight,
      enabled: true,
      status: 'active',
      usage_stats: {
        total_requests: 0,
        total_cost: 0,
      },
    }
    setKeys([...keys, mockKey])
    setShowAddModal(false)
    setNewKey({ provider: 'anthropic', key_name: '', api_key: '', weight: 100 })
  }

  const handleDeleteKey = (id: string) => {
    setKeys(keys.filter(k => k.id !== id))
  }

  const toggleKeyStatus = (id: string) => {
    setKeys(keys.map(k => k.id === id ? { ...k, enabled: !k.enabled } : k))
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-neon-cyan">API Key Management</h2>
          <p className="text-sm text-muted-foreground font-mono mt-1">
            Manage API keys for multiple AI providers with load balancing
          </p>
        </div>
        <button
          onClick={() => setShowAddModal(true)}
          className="flex items-center gap-2 px-4 py-2 bg-primary/20 hover:bg-primary/30 text-primary border border-primary/40 rounded-lg transition-all duration-300 shadow-neon-cyan"
        >
          <Plus size={20} />
          Add API Key
        </button>
      </div>

      {/* Provider Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="border border-primary/20 rounded-lg p-4 bg-card/60 backdrop-blur-md">
          <div className="text-sm text-muted-foreground font-mono">Total Keys</div>
          <div className="text-3xl font-bold text-foreground mt-2">{keys.length}</div>
        </div>
        <div className="border border-primary/20 rounded-lg p-4 bg-card/60 backdrop-blur-md">
          <div className="text-sm text-muted-foreground font-mono">Active Keys</div>
          <div className="text-3xl font-bold text-neon-green mt-2">{keys.filter(k => k.enabled).length}</div>
        </div>
        <div className="border border-primary/20 rounded-lg p-4 bg-card/60 backdrop-blur-md">
          <div className="text-sm text-muted-foreground font-mono">Total Cost</div>
          <div className="text-3xl font-bold text-neon-purple mt-2">
            ${keys.reduce((sum, k) => sum + k.usage_stats.total_cost, 0).toFixed(2)}
          </div>
        </div>
      </div>

      {/* Keys List */}
      <div className="border border-primary/20 rounded-lg bg-card/60 backdrop-blur-md overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-primary/10 border-b border-primary/20">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-mono font-medium text-neon-cyan uppercase tracking-wider">
                  Provider
                </th>
                <th className="px-6 py-3 text-left text-xs font-mono font-medium text-neon-cyan uppercase tracking-wider">
                  Name
                </th>
                <th className="px-6 py-3 text-left text-xs font-mono font-medium text-neon-cyan uppercase tracking-wider">
                  Key
                </th>
                <th className="px-6 py-3 text-left text-xs font-mono font-medium text-neon-cyan uppercase tracking-wider">
                  Weight
                </th>
                <th className="px-6 py-3 text-left text-xs font-mono font-medium text-neon-cyan uppercase tracking-wider">
                  Requests
                </th>
                <th className="px-6 py-3 text-left text-xs font-mono font-medium text-neon-cyan uppercase tracking-wider">
                  Cost
                </th>
                <th className="px-6 py-3 text-left text-xs font-mono font-medium text-neon-cyan uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-mono font-medium text-neon-cyan uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-primary/10">
              {keys.length === 0 ? (
                <tr>
                  <td colSpan={8} className="px-6 py-12 text-center text-muted-foreground">
                    No API keys configured. Click "Add API Key" to get started.
                  </td>
                </tr>
              ) : (
                keys.map(key => (
                  <tr key={key.id} className="hover:bg-primary/5 transition-colors">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center gap-2">
                        <span className="text-2xl">
                          {PROVIDERS.find(p => p.id === key.provider)?.icon}
                        </span>
                        <span className="font-medium text-foreground">
                          {PROVIDERS.find(p => p.id === key.provider)?.name.split(' ')[0]}
                        </span>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-foreground font-mono">
                      {key.key_name}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-muted-foreground font-mono text-sm">
                      {key.key_preview}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-foreground">
                      {key.weight}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-foreground">
                      {key.usage_stats.total_requests}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-neon-purple font-mono">
                      ${key.usage_stats.total_cost.toFixed(2)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <button
                        onClick={() => toggleKeyStatus(key.id)}
                        className={`px-3 py-1 rounded-full text-xs font-medium transition-all ${
                          key.enabled
                            ? 'bg-neon-green/20 text-neon-green border border-neon-green/30'
                            : 'bg-muted/20 text-muted-foreground border border-muted/30'
                        }`}
                      >
                        {key.enabled ? 'Active' : 'Disabled'}
                      </button>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center gap-2">
                        <button
                          onClick={() => handleDeleteKey(key.id)}
                          className="p-2 hover:bg-destructive/20 text-destructive rounded transition-colors"
                          title="Delete key"
                        >
                          <Trash2 size={16} />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Add Key Modal */}
      {showAddModal && (
        <div className="fixed inset-0 bg-background/80 backdrop-blur-sm flex items-center justify-center z-50">
          <div className="bg-card border border-primary/20 rounded-lg shadow-neon-cyan p-6 w-full max-w-md">
            <h3 className="text-xl font-bold text-neon-cyan mb-4">Add API Key</h3>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-foreground mb-2">Provider</label>
                <select
                  value={newKey.provider}
                  onChange={(e) => setNewKey({ ...newKey, provider: e.target.value })}
                  className="w-full px-3 py-2 bg-background border border-primary/20 rounded-lg text-foreground focus:border-primary focus:outline-none"
                >
                  {PROVIDERS.map(provider => (
                    <option key={provider.id} value={provider.id}>
                      {provider.icon} {provider.name}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-foreground mb-2">Key Name</label>
                <input
                  type="text"
                  value={newKey.key_name}
                  onChange={(e) => setNewKey({ ...newKey, key_name: e.target.value })}
                  placeholder="e.g., Production Key 1"
                  className="w-full px-3 py-2 bg-background border border-primary/20 rounded-lg text-foreground focus:border-primary focus:outline-none font-mono"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-foreground mb-2">API Key</label>
                <input
                  type="password"
                  value={newKey.api_key}
                  onChange={(e) => setNewKey({ ...newKey, api_key: e.target.value })}
                  placeholder="sk-..."
                  className="w-full px-3 py-2 bg-background border border-primary/20 rounded-lg text-foreground focus:border-primary focus:outline-none font-mono"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-foreground mb-2">
                  Weight (for load balancing)
                </label>
                <input
                  type="number"
                  value={newKey.weight}
                  onChange={(e) => setNewKey({ ...newKey, weight: parseInt(e.target.value) })}
                  min="1"
                  max="1000"
                  className="w-full px-3 py-2 bg-background border border-primary/20 rounded-lg text-foreground focus:border-primary focus:outline-none"
                />
              </div>
            </div>

            <div className="flex items-center gap-3 mt-6">
              <button
                onClick={handleAddKey}
                disabled={!newKey.key_name || !newKey.api_key}
                className="flex-1 px-4 py-2 bg-primary/20 hover:bg-primary/30 text-primary border border-primary/40 rounded-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <Check className="inline mr-2" size={16} />
                Add Key
              </button>
              <button
                onClick={() => setShowAddModal(false)}
                className="flex-1 px-4 py-2 bg-muted/20 hover:bg-muted/30 text-foreground border border-muted/40 rounded-lg transition-all"
              >
                <X className="inline mr-2" size={16} />
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
