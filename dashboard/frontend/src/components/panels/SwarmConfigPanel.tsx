import React, { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card'
import { Button } from '../ui/button'
import { Slider } from '../ui/slider'
import { Switch } from '../ui/switch'

export interface SwarmConfigPanelProps {
  projectId?: string
}

interface SwarmConfig {
  parallelization: {
    maxParallelTasks: number
    maxParallelAgents: number
    autoScale: boolean
    scaleUpThreshold: number
    scaleDownThreshold: number
  }
  intelligenceMode: {
    mode: 'speed' | 'cost' | 'quality' | 'balanced' | 'custom'
    weights: {
      speed: number
      cost: number
      quality: number
    }
  }
  feedbackLoops: {
    adaptiveIterations: boolean
    maxIterationsPerTask: number
    learningRate: number
    explorationFactor: number
  }
  costControl: {
    dailyBudget: number
    perTaskLimit: number
    preferCheaperModels: boolean
  }
}

const DEFAULT_CONFIG: SwarmConfig = {
  parallelization: {
    maxParallelTasks: 10,
    maxParallelAgents: 5,
    autoScale: true,
    scaleUpThreshold: 80,
    scaleDownThreshold: 20
  },
  intelligenceMode: {
    mode: 'balanced',
    weights: {
      speed: 33,
      cost: 33,
      quality: 34
    }
  },
  feedbackLoops: {
    adaptiveIterations: true,
    maxIterationsPerTask: 7,
    learningRate: 0.01,
    explorationFactor: 10
  },
  costControl: {
    dailyBudget: 100,
    perTaskLimit: 10,
    preferCheaperModels: true
  }
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

export const SwarmConfigPanel: React.FC<SwarmConfigPanelProps> = ({ projectId }) => {
  const [config, setConfig] = useState<SwarmConfig>(DEFAULT_CONFIG)

  const applyPresetMode = (mode: SwarmConfig['intelligenceMode']['mode']) => {
    const presets: Record<string, { speed: number; cost: number; quality: number }> = {
      speed: { speed: 70, cost: 15, quality: 15 },
      cost: { speed: 15, cost: 70, quality: 15 },
      quality: { speed: 15, cost: 15, quality: 70 },
      balanced: { speed: 33, cost: 33, quality: 34 }
    }

    if (mode !== 'custom') {
      setConfig({
        ...config,
        intelligenceMode: {
          mode,
          weights: presets[mode]
        }
      })
    }
  }

  const applyChanges = async () => {
    console.log('Applying Swarm config:', config)
  }

  const resetChanges = () => {
    setConfig(DEFAULT_CONFIG)
  }

  // Calculate current daily usage (mock)
  const currentDailyUsage = 45.20

  return (
    <div className="space-y-6">
      {/* Header Info */}
      <Card className="bg-gradient-to-br from-slate-900 to-slate-800 border-cyan-500/30">
        <CardHeader>
          <CardTitle className="text-cyan-400 flex items-center gap-2">
            <span className="text-2xl">🌊</span>
            Swarm Orchestration
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-sm text-slate-300">
            Configure how the swarm coordinates multiple agents for parallel task execution
          </div>
        </CardContent>
      </Card>

      {/* Parallelization */}
      <CollapsibleSection title="Parallelization" icon="⚡" defaultOpen={true}>
        <div className="space-y-4">
          <div>
            <label className="text-sm text-slate-400 mb-1 block">
              Max Parallel Tasks: {config.parallelization.maxParallelTasks}
            </label>
            <Slider
              value={[config.parallelization.maxParallelTasks]}
              onValueChange={([value]) =>
                setConfig({
                  ...config,
                  parallelization: { ...config.parallelization, maxParallelTasks: value }
                })
              }
              min={1}
              max={50}
              step={1}
            />
          </div>

          <div>
            <label className="text-sm text-slate-400 mb-1 block">
              Max Parallel Agents: {config.parallelization.maxParallelAgents}
            </label>
            <Slider
              value={[config.parallelization.maxParallelAgents]}
              onValueChange={([value]) =>
                setConfig({
                  ...config,
                  parallelization: { ...config.parallelization, maxParallelAgents: value }
                })
              }
              min={1}
              max={20}
              step={1}
            />
          </div>

          <div className="p-3 bg-slate-800/50 rounded">
            <label className="flex items-center justify-between text-sm text-slate-300 mb-3">
              <span>Auto-Scale</span>
              <Switch
                checked={config.parallelization.autoScale}
                onCheckedChange={(checked) =>
                  setConfig({
                    ...config,
                    parallelization: { ...config.parallelization, autoScale: checked }
                  })
                }
              />
            </label>

            {config.parallelization.autoScale && (
              <div className="space-y-3">
                <div>
                  <label className="text-xs text-slate-400 mb-1 block">
                    Scale Up Threshold: {config.parallelization.scaleUpThreshold}%
                  </label>
                  <Slider
                    value={[config.parallelization.scaleUpThreshold]}
                    onValueChange={([value]) =>
                      setConfig({
                        ...config,
                        parallelization: { ...config.parallelization, scaleUpThreshold: value }
                      })
                    }
                    min={50}
                    max={100}
                    step={5}
                  />
                </div>
                <div>
                  <label className="text-xs text-slate-400 mb-1 block">
                    Scale Down Threshold: {config.parallelization.scaleDownThreshold}%
                  </label>
                  <Slider
                    value={[config.parallelization.scaleDownThreshold]}
                    onValueChange={([value]) =>
                      setConfig({
                        ...config,
                        parallelization: { ...config.parallelization, scaleDownThreshold: value }
                      })
                    }
                    min={0}
                    max={50}
                    step={5}
                  />
                </div>
              </div>
            )}
          </div>
        </div>
      </CollapsibleSection>

      {/* Intelligence Mode */}
      <CollapsibleSection title="Intelligence Mode" icon="🧠" defaultOpen={true}>
        <div className="space-y-4">
          <div>
            <label className="text-sm text-slate-400 mb-2 block">Mode</label>
            <div className="grid grid-cols-2 gap-2">
              {(['speed', 'cost', 'quality', 'balanced'] as const).map((mode) => (
                <Button
                  key={mode}
                  onClick={() => applyPresetMode(mode)}
                  size="sm"
                  variant={config.intelligenceMode.mode === mode ? 'default' : 'outline'}
                  className={`${
                    config.intelligenceMode.mode === mode
                      ? 'bg-cyan-500 text-slate-900'
                      : 'border-cyan-500/30 text-cyan-400'
                  }`}
                >
                  {mode === 'speed' && '⚡'}
                  {mode === 'cost' && '💰'}
                  {mode === 'quality' && '🎯'}
                  {mode === 'balanced' && '⚖️'}
                  {' '}
                  {mode.charAt(0).toUpperCase() + mode.slice(1)}
                </Button>
              ))}
            </div>
          </div>

          <div className="p-3 bg-slate-800/50 rounded space-y-3">
            <div className="text-xs text-slate-400 mb-2">Custom Weights</div>
            <div>
              <label className="text-xs text-slate-400 mb-1 block">
                Speed: {config.intelligenceMode.weights.speed}%
              </label>
              <Slider
                value={[config.intelligenceMode.weights.speed]}
                onValueChange={([value]) => {
                  setConfig({
                    ...config,
                    intelligenceMode: {
                      mode: 'custom',
                      weights: { ...config.intelligenceMode.weights, speed: value }
                    }
                  })
                }}
                min={0}
                max={100}
                step={1}
              />
            </div>
            <div>
              <label className="text-xs text-slate-400 mb-1 block">
                Cost: {config.intelligenceMode.weights.cost}%
              </label>
              <Slider
                value={[config.intelligenceMode.weights.cost]}
                onValueChange={([value]) => {
                  setConfig({
                    ...config,
                    intelligenceMode: {
                      mode: 'custom',
                      weights: { ...config.intelligenceMode.weights, cost: value }
                    }
                  })
                }}
                min={0}
                max={100}
                step={1}
              />
            </div>
            <div>
              <label className="text-xs text-slate-400 mb-1 block">
                Quality: {config.intelligenceMode.weights.quality}%
              </label>
              <Slider
                value={[config.intelligenceMode.weights.quality]}
                onValueChange={([value]) => {
                  setConfig({
                    ...config,
                    intelligenceMode: {
                      mode: 'custom',
                      weights: { ...config.intelligenceMode.weights, quality: value }
                    }
                  })
                }}
                min={0}
                max={100}
                step={1}
              />
            </div>
          </div>
        </div>
      </CollapsibleSection>

      {/* Feedback Loops */}
      <CollapsibleSection title="Feedback Loops" icon="🔄">
        <div className="space-y-4">
          <label className="flex items-center justify-between text-sm text-slate-300">
            <span>Adaptive Iterations</span>
            <Switch
              checked={config.feedbackLoops.adaptiveIterations}
              onCheckedChange={(checked) =>
                setConfig({
                  ...config,
                  feedbackLoops: { ...config.feedbackLoops, adaptiveIterations: checked }
                })
              }
            />
          </label>

          <div>
            <label className="text-sm text-slate-400 mb-1 block">
              Max Iterations per Task: {config.feedbackLoops.maxIterationsPerTask}
            </label>
            <Slider
              value={[config.feedbackLoops.maxIterationsPerTask]}
              onValueChange={([value]) =>
                setConfig({
                  ...config,
                  feedbackLoops: { ...config.feedbackLoops, maxIterationsPerTask: value }
                })
              }
              min={2}
              max={20}
              step={1}
            />
          </div>

          <div>
            <label className="text-sm text-slate-400 mb-1 block">
              Learning Rate: {config.feedbackLoops.learningRate.toFixed(3)}
            </label>
            <Slider
              value={[config.feedbackLoops.learningRate * 1000]}
              onValueChange={([value]) =>
                setConfig({
                  ...config,
                  feedbackLoops: { ...config.feedbackLoops, learningRate: value / 1000 }
                })
              }
              min={1}
              max={100}
              step={1}
            />
          </div>

          <div>
            <label className="text-sm text-slate-400 mb-1 block">
              Exploration Factor: {config.feedbackLoops.explorationFactor}%
            </label>
            <Slider
              value={[config.feedbackLoops.explorationFactor]}
              onValueChange={([value]) =>
                setConfig({
                  ...config,
                  feedbackLoops: { ...config.feedbackLoops, explorationFactor: value }
                })
              }
              min={0}
              max={100}
              step={5}
            />
          </div>
        </div>
      </CollapsibleSection>

      {/* Cost Control */}
      <CollapsibleSection title="Cost Control" icon="💰">
        <div className="space-y-4">
          <div>
            <label className="text-sm text-slate-400 mb-1 block">
              Daily Budget: ${config.costControl.dailyBudget}
            </label>
            <Slider
              value={[config.costControl.dailyBudget]}
              onValueChange={([value]) =>
                setConfig({
                  ...config,
                  costControl: { ...config.costControl, dailyBudget: value }
                })
              }
              min={0}
              max={1000}
              step={10}
            />
          </div>

          <div>
            <label className="text-sm text-slate-400 mb-1 block">
              Per-Task Limit: ${config.costControl.perTaskLimit}
            </label>
            <Slider
              value={[config.costControl.perTaskLimit]}
              onValueChange={([value]) =>
                setConfig({
                  ...config,
                  costControl: { ...config.costControl, perTaskLimit: value }
                })
              }
              min={0}
              max={100}
              step={1}
            />
          </div>

          <label className="flex items-center justify-between text-sm text-slate-300">
            <span>Prefer Cheaper Models</span>
            <Switch
              checked={config.costControl.preferCheaperModels}
              onCheckedChange={(checked) =>
                setConfig({
                  ...config,
                  costControl: { ...config.costControl, preferCheaperModels: checked }
                })
              }
            />
          </label>

          <div className="p-3 bg-slate-800/50 rounded">
            <div className="text-xs text-slate-400 mb-2">Current Usage Today</div>
            <div className="mb-2">
              <div className="flex justify-between text-sm mb-1">
                <span className="text-cyan-400">${currentDailyUsage.toFixed(2)}</span>
                <span className="text-slate-400">/ ${config.costControl.dailyBudget}</span>
              </div>
              <div className="w-full h-2 bg-slate-700 rounded-full overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-cyan-500 to-blue-500"
                  style={{ width: `${(currentDailyUsage / config.costControl.dailyBudget) * 100}%` }}
                />
              </div>
            </div>
            <div className="text-xs text-slate-500">
              {((currentDailyUsage / config.costControl.dailyBudget) * 100).toFixed(0)}% of daily budget used
            </div>
          </div>
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
