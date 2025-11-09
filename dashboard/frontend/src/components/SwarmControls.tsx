import { useState } from 'react'
import { Cpu, Zap, DollarSign, RefreshCw, Settings } from 'lucide-react'

export default function SwarmControls() {
  const [config, setConfig] = useState({
    // Parallelization
    maxParallelTasks: 5,
    maxParallelAgents: 3,
    autoScale: true,

    // Intelligence
    mode: 'balanced',
    temperature: 0.7,
    useLatentReasoning: true,
    reasoningDepth: 3,

    // Feedback Loop
    maxIterations: 5,
    qualityThreshold: 0.85,
    adaptiveIterations: true,

    // Cost Control
    dailyBudget: 50,
    preferCheaperModels: false,

    // Caching
    cachingStrategy: 'balanced',
    ttl: 3600,

    // Retry
    retryStrategy: 'exponential_backoff',
    maxRetries: 3,
  })

  const updateConfig = (key: string, value: any) => {
    setConfig({ ...config, [key]: value })
  }

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-neon-cyan">Swarm Orchestration Controls</h2>
        <p className="text-sm text-muted-foreground font-mono mt-1">
          Configure intelligence modes, parallelization, and cost optimization
        </p>
      </div>

      {/* Preset Configurations */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {[
          { name: 'Speed Optimized', icon: '⚡', desc: 'Maximum speed with parallel execution' },
          { name: 'Cost Optimized', icon: '💰', desc: 'Minimize costs with caching' },
          { name: 'Quality First', icon: '✨', desc: 'Maximum quality with expert mode' },
        ].map(preset => (
          <button
            key={preset.name}
            className="border border-primary/20 rounded-lg p-4 bg-card/60 backdrop-blur-md hover:bg-primary/10 hover:border-primary/40 transition-all text-left group"
          >
            <div className="text-3xl mb-2">{preset.icon}</div>
            <div className="font-bold text-foreground group-hover:text-primary transition-colors">
              {preset.name}
            </div>
            <div className="text-sm text-muted-foreground mt-1">{preset.desc}</div>
          </button>
        ))}
      </div>

      {/* Parallelization Controls */}
      <div className="border border-primary/20 rounded-lg p-6 bg-card/60 backdrop-blur-md space-y-4">
        <div className="flex items-center gap-2 text-neon-cyan mb-4">
          <Cpu size={20} />
          <h3 className="text-lg font-bold">Parallelization</h3>
        </div>

        <div className="space-y-4">
          <div>
            <label className="flex items-center justify-between text-sm font-medium text-foreground mb-2">
              <span>Max Parallel Tasks</span>
              <span className="text-neon-purple font-mono">{config.maxParallelTasks}</span>
            </label>
            <input
              type="range"
              min="1"
              max="20"
              value={config.maxParallelTasks}
              onChange={(e) => updateConfig('maxParallelTasks', parseInt(e.target.value))}
              className="w-full h-2 bg-primary/20 rounded-lg appearance-none cursor-pointer slider"
            />
          </div>

          <div>
            <label className="flex items-center justify-between text-sm font-medium text-foreground mb-2">
              <span>Max Parallel Agents</span>
              <span className="text-neon-purple font-mono">{config.maxParallelAgents}</span>
            </label>
            <input
              type="range"
              min="1"
              max="10"
              value={config.maxParallelAgents}
              onChange={(e) => updateConfig('maxParallelAgents', parseInt(e.target.value))}
              className="w-full h-2 bg-primary/20 rounded-lg appearance-none cursor-pointer slider"
            />
          </div>

          <label className="flex items-center gap-2 text-foreground">
            <input
              type="checkbox"
              checked={config.autoScale}
              onChange={(e) => updateConfig('autoScale', e.target.checked)}
              className="w-4 h-4 rounded border-primary/20 bg-background text-primary focus:ring-primary"
            />
            <span className="text-sm font-mono">Auto-scale based on load</span>
          </label>
        </div>
      </div>

      {/* Intelligence Mode */}
      <div className="border border-primary/20 rounded-lg p-6 bg-card/60 backdrop-blur-md space-y-4">
        <div className="flex items-center gap-2 text-neon-cyan mb-4">
          <Zap size={20} />
          <h3 className="text-lg font-bold">Intelligence Mode</h3>
        </div>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-foreground mb-2">Mode</label>
            <select
              value={config.mode}
              onChange={(e) => updateConfig('mode', e.target.value)}
              className="w-full px-3 py-2 bg-background border border-primary/20 rounded-lg text-foreground focus:border-primary focus:outline-none"
            >
              <option value="speed">Speed - Fast responses</option>
              <option value="balanced">Balanced - Good mix</option>
              <option value="quality">Quality - High quality</option>
              <option value="expert">Expert - Maximum quality</option>
              <option value="custom">Custom - User-defined</option>
            </select>
          </div>

          <div>
            <label className="flex items-center justify-between text-sm font-medium text-foreground mb-2">
              <span>Temperature</span>
              <span className="text-neon-purple font-mono">{config.temperature.toFixed(2)}</span>
            </label>
            <input
              type="range"
              min="0"
              max="2"
              step="0.1"
              value={config.temperature}
              onChange={(e) => updateConfig('temperature', parseFloat(e.target.value))}
              className="w-full h-2 bg-primary/20 rounded-lg appearance-none cursor-pointer slider"
            />
          </div>

          <label className="flex items-center gap-2 text-foreground">
            <input
              type="checkbox"
              checked={config.useLatentReasoning}
              onChange={(e) => updateConfig('useLatentReasoning', e.target.checked)}
              className="w-4 h-4 rounded border-primary/20 bg-background text-primary focus:ring-primary"
            />
            <span className="text-sm font-mono">Use latent reasoning (extended thinking)</span>
          </label>

          {config.useLatentReasoning && (
            <div>
              <label className="flex items-center justify-between text-sm font-medium text-foreground mb-2">
                <span>Reasoning Depth</span>
                <span className="text-neon-purple font-mono">{config.reasoningDepth}</span>
              </label>
              <input
                type="range"
                min="1"
                max="10"
                value={config.reasoningDepth}
                onChange={(e) => updateConfig('reasoningDepth', parseInt(e.target.value))}
                className="w-full h-2 bg-primary/20 rounded-lg appearance-none cursor-pointer slider"
              />
            </div>
          )}
        </div>
      </div>

      {/* Feedback Loop */}
      <div className="border border-primary/20 rounded-lg p-6 bg-card/60 backdrop-blur-md space-y-4">
        <div className="flex items-center gap-2 text-neon-cyan mb-4">
          <RefreshCw size={20} />
          <h3 className="text-lg font-bold">Feedback Loop & Iterations</h3>
        </div>

        <div className="space-y-4">
          <div>
            <label className="flex items-center justify-between text-sm font-medium text-foreground mb-2">
              <span>Max Iterations</span>
              <span className="text-neon-purple font-mono">{config.maxIterations}</span>
            </label>
            <input
              type="range"
              min="1"
              max="20"
              value={config.maxIterations}
              onChange={(e) => updateConfig('maxIterations', parseInt(e.target.value))}
              className="w-full h-2 bg-primary/20 rounded-lg appearance-none cursor-pointer slider"
            />
          </div>

          <div>
            <label className="flex items-center justify-between text-sm font-medium text-foreground mb-2">
              <span>Quality Threshold</span>
              <span className="text-neon-purple font-mono">{config.qualityThreshold.toFixed(2)}</span>
            </label>
            <input
              type="range"
              min="0"
              max="1"
              step="0.05"
              value={config.qualityThreshold}
              onChange={(e) => updateConfig('qualityThreshold', parseFloat(e.target.value))}
              className="w-full h-2 bg-primary/20 rounded-lg appearance-none cursor-pointer slider"
            />
          </div>

          <label className="flex items-center gap-2 text-foreground">
            <input
              type="checkbox"
              checked={config.adaptiveIterations}
              onChange={(e) => updateConfig('adaptiveIterations', e.target.checked)}
              className="w-4 h-4 rounded border-primary/20 bg-background text-primary focus:ring-primary"
            />
            <span className="text-sm font-mono">ML-optimized adaptive iterations</span>
          </label>
        </div>
      </div>

      {/* Cost Control */}
      <div className="border border-primary/20 rounded-lg p-6 bg-card/60 backdrop-blur-md space-y-4">
        <div className="flex items-center gap-2 text-neon-cyan mb-4">
          <DollarSign size={20} />
          <h3 className="text-lg font-bold">Cost Control</h3>
        </div>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-foreground mb-2">
              Daily Budget (USD)
            </label>
            <input
              type="number"
              value={config.dailyBudget}
              onChange={(e) => updateConfig('dailyBudget', parseFloat(e.target.value))}
              min="0"
              step="10"
              className="w-full px-3 py-2 bg-background border border-primary/20 rounded-lg text-foreground focus:border-primary focus:outline-none font-mono"
            />
          </div>

          <label className="flex items-center gap-2 text-foreground">
            <input
              type="checkbox"
              checked={config.preferCheaperModels}
              onChange={(e) => updateConfig('preferCheaperModels', e.target.checked)}
              className="w-4 h-4 rounded border-primary/20 bg-background text-primary focus:ring-primary"
            />
            <span className="text-sm font-mono">Prefer cheaper models when possible</span>
          </label>
        </div>
      </div>

      {/* Save Button */}
      <div className="flex items-center gap-3">
        <button className="flex-1 px-6 py-3 bg-primary/20 hover:bg-primary/30 text-primary border border-primary/40 rounded-lg transition-all shadow-neon-cyan font-medium">
          <Settings className="inline mr-2" size={18} />
          Save Configuration
        </button>
        <button className="px-6 py-3 bg-muted/20 hover:bg-muted/30 text-foreground border border-muted/40 rounded-lg transition-all font-medium">
          Reset to Defaults
        </button>
      </div>
    </div>
  )
}
