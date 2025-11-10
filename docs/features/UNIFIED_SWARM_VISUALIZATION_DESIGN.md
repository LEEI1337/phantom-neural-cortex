# Unified Swarm Visualization - Enterprise Design Specification

**Project:** Phantom Neural Cortex
**Feature:** Unified HRM + Settings + Swarm Visualization Page
**Version:** 3.0.0 - COMPLETE REDESIGN
**Date:** 2025-11-10
**Status:** ENTERPRISE GRADE - NO COMPROMISES

---

## 1. EXECUTIVE SUMMARY

### Vision
**ONE UNIFIED PAGE** that visualizes the entire AI orchestration system as an **interactive network diagram**. Users see all components (HRM, Agents, Swarm, Cache, Quality, Metrics) as **interconnected nodes**. Clicking on any node opens its configuration panel **in place** with collapsible controls.

### Key Principles
1. ✅ **Visual First** - Network graph shows all system relationships
2. ✅ **Interactive Nodes** - Click to expand/collapse settings
3. ✅ **Real-time Updates** - Nodes pulse/glow with live data
4. ✅ **No Separate Pages** - Everything in ONE unified interface
5. ✅ **Enterprise Grade** - Production-ready, scalable, maintainable

---

## 2. SYSTEM ARCHITECTURE VISUALIZATION

### 2.1 The Complete Swarm Network

```
┌─────────────────────────────────────────────────────────────────┐
│  🧠 PHANTOM NEURAL CORTEX - UNIFIED SWARM CONTROL CENTER        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  [Live Mode] [Topology View] [Impact Mode] [History]   🔴 LIVE │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                                                         │   │
│  │                  INTERACTIVE SWARM GRAPH                │   │
│  │                                                         │   │
│  │        ┌──────────┐                                     │   │
│  │        │  PROJECT │                                     │   │
│  │        │ Projekt-A│                                     │   │
│  │        └────┬─────┘                                     │   │
│  │             │                                           │   │
│  │     ┌───────┼───────┐                                   │   │
│  │     │       │       │                                   │   │
│  │ ┌───▼───┐ ┌▼───────▼┐ ┌─────────┐                      │   │
│  │ │  HRM  │ │  SWARM  │ │ QUALITY │                      │   │
│  │ │CONFIG │ │ ORCHESTR│ │ SYSTEM  │                      │   │
│  │ └───┬───┘ └┬───────┬┘ └────┬────┘                      │   │
│  │     │      │       │       │                            │   │
│  │     │   ┌──┴──┐ ┌──┴──┐    │                            │   │
│  │     │   │Agent│ │Agent│    │                            │   │
│  │     │   │Pool │ │Route│    │                            │   │
│  │     │   └──┬──┘ └──┬──┘    │                            │   │
│  │     │      │       │       │                            │   │
│  │  ┌──▼──────▼───────▼───────▼────┐                       │   │
│  │  │         AGENTS LAYER          │                       │   │
│  │  │  ⚡Claude  💎Gemini  🚀Copilot │                       │   │
│  │  │  📐Cursor  🌊Windsurf          │                       │   │
│  │  └──┬──────┬────────┬────────┬───┘                       │   │
│  │     │      │        │        │                           │   │
│  │  ┌──▼──┐ ┌▼────┐ ┌─▼────┐ ┌▼────┐                       │   │
│  │  │CACHE│ │METRICS│ │COST │ │LOGS │                       │   │
│  │  │LAYER│ │EXPORT │ │TRACK│ │     │                       │   │
│  │  └─────┘ └──────┘ └──────┘ └─────┘                       │   │
│  │                                                         │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ 📊 SELECTED NODE: HRM CONFIG                            │   │
│  ├─────────────────────────────────────────────────────────┤   │
│  │                                                         │   │
│  │  [Core Optimizations ▼]  [Agent Control ▼]  [Quality ▼]│   │
│  │                                                         │   │
│  │  Impact Preview:  Cost: -28% ⬇️  Speed: +30% ⬆️          │   │
│  │                   Quality: +6% ⬆️  Tokens: -40% ⬇️       │   │
│  │                                                         │   │
│  │  [Apply to Running Tasks]  [Save as Preset]  [Reset]   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. NODE TYPES & LAYERS

### 3.1 System Layers (Top to Bottom)

```
LAYER 0: PROJECT LAYER
├─ Projects (Projekt-A, Projekt-B, etc.)
├─ Status: Active/Paused/Archived
└─ 5-Dimension Config Visualization

LAYER 1: ORCHESTRATION LAYER
├─ HRM Configuration
│  ├─ 12 ML/RL Optimizations
│  ├─ Presets (Speed/Cost/Quality/Balanced)
│  └─ Real-time Parameter Control
│
├─ Swarm Orchestration
│  ├─ Agent Pool (5 agents)
│  ├─ Agent Routing Logic
│  ├─ Load Balancing
│  └─ Parallelization Settings
│
└─ Quality System
   ├─ Quality Metrics (7 dimensions)
   ├─ Deep Supervision Checkpoints
   └─ Parallel Evaluation

LAYER 2: AGENTS LAYER
├─ Claude (Quality-First)
├─ Gemini (Cost-Optimized)
├─ Copilot (Code-Specialized)
├─ Cursor (IDE-Integrated)
└─ Windsurf (Multi-Modal)

