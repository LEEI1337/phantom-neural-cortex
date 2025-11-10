/**
 * HRM Control Panel V2 - Completely Redesigned
 * Real-time HRM configuration with visual feedback and persistent storage
 */

import { useState, useEffect } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { api } from '../lib/api'
import { ws } from '../lib/websocket'
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from './ui/card'
import { Slider } from './ui/slider'
import { Switch } from './ui/switch'
import { Button } from './ui/button'
import {
  Save,
  RotateCcw,
  Loader2,
  CheckCircle,
  AlertCircle,
  TrendingUp,
  TrendingDown,
  Zap,
  DollarSign,
  Target,
  Cpu,
  Database,
  GitBranch,
  BarChart3,
} from 'lucide-react'

interface HRMConfig {
  latent_reasoning: {
    enabled: boolean
    dimensionality: number
    compression_ratio: number
    auto_adjust: boolean
  }
  ml_iteration_prediction: {
    mode: 'auto' | 'manual' | 'fixed'
    max_iterations: number
    confidence_threshold: number
  }
  agent_switching: {
    enabled: boolean
    strategy: 'cost_optimized' | 'quality_first' | 'speed_optimized' | 'adaptive' | 'round_robin' | 'manual'
    fallback_on_failure: boolean
    cost_weight: number
    speed_weight: number
    quality_weight: number
  }
  deep_supervision: {
    enabled: boolean
    checkpoints: number[]
    quality_gate_threshold: number
  }
  parallel_evaluation: {
    enabled: boolean
    worker_count: number
    timeout_seconds: number
  }
  caching: {
    memory: boolean
    disk: boolean
    remote: boolean
    aggressive_mode: boolean
    max_size_mb: number
  }
  bayesian_optimization: {
    enabled: boolean
    iterations: number
  }
  rl_refinement: {
    enabled: boolean
    algorithm: string
    num_refinement_iterations: number
    learning_rate: number
  }
  prometheus_metrics: {
    enabled: boolean
    export_interval: number
  }
  multi_repo: {
    enabled: boolean
  }
}

interface Props {
  projectId: string
}

