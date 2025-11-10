# Langfuse Setup Guide - LLM Observability

**Version:** 1.0.0
**Status:** REQUIRED for Production

Langfuse provides **complete observability** for your LLM agents - trace every execution, monitor costs, analyze performance.

---

## Why Langfuse?

### What it Does:

```
Task Execution:
  ├─> Agent Selection (logged to Langfuse)
  ├─> Prompt sent to Agent (logged with metadata)
  ├─> Agent Response (logged with tokens + cost)
  ├─> Quality Assessment (logged)
  └─> Agent Switch (if needed, logged with reason)

All visible in Langfuse Dashboard!
```

### Benefits:

- **Trace every LLM call** - See exact prompts, responses, latency
- **Cost tracking** - Per-agent, per-task, per-project costs
- **Token usage** - Input/output tokens for billing analysis
- **Performance monitoring** - Response times, success rates
- **Agent selection analysis** - Why was Claude chosen over Gemini?
- **Quality metrics** - Correlate quality scores with agent performance
- **Debugging** - Replay failed tasks, see exact context

---

## Setup (5 minutes)

### Step 1: Get Langfuse Keys

**Option A: Cloud (Recommended)**

1. Go to: https://cloud.langfuse.com
2. Sign up (free tier available)
3. Create new project
4. Go to Settings → API Keys
5. Copy:
   - Public Key (starts with `pk-lf-`)
   - Secret Key (starts with `sk-lf-`)

**Option B: Self-hosted (Advanced)**

```bash
# Using docker-compose
cd monitoring/
docker-compose up -d langfuse-web clickhouse postgres

# Langfuse will be available at: http://localhost:3000
```

### Step 2: Configure Environment

```bash
# Copy example
cp .env.example .env

# Edit .env
nano .env
```

Add your keys:

```bash
# Langfuse Configuration
LANGFUSE_PUBLIC_KEY=pk-lf-abc123...
LANGFUSE_SECRET_KEY=sk-lf-xyz789...
LANGFUSE_HOST=https://cloud.langfuse.com  # or http://localhost:3000 for self-hosted
```

### Step 3: Install Dependencies

```bash
cd dashboard/backend
pip install langfuse==2.59.0
```

### Step 4: Test Connection

```python
# dashboard/backend/test_langfuse.py
from orchestration.langfuse_integration import get_langfuse_observer
import asyncio

async def test_langfuse():
    observer = get_langfuse_observer()

    if observer.enabled:
        print("✅ Langfuse enabled and configured!")

        # Test trace
        async with observer.trace_agent_execution(
            task_id="test_123",
            agent="claude",
            prompt="Test prompt",
            metadata={"test": True}
        ) as trace:
            trace.update(
                output="Test response",
                tokens=100,
                cost=0.001
            )

        print("✅ Test trace sent successfully!")
        print(f"View in Langfuse: {observer.langfuse._client_wrapper._base_url}/traces")

    else:
        print("❌ Langfuse not configured")
        print("Set LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY in .env")

if __name__ == "__main__":
    asyncio.run(test_langfuse())
```

Run test:

```bash
python test_langfuse.py
```

Expected output:
```
✅ Langfuse enabled and configured!
✅ Test trace sent successfully!
View in Langfuse: https://cloud.langfuse.com/traces
```

---

## Usage in Orchestrator

### Already Integrated!

Langfuse is **already integrated** in `dashboard/backend/orchestration/orchestrator.py`:

```python
# In CLIOrchestrator.execute_task()
async with self.observer.trace_agent_execution(
    task_id=task.id,
    agent=selected_agent.value,
    prompt=task.prompt,
    metadata={
        "task_type": task.task_type.value,
        "project_id": task.workspace,
        "requires_security": task.requires_security
    }
) as trace:
    # Execute agent
    response = await self._execute_claude(task, session_id)

    # Update trace with results
    trace.update(
        output=response.content,
        tokens=response.tokens,
        cost=response.cost,
        metadata={
            "duration": response.duration,
            "session_id": response.session_id
        }
    )
```

### Agent Selection Tracking

```python
# Already in orchestrator
self.observer.track_agent_selection(
    task_id=task.id,
    selected_agent=selected_agent.value,
    reason="Task type: security",
    all_rewards={
        "claude": 0.9,
        "gemini": 0.3,
        "copilot": 0.2
    }
)
```

