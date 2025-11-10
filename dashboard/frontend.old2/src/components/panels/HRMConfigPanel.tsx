import React, { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../ui/card'
import { Button } from '../ui/button'
import { Slider } from '../ui/slider'
import { Switch } from '../ui/switch'

export interface HRMConfigPanelProps {
  projectId?: string
}

interface HRMConfig {
  // Core Optimizations
  latentReasoning: {
    enabled: boolean
    dimensionality: number
  }
  mlIterationPrediction: {
    mode: 'auto' | 'manual' | 'fixed'
    maxIterations: number
  }
  caching: {
    memory: boolean
    disk: boolean
    remote: boolean
    aggressive: boolean
    maxSizeMB: number
  }

  // Agent Control
  agentSwitching: {
    strategy: 'cost_optimized' | 'quality_first' | 'speed_optimized' | 'adaptive' | 'round_robin' | 'manual'
    qualityDropThreshold: number
    costCeiling: number
    maxSwitches: number
  }

  // Quality & Testing
  deepSupervision: {
    enabled: boolean
    qualityGate: number
  }
  parallelEvaluation: {
    enabled: boolean
    workers: number
    timeout: number
  }

  // Advanced Options
  bayesianOptimization: {
    enabled: boolean
    iterations: number
  }
  rlRefinement: {
    enabled: boolean
    epsilon: number
    learningRate: number
  }
  prometheusMetrics: {
    enabled: boolean
    interval: number
  }
  multiRepo: boolean
}

const DEFAULT_CONFIG: HRMConfig = {
  latentReasoning: { enabled: true, dimensionality: 512 },
  mlIterationPrediction: { mode: 'auto', maxIterations: 7 },
  caching: { memory: true, disk: true, remote: false, aggressive: true, maxSizeMB: 500 },
  agentSwitching: { strategy: 'adaptive', qualityDropThreshold: 20, costCeiling: 5, maxSwitches: 3 },
  deepSupervision: { enabled: true, qualityGate: 75 },
  parallelEvaluation: { enabled: true, workers: 4, timeout: 60 },
  bayesianOptimization: { enabled: false, iterations: 30 },
  rlRefinement: { enabled: true, epsilon: 0.1, learningRate: 0.001 },
  prometheusMetrics: { enabled: true, interval: 15 },
  multiRepo: true
}

interface ImpactMetrics {
  cost: { current: number; predicted: number; change: number }
  speed: { current: number; predicted: number; change: number }
  quality: { current: number; predicted: number; change: number }
  tokens: { current: number; predicted: number; change: number }
}

const CollapsibleSection: React.FC<{
  title: string
  icon: string
  defaultOpen?: boolean
  children: React.ReactNode
}> = ({ title, icon, defaultOpen = false, children }) => {
  const [isOpen, setIsOpen] = useState(defaultOpen)

  return (
    <div className="mb-4 border border-cyan-500/30 rounded-lg overflow-hidden bg-slate-900/50">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full p-4 flex items-center justify-between hover:bg-slate-800/50 transition-colors"
      >
        <div className="flex items-center gap-2">
          <span className="text-2xl">{icon}</span>
          <h3 className="text-lg font-semibold text-cyan-400">{title}</h3>
        </div>
        <span className="text-cyan-400 text-xl">{isOpen ? '▼' : '▶'}</span>
      </button>
      {isOpen && (
        <div className="p-4 border-t border-cyan-500/20 bg-slate-950/30">
          {children}
        </div>
      )}
    </div>
  )
}

const InfoButton: React.FC<{ tooltip: string }> = ({ tooltip }) => {
  const [showTooltip, setShowTooltip] = useState(false)

  return (
    <div className="relative inline-block">
      <button
        className="w-5 h-5 rounded-full bg-cyan-500/20 text-cyan-400 text-xs font-bold hover:bg-cyan-500/40 transition-colors"
        onMouseEnter={() => setShowTooltip(true)}
        onMouseLeave={() => setShowTooltip(false)}
      >
        ⓘ
      </button>
      {showTooltip && (
        <div className="absolute z-10 bottom-full left-1/2 -translate-x-1/2 mb-2 w-64 p-2 bg-slate-800 border border-cyan-500/50 rounded text-xs text-slate-200 shadow-lg">
          {tooltip}
        </div>
      )}
    </div>
  )
}

export const HRMConfigPanel: React.FC<HRMConfigPanelProps> = ({ projectId }) => {
  const [config, setConfig] = useState<HRMConfig>(DEFAULT_CONFIG)
  const [impact, setImpact] = useState<ImpactMetrics | null>(null)
  const [isSimulating, setIsSimulating] = useState(false)

  // Calculate impact preview when config changes
  useEffect(() => {
    const calculateImpact = () => {
      // Mock calculation - in real app, call API
      const baselineCost = 2.50
      const baselineSpeed = 450
      const baselineQuality = 87
      const baselineTokens = 50000

      let costMultiplier = 1.0
      let speedMultiplier = 1.0
      let qualityMultiplier = 1.0
      let tokenMultiplier = 1.0

      // Latent Reasoning impact
      if (config.latentReasoning.enabled) {
        const dim = config.latentReasoning.dimensionality
        tokenMultiplier *= dim === 256 ? 0.5 : dim === 512 ? 0.6 : 0.7
        qualityMultiplier *= dim === 256 ? 0.98 : dim === 512 ? 1.0 : 1.02
      }

      // Agent Switching impact
      if (config.agentSwitching.strategy === 'cost_optimized') {
        costMultiplier *= 0.6
        qualityMultiplier *= 0.95
      } else if (config.agentSwitching.strategy === 'quality_first') {
        costMultiplier *= 1.4
        qualityMultiplier *= 1.08
      } else if (config.agentSwitching.strategy === 'adaptive') {
        costMultiplier *= 0.8
        qualityMultiplier *= 1.05
      }

      // Caching impact
      if (config.caching.aggressive) {
        speedMultiplier *= 0.7
        costMultiplier *= 0.85
      }

      const newCost = baselineCost * costMultiplier
      const newSpeed = baselineSpeed * speedMultiplier
      const newQuality = baselineQuality * qualityMultiplier
      const newTokens = baselineTokens * tokenMultiplier

      setImpact({
        cost: {
          current: baselineCost,
          predicted: newCost,
          change: ((newCost - baselineCost) / baselineCost) * 100
        },
        speed: {
          current: baselineSpeed,
          predicted: newSpeed,
          change: ((newSpeed - baselineSpeed) / baselineSpeed) * 100
        },
        quality: {
          current: baselineQuality,
          predicted: newQuality,
          change: ((newQuality - baselineQuality) / baselineQuality) * 100
        },
        tokens: {
          current: baselineTokens,
          predicted: newTokens,
          change: ((newTokens - baselineTokens) / baselineTokens) * 100
        }
      })
    }

    calculateImpact()
  }, [config])

  const applyPreset = (preset: 'speed' | 'cost' | 'quality' | 'balanced') => {
    const presets: Record<string, Partial<HRMConfig>> = {
      speed: {
        latentReasoning: { enabled: true, dimensionality: 256 },
        mlIterationPrediction: { mode: 'fixed', maxIterations: 2 },
        agentSwitching: { ...config.agentSwitching, strategy: 'speed_optimized' },
        caching: { ...config.caching, aggressive: true }
      },
      cost: {
        latentReasoning: { enabled: true, dimensionality: 512 },
        agentSwitching: { ...config.agentSwitching, strategy: 'cost_optimized' },
        caching: { ...config.caching, aggressive: true }
      },
      quality: {
        latentReasoning: { enabled: true, dimensionality: 1024 },
        mlIterationPrediction: { mode: 'auto', maxIterations: 10 },
        agentSwitching: { ...config.agentSwitching, strategy: 'quality_first' },
        bayesianOptimization: { enabled: true, iterations: 100 }
      },
      balanced: DEFAULT_CONFIG
    }

    setConfig({ ...config, ...presets[preset] })
  }

  const applyChanges = async () => {
    // TODO: Implement API call
    console.log('Applying HRM config:', config)
  }

  const resetChanges = () => {
    setConfig(DEFAULT_CONFIG)
  }

  return (
    <div className="space-y-6">
      {/* Quick Actions */}
      <Card className="bg-gradient-to-br from-slate-900 to-slate-800 border-cyan-500/30">
        <CardHeader>
          <CardTitle className="text-cyan-400 flex items-center gap-2">
            <span className="text-2xl">⚡</span>
            Quick Presets
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap gap-2">
            <Button onClick={() => applyPreset('speed')} size="sm" className="bg-yellow-500/20 text-yellow-400 border-yellow-500/50 hover:bg-yellow-500/30">
              ⚡ Speed
            </Button>
            <Button onClick={() => applyPreset('cost')} size="sm" className="bg-green-500/20 text-green-400 border-green-500/50 hover:bg-green-500/30">
              💰 Cost
            </Button>
            <Button onClick={() => applyPreset('quality')} size="sm" className="bg-purple-500/20 text-purple-400 border-purple-500/50 hover:bg-purple-500/30">
              🎯 Quality
            </Button>
            <Button onClick={() => applyPreset('balanced')} size="sm" className="bg-cyan-500/20 text-cyan-400 border-cyan-500/50 hover:bg-cyan-500/30">
              ⚖️ Balanced
            </Button>
            <Button onClick={resetChanges} variant="outline" size="sm" className="ml-auto border-slate-500/50 text-slate-400 hover:bg-slate-800">
              Reset
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Live Impact Preview */}
      {impact && (
        <Card className="bg-gradient-to-br from-slate-900 to-slate-800 border-cyan-500/30">
          <CardHeader>
            <CardTitle className="text-cyan-400 flex items-center gap-2">
              <span className="text-2xl">📊</span>
              Live Impact Preview
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="p-3 bg-slate-950/50 rounded border border-cyan-500/20">
                <div className="text-xs text-slate-400 mb-1">Cost</div>
                <div className="text-lg font-bold text-cyan-400">
                  ${impact.cost.predicted.toFixed(2)}
                </div>
                <div className={`text-xs ${impact.cost.change < 0 ? 'text-green-400' : 'text-red-400'}`}>
                  {impact.cost.change > 0 ? '+' : ''}{impact.cost.change.toFixed(0)}% {impact.cost.change < 0 ? '⬇️' : '⬆️'}
                </div>
              </div>
              <div className="p-3 bg-slate-950/50 rounded border border-cyan-500/20">
                <div className="text-xs text-slate-400 mb-1">Speed</div>
                <div className="text-lg font-bold text-cyan-400">
                  {Math.round(impact.speed.predicted)}s
                </div>
                <div className={`text-xs ${impact.speed.change < 0 ? 'text-green-400' : 'text-red-400'}`}>
                  {impact.speed.change > 0 ? '+' : ''}{impact.speed.change.toFixed(0)}% {impact.speed.change < 0 ? '⬇️' : '⬆️'}
                </div>
              </div>
              <div className="p-3 bg-slate-950/50 rounded border border-cyan-500/20">
                <div className="text-xs text-slate-400 mb-1">Quality</div>
                <div className="text-lg font-bold text-cyan-400">
                  {impact.quality.predicted.toFixed(0)}%
                </div>
                <div className={`text-xs ${impact.quality.change > 0 ? 'text-green-400' : 'text-red-400'}`}>
                  {impact.quality.change > 0 ? '+' : ''}{impact.quality.change.toFixed(0)}% {impact.quality.change > 0 ? '⬆️' : '⬇️'}
                </div>
              </div>
              <div className="p-3 bg-slate-950/50 rounded border border-cyan-500/20">
                <div className="text-xs text-slate-400 mb-1">Tokens</div>
                <div className="text-lg font-bold text-cyan-400">
                  {Math.round(impact.tokens.predicted / 1000)}k
                </div>
                <div className={`text-xs ${impact.tokens.change < 0 ? 'text-green-400' : 'text-red-400'}`}>
                  {impact.tokens.change > 0 ? '+' : ''}{impact.tokens.change.toFixed(0)}% {impact.tokens.change < 0 ? '⬇️' : '⬆️'}
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Core Optimizations */}
      <CollapsibleSection title="Core Optimizations" icon="⚙️" defaultOpen={true}>
        {/* Latent Reasoning */}
        <div className="mb-6 p-4 bg-slate-800/30 rounded-lg">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <span className="font-semibold text-slate-200">Latent Reasoning Compression</span>
              <InfoButton tooltip="Compresses reasoning steps to reduce token usage while maintaining quality" />
            </div>
            <Switch
              checked={config.latentReasoning.enabled}
              onCheckedChange={(checked) =>
                setConfig({ ...config, latentReasoning: { ...config.latentReasoning, enabled: checked } })
              }
            />
          </div>
          {config.latentReasoning.enabled && (
            <>
              <div className="mb-2">
                <label className="text-sm text-slate-400 mb-1 block">
                  Dimensionality: {config.latentReasoning.dimensionality}D
                </label>
                <Slider
                  value={[config.latentReasoning.dimensionality]}
                  onValueChange={([value]) =>
                    setConfig({ ...config, latentReasoning: { ...config.latentReasoning, dimensionality: value } })
                  }
                  min={128}
                  max={1024}
                  step={128}
                />
              </div>
              <div className="text-xs text-slate-500 mt-2">
                Token Savings: ~{Math.round((1 - config.latentReasoning.dimensionality / 1024) * 50)}%
              </div>
            </>
          )}
        </div>

        {/* ML Iteration Prediction */}
        <div className="mb-6 p-4 bg-slate-800/30 rounded-lg">
          <div className="flex items-center gap-2 mb-3">
            <span className="font-semibold text-slate-200">ML Iteration Prediction</span>
            <InfoButton tooltip="Uses ML to predict optimal number of iterations needed" />
          </div>
          <div className="mb-3">
            <label className="text-sm text-slate-400 mb-2 block">Mode</label>
            <div className="flex gap-2">
              {(['auto', 'manual', 'fixed'] as const).map((mode) => (
                <Button
                  key={mode}
                  onClick={() => setConfig({ ...config, mlIterationPrediction: { ...config.mlIterationPrediction, mode } })}
                  size="sm"
                  variant={config.mlIterationPrediction.mode === mode ? 'default' : 'outline'}
                  className={config.mlIterationPrediction.mode === mode ? 'bg-cyan-500' : ''}
                >
                  {mode.charAt(0).toUpperCase() + mode.slice(1)}
                </Button>
              ))}
            </div>
          </div>
          <div>
            <label className="text-sm text-slate-400 mb-1 block">
              Max Iterations: {config.mlIterationPrediction.maxIterations}
            </label>
            <Slider
              value={[config.mlIterationPrediction.maxIterations]}
              onValueChange={([value]) =>
                setConfig({ ...config, mlIterationPrediction: { ...config.mlIterationPrediction, maxIterations: value } })
              }
              min={2}
              max={20}
              step={1}
            />
          </div>
        </div>

        {/* Three-Layer Caching */}
        <div className="p-4 bg-slate-800/30 rounded-lg">
          <div className="flex items-center gap-2 mb-3">
            <span className="font-semibold text-slate-200">Three-Layer Caching</span>
            <InfoButton tooltip="Multi-tier caching for maximum performance" />
          </div>
          <div className="grid grid-cols-2 gap-3 mb-3">
            <label className="flex items-center gap-2 text-sm text-slate-300">
              <Switch
                checked={config.caching.memory}
                onCheckedChange={(checked) =>
                  setConfig({ ...config, caching: { ...config.caching, memory: checked } })
                }
              />
              Memory Cache
            </label>
            <label className="flex items-center gap-2 text-sm text-slate-300">
              <Switch
                checked={config.caching.disk}
                onCheckedChange={(checked) =>
                  setConfig({ ...config, caching: { ...config.caching, disk: checked } })
                }
              />
              Disk Cache
            </label>
            <label className="flex items-center gap-2 text-sm text-slate-300">
              <Switch
                checked={config.caching.remote}
                onCheckedChange={(checked) =>
                  setConfig({ ...config, caching: { ...config.caching, remote: checked } })
                }
              />
              Remote Cache
            </label>
            <label className="flex items-center gap-2 text-sm text-slate-300">
              <Switch
                checked={config.caching.aggressive}
                onCheckedChange={(checked) =>
                  setConfig({ ...config, caching: { ...config.caching, aggressive: checked } })
                }
              />
              Aggressive Mode
            </label>
          </div>
          <div>
            <label className="text-sm text-slate-400 mb-1 block">
              Max Size: {config.caching.maxSizeMB}MB
            </label>
            <Slider
              value={[config.caching.maxSizeMB]}
              onValueChange={([value]) =>
                setConfig({ ...config, caching: { ...config.caching, maxSizeMB: value } })
              }
              min={100}
              max={5000}
              step={100}
            />
          </div>
        </div>
      </CollapsibleSection>

      {/* Agent Control */}
      <CollapsibleSection title="Agent Control" icon="🤖">
        <div className="p-4 bg-slate-800/30 rounded-lg">
          <div className="flex items-center gap-2 mb-3">
            <span className="font-semibold text-slate-200">Smart Agent Switching</span>
            <InfoButton tooltip="Automatically switch between agents based on task requirements" />
          </div>

          <div className="mb-4">
            <label className="text-sm text-slate-400 mb-2 block">Strategy</label>
            <select
              value={config.agentSwitching.strategy}
              onChange={(e) =>
                setConfig({
                  ...config,
                  agentSwitching: { ...config.agentSwitching, strategy: e.target.value as any }
                })
              }
              className="w-full p-2 bg-slate-900 border border-cyan-500/30 rounded text-slate-200 text-sm"
            >
              <option value="cost_optimized">Cost-Optimized (Gemini-first)</option>
              <option value="quality_first">Quality-First (Claude-first)</option>
              <option value="speed_optimized">Speed-Optimized (Fastest)</option>
              <option value="adaptive">Adaptive (ML-predicted) ✨</option>
              <option value="round_robin">Round-Robin (Equal distribution)</option>
              <option value="manual">Manual (No switching)</option>
            </select>
          </div>

          <div className="space-y-3">
            <div>
              <label className="text-sm text-slate-400 mb-1 block">
                Quality Drop Threshold: {config.agentSwitching.qualityDropThreshold}%
              </label>
              <Slider
                value={[config.agentSwitching.qualityDropThreshold]}
                onValueChange={([value]) =>
                  setConfig({ ...config, agentSwitching: { ...config.agentSwitching, qualityDropThreshold: value } })
                }
                min={0}
                max={100}
                step={5}
              />
            </div>
            <div>
              <label className="text-sm text-slate-400 mb-1 block">
                Cost Ceiling: ${config.agentSwitching.costCeiling}
              </label>
              <Slider
                value={[config.agentSwitching.costCeiling]}
                onValueChange={([value]) =>
                  setConfig({ ...config, agentSwitching: { ...config.agentSwitching, costCeiling: value } })
                }
                min={1}
                max={20}
                step={0.5}
              />
            </div>
            <div>
              <label className="text-sm text-slate-400 mb-1 block">
                Max Switches per Task: {config.agentSwitching.maxSwitches}
              </label>
              <Slider
                value={[config.agentSwitching.maxSwitches]}
                onValueChange={([value]) =>
                  setConfig({ ...config, agentSwitching: { ...config.agentSwitching, maxSwitches: value } })
                }
                min={0}
                max={10}
                step={1}
              />
            </div>
          </div>
        </div>
      </CollapsibleSection>

      {/* Quality & Testing */}
      <CollapsibleSection title="Quality & Testing" icon="🎯">
        {/* Deep Supervision */}
        <div className="mb-6 p-4 bg-slate-800/30 rounded-lg">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <span className="font-semibold text-slate-200">Deep Supervision Checkpoints</span>
              <InfoButton tooltip="Quality gates at key milestones (33%, 66%, 100%)" />
            </div>
            <Switch
              checked={config.deepSupervision.enabled}
              onCheckedChange={(checked) =>
                setConfig({ ...config, deepSupervision: { ...config.deepSupervision, enabled: checked } })
              }
            />
          </div>
          {config.deepSupervision.enabled && (
            <div>
              <label className="text-sm text-slate-400 mb-1 block">
                Quality Gate Threshold: {config.deepSupervision.qualityGate}%
              </label>
              <Slider
                value={[config.deepSupervision.qualityGate]}
                onValueChange={([value]) =>
                  setConfig({ ...config, deepSupervision: { ...config.deepSupervision, qualityGate: value } })
                }
                min={50}
                max={100}
                step={5}
              />
            </div>
          )}
        </div>

        {/* Parallel Quality Evaluation */}
        <div className="p-4 bg-slate-800/30 rounded-lg">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <span className="font-semibold text-slate-200">Parallel Quality Evaluation</span>
              <InfoButton tooltip="Run quality checks in parallel for faster feedback" />
            </div>
            <Switch
              checked={config.parallelEvaluation.enabled}
              onCheckedChange={(checked) =>
                setConfig({ ...config, parallelEvaluation: { ...config.parallelEvaluation, enabled: checked } })
              }
            />
          </div>
          {config.parallelEvaluation.enabled && (
            <div className="space-y-3">
              <div>
                <label className="text-sm text-slate-400 mb-1 block">
                  Workers: {config.parallelEvaluation.workers}
                </label>
                <Slider
                  value={[config.parallelEvaluation.workers]}
                  onValueChange={([value]) =>
                    setConfig({ ...config, parallelEvaluation: { ...config.parallelEvaluation, workers: value } })
                  }
                  min={1}
                  max={16}
                  step={1}
                />
              </div>
              <div>
                <label className="text-sm text-slate-400 mb-1 block">
                  Timeout: {config.parallelEvaluation.timeout}s
                </label>
                <Slider
                  value={[config.parallelEvaluation.timeout]}
                  onValueChange={([value]) =>
                    setConfig({ ...config, parallelEvaluation: { ...config.parallelEvaluation, timeout: value } })
                  }
                  min={10}
                  max={300}
                  step={10}
                />
              </div>
            </div>
          )}
        </div>
      </CollapsibleSection>

      {/* Advanced Options */}
      <CollapsibleSection title="Advanced Options" icon="🔬">
        {/* Bayesian Optimization */}
        <div className="mb-6 p-4 bg-slate-800/30 rounded-lg">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <span className="font-semibold text-slate-200">Bayesian Optimization</span>
              <InfoButton tooltip="ML-based parameter optimization (experimental)" />
            </div>
            <Switch
              checked={config.bayesianOptimization.enabled}
              onCheckedChange={(checked) =>
                setConfig({ ...config, bayesianOptimization: { ...config.bayesianOptimization, enabled: checked } })
              }
            />
          </div>
          {config.bayesianOptimization.enabled && (
            <div>
              <label className="text-sm text-slate-400 mb-1 block">
                Iterations: {config.bayesianOptimization.iterations}
              </label>
              <Slider
                value={[config.bayesianOptimization.iterations]}
                onValueChange={([value]) =>
                  setConfig({ ...config, bayesianOptimization: { ...config.bayesianOptimization, iterations: value } })
                }
                min={10}
                max={100}
                step={10}
              />
            </div>
          )}
        </div>

        {/* RL Refinement */}
        <div className="mb-6 p-4 bg-slate-800/30 rounded-lg">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <span className="font-semibold text-slate-200">RL Refinement Chain</span>
              <InfoButton tooltip="Reinforcement learning for iterative improvement" />
            </div>
            <Switch
              checked={config.rlRefinement.enabled}
              onCheckedChange={(checked) =>
                setConfig({ ...config, rlRefinement: { ...config.rlRefinement, enabled: checked } })
              }
            />
          </div>
          {config.rlRefinement.enabled && (
            <div className="space-y-3">
              <div>
                <label className="text-sm text-slate-400 mb-1 block">
                  Epsilon: {config.rlRefinement.epsilon.toFixed(2)}
                </label>
                <Slider
                  value={[config.rlRefinement.epsilon * 100]}
                  onValueChange={([value]) =>
                    setConfig({ ...config, rlRefinement: { ...config.rlRefinement, epsilon: value / 100 } })
                  }
                  min={0}
                  max={100}
                  step={1}
                />
              </div>
              <div>
                <label className="text-sm text-slate-400 mb-1 block">
                  Learning Rate: {config.rlRefinement.learningRate.toFixed(4)}
                </label>
                <Slider
                  value={[config.rlRefinement.learningRate * 10000]}
                  onValueChange={([value]) =>
                    setConfig({ ...config, rlRefinement: { ...config.rlRefinement, learningRate: value / 10000 } })
                  }
                  min={1}
                  max={1000}
                  step={1}
                />
              </div>
            </div>
          )}
        </div>

        {/* Other Settings */}
        <div className="p-4 bg-slate-800/30 rounded-lg space-y-3">
          <label className="flex items-center justify-between text-sm text-slate-300">
            <div className="flex items-center gap-2">
              <span>Prometheus Metrics Export</span>
              <InfoButton tooltip="Export metrics to Prometheus for monitoring" />
            </div>
            <Switch
              checked={config.prometheusMetrics.enabled}
              onCheckedChange={(checked) =>
                setConfig({ ...config, prometheusMetrics: { ...config.prometheusMetrics, enabled: checked } })
              }
            />
          </label>
          {config.prometheusMetrics.enabled && (
            <div>
              <label className="text-sm text-slate-400 mb-1 block">
                Export Interval: {config.prometheusMetrics.interval}s
              </label>
              <Slider
                value={[config.prometheusMetrics.interval]}
                onValueChange={([value]) =>
                  setConfig({ ...config, prometheusMetrics: { ...config.prometheusMetrics, interval: value } })
                }
                min={5}
                max={60}
                step={5}
              />
            </div>
          )}

          <label className="flex items-center justify-between text-sm text-slate-300">
            <div className="flex items-center gap-2">
              <span>Multi-Repository Coordination</span>
              <InfoButton tooltip="Coordinate across multiple Git repositories" />
            </div>
            <Switch
              checked={config.multiRepo}
              onCheckedChange={(checked) => setConfig({ ...config, multiRepo: checked })}
            />
          </label>
        </div>
      </CollapsibleSection>

      {/* Action Buttons */}
      <div className="flex gap-3 sticky bottom-0 bg-slate-900 p-4 border-t border-cyan-500/30 -mx-4">
        <Button
          onClick={applyChanges}
          className="flex-1 bg-cyan-500 text-slate-900 hover:bg-cyan-400 shadow-lg shadow-cyan-500/30"
        >
          Apply Changes
        </Button>
        <Button
          onClick={() => setIsSimulating(!isSimulating)}
          variant="outline"
          className="border-cyan-500/50 text-cyan-400 hover:bg-cyan-500/10"
        >
          Simulate Impact
        </Button>
        <Button
          onClick={resetChanges}
          variant="outline"
          className="border-slate-500/50 text-slate-400 hover:bg-slate-800"
        >
          Reset
        </Button>
      </div>
    </div>
  )
}
