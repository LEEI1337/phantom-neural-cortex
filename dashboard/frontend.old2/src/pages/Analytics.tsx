import { useState } from 'react'
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/tabs'
import CostAnalysis from '@/components/CostAnalysis'
import QualityTrends from '@/components/QualityTrends'
import AgentPerformance from '@/components/AgentPerformance'

export default function Analytics() {
  const [activeTab, setActiveTab] = useState('cost')

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold">Analytics</h1>
        <p className="text-muted-foreground mt-1">Deep insights into performance, costs, and quality</p>
      </div>

      <div className="border-b">
        <div className="flex gap-4">
          {[
            { id: 'cost', label: 'Cost Analysis' },
            { id: 'quality', label: 'Quality Trends' },
            { id: 'agents', label: 'Agent Performance' },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-4 py-2 font-medium border-b-2 transition-colors ${
                activeTab === tab.id
                  ? 'border-primary text-primary'
                  : 'border-transparent text-muted-foreground hover:text-foreground'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>
      </div>

      <div>
        {activeTab === 'cost' && <CostAnalysis />}
        {activeTab === 'quality' && <QualityTrends />}
        {activeTab === 'agents' && <AgentPerformance />}
      </div>
    </div>
  )
}