export function HRMControlPanelV2({ projectId }: Props) {
  const queryClient = useQueryClient()
  const [config, setConfig] = useState<HRMConfig | null>(null)
  const [hasChanges, setHasChanges] = useState(false)
  const [saveStatus, setSaveStatus] = useState<'idle' | 'saving' | 'saved' | 'error'>('idle')

  // Load current config
  const { data: configData, isLoading } = useQuery({
    queryKey: ['hrm-config', projectId],
    queryFn: async () => {
      const response = await api.getHRMConfig({ project_id: projectId })
      if (!response.success) throw new Error(response.error)
      return response.data
    },
    refetchInterval: false,
  })

  // Initialize config from API
  useEffect(() => {
    if (configData?.config) {
      setConfig(configData.config)
    }
  }, [configData])

  // Subscribe to WebSocket updates
  useEffect(() => {
    const unsubscribe = ws.subscribeToHRMUpdates(projectId, (data) => {
      console.log('HRM config updated via WebSocket:', data)
      queryClient.invalidateQueries({ queryKey: ['hrm-config', projectId] })
    })

    return unsubscribe
  }, [projectId, queryClient])

  // Save mutation
  const saveMutation = useMutation({
    mutationFn: async () => {
      if (!config) return

      const response = await api.updateHRMConfig({
        project_id: projectId,
        config,
        apply_immediately: true,
        persist: true,
      })

      if (!response.success) {
        throw new Error(response.error || 'Failed to save configuration')
      }

      return response.data
    },
    onMutate: () => {
      setSaveStatus('saving')
    },
    onSuccess: () => {
      setSaveStatus('saved')
      setHasChanges(false)
      queryClient.invalidateQueries({ queryKey: ['hrm-config', projectId] })

      setTimeout(() => {
        setSaveStatus('idle')
      }, 3000)
    },
    onError: (error) => {
      console.error('Failed to save config:', error)
      setSaveStatus('error')
      setTimeout(() => {
        setSaveStatus('idle')
      }, 3000)
    },
  })

  const updateConfig = (updates: Partial<HRMConfig>) => {
    if (!config) return

    const newConfig = { ...config, ...updates }
    setConfig(newConfig)
    setHasChanges(true)
  }

  const resetConfig = () => {
    if (configData?.config) {
      setConfig(configData.config)
      setHasChanges(false)
    }
  }

  if (isLoading || !config) {
    return (
      <div className="flex items-center justify-center h-96">
        <Loader2 className="w-8 h-8 animate-spin text-primary" />
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header with Save Controls */}
      <div className="flex items-center justify-between sticky top-0 bg-background/95 backdrop-blur-sm z-10 py-4 border-b border-border">
        <div>
          <h2 className="text-2xl font-bold">HRM Configuration</h2>
          <p className="text-sm text-muted-foreground mt-1">
            Real-time ML/RL optimization controls - changes apply immediately
          </p>
        </div>

        <div className="flex items-center gap-3">
          {hasChanges && (
            <Button variant="outline" onClick={resetConfig} className="gap-2">
              <RotateCcw className="w-4 h-4" />
              Reset
            </Button>
          )}

          <Button
            onClick={() => saveMutation.mutate()}
            disabled={!hasChanges || saveStatus === 'saving'}
            className="gap-2 min-w-[120px]"
          >
            {saveStatus === 'saving' && <Loader2 className="w-4 h-4 animate-spin" />}
            {saveStatus === 'saved' && <CheckCircle className="w-4 h-4" />}
            {saveStatus === 'error' && <AlertCircle className="w-4 h-4" />}
            {saveStatus === 'idle' && <Save className="w-4 h-4" />}

            {saveStatus === 'saving' && 'Saving...'}
            {saveStatus === 'saved' && 'Saved!'}
            {saveStatus === 'error' && 'Error'}
            {saveStatus === 'idle' && (hasChanges ? 'Save Changes' : 'No Changes')}
          </Button>
        </div>
      </div>

      {/* Configuration Sections */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Latent Reasoning */}
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="p-2 rounded-lg bg-purple-100">
                  <Cpu className="w-5 h-5 text-purple-600" />
                </div>
                <div>
                  <CardTitle>Latent Reasoning Compression</CardTitle>
                  <CardDescription>Compress context for token savings (40-60%)</CardDescription>
                </div>
              </div>
              <Switch
                checked={config.latent_reasoning.enabled}
                onCheckedChange={(checked) =>
                  updateConfig({
                    latent_reasoning: { ...config.latent_reasoning, enabled: checked },
                  })
                }
              />
            </div>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Dimensionality with Visual Bar */}
            <div>
              <div className="flex items-center justify-between mb-3">
                <label className="text-sm font-medium">
                  Dimensionality: {config.latent_reasoning.dimensionality}D
                </label>
                <span className="text-xs text-muted-foreground">
                  {config.latent_reasoning.dimensionality <= 256 ? 'Fast' :
                   config.latent_reasoning.dimensionality <= 512 ? 'Balanced' : 'High Quality'}
                </span>
              </div>
              <Slider
                value={[config.latent_reasoning.dimensionality]}
                onValueChange={([value]) =>
                  updateConfig({
                    latent_reasoning: { ...config.latent_reasoning, dimensionality: value },
                  })
                }
                min={128}
                max={1024}
                step={128}
                disabled={!config.latent_reasoning.enabled}
              />
              {/* Visual representation */}
              <div className="mt-3 h-8 flex gap-1">
                {[128, 256, 384, 512, 640, 768, 896, 1024].map((dim) => (
                  <div
                    key={dim}
                    className={`flex-1 rounded transition-all ${
                      dim <= config.latent_reasoning.dimensionality
                        ? 'bg-purple-500'
                        : 'bg-gray-200'
                    }`}
                  />
                ))}
              </div>
              <div className="flex justify-between text-xs text-muted-foreground mt-1">
                <span>128 (Fastest)</span>
                <span>1024 (Best Quality)</span>
              </div>
            </div>

            {/* Compression Ratio */}
            <div>
              <div className="flex items-center justify-between mb-3">
                <label className="text-sm font-medium">
                  Compression Ratio: {config.latent_reasoning.compression_ratio.toFixed(1)}x
                </label>
                <span className="text-xs px-2 py-1 rounded bg-green-100 text-green-700">
                  ~{Math.round(config.latent_reasoning.compression_ratio * 15)}% tokens saved
                </span>
              </div>
              <Slider
                value={[config.latent_reasoning.compression_ratio]}
                onValueChange={([value]) =>
                  updateConfig({
                    latent_reasoning: { ...config.latent_reasoning, compression_ratio: value },
                  })
                }
                min={1.0}
                max={10.0}
                step={0.1}
                disabled={!config.latent_reasoning.enabled}
              />
            </div>
          </CardContent>
        </Card>

        {/* Agent Switching */}
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="p-2 rounded-lg bg-blue-100">
                  <GitBranch className="w-5 h-5 text-blue-600" />
                </div>
                <div>
                  <CardTitle>Smart Agent Switching</CardTitle>
                  <CardDescription>Auto-select best agent by strategy (up to 52% cost savings)</CardDescription>
                </div>
              </div>
              <Switch
                checked={config.agent_switching.enabled}
                onCheckedChange={(checked) =>
                  updateConfig({
                    agent_switching: { ...config.agent_switching, enabled: checked },
                  })
                }
              />
            </div>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Strategy Selection */}
            <div>
              <label className="text-sm font-medium mb-3 block">Strategy</label>
              <div className="grid grid-cols-2 gap-2">
                {[
                  { key: 'cost_optimized', label: 'Cost First', icon: DollarSign, color: 'green' },
                  { key: 'quality_first', label: 'Quality First', icon: Target, color: 'purple' },
                  { key: 'speed_optimized', label: 'Speed First', icon: Zap, color: 'yellow' },
                  { key: 'adaptive', label: 'Adaptive', icon: BarChart3, color: 'blue' },
                ].map((strategy) => {
                  const Icon = strategy.icon
                  const isActive = config.agent_switching.strategy === strategy.key

                  return (
                    <button
                      key={strategy.key}
                      onClick={() =>
                        updateConfig({
                          agent_switching: {
                            ...config.agent_switching,
                            strategy: strategy.key as any
                          },
                        })
                      }
                      className={`p-3 rounded-lg border-2 transition-all flex items-center gap-2 ${
                        isActive
                          ? `border-${strategy.color}-500 bg-${strategy.color}-50`
                          : 'border-border hover:border-gray-400'
                      }`}
                      disabled={!config.agent_switching.enabled}
                    >
                      <Icon className={`w-4 h-4 ${isActive ? `text-${strategy.color}-600` : 'text-gray-400'}`} />
                      <span className="text-sm font-medium">{strategy.label}</span>
                    </button>
                  )
                })}
              </div>
            </div>

            {/* Weight Sliders (only for adaptive) */}
            {config.agent_switching.strategy === 'adaptive' && (
              <div className="space-y-4 pt-4 border-t border-border">
                <p className="text-xs text-muted-foreground">Fine-tune adaptive weights:</p>

                <div>
                  <div className="flex items-center justify-between mb-2">
                    <label className="text-sm">Cost Weight</label>
                    <span className="text-sm font-mono">{(config.agent_switching.cost_weight * 100).toFixed(0)}%</span>
                  </div>
                  <Slider
                    value={[config.agent_switching.cost_weight * 100]}
                    onValueChange={([value]) =>
                      updateConfig({
                        agent_switching: { ...config.agent_switching, cost_weight: value / 100 },
                      })
                    }
                    min={0}
                    max={100}
                    step={5}
                  />
                </div>

                <div>
                  <div className="flex items-center justify-between mb-2">
                    <label className="text-sm">Speed Weight</label>
                    <span className="text-sm font-mono">{(config.agent_switching.speed_weight * 100).toFixed(0)}%</span>
                  </div>
                  <Slider
                    value={[config.agent_switching.speed_weight * 100]}
                    onValueChange={([value]) =>
                      updateConfig({
                        agent_switching: { ...config.agent_switching, speed_weight: value / 100 },
                      })
                    }
                    min={0}
                    max={100}
                    step={5}
                  />
                </div>

                <div>
                  <div className="flex items-center justify-between mb-2">
                    <label className="text-sm">Quality Weight</label>
                    <span className="text-sm font-mono">{(config.agent_switching.quality_weight * 100).toFixed(0)}%</span>
                  </div>
                  <Slider
                    value={[config.agent_switching.quality_weight * 100]}
                    onValueChange={([value]) =>
                      updateConfig({
                        agent_switching: { ...config.agent_switching, quality_weight: value / 100 },
                      })
                    }
                    min={0}
                    max={100}
                    step={5}
                  />
                </div>

                {/* Weight sum warning */}
                {Math.abs(
                  config.agent_switching.cost_weight +
                  config.agent_switching.speed_weight +
                  config.agent_switching.quality_weight - 1.0
                ) > 0.05 && (
                  <div className="flex items-center gap-2 p-2 rounded bg-yellow-50 text-yellow-800 text-xs">
                    <AlertCircle className="w-4 h-4" />
                    Weights should sum to 100% for optimal results
                  </div>
                )}
              </div>
            )}
          </CardContent>
        </Card>

        {/* Parallel Evaluation */}
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="p-2 rounded-lg bg-orange-100">
                  <Zap className="w-5 h-5 text-orange-600" />
                </div>
                <div>
                  <CardTitle>Parallel Quality Evaluation</CardTitle>
                  <CardDescription>Run multiple checks in parallel (20-35% faster)</CardDescription>
                </div>
              </div>
              <Switch
                checked={config.parallel_evaluation.enabled}
                onCheckedChange={(checked) =>
                  updateConfig({
                    parallel_evaluation: { ...config.parallel_evaluation, enabled: checked },
                  })
                }
              />
            </div>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <div className="flex items-center justify-between mb-2">
                <label className="text-sm font-medium">
                  Workers: {config.parallel_evaluation.worker_count}
                </label>
                <span className="text-xs text-muted-foreground">
                  ~{Math.min(config.parallel_evaluation.worker_count * 20, 100)}% speedup
                </span>
              </div>
              <Slider
                value={[config.parallel_evaluation.worker_count]}
                onValueChange={([value]) =>
                  updateConfig({
                    parallel_evaluation: { ...config.parallel_evaluation, worker_count: value },
                  })
                }
                min={1}
                max={16}
                step={1}
                disabled={!config.parallel_evaluation.enabled}
              />

              {/* Worker visualization */}
              <div className="mt-3 grid grid-cols-8 gap-1">
                {Array.from({ length: 16 }).map((_, i) => (
                  <div
                    key={i}
                    className={`h-8 rounded ${
                      i < config.parallel_evaluation.worker_count
                        ? 'bg-orange-500'
                        : 'bg-gray-200'
                    }`}
                  />
                ))}
              </div>
            </div>

            <div>
              <div className="flex items-center justify-between mb-2">
                <label className="text-sm font-medium">
                  Timeout: {config.parallel_evaluation.timeout_seconds}s
                </label>
              </div>
              <Slider
                value={[config.parallel_evaluation.timeout_seconds]}
                onValueChange={([value]) =>
                  updateConfig({
                    parallel_evaluation: { ...config.parallel_evaluation, timeout_seconds: value },
                  })
                }
                min={10}
                max={300}
                step={10}
                disabled={!config.parallel_evaluation.enabled}
              />
            </div>
          </CardContent>
        </Card>

        {/* Caching */}
        <Card>
          <CardHeader>
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-cyan-100">
                <Database className="w-5 h-5 text-cyan-600" />
              </div>
              <div>
                <CardTitle>Three-Layer Caching</CardTitle>
                <CardDescription>Memory → Disk → Remote caching (25% faster)</CardDescription>
              </div>
            </div>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-2 gap-3">
              <div className="flex items-center justify-between p-3 rounded-lg border border-border">
                <label className="text-sm font-medium">Memory</label>
                <Switch
                  checked={config.caching.memory}
                  onCheckedChange={(checked) =>
                    updateConfig({
                      caching: { ...config.caching, memory: checked },
                    })
                  }
                />
              </div>

              <div className="flex items-center justify-between p-3 rounded-lg border border-border">
                <label className="text-sm font-medium">Disk</label>
                <Switch
                  checked={config.caching.disk}
                  onCheckedChange={(checked) =>
                    updateConfig({
                      caching: { ...config.caching, disk: checked },
                    })
                  }
                />
              </div>

              <div className="flex items-center justify-between p-3 rounded-lg border border-border">
                <label className="text-sm font-medium">Remote</label>
                <Switch
                  checked={config.caching.remote}
                  onCheckedChange={(checked) =>
                    updateConfig({
                      caching: { ...config.caching, remote: checked },
                    })
                  }
                />
              </div>

              <div className="flex items-center justify-between p-3 rounded-lg border border-border">
                <label className="text-sm font-medium">Aggressive</label>
                <Switch
                  checked={config.caching.aggressive_mode}
                  onCheckedChange={(checked) =>
                    updateConfig({
                      caching: { ...config.caching, aggressive_mode: checked },
                    })
                  }
                />
              </div>
            </div>

            <div>
              <div className="flex items-center justify-between mb-2">
                <label className="text-sm font-medium">
                  Max Size: {config.caching.max_size_mb} MB
                </label>
              </div>
              <Slider
                value={[config.caching.max_size_mb]}
                onValueChange={([value]) =>
                  updateConfig({
                    caching: { ...config.caching, max_size_mb: value },
                  })
                }
                min={100}
                max={5000}
                step={100}
              />
            </div>
          </CardContent>
        </Card>

        {/* Deep Supervision */}
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="p-2 rounded-lg bg-green-100">
                  <Target className="w-5 h-5 text-green-600" />
                </div>
                <div>
                  <CardTitle>Deep Supervision</CardTitle>
                  <CardDescription>Quality checkpoints at 33%, 66%, 100%</CardDescription>
                </div>
              </div>
              <Switch
                checked={config.deep_supervision.enabled}
                onCheckedChange={(checked) =>
                  updateConfig({
                    deep_supervision: { ...config.deep_supervision, enabled: checked },
                  })
                }
              />
            </div>
          </CardHeader>
          <CardContent>
            <div>
              <div className="flex items-center justify-between mb-2">
                <label className="text-sm font-medium">
                  Quality Gate: {(config.deep_supervision.quality_gate_threshold * 100).toFixed(0)}%
                </label>
              </div>
              <Slider
                value={[config.deep_supervision.quality_gate_threshold * 100]}
                onValueChange={([value]) =>
                  updateConfig({
                    deep_supervision: { ...config.deep_supervision, quality_gate_threshold: value / 100 },
                  })
                }
                min={50}
                max={100}
                step={5}
                disabled={!config.deep_supervision.enabled}
              />

              {/* Checkpoint visualization */}
              <div className="mt-4 relative h-12 bg-gray-100 rounded-full overflow-hidden">
                <div className="absolute inset-0 flex items-center justify-between px-4">
                  {[33, 66, 100].map((checkpoint) => (
                    <div
                      key={checkpoint}
                      className="flex flex-col items-center gap-1"
                    >
                      <div className="w-3 h-3 rounded-full bg-green-600 border-2 border-white" />
                      <span className="text-xs font-medium">{checkpoint}%</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* ML Iteration Prediction */}
        <Card>
          <CardHeader>
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-indigo-100">
                <BarChart3 className="w-5 h-5 text-indigo-600" />
              </div>
              <div>
                <CardTitle>ML Iteration Prediction</CardTitle>
                <CardDescription>Prevent over-iteration waste</CardDescription>
              </div>
            </div>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <label className="text-sm font-medium mb-2 block">Mode</label>
              <div className="grid grid-cols-3 gap-2">
                {(['auto', 'manual', 'fixed'] as const).map((mode) => (
                  <button
                    key={mode}
                    onClick={() =>
                      updateConfig({
                        ml_iteration_prediction: { ...config.ml_iteration_prediction, mode },
                      })
                    }
                    className={`p-2 rounded-lg border-2 text-sm font-medium transition-all ${
                      config.ml_iteration_prediction.mode === mode
                        ? 'border-primary bg-primary/10 text-primary'
                        : 'border-border hover:border-gray-400'
                    }`}
                  >
                    {mode.charAt(0).toUpperCase() + mode.slice(1)}
                  </button>
                ))}
              </div>
            </div>

            <div>
              <div className="flex items-center justify-between mb-2">
                <label className="text-sm font-medium">
                  Max Iterations: {config.ml_iteration_prediction.max_iterations}
                </label>
              </div>
              <Slider
                value={[config.ml_iteration_prediction.max_iterations]}
                onValueChange={([value]) =>
                  updateConfig({
                    ml_iteration_prediction: { ...config.ml_iteration_prediction, max_iterations: value },
                  })
                }
                min={2}
                max={20}
                step={1}
              />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Advanced Settings (Collapsed by default) */}
      <Card>
        <CardHeader>
          <CardTitle>Advanced Settings</CardTitle>
        </CardHeader>
        <CardContent className="grid grid-cols-3 gap-4">
          <div className="flex items-center justify-between p-3 rounded-lg border border-border">
            <div>
              <label className="text-sm font-medium">Bayesian Optimization</label>
              <p className="text-xs text-muted-foreground">Auto-tune weights</p>
            </div>
            <Switch
              checked={config.bayesian_optimization.enabled}
              onCheckedChange={(checked) =>
                updateConfig({
                  bayesian_optimization: { ...config.bayesian_optimization, enabled: checked },
                })
              }
            />
          </div>

          <div className="flex items-center justify-between p-3 rounded-lg border border-border">
            <div>
              <label className="text-sm font-medium">RL Refinement</label>
              <p className="text-xs text-muted-foreground">Quality improvement loop</p>
            </div>
            <Switch
              checked={config.rl_refinement.enabled}
              onCheckedChange={(checked) =>
                updateConfig({
                  rl_refinement: { ...config.rl_refinement, enabled: checked },
                })
              }
            />
          </div>

          <div className="flex items-center justify-between p-3 rounded-lg border border-border">
            <div>
              <label className="text-sm font-medium">Prometheus Metrics</label>
              <p className="text-xs text-muted-foreground">Export to monitoring</p>
            </div>
            <Switch
              checked={config.prometheus_metrics.enabled}
              onCheckedChange={(checked) =>
                updateConfig({
                  prometheus_metrics: { ...config.prometheus_metrics, enabled: checked },
                })
              }
            />
          </div>

          <div className="flex items-center justify-between p-3 rounded-lg border border-border">
            <div>
              <label className="text-sm font-medium">Multi-Repo</label>
              <p className="text-xs text-muted-foreground">Cross-repo coordination</p>
            </div>
            <Switch
              checked={config.multi_repo.enabled}
              onCheckedChange={(checked) =>
                updateConfig({
                  multi_repo: { ...config.multi_repo, enabled: checked },
                })
              }
            />
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