LAYER 3: INFRASTRUCTURE LAYER
├─ Cache Layer (Memory/Disk/Remote)
├─ Metrics Export (Prometheus)
├─ Cost Tracking
├─ System Logs
└─ API Keys Management
```

---

## 4. INTERACTIVE NODE DESIGN

### 4.1 Node States

```tsx
type NodeState = {
  id: string
  type: 'project' | 'hrm' | 'swarm' | 'agent' | 'cache' | 'metrics'
  label: string
  status: 'active' | 'idle' | 'warning' | 'error'
  connections: string[]  // IDs of connected nodes
  metrics: {
    activity: number  // 0-100%
    health: number    // 0-100%
    cost: number      // USD
    performance: number  // 0-100%
  }
  config: any  // Node-specific configuration
  collapsed: boolean  // Expanded or collapsed
}
```

### 4.2 Node Visual Design

```
┌─────────────────────┐
│   🧠 HRM CONFIG     │  ← Icon + Label
├─────────────────────┤
│ ● Active  95% ⚡    │  ← Status Badge + Health
├─────────────────────┤
│ 12 Optimizations    │  ← Quick Stats
│ Balanced Preset     │
│ $1.80/task avg      │
└─────────────────────┘
         ↓ ↑
    (connections)
```

**Collapsed (Default):**
- Icon + Label
- Status indicator (dot)
- Key metric (health %)
- Small visual indicator

**Expanded (On Click):**
- Full node with detailed panel below
- All configuration options
- Live metrics
- Connection visualization

---

## 5. PAGE LAYOUT STRUCTURE

### 5.1 Main Layout

```
┌─────────────────────────────────────────────────────────────────┐
│ HEADER BAR                                                      │
│ [Logo] Phantom Neural Cortex       [Search] [Alerts] [Profile] │
├──────┬──────────────────────────────────────────────────────────┤
│      │  MAIN CANVAS (60%)        │  CONTROL PANEL (40%)        │
│ SIDE │                            │                             │
│ BAR  │  ┌──────────────────────┐  │  ┌──────────────────────┐  │
│      │  │                      │  │  │  SELECTED NODE       │  │
│ [🏠] │  │   SWARM NETWORK      │  │  │  CONFIGURATION       │  │
│ [📊] │  │   VISUALIZATION      │  │  │                      │  │
│ [⚙️] │  │   (Interactive       │  │  │  [Tabs]              │  │
│ [📈] │  │    React Flow)       │  │  │  [Controls]          │  │
│ [🔧] │  │                      │  │  │  [Metrics]           │  │
│      │  │                      │  │  │  [Actions]           │  │
│      │  └──────────────────────┘  │  └──────────────────────┘  │
│      │                            │                             │
│      │  [Minimap]  [Zoom] [Fit]  │  [Apply] [Reset] [Save]    │
├──────┴────────────────────────────┴─────────────────────────────┤
│ BOTTOM STATUS BAR                                               │
│ 🟢 All Systems Operational  │  5 Agents Active  │  $2.50/hr    │
└─────────────────────────────────────────────────────────────────┘
```

**Layout Ratios:**
- Sidebar: 80px (fixed)
- Main Canvas: 60% (graph visualization)
- Control Panel: 40% (node configuration)

**Responsive Behavior:**
- Desktop (>1440px): Side-by-side layout
- Tablet (768-1440px): Slide-out control panel
- Mobile (<768px): Full-screen graph, modal for controls

---

## 6. NODE CONFIGURATION PANELS

### 6.1 HRM Configuration Panel

**When HRM node is clicked:**

```
┌─────────────────────────────────────────────────────────────┐
│ 🧠 HRM CONFIGURATION                                   [✕]  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ Quick Actions:                                              │
│ [⚡ Speed] [💰 Cost] [🎯 Quality] [⚖️ Balanced] [Reset]    │
│                                                             │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ 📊 Live Impact Preview                                  │ │
│ ├─────────────────────────────────────────────────────────┤ │
│ │ Cost:    $2.50 → $1.80 (-28%) ⬇️                        │ │
│ │ Speed:   450s  → 315s  (+30%) ⬆️                        │ │
│ │ Quality: 87%   → 92%   (+6%)  ⬆️                        │ │
│ │ Tokens:  50k   → 30k   (-40%) ⬇️                        │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ ┌─ Core Optimizations ────────────────────────────────┐    │
│ │                                                      │    │
│ │ Latent Reasoning Compression                         │    │
│ │ Enabled: [✅ ON]                                     │    │
│ │ Dimensionality: 128 ●────●──● 512 ●────● 1024       │    │
│ │ Compression: [3.8x]  Token Savings: [40%]           │    │
│ │                                                      │    │
│ │ ML Iteration Prediction                              │    │
│ │ Mode: [Auto ▼] [Manual] [Fixed]                     │    │
│ │ Max Iterations: 2 ●────●──● 7 ●────● 20             │    │
│ │ Confidence: [85%]  Accuracy: [82%]                   │    │
│ │                                                      │    │
│ │ Three-Layer Caching                                  │    │
│ │ [✅ Memory] [✅ Disk] [❌ Remote] [✅ Aggressive]     │    │
│ │ Max Size: 100MB ●────────● 500MB ────────● 5000MB   │    │
│ │                                                      │    │
│ └──────────────────────────────────────────────────────┘    │
│                                                             │
│ ┌─ Agent Control ─────────────────────────────────────┐    │
│ │                                                      │    │
│ │ Smart Agent Switching                                │    │
│ │ Strategy:                                            │    │
│ │ ○ Cost-Optimized (Gemini-first)                     │    │
│ │ ○ Quality-First (Claude-first)                      │    │
│ │ ○ Speed-Optimized (Fastest)                         │    │
│ │ ● Adaptive (ML-predicted) ✅ Recommended            │    │
│ │ ○ Round-Robin (Equal distribution)                  │    │
│ │ ○ Manual (No switching)                             │    │
│ │                                                      │    │
│ │ Thresholds:                                          │    │
│ │ Quality Drop: 0% ●────● 20% ────────────────● 100%  │    │
│ │ Cost Ceiling: $1 ●──────● $5 ────────────● $20      │    │
│ │ Max Switches: 0 ●─● 3 ──────────────────● 10        │    │
│ │                                                      │    │
│ └──────────────────────────────────────────────────────┘    │
│                                                             │
│ ┌─ Quality & Testing ─────────────────────────────────┐    │
│ │                                                      │    │
│ │ Deep Supervision Checkpoints                         │    │
│ │ Enabled: [✅ ON]                                     │    │
│ │ Checkpoints: [33%] [66%] [100%]                     │    │
│ │ Quality Gate: 50% ●──────● 75% ──────────● 100%     │    │
│ │                                                      │    │
│ │ Parallel Quality Evaluation                          │    │
│ │ Enabled: [✅ ON]                                     │    │
│ │ Workers: 1 ●──● 4 ───────────────────● 16           │    │
│ │ Timeout: 10s ●────● 60s ──────────● 300s            │    │
│ │                                                      │    │
│ └──────────────────────────────────────────────────────┘    │
│                                                             │
│ ┌─ Advanced Options ──────────────────────────────────┐    │
│ │                                                      │    │
│ │ Bayesian Optimization                                │    │
│ │ Enabled: [❌ OFF]                                    │    │
│ │ Iterations: 10 ●──────● 30 ─────────────● 100       │    │
│ │                                                      │    │
│ │ RL Refinement Chain                                  │    │
│ │ Enabled: [✅ ON]                                     │    │
│ │ Epsilon: 0.0 ●─● 0.1 ───────────────────● 1.0       │    │
│ │ Learning Rate: 0.0001 ●──● 0.001 ────● 0.1          │    │
│ │                                                      │    │
│ │ Other Settings                                       │    │
│ │ [✅ Prometheus Metrics] Export Interval: [15s]       │    │
│ │ [✅ Multi-Repository Coordination]                   │    │
│ │                                                      │    │
│ └──────────────────────────────────────────────────────┘    │
│                                                             │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ [Apply Changes]  [Simulate Impact]  [Save as Preset]  │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

