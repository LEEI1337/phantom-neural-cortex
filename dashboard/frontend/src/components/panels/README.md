# Control Panel System - Complete Documentation

## Overview

A comprehensive Control Panel system with 6 specialized configuration panels for managing the entire AI orchestration platform. Built with React, TypeScript, and Tailwind CSS with a professional cyberpunk aesthetic.

## Location

```
dashboard/frontend/src/components/panels/
```

## Files Created

1. **ControlPanel.tsx** (2.7 KB) - Main panel container with mode switching
2. **HRMConfigPanel.tsx** (30.7 KB) - Full HRM configuration with all 12 parameters
3. **SwarmConfigPanel.tsx** (16.6 KB) - Swarm orchestration panel
4. **AgentConfigPanel.tsx** (17.5 KB) - Individual agent configuration
5. **SystemHealthPanel.tsx** (11.2 KB) - System health and cache management
6. **GlobalSettingsPanel.tsx** (16.2 KB) - Global system settings
7. **index.ts** - Barrel exports for all panels

**Total Size:** ~95 KB of TypeScript code

---

## 1. ControlPanel.tsx

### Purpose
Main container component that switches between different configuration modes.

### Features
- **Mode Switching:** Toggle between HRM, Swarm, Agent, Health, and Settings modes
- **Unified Interface:** Single component that loads appropriate sub-panel
- **Clean Navigation:** Icon-based tab navigation with active state highlighting
- **Close Handler:** Optional close callback for modal usage

### Props
```typescript
interface ControlPanelProps {
  initialMode?: PanelMode  // 'hrm' | 'swarm' | 'agent' | 'health' | 'global'
  projectId?: string       // Optional project context
  onClose?: () => void     // Close callback
}
```

### Usage
```tsx
import { ControlPanel } from '@/components/panels'

<ControlPanel
  initialMode="hrm"
  projectId="projekt-a"
  onClose={() => setShowPanel(false)}
/>
```

---

## 2. HRMConfigPanel.tsx

### Purpose
Complete HRM (Hierarchical Reasoning Module) configuration with all 12 ML/RL optimizations.

### Features

#### Collapsible Sections (4)
1. **Core Optimizations** ⚙️ (Default: Open)
   - Latent Reasoning Compression
   - ML Iteration Prediction
   - Three-Layer Caching

2. **Agent Control** 🤖
   - Smart Agent Switching
   - Strategy Selection (6 modes)
   - Threshold Configuration

3. **Quality & Testing** 🎯
   - Deep Supervision Checkpoints
   - Parallel Quality Evaluation

4. **Advanced Options** 🔬
   - Bayesian Optimization
   - RL Refinement Chain
   - Prometheus Metrics
   - Multi-Repository Coordination

#### Live Impact Preview
Real-time calculation showing:
- **Cost Impact:** -28% ⬇️
- **Speed Impact:** +30% ⬆️
- **Quality Impact:** +6% ⬆️
- **Token Reduction:** -40% ⬇️

#### Quick Presets
- ⚡ **Speed Mode** - Optimized for fast completion
- 💰 **Cost Mode** - Minimized costs, free-tier priority
- 🎯 **Quality Mode** - Maximum quality, cost secondary
- ⚖️ **Balanced Mode** - Equal weight to all factors

#### Configuration Parameters

**Latent Reasoning:**
- Toggle: Enable/Disable
- Dimensionality: 128D - 1024D (slider)
- Shows token savings percentage

**ML Iteration Prediction:**
- Mode: Auto / Manual / Fixed (radio buttons)
- Max Iterations: 2-20 (slider)

**Three-Layer Caching:**
- Memory Cache (toggle)
- Disk Cache (toggle)
- Remote Cache (toggle)
- Aggressive Mode (toggle)
- Max Size: 100MB - 5000MB (slider)

**Smart Agent Switching:**
- Strategy dropdown (6 options)
- Quality Drop Threshold: 0-100% (slider)
- Cost Ceiling: $1-$20 (slider)
- Max Switches: 0-10 (slider)

