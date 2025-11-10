# HRM Parameter Control System - UI/UX Design Specification

**Feature:** Real-time HRM (Hierarchical Reasoning Module) Parameter Control via Web Dashboard
**Version:** 2.0.0
**Date:** 2025-11-09

---

## 1. EXECUTIVE SUMMARY

Das HRM-Parameter-Steuerungssystem ermöglicht **Echtzeit-Kontrolle** über alle UltraThink/HRM-Optimierungen direkt über die Web-Oberfläche. Benutzer können mit Reglern, Buttons und interaktiven Komponenten das Verhalten der ML/RL-Systeme präzise steuern.

**Hauptziele:**
1. Intuitive visuelle Steuerung aller 12 ML/RL-Optimierungen
2. Echtzeit-Feedback über Auswirkungen von Parameteränderungen
3. Preset-Management für verschiedene Szenarien
4. Live-Visualisierung der aktuellen Systemkonfiguration
5. A/B-Testing von HRM-Konfigurationen

---

## 2. PARAMETER-KATEGORIEN

### 2.1 Core HRM Parameters (12 Optimizations)

| # | Optimization | Parameter Type | Range | Default | Real-time Adjustable |
|---|--------------|----------------|-------|---------|---------------------|
| 1 | Latent Reasoning Compression | Slider + Toggle | 128D-1024D | 512D | ✅ Yes |
| 2 | ML Iteration Prediction | Toggle + Dropdown | 2-10 iterations | Auto | ✅ Yes |
| 3 | Hierarchical Embeddings | Multi-Select | 256D/512D/1024D | All | ✅ Yes |
| 4 | Deep Supervision Checkpoints | Slider (%) | 0%-100% | 33%/66%/100% | ✅ Yes |
| 5 | Smart Agent Switching | Toggle + Strategy | 6 strategies | Adaptive | ✅ Yes |
| 6 | Parallel Quality Evaluation | Toggle + Workers | 1-16 workers | 4 | ✅ Yes |
| 7 | Three-Layer Caching | Multi-Toggle | Memory/Disk/Remote | All | ✅ Yes |
| 8 | Bayesian Weight Optimization | Slider | Iterations 10-100 | 30 | ⚠️ Limited |
| 9 | Multi-Repository Coordination | Toggle | On/Off | On | ✅ Yes |
| 10 | Prometheus Metrics | Toggle + Interval | 5s-60s | 15s | ✅ Yes |
| 11 | RL Refinement Chain | Slider + Mode | Epsilon 0-1 | 0.1 | ✅ Yes |
| 12 | Cross-Platform Docker | Multi-Select | amd64/arm64/win | All | ❌ No (build-time) |

---

## 3. UI COMPONENT DESIGN

### 3.1 Main HRM Control Panel Layout

