/**
 * HRM Impact Visualization Component
 * Real-time visualization of HRM configuration impact
 */

import { useState, useEffect } from 'react'
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from './ui/card'
import { Badge } from './ui/badge'
import {
  DollarSign,
  Zap,
  Target,
  ArrowRight,
  TrendingUp,
  TrendingDown,
  Minus,
  AlertTriangle,
  CheckCircle,
} from 'lucide-react'

interface ImpactMetrics {
  cost: {
    current: number
    predicted: number
    change_percent: number
    confidence: number
  }
  speed: {
    current: number
    predicted: number
    change_percent: number
    confidence: number
  }
  quality: {
    current: number
    predicted: number
    change_percent: number
    confidence: number
  }
  tokens: {
    current: number
    predicted: number
    change_percent: number
    confidence: number
  }
}

interface HRMImpactVisualizationProps {
  impact: ImpactMetrics | null
  warnings?: string[]
  recommendations?: string[]
}

export function HRMImpactVisualization({
  impact,
  warnings = [],
  recommendations = [],
}: HRMImpactVisualizationProps) {
  if (!impact) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Impact Analysis</CardTitle>
          <CardDescription>
            Make changes to see predicted impact
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="text-center py-8 text-gray-400">
            <Target className="w-12 h-12 mx-auto mb-2 opacity-50" />
            <p>No changes detected</p>
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <div className="space-y-4">
      {/* Impact Metrics Grid */}
      <div className="grid grid-cols-2 gap-4">
        <ImpactCard
          title="Cost Impact"
          icon={DollarSign}
          current={impact.cost.current}
          predicted={impact.cost.predicted}
          changePercent={impact.cost.change_percent}
          confidence={impact.cost.confidence}
          unit="$"
          inverse={true}
        />
        <ImpactCard
          title="Speed Impact"
          icon={Zap}
          current={impact.speed.current}
          predicted={impact.speed.predicted}
          changePercent={impact.speed.change_percent}
          confidence={impact.speed.confidence}
          unit="s"
          inverse={true}
        />
        <ImpactCard
          title="Quality Impact"
          icon={Target}
          current={impact.quality.current}
          predicted={impact.quality.predicted}
          changePercent={impact.quality.change_percent}
          confidence={impact.quality.confidence}
          unit="%"
          multiplier={100}
        />
        <ImpactCard
          title="Token Usage"
          icon={ArrowRight}
          current={impact.tokens.current}
          predicted={impact.tokens.predicted}
          changePercent={impact.tokens.change_percent}
          confidence={impact.tokens.confidence}
          unit=""
          inverse={true}
        />
      </div>

      {/* Warnings */}
      {warnings.length > 0 && (
        <Card className="border-yellow-200 bg-yellow-50">
          <CardHeader>
            <CardTitle className="text-yellow-800 flex items-center gap-2 text-base">
              <AlertTriangle className="w-5 h-5" />
              Warnings
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="space-y-1 text-sm text-yellow-700">
              {warnings.map((warning, i) => (
                <li key={i} className="flex items-start gap-2">
                  <span className="text-yellow-400 mt-0.5">•</span>
                  {warning}
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
      )}

      {/* Recommendations */}
      {recommendations.length > 0 && (
        <Card className="border-blue-200 bg-blue-50">
          <CardHeader>
            <CardTitle className="text-blue-800 flex items-center gap-2 text-base">
              <CheckCircle className="w-5 h-5" />
              Recommendations
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="space-y-1 text-sm text-blue-700">
              {recommendations.map((rec, i) => (
                <li key={i} className="flex items-start gap-2">
                  <span className="text-blue-400 mt-0.5">•</span>
                  {rec}
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
      )}
    </div>
  )
}

interface ImpactCardProps {
  title: string
  icon: any
  current: number
  predicted: number
  changePercent: number
  confidence: number
  unit: string
  inverse?: boolean
  multiplier?: number
}

function ImpactCard({
  title,
  icon: Icon,
  current,
  predicted,
  changePercent,
  confidence,
  unit,
  inverse = false,
  multiplier = 1,
}: ImpactCardProps) {
  const isPositive = inverse ? changePercent < 0 : changePercent > 0
  const isNegative = inverse ? changePercent > 0 : changePercent < 0
  const isNeutral = Math.abs(changePercent) < 1

  const color = isPositive
    ? 'text-green-600'
    : isNegative
    ? 'text-red-600'
    : 'text-gray-600'

  const bgColor = isPositive
    ? 'bg-green-50 border-green-200'
    : isNegative
    ? 'bg-red-50 border-red-200'
    : 'bg-gray-50 border-gray-200'

  return (
    <Card className={bgColor}>
      <CardContent className="p-4">
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-2">
            <Icon className={`w-5 h-5 ${color}`} />
            <h4 className="font-medium text-sm">{title}</h4>
          </div>
          <Badge variant={isPositive ? 'success' : isNegative ? 'danger' : 'default'}>
            {confidence}% conf
          </Badge>
        </div>

        <div className="space-y-2">
          {/* Current → Predicted */}
          <div className="flex items-center justify-between text-sm">
            <span className="text-gray-500">Current:</span>
            <span className="font-semibold">
              {unit === '%' ? (current * multiplier).toFixed(1) : current.toFixed(2)}
              {unit}
            </span>
          </div>

          <div className="flex items-center justify-center">
            <ArrowRight className="w-4 h-4 text-gray-400" />
          </div>

          <div className="flex items-center justify-between text-sm">
            <span className="text-gray-500">Predicted:</span>
            <span className={`font-semibold ${color}`}>
              {unit === '%' ? (predicted * multiplier).toFixed(1) : predicted.toFixed(2)}
              {unit}
            </span>
          </div>

          {/* Change Badge */}
          <div className="pt-2 mt-2 border-t border-gray-200">
            <div className={`flex items-center justify-center gap-1 ${color} font-semibold`}>
              {isPositive && <TrendingUp className="w-4 h-4" />}
              {isNegative && <TrendingDown className="w-4 h-4" />}
              {isNeutral && <Minus className="w-4 h-4" />}
              <span>
                {changePercent > 0 && '+'}
                {changePercent.toFixed(1)}%
              </span>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
