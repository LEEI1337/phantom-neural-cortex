# Swarm Graph Visualization

A professional React Flow-based graph visualization showing the complete 4-layer agent orchestration hierarchy.

## Components Created

### 1. **SwarmGraph.tsx** (`/components/SwarmGraph.tsx`)
Main visualization component with React Flow integration.

**Features:**
- Custom node types for each layer (Project, HRM, Swarm, Quality, Agent, Infrastructure)
- Interactive node selection with click handlers
- Animated edges for active connections
- MiniMap with color-coded status indicators
- Controls (zoom, fit view, reset)
- Background with dots pattern
- Professional cyberpunk-themed styling

**Props:**
```typescript
interface SwarmGraphProps {
  onNodeClick?: (nodeId: string) => void;
  className?: string;
}
```

**Custom Node Types:**
- `ProjectNode` - Layer 0, gradient purple/blue, 280x100px
- `HRMNode` - Layer 1, gradient pink/purple, 180x90px
- `SwarmNode` - Layer 1, gradient blue/cyan, 180x90px
- `QualityNode` - Layer 1, gradient purple/indigo, 180x90px
- `AgentNode` - Layer 2, gradient green/emerald, 140x80px
- `InfrastructureNode` - Layer 3, gradient orange/amber, 160x80px

### 2. **swarmStore.ts** (`/lib/swarmStore.ts`)
Zustand store for graph state management.

**State:**
```typescript
interface SwarmState {
  nodes: Map<string, SwarmNodeData>;      // All node data
  selectedNodeId: string | null;          // Currently selected node
  isAutoLayout: boolean;                  // Enable Dagre layout
  isAnimated: boolean;                    // Animated edges
}
```

**Actions:**
- `setNodeStatus(nodeId, status)` - Update node status
- `setNodeMetrics(nodeId, metrics)` - Update node metrics
- `selectNode(nodeId)` - Select a node
- `updateNodeData(nodeId, data)` - Update any node data
- `setAutoLayout(enabled)` - Toggle auto-layout
- `setAnimated(enabled)` - Toggle edge animation
- `updateMultipleMetrics(updates)` - Bulk metric updates
- `resetNodes()` - Reset to initial state

