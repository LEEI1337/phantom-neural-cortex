import React, { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card'
import { Button } from '../ui/button'
import { HRMConfigPanel } from './HRMConfigPanel'
import { SwarmConfigPanel } from './SwarmConfigPanel'
import { AgentConfigPanel } from './AgentConfigPanel'
import { SystemHealthPanel } from './SystemHealthPanel'
import { GlobalSettingsPanel } from './GlobalSettingsPanel'
import ImpactPreviewPanel from './ImpactPreviewPanel'

export type PanelMode = 'hrm' | 'swarm' | 'agent' | 'health' | 'global' | 'impact'

export interface ControlPanelProps {
  initialMode?: PanelMode
  projectId?: string
  onClose?: () => void
}

export const ControlPanel: React.FC<ControlPanelProps> = ({
  initialMode = 'hrm',
  projectId,
  onClose
}) => {
  const [mode, setMode] = useState<PanelMode>(initialMode)

  const modes = [
    { id: 'hrm' as PanelMode, label: 'HRM Config', icon: '🧠' },
    { id: 'swarm' as PanelMode, label: 'Swarm', icon: '🌊' },
    { id: 'agent' as PanelMode, label: 'Agents', icon: '⚡' },
    { id: 'impact' as PanelMode, label: 'Impact', icon: '🔮' },
    { id: 'health' as PanelMode, label: 'Health', icon: '🏥' },
    { id: 'global' as PanelMode, label: 'Settings', icon: '⚙️' }
  ]

  return (
    <div className="w-full h-full flex flex-col">
      {/* Mode Switcher */}
      <div className="flex items-center gap-2 mb-6 p-4 bg-gradient-to-r from-slate-900/90 to-slate-800/90 rounded-lg border border-cyan-500/30">
        {modes.map((m) => (
          <Button
            key={m.id}
            onClick={() => setMode(m.id)}
            variant={mode === m.id ? 'default' : 'outline'}
            size="sm"
            className={`
              transition-all duration-200
              ${mode === m.id
                ? 'bg-cyan-500 text-slate-900 hover:bg-cyan-400 shadow-lg shadow-cyan-500/50'
                : 'bg-slate-800 text-cyan-400 border-cyan-500/30 hover:bg-slate-700 hover:border-cyan-500/50'
              }
            `}
          >
            <span className="mr-1">{m.icon}</span>
            {m.label}
          </Button>
        ))}
        {onClose && (
          <Button
            onClick={onClose}
            variant="ghost"
            size="sm"
            className="ml-auto text-slate-400 hover:text-slate-200"
          >
            ✕
          </Button>
        )}
      </div>

      {/* Panel Content */}
      <div className="flex-1 overflow-y-auto">
        {mode === 'hrm' && <HRMConfigPanel projectId={projectId} />}
        {mode === 'swarm' && <SwarmConfigPanel projectId={projectId} />}
        {mode === 'agent' && <AgentConfigPanel projectId={projectId} />}
        {mode === 'impact' && <ImpactPreviewPanel />}
        {mode === 'health' && <SystemHealthPanel />}
        {mode === 'global' && <GlobalSettingsPanel />}
      </div>
    </div>
  )
}
