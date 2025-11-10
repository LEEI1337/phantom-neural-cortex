/**
 * ConfigEditor Component
 * 5-Dimension Project Configuration Editor
 */

import { useState, useEffect } from 'react'
import { Save, RotateCcw } from 'lucide-react'
import type { ProjectConfiguration, PriorityMode, DeploymentTarget } from '@/lib/types'

interface ConfigEditorProps {
  config: ProjectConfiguration
  onChange: (config: ProjectConfiguration) => void
  onSave: () => void
  isSaving?: boolean
}

export default function ConfigEditor({
  config,
  onChange,
  onSave,
  isSaving = false,
}: ConfigEditorProps) {
  const [localConfig, setLocalConfig] = useState<ProjectConfiguration>(config)
  const [hasChanges, setHasChanges] = useState(false)

  useEffect(() => {
    setLocalConfig(config)
    setHasChanges(false)
  }, [config])

  const updateConfig = (updates: Partial<ProjectConfiguration>) => {
    const newConfig = { ...localConfig, ...updates }
    setLocalConfig(newConfig)
    onChange(newConfig)
    setHasChanges(true)
  }

  const resetConfig = () => {
    setLocalConfig(config)
    onChange(config)
    setHasChanges(false)
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-xl font-semibold">Project Configuration</h3>
          <p className="text-sm text-muted-foreground mt-1">
            Configure the 5 dimensions for optimal performance
          </p>
        </div>
        <div className="flex gap-2">
          {hasChanges && (
            <button
              onClick={resetConfig}
              className="px-4 py-2 border rounded-lg hover:bg-accent flex items-center gap-2"
            >
              <RotateCcw size={16} />
              Reset
            </button>
          )}
          <button
            onClick={onSave}
            disabled={!hasChanges || isSaving}
            className="px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:opacity-90 disabled:opacity-50 flex items-center gap-2"
          >
            <Save size={16} />
            {isSaving ? 'Saving...' : 'Save Configuration'}
          </button>
        </div>
      </div>

      {/* Dimension 1: Priorität */}
      <DimensionCard title="1. Priority" description="Balance between speed, cost, and quality">
        <PriorityConfig
          priority={localConfig.priority}
          onChange={(priority) => updateConfig({ priority })}
        />
      </DimensionCard>

      {/* Dimension 2: Zeitrahmen */}
      <DimensionCard title="2. Timeframe" description="Maximum time per task">
        <TimeframeConfig
          timeframe={localConfig.timeframe}
          onChange={(timeframe) => updateConfig({ timeframe })}
        />
      </DimensionCard>

      {/* Dimension 3: Risikotoleranz */}
      <DimensionCard
        title="3. Risk Tolerance"
        description="Experimental features and ML capabilities"
      >
        <RiskToleranceConfig
          riskTolerance={localConfig.risk_tolerance}
          onChange={(risk_tolerance) => updateConfig({ risk_tolerance })}
        />
      </DimensionCard>

      {/* Dimension 4: Deployment */}
      <DimensionCard title="4. Deployment" description="Target platforms and containerization">
        <DeploymentConfig
          deployment={localConfig.deployment}
          onChange={(deployment) => updateConfig({ deployment })}
        />
      </DimensionCard>

      {/* Dimension 5: ML Components */}
      <DimensionCard
        title="5. ML Components"
        description="Enable/disable advanced ML optimizations"
      >
        <MLComponentsConfig
          mlComponents={localConfig.ml_components}
          onChange={(ml_components) => updateConfig({ ml_components })}
        />
      </DimensionCard>
    </div>
  )
}

function DimensionCard({
  title,
  description,
  children,
}: {
  title: string
  description: string
  children: React.ReactNode
}) {
  return (
    <div className="border rounded-lg p-6 bg-card">
      <div className="mb-4">
        <h4 className="text-lg font-semibold">{title}</h4>
        <p className="text-sm text-muted-foreground mt-1">{description}</p>
      </div>
      {children}
    </div>
  )
}

