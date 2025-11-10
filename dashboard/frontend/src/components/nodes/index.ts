// Export all node components for easy import
export { default as ProjectNode } from './ProjectNode'
export { default as HRMNode } from './HRMNode'
export { default as SwarmNode } from './SwarmNode'
export { default as QualityNode } from './QualityNode'
export { default as AgentNode } from './AgentNode'
export { default as CacheNode } from './CacheNode'
export { default as MetricsNode } from './MetricsNode'

// Node type definitions for React Flow
export const nodeTypes = {
  projectNode: ProjectNode,
  hrmNode: HRMNode,
  swarmNode: SwarmNode,
  qualityNode: QualityNode,
  agentNode: AgentNode,
  cacheNode: CacheNode,
  metricsNode: MetricsNode,
}

// Common node data interface
export interface NodeData {
  label: string
  status: 'active' | 'idle' | 'warning' | 'error'
  metrics: {
    activity: number
    health: number
    cost: number
    performance: number
  }
  config: any
}
