/**
 * HRM Control Panel Component
 * Real-time control over 12 ML/RL optimization parameters
 */

import { useState, useEffect } from 'react'
import { api } from '../lib/api'
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from './ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs'
import { Slider } from './ui/slider'
import { Switch } from './ui/switch'
import { Button } from './ui/button'
import { Badge } from './ui/badge'
import {
  Settings,
  Zap,
  DollarSign,
  Target,
  Scale,
  TrendingUp,
  TrendingDown,
  ArrowRight,
  Loader2,
  Check,
  AlertTriangle,
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

interface ImpactEstimate {
  cost_change: number
  speed_change: number
  quality_change: number
  token_reduction: number
}

interface HRMControlPanelProps {
  projectId: string
  onConfigChange?: (config: HRMConfig) => void
}

export function HRMControlPanel({ projectId, onConfigChange }: HRMControlPanelProps) {
  const [config, setConfig] = useState<HRMConfig | null>(null)
  const [originalConfig, setOriginalConfig] = useState<HRMConfig | null>(null)
  const [impact, setImpact] = useState<ImpactEstimate | null>(null)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [hasChanges, setHasChanges] = useState(false)

  // Load current configuration
  useEffect(() => {
    loadConfig()
  }, [projectId])

  const loadConfig = async () => {
    setLoading(true)
    const response = await api.getHRMConfig({ project_id: projectId })

    if (response.success && response.data) {
      // API returns {config_id, preset_name, config: {...}}, extract config object
      const configData = response.data.config || response.data
      setConfig(configData)
      setOriginalConfig(JSON.parse(JSON.stringify(configData)))
    } else {
      // Load default config
      const defaultConfig: HRMConfig = {
        latent_reasoning: {
          enabled: true,
          dimensionality: 512,
          compression_ratio: 3.8,
          auto_adjust: false,
        },
        ml_iteration_prediction: {
          mode: 'auto',
          max_iterations: 7,
          confidence_threshold: 0.80,
        },
        agent_switching: {
          enabled: true,
          strategy: 'adaptive',
          fallback_on_failure: true,
          cost_weight: 0.33,
          speed_weight: 0.33,
          quality_weight: 0.34,
        },
        deep_supervision: {
          enabled: true,
          checkpoints: [0.33, 0.66, 1.00],
          quality_gate_threshold: 0.75,
        },
        parallel_evaluation: {
          enabled: true,
          worker_count: 4,
          timeout_seconds: 60,
        },
        caching: {
          memory: true,
          disk: true,
          remote: false,
          aggressive_mode: true,
          max_size_mb: 500,
        },
        bayesian_optimization: {
          enabled: false,
          iterations: 30,
        },
        rl_refinement: {
          enabled: true,
          algorithm: 'ppo',
          num_refinement_iterations: 3,
          learning_rate: 0.0003,
        },
        prometheus_metrics: {
          enabled: true,
          export_interval: 15,
        },
        multi_repo: {
          enabled: true,
        },
      }
      setConfig(defaultConfig)
      setOriginalConfig(JSON.parse(JSON.stringify(defaultConfig)))
    }
    setLoading(false)
  }

  // Update configuration and calculate impact
  const updateConfig = async (newConfig: HRMConfig) => {
    setConfig(newConfig)
    setHasChanges(true)

    if (onConfigChange) {
      onConfigChange(newConfig)
    }

    // Simulate impact
    if (originalConfig) {
      const response = await api.simulateHRMImpact({
        current_config: originalConfig,
        proposed_config: newConfig,
        task_context: {
          complexity: 10,
          estimated_duration: 450,
          current_quality: 0.87,
        },
      })

      if (response.success && response.data) {
        setImpact({
          cost_change: response.data.impact_analysis.cost.change_percent / 100,
          speed_change: response.data.impact_analysis.speed.change_percent / 100,
          quality_change: response.data.impact_analysis.quality.change_percent / 100,
          token_reduction: response.data.impact_analysis.tokens.change_percent / 100,
        })
      }
    }
  }

  // Apply configuration
  const applyConfig = async () => {
    if (!config) return

    setSaving(true)
    const response = await api.updateHRMConfig({
      project_id: projectId,
      config,
      apply_immediately: true,
      persist: true,
    })

    if (response.success) {
      setOriginalConfig(JSON.parse(JSON.stringify(config)))
      setHasChanges(false)
      setImpact(null)
    }
    setSaving(false)
  }

  // Reset to original
  const resetConfig = () => {
    if (originalConfig) {
      setConfig(JSON.parse(JSON.stringify(originalConfig)))
      setHasChanges(false)
      setImpact(null)
    }
  }

  if (loading || !config) {
    return (
      <div className="flex items-center justify-center h-96">
        <Loader2 className="w-8 h-8 animate-spin text-blue-500" />
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header with Impact Preview */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold flex items-center gap-2">
            <Settings className="w-6 h-6" />
            HRM Control Panel
          </h2>
          <p className="text-gray-500 mt-1">
            Real-time control over 12 ML/RL optimization parameters
          </p>
        </div>

        {hasChanges && impact && (
          <div className="flex items-center gap-4">
            <ImpactPreview impact={impact} />
            <Button onClick={applyConfig} disabled={saving} className="gap-2">
              {saving ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  Applying...
                </>
              ) : (
                <>
                  <Check className="w-4 h-4" />
                  Apply Changes
                </>
              )}
            </Button>
            <Button onClick={resetConfig} variant="outline">
              Reset
            </Button>
          </div>
        )}
      </div>

      {/* Tabs for different parameter categories */}
      <Tabs defaultValue="core" className="w-full">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="core">Core Optimizations</TabsTrigger>
          <TabsTrigger value="agents">Agent Control</TabsTrigger>
          <TabsTrigger value="quality">Quality & Testing</TabsTrigger>
          <TabsTrigger value="advanced">Advanced</TabsTrigger>
        </TabsList>

        {/* Core Optimizations Tab */}
        <TabsContent value="core" className="space-y-4">
          {/* Latent Reasoning */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                <span>Latent Reasoning Compression</span>
                <Switch
                  checked={config.latent_reasoning.enabled}
                  onCheckedChange={(checked) =>
                    updateConfig({
                      ...config,
                      latent_reasoning: { ...config.latent_reasoning, enabled: checked },
                    })
                  }
                />
              </CardTitle>
              <CardDescription>
                Compress context into lower-dimensional vectors for token savings
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <label className="text-sm font-medium mb-2 block">
                  Dimensionality: {config.latent_reasoning.dimensionality}D
                </label>
                <Slider
                  value={[config.latent_reasoning.dimensionality]}
                  onValueChange={([value]) =>
                    updateConfig({
                      ...config,
                      latent_reasoning: { ...config.latent_reasoning, dimensionality: value },
                    })
                  }
                  min={128}
                  max={1024}
                  step={128}
                  disabled={!config.latent_reasoning.enabled}
                />
                <div className="flex justify-between text-xs text-gray-500 mt-1">
                  <span>128 (Fast)</span>
                  <span>1024 (High Quality)</span>
                </div>
              </div>

              <div>
                <label className="text-sm font-medium mb-2 block">
                  Compression Ratio: {config.latent_reasoning.compression_ratio.toFixed(1)}x
                </label>
                <Slider
                  value={[config.latent_reasoning.compression_ratio]}
                  onValueChange={([value]) =>
                    updateConfig({
                      ...config,
                      latent_reasoning: { ...config.latent_reasoning, compression_ratio: value },
                    })
                  }
                  min={1.0}
                  max={10.0}
                  step={0.1}
                  disabled={!config.latent_reasoning.enabled}
                />
                <div className="flex justify-between text-xs text-gray-500 mt-1">
                  <span>1.0x (No compression)</span>
                  <span>10.0x (Maximum compression)</span>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* ML Iteration Prediction */}
          <Card>
            <CardHeader>
              <CardTitle>ML Iteration Prediction</CardTitle>
              <CardDescription>
                Predict optimal iteration count to prevent over-iteration
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <label className="text-sm font-medium mb-2 block">Mode</label>
                <div className="flex gap-2">
                  {(['auto', 'manual', 'fixed'] as const).map((mode) => (
                    <Button
                      key={mode}
                      variant={config.ml_iteration_prediction.mode === mode ? 'default' : 'outline'}
                      onClick={() =>
                        updateConfig({
                          ...config,
                          ml_iteration_prediction: { ...config.ml_iteration_prediction, mode },
                        })
                      }
                      className="flex-1"
                    >
                      {mode.charAt(0).toUpperCase() + mode.slice(1)}
                    </Button>
                  ))}
                </div>
              </div>

              <div>
                <label className="text-sm font-medium mb-2 block">
                  Max Iterations: {config.ml_iteration_prediction.max_iterations}
                </label>
                <Slider
                  value={[config.ml_iteration_prediction.max_iterations]}
                  onValueChange={([value]) =>
                    updateConfig({
                      ...config,
                      ml_iteration_prediction: { ...config.ml_iteration_prediction, max_iterations: value },
                    })
                  }
                  min={2}
                  max={20}
                  step={1}
                />
              </div>

              <div>
                <label className="text-sm font-medium mb-2 block">
                  Confidence Threshold: {(config.ml_iteration_prediction.confidence_threshold * 100).toFixed(0)}%
                </label>
                <Slider
                  value={[config.ml_iteration_prediction.confidence_threshold * 100]}
                  onValueChange={([value]) =>
                    updateConfig({
                      ...config,
                      ml_iteration_prediction: {
                        ...config.ml_iteration_prediction,
                        confidence_threshold: value / 100,
                      },
                    })
                  }
                  min={0}
                  max={100}
                  step={5}
                />
              </div>
            </CardContent>
          </Card>

          {/* Caching */}
          <Card>
            <CardHeader>
              <CardTitle>Three-Layer Caching</CardTitle>
              <CardDescription>
                Memory → Disk → Remote caching for speed optimization
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="flex items-center justify-between">
                  <label className="text-sm font-medium">Memory Cache</label>
                  <Switch
                    checked={config.caching.memory}
                    onCheckedChange={(checked) =>
                      updateConfig({
                        ...config,
                        caching: { ...config.caching, memory: checked },
                      })
                    }
                  />
                </div>
                <div className="flex items-center justify-between">
                  <label className="text-sm font-medium">Disk Cache</label>
                  <Switch
                    checked={config.caching.disk}
                    onCheckedChange={(checked) =>
                      updateConfig({
                        ...config,
                        caching: { ...config.caching, disk: checked },
                      })
                    }
                  />
                </div>
                <div className="flex items-center justify-between">
                  <label className="text-sm font-medium">Remote Cache</label>
                  <Switch
                    checked={config.caching.remote}
                    onCheckedChange={(checked) =>
                      updateConfig({
                        ...config,
                        caching: { ...config.caching, remote: checked },
                      })
                    }
                  />
                </div>
                <div className="flex items-center justify-between">
                  <label className="text-sm font-medium">Aggressive Mode</label>
                  <Switch
                    checked={config.caching.aggressive_mode}
                    onCheckedChange={(checked) =>
                      updateConfig({
                        ...config,
                        caching: { ...config.caching, aggressive_mode: checked },
                      })
                    }
                  />
                </div>
              </div>

              <div>
                <label className="text-sm font-medium mb-2 block">
                  Max Size: {config.caching.max_size_mb} MB
                </label>
                <Slider
                  value={[config.caching.max_size_mb]}
                  onValueChange={([value]) =>
                    updateConfig({
                      ...config,
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
        </TabsContent>

        {/* Agent Control Tab */}
        <TabsContent value="agents" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Smart Agent Switching</CardTitle>
              <CardDescription>
                Automatically switch between agents based on cost, quality, and speed
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <label className="text-sm font-medium mb-2 block">Strategy</label>
                <div className="grid grid-cols-3 gap-2">
                  {(['cost_optimized', 'quality_first', 'speed_optimized', 'adaptive'] as const).map((strategy) => (
                    <Button
                      key={strategy}
                      variant={config.agent_switching.strategy === strategy ? 'default' : 'outline'}
                      onClick={() =>
                        updateConfig({
                          ...config,
                          agent_switching: { ...config.agent_switching, strategy },
                        })
                      }
                      className="text-xs"
                    >
                      {strategy.replace('_', ' ').charAt(0).toUpperCase() +
                        strategy.replace('_', ' ').slice(1)}
                    </Button>
                  ))}
                </div>
              </div>

              <div>
                <label className="text-sm font-medium mb-2 block">
                  Cost Weight: {(config.agent_switching.cost_weight * 100).toFixed(0)}%
                </label>
                <Slider
                  value={[config.agent_switching.cost_weight * 100]}
                  onValueChange={([value]) =>
                    updateConfig({
                      ...config,
                      agent_switching: { ...config.agent_switching, cost_weight: value / 100 },
                    })
                  }
                  min={0}
                  max={100}
                  step={5}
                />
              </div>

              <div>
                <label className="text-sm font-medium mb-2 block">
                  Speed Weight: {(config.agent_switching.speed_weight * 100).toFixed(0)}%
                </label>
                <Slider
                  value={[config.agent_switching.speed_weight * 100]}
                  onValueChange={([value]) =>
                    updateConfig({
                      ...config,
                      agent_switching: { ...config.agent_switching, speed_weight: value / 100 },
                    })
                  }
                  min={0}
                  max={100}
                  step={5}
                />
              </div>

              <div>
                <label className="text-sm font-medium mb-2 block">
                  Quality Weight: {(config.agent_switching.quality_weight * 100).toFixed(0)}%
                </label>
                <Slider
                  value={[config.agent_switching.quality_weight * 100]}
                  onValueChange={([value]) =>
                    updateConfig({
                      ...config,
                      agent_switching: { ...config.agent_switching, quality_weight: value / 100 },
                    })
                  }
                  min={0}
                  max={100}
                  step={5}
                />
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Quality & Testing Tab */}
        <TabsContent value="quality" className="space-y-4">
          {/* Deep Supervision */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                <span>Deep Supervision Checkpoints</span>
                <Switch
                  checked={config.deep_supervision.enabled}
                  onCheckedChange={(checked) =>
                    updateConfig({
                      ...config,
                      deep_supervision: { ...config.deep_supervision, enabled: checked },
                    })
                  }
                />
              </CardTitle>
              <CardDescription>
                Quality checkpoints at 33%, 66%, 100% with auto-rollback
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <label className="text-sm font-medium mb-2 block">
                  Quality Gate Threshold: {(config.deep_supervision.quality_gate_threshold * 100).toFixed(0)}%
                </label>
                <Slider
                  value={[config.deep_supervision.quality_gate_threshold * 100]}
                  onValueChange={([value]) =>
                    updateConfig({
                      ...config,
                      deep_supervision: { ...config.deep_supervision, quality_gate_threshold: value / 100 },
                    })
                  }
                  min={50}
                  max={100}
                  step={5}
                  disabled={!config.deep_supervision.enabled}
                />
              </div>
            </CardContent>
          </Card>

          {/* Parallel Evaluation */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                <span>Parallel Quality Evaluation</span>
                <Switch
                  checked={config.parallel_evaluation.enabled}
                  onCheckedChange={(checked) =>
                    updateConfig({
                      ...config,
                      parallel_evaluation: { ...config.parallel_evaluation, enabled: checked },
                    })
                  }
                />
              </CardTitle>
              <CardDescription>
                Run multiple quality checks in parallel for faster results
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <label className="text-sm font-medium mb-2 block">
                  Worker Count: {config.parallel_evaluation.worker_count}
                </label>
                <Slider
                  value={[config.parallel_evaluation.worker_count]}
                  onValueChange={([value]) =>
                    updateConfig({
                      ...config,
                      parallel_evaluation: { ...config.parallel_evaluation, worker_count: value },
                    })
                  }
                  min={1}
                  max={16}
                  step={1}
                  disabled={!config.parallel_evaluation.enabled}
                />
              </div>

              <div>
                <label className="text-sm font-medium mb-2 block">
                  Timeout: {config.parallel_evaluation.timeout_seconds}s
                </label>
                <Slider
                  value={[config.parallel_evaluation.timeout_seconds]}
                  onValueChange={([value]) =>
                    updateConfig({
                      ...config,
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
        </TabsContent>

        {/* Advanced Tab */}
        <TabsContent value="advanced" className="space-y-4">
          {/* Bayesian Optimization */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                <span>Bayesian Weight Optimization</span>
                <Switch
                  checked={config.bayesian_optimization.enabled}
                  onCheckedChange={(checked) =>
                    updateConfig({
                      ...config,
                      bayesian_optimization: { ...config.bayesian_optimization, enabled: checked },
                    })
                  }
                />
              </CardTitle>
              <CardDescription>
                Optimize parameter weights using Bayesian methods
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div>
                <label className="text-sm font-medium mb-2 block">
                  Iterations: {config.bayesian_optimization.iterations}
                </label>
                <Slider
                  value={[config.bayesian_optimization.iterations]}
                  onValueChange={([value]) =>
                    updateConfig({
                      ...config,
                      bayesian_optimization: { ...config.bayesian_optimization, iterations: value },
                    })
                  }
                  min={10}
                  max={100}
                  step={5}
                  disabled={!config.bayesian_optimization.enabled}
                />
              </div>
            </CardContent>
          </Card>

          {/* RL Refinement */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                <span>RL Refinement Chain (PPO)</span>
                <Switch
                  checked={config.rl_refinement.enabled}
                  onCheckedChange={(checked) =>
                    updateConfig({
                      ...config,
                      rl_refinement: { ...config.rl_refinement, enabled: checked },
                    })
                  }
                />
              </CardTitle>
              <CardDescription>
                Reinforcement learning for quality improvement
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <label className="text-sm font-medium mb-2 block">
                  Refinement Iterations: {config.rl_refinement.num_refinement_iterations}
                </label>
                <Slider
                  value={[config.rl_refinement.num_refinement_iterations]}
                  onValueChange={([value]) =>
                    updateConfig({
                      ...config,
                      rl_refinement: { ...config.rl_refinement, num_refinement_iterations: value },
                    })
                  }
                  min={1}
                  max={10}
                  step={1}
                  disabled={!config.rl_refinement.enabled}
                />
              </div>

              <div>
                <label className="text-sm font-medium mb-2 block">
                  Learning Rate: {config.rl_refinement.learning_rate.toFixed(4)}
                </label>
                <Slider
                  value={[config.rl_refinement.learning_rate * 10000]}
                  onValueChange={([value]) =>
                    updateConfig({
                      ...config,
                      rl_refinement: { ...config.rl_refinement, learning_rate: value / 10000 },
                    })
                  }
                  min={1}
                  max={1000}
                  step={1}
                  disabled={!config.rl_refinement.enabled}
                />
                <div className="flex justify-between text-xs text-gray-500 mt-1">
                  <span>0.0001</span>
                  <span>0.1000</span>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Other Settings */}
          <Card>
            <CardHeader>
              <CardTitle>Additional Settings</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <label className="text-sm font-medium">Prometheus Metrics</label>
                  <p className="text-xs text-gray-500">Export metrics for monitoring</p>
                </div>
                <Switch
                  checked={config.prometheus_metrics.enabled}
                  onCheckedChange={(checked) =>
                    updateConfig({
                      ...config,
                      prometheus_metrics: { ...config.prometheus_metrics, enabled: checked },
                    })
                  }
                />
              </div>

              {config.prometheus_metrics.enabled && (
                <div>
                  <label className="text-sm font-medium mb-2 block">
                    Export Interval: {config.prometheus_metrics.export_interval}s
                  </label>
                  <Slider
                    value={[config.prometheus_metrics.export_interval]}
                    onValueChange={([value]) =>
                      updateConfig({
                        ...config,
                        prometheus_metrics: { ...config.prometheus_metrics, export_interval: value },
                      })
                    }
                    min={5}
                    max={60}
                    step={5}
                  />
                </div>
              )}

              <div className="flex items-center justify-between">
                <div>
                  <label className="text-sm font-medium">Multi-Repository Coordination</label>
                  <p className="text-xs text-gray-500">Cross-repo consistency</p>
                </div>
                <Switch
                  checked={config.multi_repo.enabled}
                  onCheckedChange={(checked) =>
                    updateConfig({
                      ...config,
                      multi_repo: { ...config.multi_repo, enabled: checked },
                    })
                  }
                />
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}

// Impact Preview Component
function ImpactPreview({ impact }: { impact: ImpactEstimate }) {
  return (
    <div className="flex gap-3">
      <ImpactBadge
        label="Cost"
        value={impact.cost_change}
        icon={DollarSign}
      />
      <ImpactBadge
        label="Speed"
        value={impact.speed_change}
        icon={Zap}
      />
      <ImpactBadge
        label="Quality"
        value={impact.quality_change}
        icon={Target}
      />
      <ImpactBadge
        label="Tokens"
        value={impact.token_reduction}
        icon={ArrowRight}
        inverse
      />
    </div>
  )
}

function ImpactBadge({
  label,
  value,
  icon: Icon,
  inverse = false,
}: {
  label: string
  value: number
  icon: any
  inverse?: boolean
}) {
  const isPositive = inverse ? value < 0 : value > 0
  const color = isPositive ? 'text-green-600' : value < 0 ? 'text-red-600' : 'text-gray-600'
  const bgColor = isPositive ? 'bg-green-50' : value < 0 ? 'bg-red-50' : 'bg-gray-50'

  return (
    <div className={`flex items-center gap-2 px-3 py-2 rounded-lg ${bgColor}`}>
      <Icon className={`w-4 h-4 ${color}`} />
      <div>
        <div className="text-xs text-gray-500">{label}</div>
        <div className={`text-sm font-semibold ${color} flex items-center gap-1`}>
          {value > 0 && !inverse && <TrendingUp className="w-3 h-3" />}
          {value < 0 && !inverse && <TrendingDown className="w-3 h-3" />}
          {inverse && value < 0 && <TrendingUp className="w-3 h-3" />}
          {inverse && value > 0 && <TrendingDown className="w-3 h-3" />}
          {Math.abs(value * 100).toFixed(0)}%
        </div>
      </div>
    </div>
  )
}