// ===== DIMENSION 1: PRIORITY =====

function PriorityConfig({
  priority,
  onChange,
}: {
  priority: ProjectConfiguration['priority']
  onChange: (priority: ProjectConfiguration['priority']) => void
}) {
  const modes: { value: PriorityMode; label: string; description: string }[] = [
    { value: 'performance', label: 'Performance', description: 'Speed first, quality second' },
    { value: 'cost', label: 'Cost', description: 'Minimize costs, use free tiers' },
    { value: 'quality', label: 'Quality', description: 'Maximum quality, cost secondary' },
    { value: 'balanced', label: 'Balanced', description: 'Balance all factors equally' },
    { value: 'custom', label: 'Custom', description: 'Manual weight configuration' },
  ]

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
        {modes.map((mode) => (
          <button
            key={mode.value}
            onClick={() => onChange({ mode: mode.value })}
            className={`p-4 border rounded-lg text-left transition-all ${
              priority.mode === mode.value
                ? 'border-primary bg-primary/10 ring-2 ring-primary'
                : 'border-border hover:border-primary/50'
            }`}
          >
            <div className="font-medium text-sm mb-1">{mode.label}</div>
            <div className="text-xs text-muted-foreground">{mode.description}</div>
          </button>
        ))}
      </div>

      {priority.mode === 'custom' && (
        <div className="mt-6 p-4 border rounded-lg bg-muted/50">
          <h5 className="font-medium mb-4">Custom Weights</h5>
          <div className="space-y-4">
            <SliderInput
              label="Speed"
              value={priority.custom_weights?.speed ?? 0.33}
              onChange={(speed) =>
                onChange({
                  ...priority,
                  custom_weights: { ...priority.custom_weights!, speed },
                })
              }
            />
            <SliderInput
              label="Cost Optimization"
              value={priority.custom_weights?.cost ?? 0.33}
              onChange={(cost) =>
                onChange({
                  ...priority,
                  custom_weights: { ...priority.custom_weights!, cost },
                })
              }
            />
            <SliderInput
              label="Quality"
              value={priority.custom_weights?.quality ?? 0.34}
              onChange={(quality) =>
                onChange({
                  ...priority,
                  custom_weights: { ...priority.custom_weights!, quality },
                })
              }
            />
          </div>
        </div>
      )}
    </div>
  )
}

// ===== DIMENSION 2: TIMEFRAME =====

function TimeframeConfig({
  timeframe,
  onChange,
}: {
  timeframe: ProjectConfiguration['timeframe']
  onChange: (timeframe: ProjectConfiguration['timeframe']) => void
}) {
  const presets = [
    { value: 'sprint' as const, label: 'Sprint', minutes: 15 },
    { value: 'standard' as const, label: 'Standard', minutes: 30 },
    { value: 'deep-work' as const, label: 'Deep Work', minutes: 60 },
    { value: 'marathon' as const, label: 'Marathon', minutes: 120 },
    { value: 'custom' as const, label: 'Custom', minutes: 0 },
  ]

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
        {presets.map((preset) => (
          <button
            key={preset.value}
            onClick={() =>
              onChange({
                preset: preset.value,
                max_minutes: preset.minutes || timeframe.max_minutes,
              })
            }
            className={`p-4 border rounded-lg text-left ${
              timeframe.preset === preset.value
                ? 'border-primary bg-primary/10'
                : 'border-border hover:border-primary/50'
            }`}
          >
            <div className="font-medium mb-1">{preset.label}</div>
            {preset.minutes > 0 && (
              <div className="text-sm text-muted-foreground">{preset.minutes} min</div>
            )}
          </button>
        ))}
      </div>

      {timeframe.preset === 'custom' && (
        <div className="mt-4">
          <label className="block text-sm font-medium mb-2">
            Maximum Minutes: {timeframe.max_minutes}
          </label>
          <input
            type="range"
            min="5"
            max="180"
            step="5"
            value={timeframe.max_minutes}
            onChange={(e) =>
              onChange({ ...timeframe, max_minutes: parseInt(e.target.value) })
            }
            className="w-full"
          />
          <div className="flex justify-between text-xs text-muted-foreground mt-1">
            <span>5 min</span>
            <span>180 min</span>
          </div>
        </div>
      )}
    </div>
  )
}