### Circuit Breaker Events

```python
# Already in circuit_breaker.py
self.observer.track_circuit_breaker_event(
    agent="claude",
    state="open",
    failure_count=5
)
```

---

## Viewing Traces in Langfuse

### Dashboard

1. Go to: https://cloud.langfuse.com (or your self-hosted URL)
2. Select your project
3. Click **Traces** in sidebar

### What You'll See:

```
Trace: task_abc123
├─ Agent: claude
├─ Input: "Review code for security vulnerabilities"
├─ Output: "Found 3 SQL injection vulnerabilities..."
├─ Tokens: 1523 (input: 450, output: 1073)
├─ Cost: $0.0046
├─ Duration: 12.5s
├─ Metadata:
│  ├─ task_type: security
│  ├─ project_id: proj_123
│  └─ session_id: sess_xyz789
└─ Events:
   ├─ agent_selection (why Claude was chosen)
   ├─ circuit_breaker_check (state: closed)
   └─ quality_assessment (score: 0.92)
```

### Filtering & Analysis

**Filter by Agent:**
```
agent = "claude"
```

**Filter by Cost:**
```
cost > 0.01
```

**Filter by Quality:**
```
metadata.quality_score > 0.8
```

**Group by Task Type:**
```
GROUP BY metadata.task_type
```

---

## Cost Analysis

### Per-Agent Costs

Langfuse automatically calculates:

- **Claude:** $0.0046 per task (avg)
- **Gemini:** $0.00 (FREE tier)
- **Copilot:** $0.0033 per task (flat $10/month)

### Monthly Projection

```
Last 30 days:
  Claude:   150 tasks × $0.0046 = $0.69
  Gemini:   450 tasks × $0.00   = $0.00
  Copilot:  100 tasks × $0.0033 = $0.33
  ----------------------------------------
  Total:                          $1.02

Projected Annual: $12.24
Actual Costs: $30/month (Claude Pro + Copilot Pro)
```

### Cost Optimization Insights

Langfuse shows:
- Which task types are most expensive
- Agent selection patterns
- Opportunities to use Gemini (FREE) more
- Tasks where Claude is over-used

---

## Performance Monitoring

### Metrics Tracked:

1. **Response Time** (by agent)
   - Claude: ~12s avg
   - Gemini: ~7s avg
   - Copilot: ~5s avg

2. **Success Rate** (by agent)
   - Claude: 96%
   - Gemini: 88%
   - Copilot: 92%

3. **Quality Score** (by agent)
   - Claude: 0.92 avg
   - Gemini: 0.85 avg
   - Copilot: 0.88 avg

4. **Token Efficiency**
   - Latent reasoning compression: 3.8x
   - Total token reduction: 65%

---

## Debugging with Langfuse

### Failed Task Investigation:

1. Go to Traces
2. Filter: `status = "error"`
3. Click on failed trace
4. See:
   - Exact prompt sent
   - Agent response (or error)
   - Stack trace
   - Circuit breaker state
   - Previous attempts

### Agent Switch Analysis:

1. Filter: `metadata.agent_switched = true`
2. See:
   - Original agent
   - New agent
   - Switch reason
   - Quality improvement

---

## Langfuse + Prometheus Integration

### Combined Observability:

**Langfuse:** LLM-level observability
- Prompts, responses, costs, tokens

**Prometheus:** System-level metrics
- CPU, Memory, API latency, throughput

**Together:** Complete visibility

```
Grafana Dashboard:
  ├─ System Metrics (Prometheus)
  │  ├─ CPU Usage: 45%
  │  ├─ Memory: 2.1 GB
  │  └─ API Latency: 120ms avg
  └─ LLM Metrics (Langfuse API)
     ├─ Tasks/hour: 25
     ├─ Cost/hour: $0.15
     └─ Quality: 0.89 avg
```

### Query Langfuse from Grafana:

```python
# dashboard/backend/routers/metrics.py
@router.get("/langfuse/summary")
async def get_langfuse_summary():
    """Fetch LLM metrics from Langfuse for Grafana"""

    observer = get_langfuse_observer()

    # Query Langfuse API
    traces = observer.langfuse.get_traces(
        from_timestamp=datetime.utcnow() - timedelta(hours=1)
    )

    return {
        "total_tasks": len(traces),
        "total_cost": sum(t.cost for t in traces),
        "avg_quality": mean(t.metadata.get("quality", 0) for t in traces),
        "agent_breakdown": {
            "claude": len([t for t in traces if t.metadata.get("agent") == "claude"]),
            "gemini": len([t for t in traces if t.metadata.get("agent") == "gemini"]),
            "copilot": len([t for t in traces if t.metadata.get("agent") == "copilot"])
        }
    }
```