**Node Statuses:**
- `active` - Green (#00ff88)
- `idle` - Purple (#8b5cf6)
- `warning` - Yellow (#fbbf24)
- `error` - Red (#ef4444)
- `disabled` - Gray (#64748b)

### 3. **graphLayout.ts** (`/lib/graphLayout.ts`)
Graph layout configuration and utilities.

**Features:**
- 4-layer hierarchy configuration
- Dagre auto-layout algorithm
- Node dimension specifications
- Status color mappings
- Edge creation logic
- MiniMap color functions

**Layer Configuration:**
```typescript
Layer 0: Project        (y: 50,  spacing: 400)
Layer 1: Core Systems   (y: 200, spacing: 250)
Layer 2: Agents         (y: 380, spacing: 180)
Layer 3: Infrastructure (y: 560, spacing: 250)
```

### 4. **SwarmVisualization.tsx** (`/pages/SwarmVisualization.tsx`)
Example page demonstrating the SwarmGraph usage.

**Features:**
- Full-page graph display
- Selected node detail panel
- Real-time metric simulation
- Animation toggle
- Comprehensive legend

## Graph Architecture

### 4-Layer Hierarchy

```
Layer 0: Project Alpha (1 node)
           |
           ├─────────┬─────────┐
           |         |         |
Layer 1:  HRM    Swarm    Quality (3 nodes)
           |         |         |
           └─────────┼─────────┘
                     |
         ┌───┬───┬───┼───┬───┐
         |   |   |   |   |   |
Layer 2: C   Co  G   Cu  W    (5 agent nodes)
         |   |   |   |   |
         └───┴───┴───┴───┘
                 |
         ┌───────┼───────┐
         |       |       |
Layer 3: Cache Metrics Cost (3 infra nodes)
```

**Legend:**
- C = Claude
- Co = Copilot
- G = Gemini
- Cu = Cursor
- W = Windsurf

### Initial Nodes (13 total)

**Layer 0:**
- `project-a` - Project Alpha (active)

**Layer 1:**
- `hrm-config` - HRM (active)
- `swarm-orchestrator` - Swarm (active)
- `quality-eval` - Quality (idle)

**Layer 2:**
- `agent-claude` - Claude (active)
- `agent-copilot` - Copilot (active)
- `agent-gemini` - Gemini (idle)
- `agent-cursor` - Cursor (warning)
- `agent-windsurf` - Windsurf (disabled)

**Layer 3:**
- `infra-cache` - Cache (active, 78.5% hit rate)
- `infra-metrics` - Metrics (active)
- `infra-cost` - Cost (idle, $45.32)

### Edge Connections (32 total)

**Project → Core (3 edges):**
- project-a → hrm-config (animated, active)
- project-a → swarm-orchestrator (animated, active)
- project-a → quality-eval (static, idle)

**HRM → Agents (5 edges):**
- hrm-config → all 5 agents (animated except windsurf)

**Swarm → Agents (3 edges):**
- swarm-orchestrator → claude, copilot, cursor (animated)

**Agents → Cache (5 edges):**
- All agents → infra-cache (animated except windsurf)

**Agents → Metrics (5 edges):**
- All agents → infra-metrics (animated except windsurf)

**Quality → Cost (1 edge):**
- quality-eval → infra-cost (static, idle)

## Usage Examples

### Basic Usage
```tsx
import { SwarmGraph } from '../components/SwarmGraph';

function MyPage() {
  return (
    <div className="h-screen">
      <SwarmGraph />
    </div>
  );
}
```

### With Node Click Handler
```tsx
import { SwarmGraph } from '../components/SwarmGraph';

function MyPage() {
  const handleNodeClick = (nodeId: string) => {
    console.log('Clicked:', nodeId);
    // Handle node selection
  };

  return (
    <SwarmGraph onNodeClick={handleNodeClick} />
  );
}
```

### Accessing Store State
```tsx
import { useSwarmStore } from '../lib/swarmStore';

function NodeDetails() {
  const { nodes, selectedNodeId } = useSwarmStore();
  const selectedNode = selectedNodeId ? nodes.get(selectedNodeId) : null;

  if (!selectedNode) return null;

  return (
    <div>
      <h3>{selectedNode.label}</h3>
      <p>Status: {selectedNode.status}</p>
    </div>
  );
}
```

### Updating Metrics
```tsx
import { useSwarmStore } from '../lib/swarmStore';

function MetricsUpdater() {
  const { setNodeMetrics } = useSwarmStore();

  useEffect(() => {
    const interval = setInterval(() => {
      setNodeMetrics('agent-claude', {
        requests: Math.floor(Math.random() * 500),
        latency: Math.floor(Math.random() * 1000) + 500
      });
    }, 3000);

    return () => clearInterval(interval);
  }, []);

  return null;
}
```

### Bulk Updates
```tsx
import { useSwarmStore } from '../lib/swarmStore';

function BulkUpdater() {
  const { updateMultipleMetrics } = useSwarmStore();

  const updateAllAgents = () => {
    updateMultipleMetrics([
      { nodeId: 'agent-claude', metrics: { requests: 450 } },
      { nodeId: 'agent-copilot', metrics: { requests: 320 } },
      { nodeId: 'agent-gemini', metrics: { requests: 80 } }
    ]);
  };

  return <button onClick={updateAllAgents}>Update All</button>;
}
```

## Styling

### Custom Colors
All colors are defined in `graphLayout.ts`:
```typescript
export const STATUS_COLORS = {
  active: '#00ff88',
  idle: '#8b5cf6',
  warning: '#fbbf24',
  error: '#ef4444',
  disabled: '#64748b'
};
```

### Node Gradients
Each node type has a unique gradient:
- Project: `from-purple-900/90 to-blue-900/90`
- HRM: `from-pink-900/80 to-purple-900/80`
- Swarm: `from-blue-900/80 to-cyan-900/80`
- Quality: `from-purple-900/80 to-indigo-900/80`
- Agent: `from-green-900/80 to-emerald-900/80`
- Infrastructure: `from-orange-900/80 to-amber-900/80`

## Integration Points

### WebSocket Updates
```tsx
useEffect(() => {
  socket.on('metric_update', (data) => {
    setNodeMetrics(data.nodeId, data.metrics);
  });

  socket.on('status_change', (data) => {
    setNodeStatus(data.nodeId, data.status);
  });

  return () => {
    socket.off('metric_update');
    socket.off('status_change');
  };
}, []);
```

### API Integration
```tsx
const { data } = useQuery('swarm-metrics', async () => {
  const res = await fetch('/api/swarm/metrics');
  return res.json();
});

useEffect(() => {
  if (data) {
    updateMultipleMetrics(data.metrics);
  }
}, [data]);
```

## Performance Considerations

1. **Zustand Store**: Efficient state management with Map for O(1) lookups
2. **Memoization**: Uses React.memo and useMemo for expensive calculations
3. **Dagre Layout**: Computed once, cached until graph structure changes
4. **Animation Toggle**: Can disable animations for better performance
5. **Selective Updates**: Use `updateMultipleMetrics` for bulk operations

## Dependencies

```json
{
  "reactflow": "^11.10.4",
  "dagre": "^0.8.5",
  "@types/dagre": "^0.7.52",
  "zustand": "^4.4.7"
}
```

## File Structure

```
dashboard/frontend/src/
├── components/
│   ├── SwarmGraph.tsx           # Main graph component
│   └── ui/
│       ├── card.tsx
│       ├── badge.tsx
│       └── button.tsx
├── lib/
│   ├── swarmStore.ts            # Zustand store
│   └── graphLayout.ts           # Layout configuration
└── pages/
    └── SwarmVisualization.tsx   # Example page
```

## Navigation

The Swarm Graph is accessible via:
- **Route**: `/swarm`
- **Sidebar**: "Swarm Graph" (with "NEW" badge)
- **Icon**: Network icon

## Future Enhancements

Potential improvements:
1. **Real-time Updates**: WebSocket integration for live metrics
2. **Node Expansion**: Click to expand node details inline
3. **Edge Filtering**: Show/hide edges by type or status
4. **Layout Options**: Switch between Dagre layouts (TB, LR, RL, BT)
5. **Export**: Export graph as PNG/SVG
6. **Custom Themes**: Dark/light mode with theme variants
7. **Performance Metrics**: Built-in performance monitoring
8. **Zoom to Node**: Double-click to zoom and center on node
9. **Search**: Search and highlight nodes by name
10. **History**: Undo/redo for graph interactions

## Troubleshooting

### Graph not rendering
- Ensure React Flow CSS is imported: `import 'reactflow/dist/style.css'`
- Check console for errors
- Verify all dependencies are installed

### Layout issues
- Try toggling auto-layout off/on
- Check NODE_DIMENSIONS in graphLayout.ts
- Verify Dagre is installed correctly

### Performance issues
- Disable animations: `setAnimated(false)`
- Reduce update frequency
- Use `updateMultipleMetrics` instead of multiple `setNodeMetrics`

## License

Part of the Phantom Neural Cortex dashboard.