```
┌────────────────────────────────────────────────────────────┐
│  🧠 HRM Parameter Control Center                           │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  Preset: [Custom ▼]   [Save Preset]  [Load Preset]       │
│                                                            │
│  ┌───────────────────┐  ┌───────────────────────────┐     │
│  │ Quick Actions     │  │ Real-time Impact          │     │
│  ├───────────────────┤  ├───────────────────────────┤     │
│  │ [Speed Mode]      │  │ Cost: $2.50 → $1.80 ⬇️     │     │
│  │ [Quality Mode]    │  │ Speed: +30% ⬆️             │     │
│  │ [Cost Mode]       │  │ Quality: 87% → 92% ⬆️      │     │
│  │ [Reset to Default]│  │ Tokens: -40% ⬇️            │     │
│  └───────────────────┘  └───────────────────────────┘     │
│                                                            │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ 1️⃣ Latent Reasoning Compression                      │ │
│  ├──────────────────────────────────────────────────────┤ │
│  │ ⚙️ Enabled: [✅ ON]                                   │ │
│  │                                                       │ │
│  │ Dimensionality:                                       │ │
│  │ 128D ●───────●───────● 512D ●───────● 1024D          │ │
│  │  Min       Low      Default  High     Max            │ │
│  │                                                       │ │
│  │ Compression Ratio: [   3.8x   ] (Real-time)         │ │
│  │ Token Savings:     [   40%    ]                      │ │
│  │ Quality Impact:    [   -2%    ]                      │ │
│  │                                                       │ │
│  │ Advanced Options: [⚙️ Show]                           │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                            │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ 2️⃣ ML Iteration Prediction                           │ │
│  ├──────────────────────────────────────────────────────┤ │
│  │ Mode: [🤖 Auto-Predict ▼] [Manual] [Fixed]          │ │
│  │                                                       │ │
│  │ Max Iterations:                                       │ │
│  │ 2 ●───●───●───●───●──● 10                            │ │
│  │                                                       │ │
│  │ Current Task Prediction: [  7 iterations  ]          │ │
│  │ Confidence: [        85%       ] 📊                  │ │
│  │                                                       │ │
│  │ Historical Accuracy: 82% ✅                           │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                            │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ 5️⃣ Smart Agent Switching                             │ │
│  ├──────────────────────────────────────────────────────┤ │
│  │ Strategy: [Adaptive Cost-Quality ▼]                  │ │
│  │                                                       │ │
│  │ Options:                                              │ │
│  │ • Cost-Optimized (Gemini-first)                      │ │
│  │ • Quality-First (Claude-first)                       │ │
│  │ • Speed-Optimized (Fastest available)                │ │
│  │ • Adaptive (ML-predicted best)        ✅ Selected    │ │
│  │ • Round-Robin (Equal distribution)                   │ │
│  │ • Manual (No switching)                              │ │
│  │                                                       │ │
│  │ Switch Thresholds:                                    │ │
│  │ Quality Drop Trigger:  [   20%   ] slider            │ │
│  │ Cost Ceiling:         [$   5.00  ] input             │ │
│  │ Max Switches/Task:    [     3    ] stepper           │ │
│  │                                                       │ │
│  │ Current Agent: [Claude] → [Gemini] (Predicted)       │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                            │
│  [Show All 12 Parameters ▼]                               │
│                                                            │
│  ┌──────────────────────────────────────────────────────┐ │
│  │ 📊 Live System Visualization                         │ │
│  ├──────────────────────────────────────────────────────┤ │
│  │                                                       │ │
│  │  [Real-time graph showing parameter impacts]         │ │
│  │                                                       │ │
│  │  Quality ──────────▲                                 │ │
│  │                    │         ┌────┐                  │ │
│  │            85% ────┤         │ 92%│ ← Target         │ │
│  │                    │    ┌────┴────┘                  │ │
│  │                    │    │ Current: 87%               │ │
│  │                    └────┴────────────► Time          │ │
│  │                                                       │ │
│  └──────────────────────────────────────────────────────┘ │
│                                                            │
│  [Apply Changes] [Simulate Impact] [Reset All]            │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

### 3.2 Component Specifications

#### 3.2.1 Parameter Card Component

**Structure:**
```tsx
<ParameterCard
  id="latent-reasoning"
  title="Latent Reasoning Compression"
  icon={<BrainIcon />}
  enabled={true}
  onToggle={(enabled) => updateParameter({enabled})}
>
  <SliderControl
    label="Dimensionality"
    min={128}
    max={1024}
    step={128}
    value={512}
    marks={[128, 256, 512, 768, 1024]}
    onChange={(value) => updateParameter({dimensionality: value})}
    realTimePreview={true}
  />

  <MetricsDisplay
    metrics={{
      compressionRatio: 3.8,
      tokenSavings: 0.40,
      qualityImpact: -0.02
    }}
    realTime={true}
  />

  <AdvancedOptions collapsible={true}>
    <Toggle label="Auto-adjust based on task complexity" />
    <NumberInput label="Min compression ratio" value={2.0} />
  </AdvancedOptions>
</ParameterCard>
```

---

#### 3.2.2 Slider Control Variants

**1. Standard Range Slider**
```tsx
<RangeSlider
  min={0}
  max={100}
  value={50}
  step={5}
  marks={[0, 25, 50, 75, 100]}
  showValue={true}
  showTooltip={true}
  color="neon-cyan"
  onChange={handleChange}
/>
```

**2. Dual Range Slider (Min/Max)**
```tsx
<DualRangeSlider
  min={0}
  max={100}
  value={[20, 80]}  // [min, max]
  onChange={([min, max]) => {
    setMinThreshold(min);
    setMaxThreshold(max);
  }}