### 6.2 Agent Node Configuration Panel

**When Claude agent node is clicked:**

```
┌─────────────────────────────────────────────────────────────┐
│ ⚡ CLAUDE AGENT                                        [✕]  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ Status: 🟢 Active  |  Quality Tier: Premium                │
│                                                             │
│ ┌─ Performance Metrics ────────────────────────────────┐   │
│ │ Tasks Completed: 342                                 │   │
│ │ Success Rate: 96.5%                                  │   │
│ │ Avg Quality: 94%                                     │   │
│ │ Avg Cost: $3.20/task                                 │   │
│ │ Avg Duration: 285s                                   │   │
│ └──────────────────────────────────────────────────────┘   │
│                                                             │
│ ┌─ Specializations ────────────────────────────────────┐   │
│ │ ✅ Complex Reasoning (95% strength)                  │   │
│ │ ✅ Code Quality (92% strength)                       │   │
│ │ ✅ Documentation (90% strength)                      │   │
│ │ ⚠️ Speed (65% strength)                              │   │
│ │ ⚠️ Cost Efficiency (40% strength)                    │   │
│ └──────────────────────────────────────────────────────┘   │
│                                                             │
│ ┌─ API Configuration ──────────────────────────────────┐   │
│ │ Provider: Anthropic                                  │   │
│ │ Model: claude-sonnet-4-5                             │   │
│ │ API Key: sk-ant-***************abc [✅ Valid]        │   │
│ │ Rate Limit: 1000/min                                 │   │
│ │ Current Usage: 142/1000 (14%)                        │   │
│ └──────────────────────────────────────────────────────┘   │
│                                                             │
│ ┌─ Routing Rules ──────────────────────────────────────┐   │
│ │ Use Claude when:                                     │   │
│ │ [✅] Quality threshold > 90%                         │   │
│ │ [✅] Task complexity > 8.0                           │   │
│ │ [✅] Security critical = true                        │   │
│ │ [❌] Cost ceiling exceeded                           │   │
│ │                                                      │   │
│ │ Fallback Agent: Gemini                               │   │
│ └──────────────────────────────────────────────────────┘   │
│                                                             │
│ [Edit Routing] [Test Connection] [View Logs]               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

### 6.3 Swarm Orchestration Panel

**When Swarm node is clicked:**

```
┌─────────────────────────────────────────────────────────────┐
│ 🌊 SWARM ORCHESTRATION                                [✕]  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ Active Swarm: default  [Change ▼]                          │
│                                                             │
│ ┌─ Parallelization ────────────────────────────────────┐   │
│ │ Max Parallel Tasks: 1 ●──● 10 ───────────● 50       │   │
│ │ Max Parallel Agents: 1 ●─● 5 ────────────● 20       │   │
│ │ Auto-Scale: [✅ Enabled]                             │   │
│ │   Scale Up Threshold: 80% queue depth                │   │
│ │   Scale Down Threshold: 20% queue depth              │   │
│ └──────────────────────────────────────────────────────┘   │
│                                                             │
│ ┌─ Intelligence Mode ──────────────────────────────────┐   │
│ │ ○ Speed-Optimized (Fastest completion)               │   │
│ │ ○ Cost-Optimized (Minimum cost)                      │   │
│ │ ○ Quality-Optimized (Maximum quality)                │   │
│ │ ● Balanced (Equal weight)                            │   │
│ │                                                      │   │
│ │ Custom Weights:                                      │   │
│ │ Speed:   33% ●──────────────────────● 100%           │   │
│ │ Cost:    33% ●──────────────────────● 100%           │   │
│ │ Quality: 34% ●──────────────────────● 100%           │   │
│ └──────────────────────────────────────────────────────┘   │
│                                                             │
│ ┌─ Feedback Loops ─────────────────────────────────────┐   │
│ │ Adaptive Iterations: [✅ Enabled]                    │   │
│ │ Max Iterations per Task: 2 ●─● 7 ────────● 20       │   │
│ │ Learning Rate: 0.001 ●────● 0.01 ─────● 0.1         │   │
│ │ Exploration Factor: 0% ●──● 10% ──────● 100%        │   │
│ └──────────────────────────────────────────────────────┘   │
│                                                             │
│ ┌─ Cost Control ───────────────────────────────────────┐   │
│ │ Daily Budget: $0 ●─────● $100 ────────● $1000        │   │
│ │ Per-Task Limit: $0 ●───● $10 ─────────● $100         │   │
│ │ Prefer Cheaper Models: [✅ Enabled]                  │   │
│ │                                                      │   │
│ │ Current Usage Today:                                 │   │
│ │ $45.20 / $100 (45%) ████████░░░░░░░░░░░              │   │
│ └──────────────────────────────────────────────────────┘   │
│                                                             │
│ [Apply] [Load Config] [Save as Preset]                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

