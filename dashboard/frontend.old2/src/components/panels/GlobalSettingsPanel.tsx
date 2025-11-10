import React, { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card'
import { Button } from '../ui/button'
import { Switch } from '../ui/switch'

export interface GlobalSettingsPanelProps {}

interface GlobalSettings {
  notifications: {
    email: boolean
    push: boolean
    desktop: boolean
    slack: boolean
  }
  security: {
    twoFactorAuth: boolean
    sessionTimeout: number
    apiKeyRotation: boolean
    auditLogging: boolean
  }
  performance: {
    enableCaching: boolean
    compressionLevel: number
    maxConcurrentTasks: number
    requestThrottling: boolean
  }
  integrations: {
    github: boolean
    gitlab: boolean
    prometheus: boolean
    grafana: boolean
    slack: boolean
  }
  advanced: {
    debugMode: boolean
    experimentalFeatures: boolean
    telemetry: boolean
    autoUpdate: boolean
  }
}

const DEFAULT_SETTINGS: GlobalSettings = {
  notifications: {
    email: true,
    push: false,
    desktop: true,
    slack: true
  },
  security: {
    twoFactorAuth: true,
    sessionTimeout: 30,
    apiKeyRotation: true,
    auditLogging: true
  },
  performance: {
    enableCaching: true,
    compressionLevel: 6,
    maxConcurrentTasks: 10,
    requestThrottling: true
  },
  integrations: {
    github: true,
    gitlab: false,
    prometheus: true,
    grafana: true,
    slack: true
  },
  advanced: {
    debugMode: false,
    experimentalFeatures: false,
    telemetry: true,
    autoUpdate: true
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

export const GlobalSettingsPanel: React.FC<GlobalSettingsPanelProps> = () => {
  const [settings, setSettings] = useState<GlobalSettings>(DEFAULT_SETTINGS)
  const [hasChanges, setHasChanges] = useState(false)

  const updateSetting = <K extends keyof GlobalSettings, T extends keyof GlobalSettings[K]>(
    category: K,
    key: T,
    value: GlobalSettings[K][T]
  ) => {
    setSettings({
      ...settings,
      [category]: {
        ...settings[category],
        [key]: value
      }
    })
    setHasChanges(true)
  }

  const applyChanges = async () => {
    console.log('Applying global settings:', settings)
    setHasChanges(false)
  }

  const resetChanges = () => {
    setSettings(DEFAULT_SETTINGS)
    setHasChanges(false)
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <Card className="bg-gradient-to-br from-slate-900 to-slate-800 border-cyan-500/30">
        <CardHeader>
          <CardTitle className="text-cyan-400 flex items-center gap-2">
            <span className="text-2xl">⚙️</span>
            Global System Settings
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-sm text-slate-300">
            Configure system-wide preferences and integrations
          </div>
        </CardContent>
      </Card>

      {/* Notifications */}
      <CollapsibleSection title="Notifications" icon="🔔" defaultOpen={true}>
        <div className="space-y-3">
          <label className="flex items-center justify-between text-sm text-slate-300">
            <div>
              <div>Email Notifications</div>
              <div className="text-xs text-slate-500">Receive updates via email</div>
            </div>
            <Switch
              checked={settings.notifications.email}
              onCheckedChange={(checked) => updateSetting('notifications', 'email', checked)}
            />
          </label>

          <label className="flex items-center justify-between text-sm text-slate-300">
            <div>
              <div>Push Notifications</div>
              <div className="text-xs text-slate-500">Mobile push notifications</div>
            </div>
            <Switch
              checked={settings.notifications.push}
              onCheckedChange={(checked) => updateSetting('notifications', 'push', checked)}
            />
          </label>

          <label className="flex items-center justify-between text-sm text-slate-300">
            <div>
              <div>Desktop Notifications</div>
              <div className="text-xs text-slate-500">Browser desktop notifications</div>
            </div>
            <Switch
              checked={settings.notifications.desktop}
              onCheckedChange={(checked) => updateSetting('notifications', 'desktop', checked)}
            />
          </label>

          <label className="flex items-center justify-between text-sm text-slate-300">
            <div>
              <div>Slack Notifications</div>
              <div className="text-xs text-slate-500">Send alerts to Slack channels</div>
            </div>
            <Switch
              checked={settings.notifications.slack}
              onCheckedChange={(checked) => updateSetting('notifications', 'slack', checked)}
            />
          </label>
        </div>
      </CollapsibleSection>

      {/* Security */}
      <CollapsibleSection title="Security" icon="🔒" defaultOpen={true}>
        <div className="space-y-3">
          <label className="flex items-center justify-between text-sm text-slate-300">
            <div>
              <div>Two-Factor Authentication</div>
              <div className="text-xs text-slate-500">Additional security layer for login</div>
            </div>
            <Switch
              checked={settings.security.twoFactorAuth}
              onCheckedChange={(checked) => updateSetting('security', 'twoFactorAuth', checked)}
            />
          </label>

          <div className="p-3 bg-slate-800/50 rounded">
            <label className="text-sm text-slate-300 mb-2 block">
              Session Timeout (minutes): {settings.security.sessionTimeout}
            </label>
            <input
              type="range"
              min={5}
              max={120}
              step={5}
              value={settings.security.sessionTimeout}
              onChange={(e) => updateSetting('security', 'sessionTimeout', Number(e.target.value))}
              className="w-full"
            />
          </div>

          <label className="flex items-center justify-between text-sm text-slate-300">
            <div>
              <div>API Key Rotation</div>
              <div className="text-xs text-slate-500">Automatic API key rotation every 90 days</div>
            </div>
            <Switch
              checked={settings.security.apiKeyRotation}
              onCheckedChange={(checked) => updateSetting('security', 'apiKeyRotation', checked)}
            />
          </label>

          <label className="flex items-center justify-between text-sm text-slate-300">
            <div>
              <div>Audit Logging</div>
              <div className="text-xs text-slate-500">Log all configuration changes</div>
            </div>
            <Switch
              checked={settings.security.auditLogging}
              onCheckedChange={(checked) => updateSetting('security', 'auditLogging', checked)}
            />
          </label>
        </div>
      </CollapsibleSection>

      {/* Performance */}
      <CollapsibleSection title="Performance" icon="⚡">
        <div className="space-y-3">
          <label className="flex items-center justify-between text-sm text-slate-300">
            <div>
              <div>Enable Caching</div>
              <div className="text-xs text-slate-500">Cache responses for faster performance</div>
            </div>
            <Switch
              checked={settings.performance.enableCaching}
              onCheckedChange={(checked) => updateSetting('performance', 'enableCaching', checked)}
            />
          </label>

          <div className="p-3 bg-slate-800/50 rounded">
            <label className="text-sm text-slate-300 mb-2 block">
              Compression Level: {settings.performance.compressionLevel}
            </label>
            <input
              type="range"
              min={0}
              max={9}
              step={1}
              value={settings.performance.compressionLevel}
              onChange={(e) => updateSetting('performance', 'compressionLevel', Number(e.target.value))}
              className="w-full"
            />
            <div className="text-xs text-slate-500 mt-1">
              0 = No compression, 9 = Maximum compression
            </div>
          </div>

          <div className="p-3 bg-slate-800/50 rounded">
            <label className="text-sm text-slate-300 mb-2 block">
              Max Concurrent Tasks: {settings.performance.maxConcurrentTasks}
            </label>
            <input
              type="range"
              min={1}
              max={50}
              step={1}
              value={settings.performance.maxConcurrentTasks}
              onChange={(e) => updateSetting('performance', 'maxConcurrentTasks', Number(e.target.value))}
              className="w-full"
            />
          </div>

          <label className="flex items-center justify-between text-sm text-slate-300">
            <div>
              <div>Request Throttling</div>
              <div className="text-xs text-slate-500">Rate limit API requests</div>
            </div>
            <Switch
              checked={settings.performance.requestThrottling}
              onCheckedChange={(checked) => updateSetting('performance', 'requestThrottling', checked)}
            />
          </label>
        </div>
      </CollapsibleSection>

      {/* Integrations */}
      <CollapsibleSection title="Integrations" icon="🔗">
        <div className="space-y-3">
          <label className="flex items-center justify-between text-sm text-slate-300">
            <div className="flex items-center gap-2">
              <span className="text-xl">🐙</span>
              <div>
                <div>GitHub</div>
                <div className="text-xs text-slate-500">Repository integration</div>
              </div>
            </div>
            <Switch
              checked={settings.integrations.github}
              onCheckedChange={(checked) => updateSetting('integrations', 'github', checked)}
            />
          </label>

          <label className="flex items-center justify-between text-sm text-slate-300">
            <div className="flex items-center gap-2">
              <span className="text-xl">🦊</span>
              <div>
                <div>GitLab</div>
                <div className="text-xs text-slate-500">Repository integration</div>
              </div>
            </div>
            <Switch
              checked={settings.integrations.gitlab}
              onCheckedChange={(checked) => updateSetting('integrations', 'gitlab', checked)}
            />
          </label>

          <label className="flex items-center justify-between text-sm text-slate-300">
            <div className="flex items-center gap-2">
              <span className="text-xl">📊</span>
              <div>
                <div>Prometheus</div>
                <div className="text-xs text-slate-500">Metrics collection</div>
              </div>
            </div>
            <Switch
              checked={settings.integrations.prometheus}
              onCheckedChange={(checked) => updateSetting('integrations', 'prometheus', checked)}
            />
          </label>

          <label className="flex items-center justify-between text-sm text-slate-300">
            <div className="flex items-center gap-2">
              <span className="text-xl">📈</span>
              <div>
                <div>Grafana</div>
                <div className="text-xs text-slate-500">Dashboard visualization</div>
              </div>
            </div>
            <Switch
              checked={settings.integrations.grafana}
              onCheckedChange={(checked) => updateSetting('integrations', 'grafana', checked)}
            />
          </label>

          <label className="flex items-center justify-between text-sm text-slate-300">
            <div className="flex items-center gap-2">
              <span className="text-xl">💬</span>
              <div>
                <div>Slack</div>
                <div className="text-xs text-slate-500">Team communication</div>
              </div>
            </div>
            <Switch
              checked={settings.integrations.slack}
              onCheckedChange={(checked) => updateSetting('integrations', 'slack', checked)}
            />
          </label>
        </div>
      </CollapsibleSection>

      {/* Advanced */}
      <CollapsibleSection title="Advanced" icon="🔬">
        <div className="space-y-3">
          <label className="flex items-center justify-between text-sm text-slate-300">
            <div>
              <div>Debug Mode</div>
              <div className="text-xs text-slate-500">Enable detailed logging and debugging</div>
            </div>
            <Switch
              checked={settings.advanced.debugMode}
              onCheckedChange={(checked) => updateSetting('advanced', 'debugMode', checked)}
            />
          </label>

          <label className="flex items-center justify-between text-sm text-slate-300">
            <div>
              <div>Experimental Features</div>
              <div className="text-xs text-slate-500 text-yellow-400">⚠️ May be unstable</div>
            </div>
            <Switch
              checked={settings.advanced.experimentalFeatures}
              onCheckedChange={(checked) => updateSetting('advanced', 'experimentalFeatures', checked)}
            />
          </label>

          <label className="flex items-center justify-between text-sm text-slate-300">
            <div>
              <div>Telemetry</div>
              <div className="text-xs text-slate-500">Anonymous usage statistics</div>
            </div>
            <Switch
              checked={settings.advanced.telemetry}
              onCheckedChange={(checked) => updateSetting('advanced', 'telemetry', checked)}
            />
          </label>

          <label className="flex items-center justify-between text-sm text-slate-300">
            <div>
              <div>Auto-Update</div>
              <div className="text-xs text-slate-500">Automatically update to latest version</div>
            </div>
            <Switch
              checked={settings.advanced.autoUpdate}
              onCheckedChange={(checked) => updateSetting('advanced', 'autoUpdate', checked)}
            />
          </label>
        </div>
      </CollapsibleSection>

      {/* Action Buttons */}
      <div className="flex gap-3 sticky bottom-0 bg-slate-900 p-4 border-t border-cyan-500/30 -mx-4">
        <Button
          onClick={applyChanges}
          disabled={!hasChanges}
          className={`flex-1 ${
            hasChanges
              ? 'bg-cyan-500 text-slate-900 hover:bg-cyan-400 shadow-lg shadow-cyan-500/30'
              : 'bg-slate-700 text-slate-400 cursor-not-allowed'
          }`}
        >
          {hasChanges ? 'Apply Changes' : 'No Changes'}
        </Button>
        <Button
          onClick={resetChanges}
          disabled={!hasChanges}
          variant="outline"
          className="border-slate-500/50 text-slate-400 hover:bg-slate-800"
        >
          Reset
        </Button>
      </div>
    </div>
  )
}
