import React, { useCallback, useEffect, useMemo } from 'react';
import ReactFlow, {
  Background,
  Controls,
  MiniMap,
  Node,
  useNodesState,
  useEdgesState,
  BackgroundVariant,
  Panel,
} from 'reactflow';
import 'reactflow/dist/style.css';

import { useSwarmStore, SwarmNodeData } from '../lib/swarmStore';
import {
  createNodesFromData,
  createEdges,
  getLayoutedElements,
  getMiniMapNodeColor,
  STATUS_COLORS
} from '../lib/graphLayout';
import { Card } from './ui/card';

// Custom Node Components
const ProjectNode: React.FC<{ data: SwarmNodeData }> = ({ data }) => (
  <div className="px-6 py-4 bg-gradient-to-br from-purple-900/90 to-blue-900/90 border-2 rounded-lg shadow-xl"
       style={{ borderColor: STATUS_COLORS[data.status], width: 280, height: 100 }}>
    <div className="flex items-center justify-between mb-2">
      <h3 className="text-lg font-bold text-white">{data.label}</h3>
      <div className="w-3 h-3 rounded-full animate-pulse"
           style={{ backgroundColor: STATUS_COLORS[data.status] }} />
    </div>
    <p className="text-xs text-gray-300">{data.description}</p>
    {data.metrics?.requests && (
      <p className="text-xs text-purple-300 mt-1">{data.metrics.requests} requests</p>
    )}
  </div>
);

const HRMNode: React.FC<{ data: SwarmNodeData }> = ({ data }) => (
  <div className="px-4 py-3 bg-gradient-to-br from-pink-900/80 to-purple-900/80 border-2 rounded-lg shadow-lg"
       style={{ borderColor: STATUS_COLORS[data.status], width: 180, height: 90 }}>
    <div className="flex items-center justify-between mb-1">
      <h4 className="text-sm font-bold text-white">{data.label}</h4>
      <div className="w-2 h-2 rounded-full"
           style={{ backgroundColor: STATUS_COLORS[data.status] }} />
    </div>
    <p className="text-xs text-gray-300 mb-2">{data.description}</p>
    {data.config && (
      <div className="text-xs text-pink-300">
        T: {data.config.temperature} | P: {data.config.topP}
      </div>
    )}
  </div>
);

const SwarmNode: React.FC<{ data: SwarmNodeData }> = ({ data }) => (
  <div className="px-4 py-3 bg-gradient-to-br from-blue-900/80 to-cyan-900/80 border-2 rounded-lg shadow-lg"
       style={{ borderColor: STATUS_COLORS[data.status], width: 180, height: 90 }}>
    <div className="flex items-center justify-between mb-1">
      <h4 className="text-sm font-bold text-white">{data.label}</h4>
      <div className="w-2 h-2 rounded-full"
           style={{ backgroundColor: STATUS_COLORS[data.status] }} />
    </div>
    <p className="text-xs text-gray-300 mb-2">{data.description}</p>
    {data.metrics?.requests && (
      <p className="text-xs text-cyan-300">{data.metrics.requests} requests</p>
    )}
  </div>
);

const QualityNode: React.FC<{ data: SwarmNodeData }> = ({ data }) => (
  <div className="px-4 py-3 bg-gradient-to-br from-purple-900/80 to-indigo-900/80 border-2 rounded-lg shadow-lg"
       style={{ borderColor: STATUS_COLORS[data.status], width: 180, height: 90 }}>
    <div className="flex items-center justify-between mb-1">
      <h4 className="text-sm font-bold text-white">{data.label}</h4>
      <div className="w-2 h-2 rounded-full"
           style={{ backgroundColor: STATUS_COLORS[data.status] }} />
    </div>
    <p className="text-xs text-gray-300 mb-2">{data.description}</p>
    {data.metrics?.requests && (
      <p className="text-xs text-indigo-300">{data.metrics.requests} checks</p>
    )}
  </div>
);

const AgentNode: React.FC<{ data: SwarmNodeData }> = ({ data }) => (
  <div className="px-3 py-2 bg-gradient-to-br from-green-900/80 to-emerald-900/80 border-2 rounded-lg shadow-lg"
       style={{ borderColor: STATUS_COLORS[data.status], width: 140, height: 80 }}>
    <div className="flex items-center justify-between mb-1">
      <h4 className="text-xs font-bold text-white">{data.label}</h4>
      <div className="w-2 h-2 rounded-full"
           style={{ backgroundColor: STATUS_COLORS[data.status] }} />
    </div>
    {data.metrics && (
      <div className="text-xs text-emerald-300">
        <div>{data.metrics.requests || 0} req</div>
        <div>{data.metrics.latency || 0}ms</div>
      </div>
    )}
  </div>
);