/>
```

**3. Logarithmic Slider (for cost, tokens)**
```tsx
<LogSlider
  min={1}
  max={10000}
  value={100}
  scale="log"
  formatLabel={(val) => `$${val.toFixed(2)}`}
/>
```

---

#### 3.2.3 Toggle/Switch Components

**1. Simple Toggle**
```tsx
<Toggle
  enabled={true}
  onChange={(enabled) => setFeatureEnabled(enabled)}
  label="Enable Latent Reasoning"
  sublabel="40% token reduction"
/>
```

**2. Multi-Toggle (OR-gates)**
```tsx
<MultiToggle
  options={[
    {id: 'memory', label: 'Memory Cache', enabled: true},
    {id: 'disk', label: 'Disk Cache', enabled: true},
    {id: 'remote', label: 'Remote Cache', enabled: false}
  ]}
  onChange={(options) => updateCacheConfig(options)}
/>
```

**3. Radio Group Toggle**
```tsx
<RadioToggle
  value="adaptive"
  options={[
    {value: 'cost', label: 'Cost-Optimized', icon: <DollarIcon />},
    {value: 'quality', label: 'Quality-First', icon: <StarIcon />},
    {value: 'speed', label: 'Speed-Optimized', icon: <ZapIcon />},
    {value: 'adaptive', label: 'Adaptive', icon: <BrainIcon />}
  ]}
  onChange={(value) => setStrategy(value)}
/>
```

---

#### 3.2.4 Dropdown/Select Components

**1. Strategy Selector**
```tsx
<StrategySelect
  value="adaptive"
  options={[
    {
      value: 'cost_optimized',
      label: 'Cost-Optimized',
      description: 'Prefer Gemini (free), use Claude when needed',
      icon: <DollarIcon />,
      estimatedSavings: 0.52
    },
    {
      value: 'quality_first',
      label: 'Quality-First',
      description: 'Use Claude for all tasks, highest quality',
      icon: <StarIcon />,
      estimatedCost: 1.5
    },
    {
      value: 'adaptive',
      label: 'Adaptive (ML-Powered)',
      description: 'ML predicts best agent for each task',
      icon: <BrainIcon />,
      recommended: true
    }
  ]}
  onChange={(strategy) => setAgentStrategy(strategy)}
  showImpactPreview={true}
/>
```

**2. Multi-Select Dropdown**
```tsx
<MultiSelect
  label="Active Embedding Dimensions"
  options={[
    {value: 256, label: '256D (Fast, Low Quality)'},
    {value: 512, label: '512D (Balanced)', default: true},
    {value: 1024, label: '1024D (Slow, High Quality)'}
  ]}
  value={[256, 512, 1024]}
  onChange={(selected) => setEmbeddingDims(selected)}
/>
```

---

#### 3.2.5 Number Input/Stepper

**1. Bounded Number Input**
```tsx
<NumberInput
  label="Max Parallel Tasks"
  value={10}
  min={1}
  max={50}
  step={1}
  showStepper={true}
  onChange={(value) => setMaxParallelTasks(value)}
  helperText="Higher values = more parallelization, higher memory usage"
/>
```

**2. Currency Input**
```tsx
<CurrencyInput
  label="Daily Budget"
  value={50.00}
  currency="USD"
  min={0}
  max={10000}
  onChange={(value) => setDailyBudget(value)}
/>
```

---

#### 3.2.6 Advanced Controls

**1. Matrix Control (Multi-Dimensional)**
```tsx
<MatrixControl
  title="Quality Weight Matrix"
  dimensions={[
    {id: 'test_coverage', label: 'Test Coverage', weight: 0.3},
    {id: 'security', label: 'Security Score', weight: 0.3},
    {id: 'type_safety', label: 'Type Safety', weight: 0.2},
    {id: 'complexity', label: 'Low Complexity', weight: 0.2}
  ]}
  onChange={(weights) => updateQualityWeights(weights)}
  visualizeImpact={true}