// ===== DIMENSION 3: RISK TOLERANCE =====

function RiskToleranceConfig({
  riskTolerance,
  onChange,
}: {
  riskTolerance: ProjectConfiguration['risk_tolerance']
  onChange: (riskTolerance: ProjectConfiguration['risk_tolerance']) => void
}) {
  const getLevelLabel = (level: number) => {
    if (level < 30) return 'Conservative'
    if (level < 60) return 'Moderate'
    if (level < 85) return 'Aggressive'
    return 'Cutting Edge'
  }

  return (
    <div className="space-y-6">
      <div>
        <div className="flex justify-between items-center mb-2">
          <label className="text-sm font-medium">Risk Level</label>
          <span className="text-sm font-medium text-primary">
            {riskTolerance.level}% - {getLevelLabel(riskTolerance.level)}
          </span>
        </div>
        <input
          type="range"
          min="0"
          max="100"
          value={riskTolerance.level}
          onChange={(e) =>
            onChange({ ...riskTolerance, level: parseInt(e.target.value) })
          }
          className="w-full"
        />
        <div className="flex justify-between text-xs text-muted-foreground mt-1">
          <span>Conservative (0%)</span>
          <span>Cutting Edge (100%)</span>
        </div>
      </div>

      <div className="space-y-3">
        <label className="flex items-center gap-3 cursor-pointer">
          <input
            type="checkbox"
            checked={riskTolerance.allow_experimental}
            onChange={(e) =>
              onChange({ ...riskTolerance, allow_experimental: e.target.checked })
            }
            className="w-4 h-4"
          />
          <div>
            <div className="font-medium text-sm">Allow Experimental Features</div>
            <div className="text-xs text-muted-foreground">
              Beta optimizations and experimental ML models
            </div>
          </div>
        </label>

        <label className="flex items-center gap-3 cursor-pointer">
          <input
            type="checkbox"
            checked={riskTolerance.ml_features_enabled}
            onChange={(e) =>
              onChange({ ...riskTolerance, ml_features_enabled: e.target.checked })
            }
            className="w-4 h-4"
          />
          <div>
            <div className="font-medium text-sm">Enable ML Features</div>
            <div className="text-xs text-muted-foreground">
              Adaptive learning and predictive optimizations
            </div>
          </div>
        </label>
      </div>
    </div>
  )
}

// ===== DIMENSION 4: DEPLOYMENT =====

