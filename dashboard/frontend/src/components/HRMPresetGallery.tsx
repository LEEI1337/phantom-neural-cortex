/**
 * HRM Preset Gallery Component
 * Browse and apply built-in and custom HRM presets
 */

import { useState, useEffect } from 'react'
import { api } from '../lib/api'
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from './ui/card'
import { Button } from './ui/button'
import { Badge } from './ui/badge'
import {
  Zap,
  DollarSign,
  Target,
  Scale,
  Plus,
  Check,
  Loader2,
  TrendingUp,
  TrendingDown,
  Star,
  Clock,
} from 'lucide-react'

interface HRMPreset {
  id: string
  name: string
  description: string
  icon: string
  color: string
  builtin: boolean
  config: any
  usage_stats: {
    usage_count: number
    avg_quality: number | null
    avg_cost: number | null
    avg_duration: number | null
  }
}

interface HRMPresetGalleryProps {
  projectId: string
  onPresetApplied?: (preset: HRMPreset) => void
}

export function HRMPresetGallery({ projectId, onPresetApplied }: HRMPresetGalleryProps) {
  const [presets, setPresets] = useState<HRMPreset[]>([])
  const [loading, setLoading] = useState(true)
  const [applying, setApplying] = useState<string | null>(null)
  const [filter, setFilter] = useState<'all' | 'builtin' | 'custom'>('all')

  useEffect(() => {
    loadPresets()
  }, [])

  const loadPresets = async () => {
    setLoading(true)
    const response = await api.getHRMPresets({ include_builtin: true })

    if (response.success && response.data) {
      // API returns array directly, not {presets: [...]}
      setPresets(Array.isArray(response.data) ? response.data : response.data.presets || [])
    }
    setLoading(false)
  }

  const applyPreset = async (preset: HRMPreset) => {
    setApplying(preset.id)

    const response = await api.applyHRMPreset(preset.id, {
      project_id: projectId,
      apply_immediately: true,
    })

    if (response.success) {
      if (onPresetApplied) {
        onPresetApplied(preset)
      }
      // Show success notification
      setTimeout(() => setApplying(null), 1000)
    } else {
      setApplying(null)
    }
  }

  const filteredPresets = presets.filter((preset) => {
    if (filter === 'builtin') return preset.builtin
    if (filter === 'custom') return !preset.builtin
    return true
  })

  const builtinPresets = [
    {
      key: 'speed_optimized',
      icon: '⚡',
      color: '#FFD700',
      gradient: 'from-yellow-400 to-orange-500',
    },
    {
      key: 'cost_optimized',
      icon: '💰',
      color: '#4CAF50',
      gradient: 'from-green-400 to-emerald-600',
    },
    {
      key: 'quality_first',
      icon: '🎯',
      color: '#9C27B0',
      gradient: 'from-purple-400 to-pink-600',
    },
    {
      key: 'balanced',
      icon: '⚖️',
      color: '#2196F3',
      gradient: 'from-blue-400 to-cyan-600',
    },
  ]

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="w-8 h-8 animate-spin text-blue-500" />
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold">HRM Presets</h2>
          <p className="text-gray-500 mt-1">
            Quick-apply optimized configurations for different scenarios
          </p>
        </div>

        <Button variant="outline" className="gap-2">
          <Plus className="w-4 h-4" />
          Create Custom Preset
        </Button>
      </div>

      {/* Filter Tabs */}
      <div className="flex gap-2">
        <Button
          variant={filter === 'all' ? 'default' : 'outline'}
          onClick={() => setFilter('all')}
          size="sm"
        >
          All Presets ({presets.length})
        </Button>
        <Button
          variant={filter === 'builtin' ? 'default' : 'outline'}
          onClick={() => setFilter('builtin')}
          size="sm"
        >
          Built-in ({presets.filter((p) => p.builtin).length})
        </Button>
        <Button
          variant={filter === 'custom' ? 'default' : 'outline'}
          onClick={() => setFilter('custom')}
          size="sm"
        >
          Custom ({presets.filter((p) => !p.builtin).length})
        </Button>
      </div>

      {/* Preset Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {filteredPresets.map((preset) => {
          const presetMeta = builtinPresets.find((p) => preset.name === p.key)

          return (
            <PresetCard
              key={preset.id}
              preset={preset}
              gradient={presetMeta?.gradient}
              isApplying={applying === preset.id}
              onApply={() => applyPreset(preset)}
            />
          )
        })}
      </div>

      {filteredPresets.length === 0 && (
        <div className="text-center py-12">
          <p className="text-gray-500">No presets found</p>
        </div>
      )}
    </div>
  )
}

interface PresetCardProps {
  preset: HRMPreset
  gradient?: string
  isApplying: boolean
  onApply: () => void
}

function PresetCard({ preset, gradient, isApplying, onApply }: PresetCardProps) {
  return (
    <Card className="relative overflow-hidden hover:shadow-lg transition-shadow">
      {/* Gradient Background */}
      {gradient && (
        <div
          className={`absolute top-0 left-0 right-0 h-24 bg-gradient-to-r ${gradient} opacity-10`}
        />
      )}

      <CardHeader className="relative">
        <div className="flex items-start justify-between">
          <div className="flex items-center gap-3">
            <div
              className="text-4xl"
              style={{ filter: 'drop-shadow(0 2px 4px rgba(0,0,0,0.1))' }}
            >
              {preset.icon}
            </div>
            <div>
              <CardTitle className="flex items-center gap-2">
                {preset.name.replace(/_/g, ' ').replace(/\b\w/g, (l) => l.toUpperCase())}
                {preset.builtin && (
                  <Badge variant="info" className="text-xs">
                    Built-in
                  </Badge>
                )}
              </CardTitle>
              <CardDescription className="mt-1">
                {preset.description}
              </CardDescription>
            </div>
          </div>
        </div>
      </CardHeader>

      <CardContent className="space-y-4 relative">
        {/* Stats */}
        {preset.usage_stats.usage_count > 0 && (
          <div className="grid grid-cols-3 gap-3">
            <StatBadge
              icon={Star}
              label="Uses"
              value={preset.usage_stats.usage_count}
            />
            {preset.usage_stats.avg_quality !== null && (
              <StatBadge
                icon={Target}
                label="Avg Quality"
                value={`${(preset.usage_stats.avg_quality * 100).toFixed(0)}%`}
              />
            )}
            {preset.usage_stats.avg_cost !== null && (
              <StatBadge
                icon={DollarSign}
                label="Avg Cost"
                value={`$${preset.usage_stats.avg_cost.toFixed(2)}`}
              />
            )}
          </div>
        )}

        {/* Config Preview */}
        <div className="flex flex-wrap gap-2">
          {preset.config.latent_reasoning?.enabled && (
            <Badge variant="default">
              Latent Reasoning ({preset.config.latent_reasoning.dimensionality}D)
            </Badge>
          )}
          {preset.config.agent_switching?.strategy && (
            <Badge variant="default">
              {preset.config.agent_switching.strategy.replace(/_/g, ' ')}
            </Badge>
          )}
          {preset.config.deep_supervision?.enabled && (
            <Badge variant="success">Deep Supervision</Badge>
          )}
          {preset.config.parallel_evaluation?.enabled && (
            <Badge variant="info">
              Parallel Eval ({preset.config.parallel_evaluation.worker_count})
            </Badge>
          )}
          {preset.config.caching?.aggressive_mode && (
            <Badge variant="warning">Aggressive Cache</Badge>
          )}
        </div>

        {/* Apply Button */}
        <Button
          onClick={onApply}
          disabled={isApplying}
          className="w-full"
        >
          {isApplying ? (
            <>
              <Loader2 className="w-4 h-4 mr-2 animate-spin" />
              Applying...
            </>
          ) : (
            <>
              <Check className="w-4 h-4 mr-2" />
              Apply Preset
            </>
          )}
        </Button>
      </CardContent>
    </Card>
  )
}

function StatBadge({
  icon: Icon,
  label,
  value,
}: {
  icon: any
  label: string
  value: string | number
}) {
  return (
    <div className="flex flex-col items-center p-2 bg-gray-50 rounded-lg">
      <Icon className="w-4 h-4 text-gray-400 mb-1" />
      <div className="text-xs text-gray-500">{label}</div>
      <div className="text-sm font-semibold">{value}</div>
    </div>
  )
}