**Deep Supervision:**
- Enable toggle
- Quality Gate: 50-100% (slider)

**Parallel Evaluation:**
- Enable toggle
- Workers: 1-16 (slider)
- Timeout: 10-300s (slider)

**Bayesian Optimization:**
- Enable toggle
- Iterations: 10-100 (slider)

**RL Refinement:**
- Enable toggle
- Epsilon: 0.0-1.0 (slider)
- Learning Rate: 0.0001-0.1 (slider)

**Other:**
- Prometheus Metrics (toggle + interval)
- Multi-Repo Coordination (toggle)

#### Action Buttons
- **Apply Changes** - Apply configuration
- **Simulate Impact** - Run impact simulation
- **Reset** - Restore defaults

---

## 3. SwarmConfigPanel.tsx

### Purpose
Configure swarm orchestration for multi-agent parallel task execution.

### Features

#### Collapsible Sections (4)
1. **Parallelization** ⚡ (Default: Open)
   - Max Parallel Tasks: 1-50
   - Max Parallel Agents: 1-20
   - Auto-Scale with thresholds

2. **Intelligence Mode** 🧠 (Default: Open)
   - Preset modes (Speed/Cost/Quality/Balanced)
   - Custom weight configuration
   - Weight sliders for Speed/Cost/Quality

3. **Feedback Loops** 🔄
   - Adaptive Iterations toggle
   - Max Iterations per Task: 2-20
   - Learning Rate: 0.001-0.1
   - Exploration Factor: 0-100%

4. **Cost Control** 💰
   - Daily Budget: $0-$1000
   - Per-Task Limit: $0-$100
   - Prefer Cheaper Models toggle
   - Real-time usage display with progress bar

#### Intelligence Modes
- **Speed-Optimized** ⚡ - 70% speed, 15% cost, 15% quality
- **Cost-Optimized** 💰 - 15% speed, 70% cost, 15% quality
- **Quality-Optimized** 🎯 - 15% speed, 15% cost, 70% quality
- **Balanced** ⚖️ - 33% speed, 33% cost, 34% quality
- **Custom** - User-defined weights

---

## 4. AgentConfigPanel.tsx

### Purpose
Configure individual AI agents (Claude, Gemini, Copilot, Cursor, Windsurf).

### Features

#### Agent Selector
- Grid of agent buttons with icons
- Shows 5 agents: ⚡ Claude, 💎 Gemini, 🚀 Copilot, 📐 Cursor, 🌊 Windsurf

#### Agent Details
- Status indicator (🟢 Active / ⚪ Idle / 🔴 Disabled)
- Quality tier badge
- Provider and model information

#### Performance Metrics (5)
- **Tasks Completed** - Total tasks processed
- **Success Rate** - Percentage of successful completions
- **Avg Quality** - Average quality score
- **Avg Cost** - Average cost per task
- **Avg Duration** - Average task duration in seconds

#### Specializations
Progress bars showing strength in:
- Complex Reasoning
- Code Quality/Generation
- Documentation
- Speed
- Cost Efficiency
- Context Awareness (Windsurf)
- IDE Integration (Cursor)
- GitHub Integration (Copilot)

Color-coded:
- Green (≥90%): Expert level
- Cyan (≥70%): Strong capability
- Yellow (<70%): Moderate capability

#### API Configuration
- Provider name
- Model name
- API Key (masked, with validation status)
- Rate Limit display with usage bar

#### Routing Rules
Toggle switches for:
- Quality threshold > 90%
- Task complexity > 8.0
- Security critical = true
- Cost ceiling exceeded

**Fallback Agent:** Dropdown to select backup agent

#### Action Buttons
- Edit Routing
- Test Connection
- View Logs

#### Mock Data
Includes realistic data for all 5 agents:

**Claude (Active):**
- 342 tasks, 96.5% success, 94% quality, $3.20 cost
- Specializations: Complex Reasoning (95%), Code Quality (92%)

**Gemini (Active):**
- 498 tasks, 89.2% success, 82% quality, $0.00 cost (Free)
- Specializations: Cost Efficiency (100%), Speed (88%)