/>
```

**2. Timeline Scrubber (for checkpoint visualization)**
```tsx
<TimelineScrubber
  checkpoints={[
    {progress: 0.33, quality: 0.72, label: 'Checkpoint 1'},
    {progress: 0.66, quality: 0.84, label: 'Checkpoint 2'},
    {progress: 1.00, quality: 0.91, label: 'Final'}
  ]}
  currentProgress={0.45}
  onSeek={(progress) => visualizeCheckpoint(progress)}
/>
```

---

### 3.3 Real-Time Impact Visualization

#### 3.3.1 Live Metrics Display

```tsx
<ImpactMetrics>
  <MetricCard
    title="Cost Impact"
    current={2.50}
    predicted={1.80}
    unit="USD"
    trend="down"
    changePercent={-28}
    icon={<DollarIcon />}
  />

  <MetricCard
    title="Speed Impact"
    current={450}
    predicted={315}
    unit="seconds"
    trend="down"
    changePercent={-30}
    icon={<ZapIcon />}
  />

  <MetricCard
    title="Quality Impact"
    current={0.87}
    predicted={0.92}
    unit="%"
    trend="up"
    changePercent={+6}
    icon={<StarIcon />}
  />

  <MetricCard
    title="Token Reduction"
    current={50000}
    predicted={30000}
    unit="tokens"
    trend="down"
    changePercent={-40}
    icon={<BrainIcon />}
  />
</ImpactMetrics>
```

---

#### 3.3.2 Real-Time Graph Visualization

**Libraries:**
- **Recharts** (already in project) for line/area charts
- **D3.js** for advanced visualizations
- **React Flow** for agent switching flow diagrams

**Example: Quality Trend Graph**
```tsx
<ResponsiveContainer width="100%" height={300}>
  <LineChart data={qualityHistory}>
    <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
    <XAxis dataKey="timestamp" stroke="#64748b" />
    <YAxis stroke="#64748b" />
    <Tooltip
      contentStyle={{
        backgroundColor: '#0f172a',
        border: '1px solid #06b6d4',
        borderRadius: '8px'
      }}
    />
    <Legend />

    <Line
      type="monotone"
      dataKey="quality"
      stroke="#06b6d4"
      strokeWidth={2}
      dot={{r: 4}}
      name="Quality Score"
    />

    <ReferenceLine
      y={0.80}
      stroke="#f59e0b"
      strokeDasharray="5 5"
      label="Target: 80%"
    />

    {/* Checkpoint markers */}
    <ReferenceLine
      x={checkpoints[0].timestamp}
      stroke="#22c55e"
      label="Checkpoint 1: 33%"
    />
  </LineChart>
</ResponsiveContainer>
```

---

#### 3.3.3 Agent Flow Diagram

**Visual representation of agent switching:**

```
  Gemini (Free)  →  Quality Drop  →  Claude (Pro)  →  Complete
     0-2min            @ 2min            2-5min          @ 5min
  Quality: 72%      Trigger: <75%    Quality: 92%    Final: 92%
  Cost: $0.00       Switch Cost: $0   Cost: $2.50     Total: $2.50
```

**React Flow Implementation:**
```tsx
<ReactFlow
  nodes={[
    {
      id: '1',
      type: 'agent',
      data: {
        agent: 'gemini',
        quality: 0.72,
        cost: 0.00,
        duration: '2min'
      },
      position: {x: 0, y: 0}
    },
    {
      id: '2',
      type: 'decision',
      data: {
        trigger: 'quality < 0.75',
        action: 'switch_to_claude'
      },
      position: {x: 200, y: 0}
    },
    {
      id: '3',
      type: 'agent',
      data: {
        agent: 'claude',
        quality: 0.92,
        cost: 2.50,
        duration: '3min'
      },
      position: {x: 400, y: 0}
    }
  ]}
  edges={[
    {id: 'e1-2', source: '1', target: '2', animated: true},
    {id: 'e2-3', source: '2', target: '3', animated: true}
  ]}