### 6.4 System Health Panel

**When any infrastructure node is clicked:**

```
┌─────────────────────────────────────────────────────────────┐
│ 🏥 SYSTEM HEALTH & INFRASTRUCTURE                     [✕]  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ Overall Status: 🟢 All Systems Operational                 │
│                                                             │
│ ┌─ Components ──────────────────────────────────────────┐  │
│ │                                                        │  │
│ │ Database (PostgreSQL)                                  │  │
│ │ Status: 🟢 Connected  |  Latency: 12ms  |  Pool: 8/20 │  │
│ │                                                        │  │
│ │ Cache (Redis)                                          │  │
│ │ Status: 🟢 Connected  |  Hit Rate: 87%  |  Mem: 45%   │  │
│ │                                                        │  │
│ │ WebSocket Server                                       │  │
│ │ Status: 🟢 Running  |  Connections: 12  |  Events: 340│  │
│ │                                                        │  │
│ │ Backend API                                            │  │
│ │ Status: 🟢 Healthy  |  RPS: 45  |  Avg Latency: 78ms  │  │
│ │                                                        │  │
│ └────────────────────────────────────────────────────────┘  │
│                                                             │
│ ┌─ Cache Management ───────────────────────────────────┐   │
│ │                                                      │   │
│ │ Guideline Cache                                      │   │
│ │ Size: 145MB  |  Entries: 2,340  |  Hit Rate: 87%    │   │
│ │ [Clear Cache]                                        │   │
│ │                                                      │   │
│ │ GitHub API Cache                                     │   │
│ │ Size: 89MB   |  Entries: 1,203  |  Hit Rate: 92%    │   │
│ │ [Clear Cache]                                        │   │
│ │                                                      │   │
│ │ Quality Pattern Cache                                │   │
│ │ Size: 56MB   |  Entries: 890    |  Hit Rate: 88%    │   │
│ │ [Clear Cache]                                        │   │
│ │                                                      │   │
│ │ [Clear All Caches]                                   │   │
│ │                                                      │   │
│ └──────────────────────────────────────────────────────┘   │
│                                                             │
│ ┌─ Real-time Metrics ──────────────────────────────────┐   │
│ │                                                      │   │
│ │ Requests per Second: 45.3 ████████░░                 │   │
│ │ Avg Response Time:   78ms ███░░░░░░░                 │   │
│ │ Error Rate:          0.2% █░░░░░░░░░░                │   │
│ │ CPU Usage:           34%  ████░░░░░░░                │   │
│ │ Memory Usage:        58%  ██████░░░░░                │   │
│ │                                                      │   │
│ └──────────────────────────────────────────────────────┘   │
│                                                             │
│ [View Logs] [Download Report] [Configure Alerts]           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 7. INTERACTIVE NETWORK GRAPH IMPLEMENTATION

### 7.1 React Flow Configuration

```tsx
import ReactFlow, {
  Node,
  Edge,
  Controls,
  MiniMap,
  Background,
  useNodesState,
  useEdgesState,
  ConnectionMode,
} from 'reactflow'

interface SwarmNode extends Node {
  data: {
    label: string
    type: 'project' | 'hrm' | 'swarm' | 'agent' | 'cache' | 'metrics'
    status: 'active' | 'idle' | 'warning' | 'error'
    metrics: {
      activity: number
      health: number
      cost: number
      performance: number
    }
    config: any
  }
}