**Copilot, Cursor, Windsurf (Idle):**
- Not yet configured, 0 tasks completed

---

## 5. SystemHealthPanel.tsx

### Purpose
Monitor system health and manage caches across infrastructure components.

### Features

#### Overall Status
- Visual indicator (🟢/🟡/🔴)
- Status text: "All Systems Operational"

#### Components (4)
1. **Database (PostgreSQL)** 🟢
   - Status: Connected
   - Latency: 12ms
   - Connection Pool: 8/20

2. **Cache (Redis)** 🟢
   - Status: Connected
   - Hit Rate: 87%
   - Memory: 45%

3. **WebSocket Server** 🟢
   - Status: Running
   - Connections: 12
   - Events: 340

4. **Backend API** 🟢
   - Status: Healthy
   - RPS: 45
   - Avg Latency: 78ms
   - Error Rate: 0.2%

#### Cache Management (3)
**Guideline Cache:**
- Size: 145MB
- Entries: 2,340
- Hit Rate: 87%
- Individual clear button

**GitHub API Cache:**
- Size: 89MB
- Entries: 1,203
- Hit Rate: 92%

**Quality Pattern Cache:**
- Size: 56MB
- Entries: 890
- Hit Rate: 88%

**Clear All Caches** button at bottom

#### Real-time Metrics (5)
Progress bars with values:
1. **Requests per Second:** 45.3 (Green)
2. **Avg Response Time:** 78ms (Cyan)
3. **Error Rate:** 0.2% (Green - low is good)
4. **CPU Usage:** 34% (Cyan)
5. **Memory Usage:** 58% (Yellow)

#### Action Buttons
- View Logs
- Download Report
- Configure Alerts

---

## 6. GlobalSettingsPanel.tsx

### Purpose
System-wide preferences and integration configuration.

### Features

#### Collapsible Sections (5)

1. **Notifications** 🔔 (Default: Open)
   - Email Notifications
   - Push Notifications
   - Desktop Notifications
   - Slack Notifications

2. **Security** 🔒 (Default: Open)
   - Two-Factor Authentication
   - Session Timeout: 5-120 minutes (slider)
   - API Key Rotation (90 days)
   - Audit Logging

3. **Performance** ⚡
   - Enable Caching
   - Compression Level: 0-9 (slider)
   - Max Concurrent Tasks: 1-50 (slider)
   - Request Throttling

4. **Integrations** 🔗
   - 🐙 GitHub (Repository integration)
   - 🦊 GitLab (Repository integration)
   - 📊 Prometheus (Metrics collection)
   - 📈 Grafana (Dashboard visualization)
   - 💬 Slack (Team communication)

5. **Advanced** 🔬
   - Debug Mode
   - Experimental Features (⚠️ May be unstable)
   - Telemetry (Anonymous usage statistics)
   - Auto-Update

#### Change Detection
- Tracks when settings are modified
- Enables/disables Apply button based on changes
- Shows "No Changes" when pristine

#### Action Buttons
- **Apply Changes** - Only enabled when changes detected
- **Reset** - Restore to defaults

---

## Design System

### Color Scheme (Cyberpunk)

**Backgrounds:**
- Primary: `from-slate-900 to-slate-800`
- Secondary: `bg-slate-950/50`
- Hover: `bg-slate-800/50`

**Borders:**
- Primary: `border-cyan-500/30`
- Hover: `border-cyan-500/50`
- Dividers: `border-cyan-500/20`

**Text:**
- Headings: `text-cyan-400`
- Body: `text-slate-200` / `text-slate-300`
- Secondary: `text-slate-400`
- Values: `text-cyan-400`

**Status Colors:**
- Success: `text-green-400` / `bg-green-500`
- Warning: `text-yellow-400` / `bg-yellow-500`
- Error: `text-red-400` / `bg-red-500`
- Info: `text-cyan-400` / `bg-cyan-500`

**Gradients:**
- Success: `from-green-500 to-emerald-500`
- Primary: `from-cyan-500 to-blue-500`
- Warning: `from-yellow-500 to-orange-500`

