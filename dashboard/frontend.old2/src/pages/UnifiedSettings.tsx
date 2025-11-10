/**
 * Unified Settings & HRM Control Page
 * Combines all system configuration in one professional interface
 */

import { useState } from 'react'
import {
  Settings,
  Cpu,
  Key,
  Users,
  Layers,
  LayoutDashboard
} from 'lucide-react'
import { HRMControlPanelV2 } from '@/components/HRMControlPanelV2'
import APIKeyManagement from '@/components/APIKeyManagement'
import SwarmControls from '@/components/SwarmControls'
import AgentTierConfiguration from '@/components/AgentTierConfiguration'
import { SystemHealthSection } from '@/components/settings/SystemHealthSection'

type Section = 'overview' | 'hrm' | 'system' | 'api-keys' | 'swarm' | 'agents'

export default function UnifiedSettings() {
  const [selectedSection, setSelectedSection] = useState<Section>('overview')

  const sections = [
    { id: 'overview' as Section, icon: LayoutDashboard, label: 'Overview', color: 'text-purple-500' },
    { id: 'hrm' as Section, icon: Cpu, label: 'HRM Control', color: 'text-blue-500' },
    { id: 'system' as Section, icon: Settings, label: 'System & Cache', color: 'text-green-500' },
    { id: 'api-keys' as Section, icon: Key, label: 'API Keys', color: 'text-yellow-500' },
    { id: 'swarm' as Section, icon: Users, label: 'Swarm', color: 'text-orange-500' },
    { id: 'agents' as Section, icon: Layers, label: 'Agent Tiers', color: 'text-cyan-500' },
  ]

  return (
    <div className="flex h-[calc(100vh-4rem)] gap-6">
      {/* LEFT: Navigation Sidebar */}
      <div className="w-60 flex-shrink-0">
        <div className="sticky top-0">
          <h1 className="text-2xl font-bold mb-6">Configuration</h1>

          <nav className="space-y-1">
            {sections.map((section) => {
              const Icon = section.icon
              const isActive = selectedSection === section.id

              return (
                <button
                  key={section.id}
                  onClick={() => setSelectedSection(section.id)}
                  className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all ${
                    isActive
                      ? 'bg-card border-l-4 border-purple-500 shadow-sm'
                      : 'hover:bg-muted/50'
                  }`}
                >
                  <Icon className={`w-5 h-5 ${isActive ? section.color : 'text-muted-foreground'}`} />
                  <span className={`font-medium ${isActive ? 'text-foreground' : 'text-muted-foreground'}`}>
                    {section.label}
                  </span>
                </button>
              )
            })}
          </nav>
        </div>
      </div>

      {/* RIGHT: Content Area */}
      <div className="flex-1 overflow-y-auto">
        {selectedSection === 'overview' && <OverviewSection />}
        {selectedSection === 'hrm' && <HRMControlPanelV2 />}
        {selectedSection === 'system' && <SystemHealthSection />}
        {selectedSection === 'api-keys' && <APIKeyManagement />}
        {selectedSection === 'swarm' && <SwarmControls />}
        {selectedSection === 'agents' && <AgentTierConfiguration />}
      </div>
    </div>
  )
}

// Overview Section with System Visualization
function OverviewSection() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold">System Overview</h2>
        <p className="text-muted-foreground mt-1">
          Monitor your AI system architecture and performance
        </p>
      </div>

      <div className="grid grid-cols-3 gap-4">
        <div className="bg-card border border-border rounded-lg p-6">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 rounded-full bg-green-500/10 flex items-center justify-center">
              <Cpu className="w-5 h-5 text-green-500" />
            </div>
            <div>
              <p className="text-2xl font-bold text-green-500">-45%</p>
              <p className="text-xs text-muted-foreground">Token Usage</p>
            </div>
          </div>
        </div>

        <div className="bg-card border border-border rounded-lg p-6">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 rounded-full bg-blue-500/10 flex items-center justify-center">
              <Settings className="w-5 h-5 text-blue-500" />
            </div>
            <div>
              <p className="text-2xl font-bold text-blue-500">-52%</p>
              <p className="text-xs text-muted-foreground">Cost Reduction</p>
            </div>
          </div>
        </div>

        <div className="bg-card border border-border rounded-lg p-6">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 rounded-full bg-orange-500/10 flex items-center justify-center">
              <Layers className="w-5 h-5 text-orange-500" />
            </div>
            <div>
              <p className="text-2xl font-bold text-orange-500">+80%</p>
              <p className="text-xs text-muted-foreground">Speed Improvement</p>
            </div>
          </div>
        </div>
      </div>

      <div className="bg-card border border-border rounded-lg p-8">
        <h3 className="text-xl font-semibold mb-6">System Architecture</h3>
        <div className="flex items-center justify-center min-h-[400px]">
          <p className="text-muted-foreground">System visualization will be implemented here</p>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-6">
        <div className="bg-card border border-border rounded-lg p-6">
          <h3 className="text-lg font-semibold mb-4">Active Components</h3>
          <div className="space-y-3">
            {[
              { name: 'Latent Reasoning', status: true },
              { name: 'Agent Switching', status: true },
              { name: 'Parallel Evaluation', status: true },
              { name: 'Deep Supervision', status: false },
            ].map((component) => (
              <div key={component.name} className="flex items-center justify-between">
                <span className="text-sm">{component.name}</span>
                <div className={`w-2 h-2 rounded-full ${component.status ? 'bg-green-500' : 'bg-muted'}`} />
              </div>
            ))}
          </div>
        </div>

        <div className="bg-card border border-border rounded-lg p-6">
          <h3 className="text-lg font-semibold mb-4">Recent Activity</h3>
          <div className="space-y-2 text-sm text-muted-foreground">
            <p>No recent configuration changes</p>
          </div>
        </div>
      </div>
    </div>
  )
}