const INITIAL_NODES: SwarmNode[] = [
  // LAYER 0: Project
  {
    id: 'project-a',
    type: 'projectNode',
    position: { x: 400, y: 50 },
    data: {
      label: 'Projekt-A',
      type: 'project',
      status: 'active',
      metrics: { activity: 85, health: 95, cost: 2.50, performance: 90 },
      config: { /* 5D config */ }
    }
  },

  // LAYER 1: Orchestration
  {
    id: 'hrm-config',
    type: 'hrmNode',
    position: { x: 200, y: 200 },
    data: {
      label: 'HRM Config',
      type: 'hrm',
      status: 'active',
      metrics: { activity: 90, health: 98, cost: 1.80, performance: 95 },
      config: { /* 12 optimizations */ }
    }
  },

  {
    id: 'swarm-orchestration',
    type: 'swarmNode',
    position: { x: 400, y: 200 },
    data: {
      label: 'Swarm Orchestration',
      type: 'swarm',
      status: 'active',
      metrics: { activity: 75, health: 92, cost: 0, performance: 88 },
      config: { /* swarm settings */ }
    }
  },

  {
    id: 'quality-system',
    type: 'qualityNode',
    position: { x: 600, y: 200 },
    data: {
      label: 'Quality System',
      type: 'metrics',
      status: 'active',
      metrics: { activity: 80, health: 96, cost: 0, performance: 92 },
      config: { /* quality thresholds */ }
    }
  },

  // LAYER 2: Agents
  {
    id: 'agent-claude',
    type: 'agentNode',
    position: { x: 100, y: 400 },
    data: {
      label: 'Claude',
      type: 'agent',
      status: 'active',
      metrics: { activity: 95, health: 99, cost: 3.20, performance: 96 },
      config: { /* Claude config */ }
    }
  },

  {
    id: 'agent-gemini',
    type: 'agentNode',
    position: { x: 250, y: 400 },
    data: {
      label: 'Gemini',
      type: 'agent',
      status: 'active',
      metrics: { activity: 60, health: 94, cost: 0.00, performance: 82 },
      config: { /* Gemini config */ }
    }
  },

  {
    id: 'agent-copilot',
    type: 'agentNode',
    position: { x: 400, y: 400 },
    data: {
      label: 'Copilot',
      type: 'agent',
      status: 'idle',
      metrics: { activity: 0, health: 100, cost: 0.00, performance: 0 },
      config: { /* Copilot config */ }
    }
  },

  {
    id: 'agent-cursor',
    type: 'agentNode',
    position: { x: 550, y: 400 },
    data: {
      label: 'Cursor',
      type: 'agent',
      status: 'idle',
      metrics: { activity: 0, health: 100, cost: 0.00, performance: 0 },
      config: { /* Cursor config */ }
    }
  },

  {
    id: 'agent-windsurf',
    type: 'agentNode',
    position: { x: 700, y: 400 },
    data: {
      label: 'Windsurf',
      type: 'agent',
      status: 'idle',
      metrics: { activity: 0, health: 100, cost: 0.00, performance: 0 },
      config: { /* Windsurf config */ }
    }
  },

  // LAYER 3: Infrastructure
  {
    id: 'cache-layer',
    type: 'cacheNode',
    position: { x: 150, y: 600 },
    data: {
      label: 'Cache Layer',
      type: 'cache',
      status: 'active',
      metrics: { activity: 87, health: 100, cost: 0, performance: 95 },
      config: { /* cache config */ }
    }
  },

  {
    id: 'metrics-export',
    type: 'metricsNode',
    position: { x: 350, y: 600 },
    data: {
      label: 'Metrics Export',
      type: 'metrics',
      status: 'active',
      metrics: { activity: 100, health: 100, cost: 0, performance: 100 },
      config: { /* prometheus config */ }
    }
  },

  {
    id: 'cost-tracking',
    type: 'costNode',
    position: { x: 550, y: 600 },
    data: {
      label: 'Cost Tracking',
      type: 'metrics',
      status: 'active',
      metrics: { activity: 100, health: 100, cost: 0, performance: 100 },
      config: { /* cost config */ }
    }
  },
]

const INITIAL_EDGES: Edge[] = [
  // Project → Orchestration Layer
  { id: 'e1', source: 'project-a', target: 'hrm-config', animated: true },
  { id: 'e2', source: 'project-a', target: 'swarm-orchestration', animated: true },
  { id: 'e3', source: 'project-a', target: 'quality-system', animated: true },

  // HRM → Agents
  { id: 'e4', source: 'hrm-config', target: 'agent-claude', animated: true },
  { id: 'e5', source: 'hrm-config', target: 'agent-gemini', animated: true },

  // Swarm → Agents
  { id: 'e6', source: 'swarm-orchestration', target: 'agent-claude', animated: true },
  { id: 'e7', source: 'swarm-orchestration', target: 'agent-gemini', animated: true },
  { id: 'e8', source: 'swarm-orchestration', target: 'agent-copilot', animated: false },
  { id: 'e9', source: 'swarm-orchestration', target: 'agent-cursor', animated: false },
  { id: 'e10', source: 'swarm-orchestration', target: 'agent-windsurf', animated: false },

  // Quality → Agents
  { id: 'e11', source: 'quality-system', target: 'agent-claude', animated: true },
  { id: 'e12', source: 'quality-system', target: 'agent-gemini', animated: true },

  // Agents → Infrastructure
  { id: 'e13', source: 'agent-claude', target: 'cache-layer', animated: true },
  { id: 'e14', source: 'agent-gemini', target: 'cache-layer', animated: true },
  { id: 'e15', source: 'agent-claude', target: 'metrics-export', animated: true },
  { id: 'e16', source: 'agent-gemini', target: 'metrics-export', animated: true },
  { id: 'e17', source: 'agent-claude', target: 'cost-tracking', animated: true },
  { id: 'e18', source: 'agent-gemini', target: 'cost-tracking', animated: true },
]
```

---

### 7.2 Custom Node Components

#### Project Node

```tsx
import { Handle, Position } from 'reactflow'