/>
```

---

## 4. PRESET MANAGEMENT

### 4.1 Preset System Design

**Built-in Presets (4):**

```typescript
const PRESETS = {
  speed_optimized: {
    name: 'Speed-Optimized',
    description: 'Maximum speed, minimal quality checks',
    icon: <ZapIcon />,
    color: 'neon-yellow',
    config: {
      latent_reasoning: {enabled: true, dimensionality: 256},
      ml_iteration_prediction: {mode: 'fixed', max_iterations: 2},
      agent_switching: {strategy: 'speed_optimized'},
      parallel_evaluation: {enabled: true, workers: 8},
      caching: {aggressive: true}
    }
  },

  cost_optimized: {
    name: 'Cost-Optimized',
    description: 'Minimize costs, use free tiers',
    icon: <DollarIcon />,
    color: 'neon-green',
    config: {
      latent_reasoning: {enabled: true, dimensionality: 512},
      agent_switching: {strategy: 'cost_optimized'},  // Gemini-first
      caching: {aggressive: true},
      parallel_evaluation: {enabled: true, workers: 4}
    }
  },

  quality_first: {
    name: 'Quality-First',
    description: 'Maximum quality, cost secondary',
    icon: <StarIcon />,
    color: 'neon-purple',
    config: {
      latent_reasoning: {enabled: true, dimensionality: 1024},
      ml_iteration_prediction: {mode: 'auto', max_iterations: 10},
      agent_switching: {strategy: 'quality_first'},  // Claude-first
      deep_supervision: {checkpoints: [0.25, 0.50, 0.75, 1.00]},
      bayesian_optimization: {iterations: 100}
    }
  },

  balanced: {
    name: 'Balanced (Default)',
    description: 'Equal weight to speed, cost, quality',
    icon: <ScaleIcon />,
    color: 'neon-cyan',
    config: {
      latent_reasoning: {enabled: true, dimensionality: 512},
      ml_iteration_prediction: {mode: 'auto', max_iterations: 7},
      agent_switching: {strategy: 'adaptive'},
      deep_supervision: {checkpoints: [0.33, 0.66, 1.00]},
      parallel_evaluation: {enabled: true, workers: 4}
    }
  }
};
```

---

### 4.2 Custom Preset Creation

**UI Flow:**

```
User adjusts parameters → [Save as Preset] button → Modal opens

Modal:
┌───────────────────────────────────────┐
│ Save Custom Preset                   │
├───────────────────────────────────────┤
│ Name: [My Custom Config_____]        │
│ Description:                          │
│ [Optimized for microservices___]     │
│                                       │
│ Icon: [🚀] [Select Icon ▼]           │
│ Color: [●] Neon Cyan ▼               │
│                                       │
│ Visibility:                           │
│ ○ Private (Only me)                  │
│ ● Shared (Team-wide)                 │
│ ○ Public (Community)                 │
│                                       │
│ [Cancel]  [Save Preset]              │
└───────────────────────────────────────┘
```

**Saved Preset Display:**
```tsx
<PresetCard
  name="My Custom Config"
  description="Optimized for microservices"
  icon={<RocketIcon />}
  color="neon-cyan"
  author="Thomas"
  usageCount={12}
  avgQuality={0.89}
  avgCost={1.25}
  onLoad={() => loadPreset(preset)}
  onEdit={() => editPreset(preset)}
  onDelete={() => deletePreset(preset)}