function DeploymentConfig({
  deployment,
  onChange,
}: {
  deployment: ProjectConfiguration['deployment']
  onChange: (deployment: ProjectConfiguration['deployment']) => void
}) {
  const targets: { value: DeploymentTarget; label: string; icon: string }[] = [
    { value: 'windows', label: 'Windows', icon: '🪟' },
    { value: 'linux', label: 'Linux', icon: '🐧' },
    { value: 'macos', label: 'macOS', icon: '🍎' },
    { value: 'kubernetes', label: 'Kubernetes', icon: '☸️' },
    { value: 'cross-platform', label: 'Cross-Platform', icon: '🌐' },
  ]

  const toggleTarget = (target: DeploymentTarget) => {
    const current = deployment.targets
    const newTargets = current.includes(target)
      ? current.filter((t) => t !== target)
      : [...current, target]

    onChange({ ...deployment, targets: newTargets })
  }

  return (
    <div className="space-y-6">
      <div>
        <label className="block text-sm font-medium mb-3">Target Platforms</label>
        <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
          {targets.map((target) => (
            <button
              key={target.value}
              onClick={() => toggleTarget(target.value)}
              className={`p-4 border rounded-lg text-center ${
                deployment.targets.includes(target.value)
                  ? 'border-primary bg-primary/10'
                  : 'border-border hover:border-primary/50'
              }`}
            >
              <div className="text-2xl mb-1">{target.icon}</div>
              <div className="text-sm font-medium">{target.label}</div>
            </button>
          ))}
        </div>
      </div>

      <div className="space-y-3">
        <label className="flex items-center gap-3 cursor-pointer">
          <input
            type="checkbox"
            checked={deployment.docker_enabled}
            onChange={(e) =>
              onChange({ ...deployment, docker_enabled: e.target.checked })
            }
            className="w-4 h-4"
          />
          <div>
            <div className="font-medium text-sm">Docker Enabled</div>
            <div className="text-xs text-muted-foreground">Containerized execution</div>
          </div>
        </label>

        <label className="flex items-center gap-3 cursor-pointer">
          <input
            type="checkbox"
            checked={deployment.kubernetes_enabled}
            onChange={(e) =>
              onChange({ ...deployment, kubernetes_enabled: e.target.checked })
            }
            className="w-4 h-4"
          />
          <div>
            <div className="font-medium text-sm">Kubernetes Enabled</div>
            <div className="text-xs text-muted-foreground">Multi-node orchestration</div>
          </div>
        </label>
      </div>
    </div>
  )
}

// ===== DIMENSION 5: ML COMPONENTS =====

function MLComponentsConfig({
  mlComponents,
  onChange,
}: {
  mlComponents: ProjectConfiguration['ml_components']
  onChange: (mlComponents: ProjectConfiguration['ml_components']) => void
}) {
  const components = [
    {
      key: 'adaptive_iterations' as const,
      label: 'Adaptive Iteration Limits',
      description: 'ML predicts optimal iteration count (2-10 vs fixed 5)',
      impact: 'Speed: +15-25%',
    },
    {
      key: 'quality_weight_learning' as const,
      label: 'Quality Weight Learning',
      description: 'Auto-optimize quality weights per project type',
      impact: 'Quality: +5-10%',
    },
    {
      key: 'latent_reasoning' as const,
      label: 'Latent Reasoning Layer',
      description: 'Compress feedback to 512D vectors for efficiency',
      impact: 'Tokens: -40%',
    },
    {
      key: 'agent_switching' as const,
      label: 'Smart Agent Switching',
      description: 'Mid-task agent changes based on requirements',
      impact: 'Cost: -15%',
    },
    {
      key: 'inference_time_scaling' as const,
      label: 'Inference-Time Scaling',
      description: 'Generalize to higher computational limits',
      impact: 'Quality: +8%',
    },
  ]

  return (
    <div className="space-y-3">
      {components.map((comp) => (
        <label
          key={comp.key}
          className="flex items-start gap-3 p-4 border rounded-lg cursor-pointer hover:bg-accent/50"
        >
          <input
            type="checkbox"
            checked={mlComponents[comp.key]}
            onChange={(e) =>
              onChange({ ...mlComponents, [comp.key]: e.target.checked })
            }
            className="w-4 h-4 mt-1"
          />
          <div className="flex-1">
            <div className="font-medium mb-1">{comp.label}</div>
            <div className="text-sm text-muted-foreground mb-1">{comp.description}</div>
            <div className="text-xs text-primary font-medium">{comp.impact}</div>
          </div>
        </label>
      ))}
    </div>
  )
}

// ===== HELPER COMPONENTS =====

function SliderInput({
  label,
  value,
  onChange,
}: {
  label: string
  value: number
  onChange: (value: number) => void
}) {
  return (
    <div>
      <div className="flex justify-between items-center mb-2">
        <label className="text-sm font-medium">{label}</label>
        <span className="text-sm text-muted-foreground">{(value * 100).toFixed(0)}%</span>
      </div>
      <input
        type="range"
        min="0"
        max="1"
        step="0.01"
        value={value}
        onChange={(e) => onChange(parseFloat(e.target.value))}
        className="w-full"
      />
    </div>
  )
}