### Components

#### CollapsibleSection
- Consistent expand/collapse pattern
- Icon + Title
- Toggle arrow (▶/▼)
- Smooth transitions
- Hover effects

#### Sliders
- Custom styled range inputs
- Visual progress indicators
- Min/max/step configuration
- Real-time value display

#### Toggles/Switches
- Consistent Switch component
- Active state: Blue background
- Inactive: Gray background
- Smooth animations

#### Buttons
- Primary: Cyan background
- Secondary: Outlined cyan
- Disabled: Gray with reduced opacity
- Shadow effects on primary actions

#### Info Buttons [ⓘ]
- Tooltip on hover
- Explains parameter purpose
- Small, unobtrusive design

### Typography

**Headings:**
- Panel Title: `text-cyan-400 flex items-center gap-2`
- Section Title: `text-lg font-semibold text-cyan-400`
- Card Title: Component from ui/card

**Labels:**
- Primary: `text-sm text-slate-300`
- Secondary: `text-xs text-slate-400`
- Values: `text-cyan-400 font-bold`

### Spacing
- Section Gap: `space-y-6`
- Card Gap: `space-y-4`
- Input Gap: `space-y-3`
- Padding: `p-4` (standard card padding)

---

## Usage Examples

### Example 1: Standalone Panel

```tsx
import { HRMConfigPanel } from '@/components/panels'

function HRMPage() {
  return (
    <div className="container mx-auto p-8">
      <HRMConfigPanel projectId="projekt-a" />
    </div>
  )
}
```

### Example 2: Modal with Control Panel

```tsx
import { ControlPanel } from '@/components/panels'

function App() {
  const [showPanel, setShowPanel] = useState(false)
  const [mode, setMode] = useState<PanelMode>('hrm')

  return (
    <>
      <button onClick={() => setShowPanel(true)}>
        Open Settings
      </button>

      {showPanel && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center">
          <div className="bg-slate-900 rounded-lg w-[90vw] h-[90vh] overflow-auto">
            <ControlPanel
              initialMode={mode}
              onClose={() => setShowPanel(false)}
            />
          </div>
        </div>
      )}
    </>
  )
}
```

### Example 3: Integrated into Settings Page

```tsx
import { ControlPanel } from '@/components/panels'

function SettingsPage() {
  return (
    <div className="min-h-screen bg-background">
      <header className="border-b border-cyan-500/30 p-6">
        <h1 className="text-3xl font-bold text-cyan-400">
          System Configuration
        </h1>
      </header>

      <main className="p-8">
        <ControlPanel initialMode="global" />
      </main>
    </div>
  )
}
```

---

## TypeScript Types

### Shared Types

```typescript
// Panel Modes
type PanelMode = 'hrm' | 'swarm' | 'agent' | 'health' | 'global'

// HRM Config
interface HRMConfig {
  latentReasoning: {
    enabled: boolean
    dimensionality: number
  }
  mlIterationPrediction: {
    mode: 'auto' | 'manual' | 'fixed'
    maxIterations: number
  }
  caching: {
    memory: boolean
    disk: boolean
    remote: boolean
    aggressive: boolean
    maxSizeMB: number
  }
  agentSwitching: {
    strategy: 'cost_optimized' | 'quality_first' | 'speed_optimized' |
              'adaptive' | 'round_robin' | 'manual'
    qualityDropThreshold: number
    costCeiling: number
    maxSwitches: number
  }
  deepSupervision: {
    enabled: boolean
    qualityGate: number
  }
  parallelEvaluation: {
    enabled: boolean
    workers: number
    timeout: number
  }
  bayesianOptimization: {
    enabled: boolean
    iterations: number
  }
  rlRefinement: {
    enabled: boolean
    epsilon: number
    learningRate: number
  }
  prometheusMetrics: {
    enabled: boolean
    interval: number
  }
  multiRepo: boolean
}

// Impact Metrics
interface ImpactMetrics {
  cost: { current: number; predicted: number; change: number }
  speed: { current: number; predicted: number; change: number }
  quality: { current: number; predicted: number; change: number }
  tokens: { current: number; predicted: number; change: number }
}
```