/>
```

---

## 5. BACKEND API SPECIFICATION

### 5.1 New HRM Endpoints

#### POST /api/hrm/config
Update HRM configuration in real-time

**Request:**
```json
{
  "project_id": "uuid",
  "task_id": "uuid",  // optional - apply to specific task
  "config": {
    "latent_reasoning": {
      "enabled": true,
      "dimensionality": 512,
      "compression_ratio_target": 3.8
    },
    "ml_iteration_prediction": {
      "mode": "auto",
      "max_iterations": 7,
      "confidence_threshold": 0.80
    },
    "agent_switching": {
      "strategy": "adaptive",
      "quality_drop_threshold": 0.20,
      "cost_ceiling": 5.00,
      "max_switches_per_task": 3
    },
    "deep_supervision": {
      "enabled": true,
      "checkpoints": [0.33, 0.66, 1.00],
      "quality_gate_threshold": 0.75
    },
    "parallel_evaluation": {
      "enabled": true,
      "worker_count": 4,
      "timeout_seconds": 60
    },
    "caching": {
      "memory": true,
      "disk": true,
      "remote": false,
      "aggressive_mode": true,
      "max_size_mb": 500
    },
    "bayesian_optimization": {
      "enabled": false,
      "iterations": 30
    },
    "rl_refinement": {
      "enabled": true,
      "epsilon": 0.1,
      "learning_rate": 0.001
    },
    "prometheus_metrics": {
      "enabled": true,
      "export_interval": 15
    },
    "multi_repo": {
      "enabled": true
    }
  },
  "apply_immediately": true,
  "persist": true
}
```

**Response:**
```json
{
  "status": "applied",
  "config_id": "uuid",
  "applied_at": "2025-11-09T10:00:00Z",
  "impact_estimate": {
    "cost_change": -0.28,
    "speed_change": 0.30,
    "quality_change": 0.06,
    "token_reduction": 0.40
  },
  "active_tasks_affected": 5,
  "future_tasks_affected": true
}
```

---

#### GET /api/hrm/config
Get current HRM configuration

**Query Params:**
- `project_id` (optional)
- `task_id` (optional)

**Response:**
```json
{
  "config_id": "uuid",
  "config": { /* Full HRM config */ },
  "preset_name": "balanced",
  "last_updated": "2025-11-09T10:00:00Z",
  "updated_by": "user@example.com"
}
```

---

#### GET /api/hrm/config/presets
Get all available presets

**Response:**
```json
[
  {
    "id": "speed_optimized",
    "name": "Speed-Optimized",
    "description": "Maximum speed, minimal quality checks",
    "icon": "⚡",
    "color": "neon-yellow",
    "builtin": true,
    "config": { /* Config */ },
    "usage_stats": {
      "usage_count": 150,
      "avg_quality": 0.82,
      "avg_cost": 0.80,
      "avg_duration": 180
    }
  }
  // ... other presets
]
```

---

#### POST /api/hrm/config/presets
Create custom preset

**Request:**
```json
{
  "name": "My Custom Config",
  "description": "Optimized for microservices",
  "icon": "🚀",
  "color": "neon-cyan",
  "visibility": "shared",
  "config": { /* HRM config */ }
}
```

**Response:**
```json
{
  "id": "uuid",
  "name": "My Custom Config",
  "created_at": "2025-11-09T10:00:00Z",
  "author": "user@example.com"
}
```

---

#### POST /api/hrm/simulate
Simulate impact of configuration change

**Request:**
```json
{
  "current_config": { /* Current HRM config */ },
  "proposed_config": { /* New HRM config */ },
  "task_context": {
    "complexity": 12.5,
    "estimated_duration": 450,
    "current_quality": 0.87
  }
}
```

**Response:**
```json
{
  "impact_analysis": {
    "cost": {
      "current": 2.50,
      "predicted": 1.80,
      "change_percent": -28,
      "confidence": 0.85
    },
    "speed": {
      "current_seconds": 450,
      "predicted_seconds": 315,
      "change_percent": -30,
      "confidence": 0.78
    },
    "quality": {
      "current": 0.87,
      "predicted": 0.92,
      "change_percent": 6,
      "confidence": 0.82
    },
    "tokens": {
      "current": 50000,
      "predicted": 30000,
      "reduction_percent": 40,
      "compression_ratio": 3.8
    }
  },
  "recommendations": [
    "Consider increasing dimensionality to 768D for +3% quality",
    "Agent switching from Gemini to Claude recommended at 2min mark"
  ],
  "warnings": [
    "Cost ceiling may be exceeded with current settings"
  ]
}
```

---

### 5.2 WebSocket Events for Real-Time Updates

#### Event: hrm_config_update
Emitted when HRM config changes

**Payload:**
```json
{
  "event": "hrm_config_update",
  "project_id": "uuid",
  "task_id": "uuid",
  "config": { /* Updated config */ },
  "updated_by": "user@example.com",
  "timestamp": "2025-11-09T10:00:00Z"
}
```

---

#### Event: hrm_impact_update
Emitted when impact metrics change

**Payload:**
```json
{
  "event": "hrm_impact_update",
  "task_id": "uuid",
  "metrics": {
    "cost": 1.80,
    "speed_seconds": 315,
    "quality": 0.92,
    "token_usage": 30000
  },
  "timestamp": "2025-11-09T10:00:00Z"
}
```

---

#### Event: hrm_checkpoint_reached
Emitted when deep supervision checkpoint reached

**Payload:**
```json
{
  "event": "hrm_checkpoint_reached",
  "task_id": "uuid",
  "checkpoint": {
    "progress": 0.66,
    "quality": 0.84,
    "tests_passing": true,
    "security_score": 0.91,
    "decision": "continue"  // continue | stop | refine
  },
  "timestamp": "2025-11-09T10:00:00Z"
}
```

---

## 6. IMPLEMENTATION ROADMAP

### Phase 1: Core Infrastructure (Week 1)
- [ ] Backend: HRM config endpoints (`/api/hrm/config`, `/api/hrm/simulate`)
- [ ] Backend: Preset management endpoints
- [ ] Backend: WebSocket events for HRM updates
- [ ] Database: HRM config storage model

### Phase 2: Frontend Components (Week 2)
- [ ] ParameterCard base component
- [ ] SliderControl with real-time preview
- [ ] Toggle/MultiToggle components
- [ ] StrategySelect dropdown
- [ ] ImpactMetrics display

### Phase 3: Advanced Features (Week 3)
- [ ] Real-time impact simulation
- [ ] Live graph visualizations (Recharts integration)
- [ ] Agent flow diagram (React Flow)
- [ ] Preset management UI
- [ ] Custom preset creation

### Phase 4: Integration & Testing (Week 4)
- [ ] Connect frontend to WebSocket events
- [ ] Real-time config updates to running tasks
- [ ] A/B testing framework
- [ ] Performance optimization
- [ ] E2E tests with Playwright

---

## 7. USER WORKFLOWS

### 7.1 Workflow: Optimize for Cost

```
User Goal: Reduce cost by 50%