const ProjectNode = ({ data }: { data: SwarmNode['data'] }) => {
  return (
    <div className="project-node">
      <div className="node-header">
        <span className="icon">📁</span>
        <span className="label">{data.label}</span>
        <span className={`status ${data.status}`}>●</span>
      </div>

      <div className="node-body">
        <div className="metric">
          <span>Activity:</span>
          <span className="value">{data.metrics.activity}%</span>
        </div>
        <div className="metric">
          <span>Health:</span>
          <span className="value">{data.metrics.health}%</span>
        </div>
        <div className="metric">
          <span>Cost:</span>
          <span className="value">${data.metrics.cost}/hr</span>
        </div>
      </div>

      <Handle type="source" position={Position.Bottom} />
    </div>
  )
}
```

#### HRM Node

```tsx
const HRMNode = ({ data }: { data: SwarmNode['data'] }) => {
  return (
    <div className="hrm-node">
      <Handle type="target" position={Position.Top} />

      <div className="node-header">
        <span className="icon">🧠</span>
        <span className="label">{data.label}</span>
        <span className={`status ${data.status}`}>●</span>
      </div>

      <div className="node-body">
        <div className="stats">
          <span className="stat">12 Optimizations</span>
          <span className="stat">Balanced Preset</span>
        </div>
        <div className="metrics">
          <div className="metric-item">
            <span className="icon">⚡</span>
            <span className="value">{data.metrics.performance}%</span>
          </div>
          <div className="metric-item">
            <span className="icon">💰</span>
            <span className="value">${data.metrics.cost}</span>
          </div>
        </div>
      </div>

      <Handle type="source" position={Position.Bottom} />
    </div>
  )
}
```

#### Agent Node

```tsx
const AgentNode = ({ data }: { data: SwarmNode['data'] }) => {
  const agentIcons = {
    'Claude': '⚡',
    'Gemini': '💎',
    'Copilot': '🚀',
    'Cursor': '📐',
    'Windsurf': '🌊'
  }

  return (
    <div className={`agent-node ${data.status}`}>
      <Handle type="target" position={Position.Top} />

      <div className="node-header">
        <span className="icon">{agentIcons[data.label] || '🤖'}</span>
        <span className="label">{data.label}</span>
      </div>

      <div className="node-body">
        {data.status === 'active' ? (
          <>
            <div className="activity-pulse" />
            <div className="metrics-compact">
              <span>{data.metrics.health}% health</span>
              <span>${data.metrics.cost}/task</span>
            </div>
          </>
        ) : (
          <div className="idle-state">
            <span>Idle</span>
          </div>
        )}
      </div>

      <Handle type="source" position={Position.Bottom} />
    </div>
  )
}
```

---

### 7.3 Node Styling (Cyberpunk Theme)

```css
/* Base Node Styles */
.project-node,
.hrm-node,
.swarm-node,
.agent-node,
.cache-node,
.metrics-node {
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  border: 2px solid #06b6d4;
  border-radius: 12px;
  padding: 16px;
  min-width: 180px;
  box-shadow: 0 8px 24px rgba(6, 182, 212, 0.25);
  transition: all 0.3s ease;
}

.project-node:hover,
.hrm-node:hover,
.agent-node:hover {
  border-color: #0ea5e9;
  box-shadow: 0 12px 32px rgba(6, 182, 212, 0.4);
  transform: translateY(-2px);
}

/* Node Header */
.node-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}

.node-header .icon {
  font-size: 24px;
}

.node-header .label {
  flex: 1;
  font-weight: 600;
  font-size: 14px;
  color: #f1f5f9;
}

.node-header .status {
  font-size: 12px;
}

.status.active {
  color: #22c55e;
  animation: pulse 2s ease-in-out infinite;
}

.status.idle {
  color: #64748b;
}

.status.warning {
  color: #f59e0b;
}

.status.error {
  color: #ef4444;
}

/* Node Body */
.node-body {
  font-size: 12px;
  color: #94a3b8;
}

.metric {
  display: flex;
  justify-content: space-between;
  margin-bottom: 4px;
}

.metric .value {
  color: #06b6d4;
  font-weight: 600;
}

/* Agent Node - Active State */
.agent-node.active {
  border-color: #22c55e;
  box-shadow: 0 8px 24px rgba(34, 197, 94, 0.3);
}

.agent-node.active .activity-pulse {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 8px;
  height: 8px;
  background: #22c55e;
  border-radius: 50%;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(1.2); }
}

/* Edge Styles */
.react-flow__edge-path {
  stroke: #06b6d4;
  stroke-width: 2;
}

.react-flow__edge.animated .react-flow__edge-path {
  stroke-dasharray: 5;
  animation: dashdraw 0.5s linear infinite;
}

@keyframes dashdraw {
  to { stroke-dashoffset: -10; }
}
```

---

## 8. REAL-TIME UPDATES & WEBSOCKET INTEGRATION

### 8.1 WebSocket Events for Graph Updates

```tsx
import { useEffect } from 'react'
import { useWebSocket } from '@/lib/websocket'