const InfrastructureNode: React.FC<{ data: SwarmNodeData }> = ({ data }) => (
  <div className="px-3 py-2 bg-gradient-to-br from-orange-900/80 to-amber-900/80 border-2 rounded-lg shadow-lg"
       style={{ borderColor: STATUS_COLORS[data.status], width: 160, height: 80 }}>
    <div className="flex items-center justify-between mb-1">
      <h4 className="text-xs font-bold text-white">{data.label}</h4>
      <div className="w-2 h-2 rounded-full"
           style={{ backgroundColor: STATUS_COLORS[data.status] }} />
    </div>
    <p className="text-xs text-gray-300 mb-1">{data.description}</p>
    {data.metrics && (
      <div className="text-xs text-amber-300">
        {data.metrics.cacheHitRate && `${data.metrics.cacheHitRate.toFixed(1)}% hit`}
        {data.metrics.cost && `$${data.metrics.cost.toFixed(2)}`}
        {data.metrics.requests && `${data.metrics.requests} req`}
      </div>
    )}
  </div>
);

// Node types mapping
const nodeTypes = {
  projectNode: ProjectNode,
  hrmNode: HRMNode,
  swarmNode: SwarmNode,
  qualityNode: QualityNode,
  agentNode: AgentNode,
  infrastructureNode: InfrastructureNode,
};

interface SwarmGraphProps {
  onNodeClick?: (nodeId: string) => void;
  className?: string;
}

export function SwarmGraph({ onNodeClick, className = '' }: SwarmGraphProps) {
  const { nodes: storeNodes, isAnimated, isAutoLayout, selectNode } = useSwarmStore();

  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);

  // Generate nodes and edges from store data
  const { nodes: generatedNodes, edges: generatedEdges } = useMemo(() => {
    const flowNodes = createNodesFromData(storeNodes);
    const flowEdges = createEdges(isAnimated);

    if (isAutoLayout) {
      return getLayoutedElements(flowNodes, flowEdges);
    }

    return { nodes: flowNodes, edges: flowEdges };
  }, [storeNodes, isAnimated, isAutoLayout]);

  // Update nodes and edges when generated data changes
  useEffect(() => {
    setNodes(generatedNodes);
    setEdges(generatedEdges);
  }, [generatedNodes, generatedEdges, setNodes, setEdges]);

  // Handle node click
  const handleNodeClick = useCallback(
    (_event: React.MouseEvent, node: Node) => {
      selectNode(node.id);
      onNodeClick?.(node.id);
    },
    [selectNode, onNodeClick]
  );

  return (
    <Card className={`relative ${className}`}>
      <div className="h-full w-full bg-slate-950">
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onNodeClick={handleNodeClick}
          nodeTypes={nodeTypes}
          fitView
          attributionPosition="bottom-left"
          minZoom={0.2}
          maxZoom={2}
          defaultEdgeOptions={{
            type: 'smoothstep',
            animated: isAnimated,
          }}
        >
          <Background
            variant={BackgroundVariant.Dots}
            gap={16}
            size={1}
            color="#4b5563"
          />

          <Controls
            className="bg-slate-800 border border-slate-700 rounded-lg"
            showInteractive={false}
          />

          <MiniMap
            nodeColor={getMiniMapNodeColor}
            className="bg-slate-900 border border-slate-700 rounded-lg"
            maskColor="rgb(15, 23, 42, 0.8)"
            position="top-right"
          />

          <Panel position="top-left" className="bg-slate-900/80 backdrop-blur-sm p-3 rounded-lg border border-slate-700">
            <div className="text-white text-sm font-semibold mb-2">Swarm Graph</div>
            <div className="flex gap-3 text-xs">
              <div className="flex items-center gap-1">
                <div className="w-2 h-2 rounded-full" style={{ backgroundColor: STATUS_COLORS.active }} />
                <span className="text-gray-300">Active</span>
              </div>
              <div className="flex items-center gap-1">
                <div className="w-2 h-2 rounded-full" style={{ backgroundColor: STATUS_COLORS.idle }} />
                <span className="text-gray-300">Idle</span>
              </div>
              <div className="flex items-center gap-1">
                <div className="w-2 h-2 rounded-full" style={{ backgroundColor: STATUS_COLORS.warning }} />
                <span className="text-gray-300">Warning</span>
              </div>
              <div className="flex items-center gap-1">
                <div className="w-2 h-2 rounded-full" style={{ backgroundColor: STATUS_COLORS.disabled }} />
                <span className="text-gray-300">Disabled</span>
              </div>
            </div>
          </Panel>
        </ReactFlow>
      </div>
    </Card>
  );
}

export default SwarmGraph;