Steps:
1. Open HRM Control Panel
2. Click "Cost Mode" quick action
3. System auto-adjusts:
   - Agent Switching → Cost-Optimized (Gemini-first)
   - Latent Reasoning → 256D (faster, cheaper)
   - Max Iterations → 3 (reduce processing)
   - Caching → Aggressive mode
4. Real-time Impact shows:
   - Cost: $2.50 → $1.25 (-50%) ✅
   - Quality: 87% → 82% (-6%) ⚠️
   - Speed: +20%
5. User clicks "Simulate Impact" to verify
6. Simulation confirms savings
7. User clicks "Apply Changes"
8. WebSocket notifies active tasks
9. Changes applied immediately
```

---

### 7.2 Workflow: Custom Preset for Microservices

```
User Goal: Create reusable config for microservices projects

Steps:
1. Start with "Balanced" preset
2. Adjust parameters:
   - Agent Switching → Adaptive
   - Deep Supervision → 4 checkpoints (25%, 50%, 75%, 100%)
   - Parallel Evaluation → 8 workers
   - Multi-Repo → Enabled
3. Test on sample project
4. Monitor results over 10 tasks
5. Tweak based on results
6. Click "Save as Preset"
7. Name: "Microservices Optimized"
8. Visibility: Shared (team-wide)
9. Save
10. Preset now available in dropdown for future projects
```

---

### 7.3 Workflow: Real-Time Task Adjustment

```
Scenario: Task quality dropping below threshold

Timeline:
- 0min: Task starts with Gemini (cost-optimized)
- 2min: Quality at 65% (below 75% threshold)
- 2min: WebSocket event: quality_drop
- 2min: UI shows alert: "Quality below threshold"
- 2min: User opens HRM panel for this task
- 2min: Sees recommendation: "Switch to Claude for quality boost"
- 2min: User adjusts:
  - Agent Switching → Force switch to Claude
  - Latent Reasoning → 1024D (max quality)