---

## API Integration Points

### HRMConfigPanel
- `POST /api/hrm/config` - Apply configuration
- `POST /api/hrm/simulate` - Simulate impact
- `GET /api/hrm/config/presets` - Load presets

### SwarmConfigPanel
- `POST /api/swarm/config` - Apply swarm config
- `GET /api/swarm/usage` - Get current usage stats

### AgentConfigPanel
- `GET /api/agents` - List all agents
- `PUT /api/agents/:id/routing` - Update routing rules
- `POST /api/agents/:id/test` - Test connection
- `GET /api/agents/:id/logs` - View logs

### SystemHealthPanel
- `GET /api/health` - System health status
- `DELETE /api/cache/:name` - Clear specific cache
- `DELETE /api/cache` - Clear all caches
- `GET /api/metrics` - Real-time metrics

### GlobalSettingsPanel
- `GET /api/settings` - Get all settings
- `PUT /api/settings` - Update settings

---

## Accessibility Features

- **Keyboard Navigation:** All controls are keyboard accessible
- **Focus Indicators:** Clear focus states on all interactive elements
- **Screen Reader Support:** Proper ARIA labels and roles
- **Color Contrast:** WCAG AA compliant contrast ratios
- **Tooltips:** Contextual help on all parameters

---

## Performance Optimizations

- **Lazy Loading:** Panels load on demand
- **Debounced Updates:** Slider changes debounced (300ms)
- **Optimistic UI:** Immediate visual feedback
- **Efficient Re-renders:** React.memo for heavy components
- **Virtual Scrolling:** For long lists (if needed)

---

## Browser Support

- Chrome/Edge: ✅ Full support
- Firefox: ✅ Full support
- Safari: ✅ Full support
- Mobile Browsers: ✅ Responsive design

---

## Future Enhancements

### Planned Features
1. **Preset Management UI**
   - Save custom presets
   - Share presets with team
   - Import/export presets

2. **A/B Testing**
   - Compare two configurations
   - Statistical analysis
   - Auto-select winner

3. **Configuration Versioning**
   - Track changes over time
   - Rollback to previous configs
   - Diff viewer

4. **Real-time Collaboration**
   - Multi-user editing
   - Conflict resolution
   - Change notifications

5. **Mobile App**
   - Native iOS/Android
   - Quick adjustments
   - Push notifications

---

## Testing

### Unit Tests
```bash
npm test src/components/panels/
```

### E2E Tests (Playwright)
```bash
npm run test:e2e -- panels
```

### Manual Testing Checklist
- [ ] All collapsible sections expand/collapse
- [ ] Sliders update values correctly
- [ ] Toggles change state
- [ ] Presets apply correctly
- [ ] Impact preview calculates
- [ ] Buttons trigger correct actions
- [ ] Responsive on mobile
- [ ] Keyboard navigation works
- [ ] Tooltips display on hover

---

## Troubleshooting

### Issue: Panels not rendering
**Solution:** Ensure all ui components are installed:
```bash
# Check if card, button, slider, switch exist
ls dashboard/frontend/src/components/ui/
```

### Issue: TypeScript errors
**Solution:** Run type checking:
```bash
npm run type-check
```

### Issue: Styles not applying
**Solution:** Verify Tailwind config includes panels directory:
```js
// tailwind.config.js
content: [
  './src/components/panels/**/*.{ts,tsx}',
]
```

---

## Credits

**Created:** 2025-11-10
**Author:** Phantom Neural Cortex Team
**Version:** 1.0.0
**License:** MIT

---

## Summary Statistics

- **Total Panels:** 6
- **Total Lines of Code:** ~2,800 lines
- **Total Parameters:** 40+ configurable settings
- **Collapsible Sections:** 17 sections across all panels
- **Action Buttons:** 20+ actions
- **Mock Data Points:** 50+ metrics and values

**Status:** ✅ Complete and ready for integration