const SwarmVisualization = () => {
  const [nodes, setNodes, onNodesChange] = useNodesState(INITIAL_NODES)
  const [edges, setEdges, onEdgesChange] = useEdgesState(INITIAL_EDGES)
  const socket = useWebSocket()

  useEffect(() => {
    // HRM Config Update → Update HRM node metrics
    socket.on('hrm_config_update', (data) => {
      setNodes((nds) =>
        nds.map((node) => {
          if (node.id === 'hrm-config') {
            return {
              ...node,
              data: {
                ...node.data,
                config: data.config,
                metrics: {
                  ...node.data.metrics,
                  performance: calculatePerformance(data.config)
                }
              }
            }
          }
          return node
        })
      )
    })

    // Agent Switch → Animate edge & update agent status
    socket.on('agent_switch', (data) => {
      // Deactivate old agent
      setNodes((nds) =>
        nds.map((node) => {
          if (node.id === `agent-${data.from_agent.toLowerCase()}`) {
            return {
              ...node,
              data: { ...node.data, status: 'idle' as const }
            }
          }
          if (node.id === `agent-${data.to_agent.toLowerCase()}`) {
            return {
              ...node,
              data: { ...node.data, status: 'active' as const }
            }
          }
          return node
        })
      )

      // Animate edge between swarm and new agent
      setEdges((eds) =>
        eds.map((edge) => {
          if (
            edge.source === 'swarm-orchestration' &&
            edge.target === `agent-${data.to_agent.toLowerCase()}`
          ) {
            return { ...edge, animated: true, style: { stroke: '#22c55e' } }
          }
          return edge
        })
      )
    })

    // Quality Update → Update quality system node
    socket.on('quality_update', (data) => {
      setNodes((nds) =>
        nds.map((node) => {
          if (node.id === 'quality-system') {
            return {
              ...node,
              data: {
                ...node.data,
                metrics: {
                  ...node.data.metrics,
                  performance: data.overall_quality * 100
                }
              }
            }
          }
          return node
        })
      )
    })

    // Cost Update → Update cost tracking node
    socket.on('cost_update', (data) => {
      setNodes((nds) =>
        nds.map((node) => {
          if (node.id === 'cost-tracking') {
            return {
              ...node,
              data: {
                ...node.data,
                metrics: {
                  ...node.data.metrics,
                  cost: data.total_cost
                }
              }
            }
          }
          return node
        })
      )
    })

    return () => {
      socket.off('hrm_config_update')
      socket.off('agent_switch')
      socket.off('quality_update')
      socket.off('cost_update')
    }
  }, [socket, setNodes, setEdges])

  return (
    <ReactFlow
      nodes={nodes}
      edges={edges}
      onNodesChange={onNodesChange}
      onEdgesChange={onEdgesChange}
      onNodeClick={(event, node) => handleNodeClick(node)}
      fitView
    >
      <Background color="#64748b" gap={16} />
      <Controls />
      <MiniMap
        nodeColor={(node) => {
          if (node.data.status === 'active') return '#22c55e'
          if (node.data.status === 'warning') return '#f59e0b'
          if (node.data.status === 'error') return '#ef4444'
          return '#06b6d4'
        }}
      />
    </ReactFlow>
  )
}
```

---

## 9. CONFIGURATION PANEL STATE MANAGEMENT

### 9.1 Shared State Between Graph & Panel

```tsx
import { create } from 'zustand'

interface UnifiedState {
  // Selected node
  selectedNode: SwarmNode | null
  setSelectedNode: (node: SwarmNode | null) => void

  // HRM Config
  hrmConfig: HRMConfigSchema
  updateHRMConfig: (config: Partial<HRMConfigSchema>) => void

  // Swarm Config
  swarmConfig: SwarmConfig
  updateSwarmConfig: (config: Partial<SwarmConfig>) => void

  // Agents
  agents: AgentConfig[]
  updateAgent: (id: string, config: Partial<AgentConfig>) => void

  // Impact Preview
  impactEstimate: ImpactEstimate | null
  simulateImpact: (config: any) => Promise<void>

  // Apply changes
  applyChanges: () => Promise<void>
  resetChanges: () => void
}

export const useUnifiedStore = create<UnifiedState>((set, get) => ({
  selectedNode: null,
  setSelectedNode: (node) => set({ selectedNode: node }),

  hrmConfig: DEFAULT_HRM_CONFIG,
  updateHRMConfig: (config) =>
    set((state) => ({
      hrmConfig: { ...state.hrmConfig, ...config }
    })),

  swarmConfig: DEFAULT_SWARM_CONFIG,
  updateSwarmConfig: (config) =>
    set((state) => ({
      swarmConfig: { ...state.swarmConfig, ...config }
    })),

  agents: DEFAULT_AGENTS,
  updateAgent: (id, config) =>
    set((state) => ({
      agents: state.agents.map((agent) =>
        agent.id === id ? { ...agent, ...config } : agent
      )
    })),

  impactEstimate: null,
  simulateImpact: async (config) => {
    const response = await api.hrm.simulate({
      current_config: get().hrmConfig,
      proposed_config: config,
      task_context: { complexity: 10.0 }
    })
    set({ impactEstimate: response.impact_analysis })
  },

  applyChanges: async () => {
    const state = get()
    if (state.selectedNode?.data.type === 'hrm') {
      await api.hrm.updateConfig({
        project_id: 'current-project',
        config: state.hrmConfig,
        apply_immediately: true
      })
    }
    // ... other node types
  },

  resetChanges: () => {
    set({
      hrmConfig: DEFAULT_HRM_CONFIG,
      swarmConfig: DEFAULT_SWARM_CONFIG,
      agents: DEFAULT_AGENTS,
      impactEstimate: null
    })
  }
}))
```

---

## 10. USER WORKFLOWS

### 10.1 Adjust HRM Parameters

```
1. User opens Unified Swarm Page
2. Sees full system graph with all nodes
3. Clicks on "HRM Config" node
4. Node expands visually (glow effect)
5. Right panel shows HRM Configuration
6. User adjusts sliders:
   - Latent Reasoning: 512D → 768D
   - Agent Switching: Adaptive → Quality-First
