import { useEffect, useState } from 'react';
import { SwarmGraph } from '../components/SwarmGraph';
import { useSwarmStore } from '../lib/swarmStore';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { Badge } from '../components/ui/badge';

export function SwarmVisualization() {
  const [selectedNodeDetails, setSelectedNodeDetails] = useState<any>(null);
  const { nodes, selectedNodeId, setNodeMetrics, setAnimated, isAnimated } = useSwarmStore();

  // Get selected node data
  useEffect(() => {
    if (selectedNodeId) {
      const nodeData = nodes.get(selectedNodeId);
      setSelectedNodeDetails(nodeData);
    } else {
      setSelectedNodeDetails(null);
    }
  }, [selectedNodeId, nodes]);

  // Simulate real-time metric updates
  useEffect(() => {
    const interval = setInterval(() => {
      // Update agent metrics
      const agentIds = ['agent-claude', 'agent-copilot', 'agent-gemini', 'agent-cursor'];
      agentIds.forEach(agentId => {
        setNodeMetrics(agentId, {
          requests: Math.floor(Math.random() * 500) + 100,
          latency: Math.floor(Math.random() * 1000) + 500
        });
      });

      // Update cache hit rate
      setNodeMetrics('infra-cache', {
        cacheHitRate: Math.random() * 20 + 70, // 70-90%
        requests: Math.floor(Math.random() * 500) + 800
      });

      // Update cost
      setNodeMetrics('infra-cost', {
        cost: Math.random() * 20 + 30 // $30-$50
      });
    }, 3000);

    return () => clearInterval(interval);
  }, [setNodeMetrics]);

  const handleNodeClick = (nodeId: string) => {
    console.log('Node clicked:', nodeId);
  };

  const getStatusBadgeVariant = (status: string) => {
    switch (status) {
      case 'active':
        return 'default';
      case 'warning':
        return 'warning';
      case 'error':
        return 'danger';
      default:
        return 'default';
    }
  };

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white mb-2">Swarm Visualization</h1>
          <p className="text-gray-400">
            Interactive graph showing the complete agent orchestration hierarchy
          </p>
        </div>
        <div className="flex items-center gap-3">
          <label className="flex items-center gap-2 text-sm text-gray-300">
            <input
              type="checkbox"
              checked={isAnimated}
              onChange={(e) => setAnimated(e.target.checked)}
              className="rounded"
            />
            Animated Edges
          </label>
        </div>
      </div>

      {/* Graph */}
      <div className="h-[600px]">
        <SwarmGraph onNodeClick={handleNodeClick} />
      </div>

      {/* Selected Node Details */}
      {selectedNodeDetails && (
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle className="text-xl">{selectedNodeDetails.label}</CardTitle>
              <Badge variant={getStatusBadgeVariant(selectedNodeDetails.status)}>
                {selectedNodeDetails.status}
              </Badge>
            </div>
            <CardDescription>{selectedNodeDetails.description}</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {selectedNodeDetails.metrics?.requests !== undefined && (
                <div>
                  <div className="text-sm text-gray-400">Requests</div>
                  <div className="text-2xl font-bold text-white">
                    {selectedNodeDetails.metrics.requests}
                  </div>
                </div>
              )}
              {selectedNodeDetails.metrics?.latency !== undefined && (
                <div>
                  <div className="text-sm text-gray-400">Latency</div>
                  <div className="text-2xl font-bold text-white">
                    {selectedNodeDetails.metrics.latency}ms
                  </div>
                </div>
              )}
              {selectedNodeDetails.metrics?.cacheHitRate !== undefined && (
                <div>
                  <div className="text-sm text-gray-400">Cache Hit Rate</div>
                  <div className="text-2xl font-bold text-white">
                    {selectedNodeDetails.metrics.cacheHitRate.toFixed(1)}%
                  </div>
                </div>
              )}
              {selectedNodeDetails.metrics?.cost !== undefined && (
                <div>
                  <div className="text-sm text-gray-400">Cost</div>
                  <div className="text-2xl font-bold text-white">
                    ${selectedNodeDetails.metrics.cost.toFixed(2)}
                  </div>
                </div>
              )}
            </div>

            {selectedNodeDetails.config && (
              <div className="mt-4 pt-4 border-t border-gray-700">
                <h4 className="text-sm font-semibold text-white mb-2">Configuration</h4>
                <div className="grid grid-cols-3 gap-3 text-sm">
                  {Object.entries(selectedNodeDetails.config).map(([key, value]) => (
                    <div key={key}>
                      <div className="text-gray-400">{key}</div>
                      <div className="text-white font-mono">{String(value)}</div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </CardContent>
        </Card>
      )}

      {/* Legend */}
      <Card>
        <CardHeader>
          <CardTitle>Graph Legend</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            <div>
              <h4 className="text-sm font-semibold text-white mb-2">Layer 0: Project</h4>
              <p className="text-xs text-gray-400">Top-level project orchestration</p>
            </div>
            <div>
              <h4 className="text-sm font-semibold text-white mb-2">Layer 1: Core Systems</h4>
              <p className="text-xs text-gray-400">HRM, Swarm, Quality evaluation</p>
            </div>
            <div>
              <h4 className="text-sm font-semibold text-white mb-2">Layer 2: Agents</h4>
              <p className="text-xs text-gray-400">AI agents (Claude, Copilot, etc.)</p>
            </div>
            <div>
              <h4 className="text-sm font-semibold text-white mb-2">Layer 3: Infrastructure</h4>
              <p className="text-xs text-gray-400">Cache, metrics, cost tracking</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

export default SwarmVisualization;