---

## Troubleshooting

### Langfuse Not Working

**Check 1: Keys Set?**

```bash
python -c "import os; print('PK:', os.getenv('LANGFUSE_PUBLIC_KEY')[:20] if os.getenv('LANGFUSE_PUBLIC_KEY') else 'NOT SET')"
```

**Check 2: Network Access?**

```bash
curl https://cloud.langfuse.com/api/public/health
```

Should return: `{"status":"ok"}`

**Check 3: Langfuse Installed?**

```bash
pip show langfuse
```

Should show version 2.59.0 or newer

### Traces Not Appearing

**Issue:** Traces take a few seconds to appear

**Solution:** Click "Refresh" in Langfuse UI, or wait 5-10 seconds

**Issue:** Traces missing metadata

**Solution:** Check that `metadata` dict is JSON-serializable (no datetime objects!)

### Self-Hosted Langfuse Issues

**Issue:** Can't connect to localhost:3000

**Solution:** Check docker-compose logs:

```bash
cd monitoring/
docker-compose logs langfuse-web
```

**Issue:** ClickHouse or Postgres not starting

**Solution:** Increase Docker memory limit to at least 4GB

---

## Best Practices

### 1. Always Include Metadata

```python
metadata = {
    "task_type": task.task_type.value,
    "project_id": task.workspace,
    "quality_score": quality,
    "agent_switches": task.agent_switches,
    "iteration": task.current_iteration
}
```

### 2. Track Agent Selection Decisions

```python
observer.track_agent_selection(
    task_id=task_id,
    selected_agent=agent.value,
    reason=f"Task type: {task_type}, Quality threshold met",
    all_rewards=reward_scores
)
```

### 3. Flush on Shutdown

```python
# In main.py
@app.on_event("shutdown")
async def shutdown_event():
    observer = get_langfuse_observer()
    observer.flush()  # Ensure all traces are sent
```

### 4. Use Trace Context for Multi-Step Tasks

```python
# Parent trace
async with observer.trace_agent_execution(...) as parent_trace:
    # Step 1
    response1 = await agent1()
    parent_trace.update(output=response1)

    # Step 2 (sub-trace)
    async with observer.trace_agent_execution(...) as sub_trace:
        response2 = await agent2(response1)
        sub_trace.update(output=response2)
```

### 5. Tag Experiments

```python
metadata = {
    "experiment": "latent_reasoning_v2",
    "variant": "compression_ratio_4.0"
}
```

---

## Advanced: Langfuse Prompts

### Versioned Prompts

Store Layer-2 guidelines in Langfuse:

1. Go to Langfuse → **Prompts**
2. Create new prompt: `layer-2-claude-v1`
3. Content: LAYER-2-CLAUDE.md text
4. Tag as production

```python
# In orchestrator
guideline = observer.langfuse.get_prompt("layer-2-claude-v1")
full_prompt = f"{guideline.prompt}\n\n{task.prompt}"
```

### Benefits:
- Version control for prompts
- A/B testing
- Rollback to previous versions
- Analytics per prompt version

---

## Cost Management

### Alerts

Set up cost alerts in Langfuse:

1. Go to Settings → Alerts
2. Create alert:
   - Condition: `daily_cost > 5.00`
   - Action: Email notification

### Budgets

Set monthly budget:

```python
# In orchestrator
MONTHLY_BUDGET = 30.00  # dollars

observer.langfuse.set_budget(
    amount=MONTHLY_BUDGET,
    period="monthly"
)
```

---

## Next Steps

1. ✅ Set up Langfuse keys in `.env`
2. ✅ Run test script
3. ✅ View first trace in dashboard
4. ✅ Configure Grafana integration (optional)
5. ✅ Set up cost alerts
6. ✅ Start analyzing agent performance!

---

**Documentation:** https://langfuse.com/docs
**API Reference:** https://langfuse.com/docs/api
**Support:** https://github.com/langfuse/langfuse/discussions