- 2min: Clicks "Apply to Running Task"
- 2.5min: Agent switches to Claude mid-task
- 5min: Quality at 92% ✅
- 5min: Task completes successfully
```

---

## 8. ACCESSIBILITY & UX CONSIDERATIONS

### 8.1 Accessibility Features

- **Keyboard Navigation:** Full keyboard control for all sliders/toggles
- **Screen Reader Support:** ARIA labels on all controls
- **High Contrast Mode:** Color scheme adjustable for visibility
- **Focus Indicators:** Clear focus states for all interactive elements
- **Tooltips:** Contextual help on hover/focus

---

### 8.2 Responsive Design

**Breakpoints:**
- Desktop (>1280px): Full panel with all controls visible
- Tablet (768px-1280px): Collapsible sections, vertical layout
- Mobile (< 768px): Accordion-style panels, simplified controls

---

### 8.3 Performance Optimization

- **Debounced Slider Updates:** Prevent excessive API calls (300ms debounce)
- **Optimistic UI Updates:** Immediate visual feedback, background API call
- **Virtual Scrolling:** For long parameter lists
- **Lazy Loading:** Load advanced options on demand

---

## 9. SECURITY CONSIDERATIONS

### 9.1 Permission Model

**Role-Based Access:**
- **Admin:** Full HRM control, create/edit/delete presets
- **Developer:** View + adjust own projects, use shared presets
- **Viewer:** Read-only access to configs and metrics

---

### 9.2 Config Validation

**Backend Validation:**
- Range checks (dimensionality, iterations, etc.)
- Cost ceiling enforcement
- Prevent dangerous combinations (e.g., max iterations + max workers = resource exhaustion)
- Audit log of all config changes

---

## 10. FUTURE ENHANCEMENTS

### 10.1 Advanced Features (Post-MVP)

1. **ML-Powered Config Recommendations**
   - Analyze historical performance
   - Suggest optimal configs per project type
   - Auto-tune based on feedback

2. **A/B Testing Framework**
   - Run parallel tasks with different configs
   - Compare results statistically
   - Auto-select winning configuration

3. **Config Versioning**
   - Track config changes over time
   - Rollback to previous configs
   - Compare config versions

4. **Collaborative Config Editing**
   - Real-time multi-user editing
   - Conflict resolution
   - Change suggestions/approvals

5. **Mobile App**
   - Native iOS/Android app
   - Push notifications for config alerts
   - Quick adjustment from mobile

---

## 11. METRICS & ANALYTICS

### 11.1 Config Usage Analytics

**Track:**
- Most popular presets
- Most adjusted parameters
- Average config lifetime
- Config performance correlation

**Dashboard:**
```
Top Presets (Last 30 Days)
1. Cost-Optimized: 450 uses, 88% avg quality, $0.80 avg cost
2. Balanced: 320 uses, 87% avg quality, $1.75 avg cost
3. Quality-First: 180 uses, 93% avg quality, $3.20 avg cost

Most Adjusted Parameters
1. Agent Switching Strategy: 85% of users adjust
2. Latent Reasoning Dimensionality: 72% of users adjust
3. Max Iterations: 65% of users adjust
```

---

## 12. IMPLEMENTATION CHECKLIST

### Backend
- [ ] HRM config database model
- [ ] HRM config CRUD endpoints
- [ ] Preset management system
- [ ] Real-time config application to running tasks
- [ ] Impact simulation engine
- [ ] WebSocket event emitters
- [ ] Config validation middleware
- [ ] Audit logging

### Frontend
- [ ] HRM Control Panel page/component
- [ ] ParameterCard component
- [ ] Slider controls (standard, dual, log)
- [ ] Toggle/MultiToggle components
- [ ] Strategy select dropdown
- [ ] Impact metrics display
- [ ] Real-time graphs (Recharts)
- [ ] Agent flow diagram (React Flow)
- [ ] Preset management UI
- [ ] Custom preset creation modal
- [ ] WebSocket event handlers
- [ ] Real-time UI updates

### Testing
- [ ] Unit tests for all components
- [ ] API integration tests
- [ ] E2E tests for config workflows
- [ ] Performance tests for real-time updates
- [ ] Accessibility tests

### Documentation
- [ ] User guide for HRM controls
- [ ] API documentation
- [ ] Preset creation guide
- [ ] Best practices guide

---

**Document Status:** DRAFT v1.0
**Next Review:** After Phase 1 implementation
**Owner:** Phantom Neural Cortex Team
**Last Updated:** 2025-11-09