7. Live Impact Preview updates in real-time:
   - Cost: $1.80 → $2.40 (+33%)
   - Quality: 92% → 96% (+4%)
8. User clicks "Simulate Impact"
9. Simulation shows detailed predictions
10. User clicks "Apply Changes"
11. WebSocket event → Graph updates
12. HRM node pulses green (applied successfully)
13. Edges to agents update (Claude edge animates brighter)
```

---

### 10.2 View Agent Performance

```
1. User clicks on "Claude" agent node
2. Right panel shows Claude configuration
3. User sees:
   - Performance metrics (96% quality)
   - Specializations
   - API key status
   - Routing rules
4. User clicks "View Logs"
5. Log panel opens at bottom
6. Shows last 50 Claude operations
7. User identifies pattern: Claude excels at complex reasoning
8. User updates routing rules:
   - "Use Claude when complexity > 8.0" → "complexity > 7.0"
9. Clicks "Apply"
10. Graph updates → More tasks route to Claude
```

---

### 10.3 Optimize for Cost

```
1. User wants to reduce costs by 50%
2. Clicks on "Swarm Orchestration" node
3. Right panel shows swarm config
4. User changes Intelligence Mode: Balanced → Cost-Optimized
5. Impact Preview updates:
   - Cost: $2.50 → $1.25 (-50%)
   - Quality: 92% → 84% (-8%)
6. User acceptable with quality trade-off
7. Clicks "Apply"
8. Graph animates:
   - Swarm node → HRM node edge thickens
   - Agent edges re-route (more to Gemini, less to Claude)
   - Gemini node becomes brighter (more active)
   - Claude node dims (less active)
9. Cost Tracking node updates → Shows new hourly rate
10. User monitors results over next hour
```

---

## 11. IMPLEMENTATION ROADMAP

### Phase 1: Foundation (Week 1)
- [ ] Setup React Flow in unified page
- [ ] Create base node components (Project, HRM, Swarm, Agent, Cache)
- [ ] Implement initial graph layout (INITIAL_NODES, INITIAL_EDGES)
- [ ] Add click handlers for node selection
- [ ] Create right panel container with tabs

### Phase 2: Node Configurations (Week 2)
- [ ] Implement HRM configuration panel (full 12 parameters)
- [ ] Implement Swarm configuration panel
- [ ] Implement Agent configuration panel
- [ ] Implement System Health panel
- [ ] Add Impact Preview component

### Phase 3: Real-time Updates (Week 3)
- [ ] Integrate WebSocket events
- [ ] Update nodes based on WebSocket data
- [ ] Animate edges on agent switches
- [ ] Add node pulse/glow effects
- [ ] Live metrics display

### Phase 4: Advanced Features (Week 4)
- [ ] Node search & filter
- [ ] Multiple graph layouts (hierarchical, circular, force-directed)
- [ ] Node grouping (collapse/expand layers)
- [ ] Export graph as image
- [ ] Preset quick-apply from graph

### Phase 5: Polish & Testing (Week 5)
- [ ] Responsive design (mobile support)
- [ ] Accessibility (keyboard navigation, screen reader)
- [ ] Performance optimization (virtualization)
- [ ] E2E tests with Playwright
- [ ] Documentation

---

## 12. TECHNICAL REQUIREMENTS

### 12.1 Dependencies

```json
{
  "dependencies": {
    "reactflow": "^11.10.0",
    "zustand": "^4.4.0",
    "@tanstack/react-query": "^5.0.0",
    "recharts": "^2.10.0",
    "lucide-react": "^0.300.0",
    "socket.io-client": "^4.6.0"
  }
}
```

### 12.2 Performance Targets

- Initial load: < 2 seconds
- Node click response: < 100ms
- WebSocket update latency: < 200ms
- Graph re-render: < 50ms (60fps)
- Memory usage: < 150MB

---

## 13. SUCCESS METRICS

- ✅ **Single Unified Page** - No separate HRM/Settings pages
- ✅ **Visual Swarm Graph** - All components visualized
- ✅ **Interactive Nodes** - Click to configure
- ✅ **Real-time Updates** - Nodes update live via WebSocket
- ✅ **Collapsible Panels** - Expand/collapse configuration
- ✅ **Enterprise Grade** - Production-ready, maintainable
- ✅ **No Compromises** - Full feature parity with original design

---

## 14. NEXT STEPS

1. ✅ **Design Complete** - This document
2. ⏳ **Backup Frontend** - Move current frontend to frontend.old
3. ⏳ **Implement Graph** - Build React Flow visualization
4. ⏳ **Implement Panels** - Build all configuration panels
5. ⏳ **Integration** - Connect to backend APIs
6. ⏳ **Testing** - E2E tests
7. ⏳ **Deployment** - Production release

---

**Document Status:** ✅ COMPLETE - Ready for Implementation
**Owner:** Phantom Neural Cortex Team
**Last Updated:** 2025-11-10
**Review Status:** Approved for Development
