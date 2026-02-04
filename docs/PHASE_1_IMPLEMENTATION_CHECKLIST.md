# Phase 1 Implementation Checklist: Context Window Management

**Target:** Implement OpenClaw-inspired context window management  
**Duration:** 2 weeks  
**Status:** Ready to Start 🚀

---

## 📋 Overview

Implement intelligent context window management to:
- Track token usage in real-time
- Automatically prune old messages
- Compact long conversations
- Provide CLI commands for inspection

---

## ✅ Tasks Breakdown

### Week 1: Core Infrastructure

#### Day 1-2: Context Tracker Module

- [ ] **Create module structure**
  ```bash
  mkdir -p dashboard/backend/context
  touch dashboard/backend/context/__init__.py
  touch dashboard/backend/context/tracker.py
  ```

- [ ] **Implement ContextTracker class**
  - [ ] Token counting for different message types
  - [ ] Track system prompt tokens
  - [ ] Track user message tokens
  - [ ] Track assistant response tokens
  - [ ] Track tool call/result tokens
  - [ ] Calculate total usage
  - [ ] Calculate percentage used
  - [ ] Support multiple models (different limits)

- [ ] **Add token counting utility**
  - [ ] Use tiktoken for accurate counting
  - [ ] Support Claude (cl100k_base)
  - [ ] Support Gemini (estimation)
  - [ ] Support GPT models
  - [ ] Cache token counts

- [ ] **Create unit tests**
  ```python
  # Test cases:
  # - Token counting accuracy
  # - Multiple message types
  # - Different models
  # - Edge cases (empty, very long)
  ```

#### Day 3-4: Context Pruner Module

- [ ] **Create pruner.py**
  ```bash
  touch dashboard/backend/context/pruner.py
  ```

- [ ] **Implement ContextPruner class**
  - [ ] Identify prunable messages
  - [ ] Keep recent N messages
  - [ ] Keep important messages (pinned, system)
  - [ ] Remove old tool outputs
  - [ ] Recalculate tokens after pruning
  - [ ] Return pruned items for logging

- [ ] **Pruning strategies**
  - [ ] Time-based (older than X minutes)
  - [ ] Importance-based (score < threshold)
  - [ ] Token-based (when > 80% full)
  - [ ] Configurable thresholds

- [ ] **Create unit tests**
  ```python
  # Test cases:
  # - Prune by age
  # - Prune by importance
  # - Keep recent messages
  # - Preserve system messages
  ```

#### Day 5: Context Compactor Module

- [ ] **Create compactor.py**
  ```bash
  touch dashboard/backend/context/compactor.py
  ```

- [ ] **Implement ContextCompactor class**
  - [ ] Identify compactable content
  - [ ] Summarize long conversations
  - [ ] Compress tool outputs
  - [ ] Use AI for intelligent summarization
  - [ ] Preserve essential information
  - [ ] Track original vs. compressed size

- [ ] **Compaction strategies**
  - [ ] Summarize conversation threads
  - [ ] Extract key points from tool outputs
  - [ ] Merge related messages
  - [ ] Use Claude/Gemini for summarization

- [ ] **Create unit tests**
  ```python
  # Test cases:
  # - Compress long conversation
  # - Extract key points
  # - Verify information preserved
  # - Token reduction metrics
  ```

---

### Week 2: CLI & Integration

#### Day 6-7: CLI Inspector Module

- [ ] **Create inspector.py**
  ```bash
  touch dashboard/backend/context/inspector.py
  ```

- [ ] **Implement CLI commands**
  - [ ] `/status` - Show context usage
    ```
    Context: 1500/4096 tokens (37%)
    ├─ System: 500 tokens (12%)
    ├─ Messages: 800 tokens (20%)
    └─ Tools: 200 tokens (5%)
    ```
  
  - [ ] `/context list` - List all items
    ```
    Context Items:
    1. [System] Initial prompt (500 tokens)
    2. [User] "Help me with..." (50 tokens)
    3. [Assistant] "Sure, I can..." (100 tokens)
    4. [Tool] grep_result (200 tokens)
    ...
    ```
  
  - [ ] `/context detail` - Detailed breakdown
    ```
    Detailed Context Breakdown:
    
    System Prompt: 500 tokens
    ├─ Guidelines: 300 tokens
    ├─ Tools: 150 tokens
    └─ Configuration: 50 tokens
    
    Conversation: 800 tokens
    ├─ Recent (last 5): 400 tokens
    ├─ Older: 400 tokens
    
    Tool Results: 200 tokens
    ├─ grep: 100 tokens
    ├─ view: 50 tokens
    └─ bash: 50 tokens
    ```
  
  - [ ] `/compact` - Trigger compaction
    ```
    Compacting context...
    Before: 3500/4096 tokens (85%)
    After:  2100/4096 tokens (51%)
    Saved: 1400 tokens (40% reduction)
    ```

- [ ] **Create unit tests**

#### Day 8: API Integration

- [ ] **Create context router**
  ```bash
  touch dashboard/backend/routers/context.py
  ```

- [ ] **Implement REST endpoints**
  - [ ] `GET /api/context/status` - Get status
  - [ ] `GET /api/context/items` - List items
  - [ ] `GET /api/context/detail` - Detailed view
  - [ ] `POST /api/context/compact` - Trigger compaction
  - [ ] `POST /api/context/prune` - Trigger pruning
  - [ ] `DELETE /api/context/item/{id}` - Remove item

- [ ] **Add to main.py**
  ```python
  from routers import context
  app.include_router(context.router, prefix="/api/context", tags=["context"])
  ```

- [ ] **Create API tests**

#### Day 9: Orchestration Integration

- [ ] **Update orchestration.py**
  - [ ] Initialize ContextTracker per session
  - [ ] Track tokens for each message
  - [ ] Auto-prune at 80% usage
  - [ ] Log pruning/compaction events
  - [ ] Integrate with existing agents

- [ ] **Add configuration**
  ```python
  # .env
  CONTEXT_MAX_TOKENS=4096  # Default limit
  CONTEXT_PRUNE_THRESHOLD=0.8  # Prune at 80%
  CONTEXT_KEEP_RECENT=5  # Keep last 5 messages
  CONTEXT_AUTO_COMPACT=true  # Auto-compact
  ```

- [ ] **Add metrics**
  - [ ] Track pruning frequency
  - [ ] Track compaction efficiency
  - [ ] Track token savings
  - [ ] Export to Prometheus

#### Day 10: Testing & Documentation

- [ ] **Integration tests**
  - [ ] E2E workflow with context tracking
  - [ ] Auto-pruning triggers correctly
  - [ ] CLI commands work
  - [ ] API endpoints work
  - [ ] Performance is acceptable

- [ ] **Documentation**
  - [ ] Create CONTEXT_MANAGEMENT.md
  - [ ] Document architecture
  - [ ] Document CLI commands
  - [ ] Document API endpoints
  - [ ] Add usage examples
  - [ ] Add troubleshooting section

- [ ] **Performance testing**
  - [ ] Token counting performance
  - [ ] Pruning performance
  - [ ] Compaction performance
  - [ ] Memory usage

- [ ] **Code review**
  - [ ] Run linters (black, mypy, pylint)
  - [ ] Run security scan (bandit, CodeQL)
  - [ ] Check test coverage (>80%)
  - [ ] Review by team

---

## 📁 File Structure

```
dashboard/backend/context/
├── __init__.py
├── tracker.py           # ContextTracker class
├── pruner.py            # ContextPruner class
├── compactor.py         # ContextCompactor class
├── inspector.py         # CLI commands
├── models.py            # Data models
├── utils.py             # Token counting utilities
└── tests/
    ├── test_tracker.py
    ├── test_pruner.py
    ├── test_compactor.py
    └── test_inspector.py

dashboard/backend/routers/
└── context.py           # REST API endpoints

docs/
└── CONTEXT_MANAGEMENT.md  # Documentation
```

---

## 🧪 Test Cases

### Unit Tests

```python
# test_tracker.py
def test_token_counting():
    tracker = ContextTracker(max_tokens=4096)
    tracker.add_system_prompt("Hello", tokens=5)
    assert tracker.used_tokens == 5
    assert tracker.usage_percent == 0.12

def test_multiple_message_types():
    tracker = ContextTracker(max_tokens=1000)
    tracker.add_system_prompt("System", tokens=100)
    tracker.add_user_message("User", tokens=50)
    tracker.add_assistant_message("Assistant", tokens=100)
    assert tracker.used_tokens == 250

# test_pruner.py
def test_prune_old_messages():
    pruner = ContextPruner(tracker)
    pruned = pruner.prune_old_messages(keep_recent=3)
    assert len(pruned) > 0
    assert tracker.usage_percent < 0.8

# test_compactor.py
def test_compact_conversation():
    compactor = ContextCompactor(tracker)
    original = tracker.used_tokens
    compactor.compact()
    assert tracker.used_tokens < original
```

### Integration Tests

```python
# test_integration.py
async def test_auto_pruning():
    # Fill context to 85%
    for i in range(100):
        await add_message(f"Message {i}")
    
    # Should auto-prune
    assert tracker.usage_percent < 0.8

async def test_cli_commands():
    response = await client.get("/api/context/status")
    assert response.status_code == 200
    assert "used_tokens" in response.json()
```

---

## 🎯 Acceptance Criteria

- [ ] Context usage tracked in real-time
- [ ] Token counting accurate (<5% error)
- [ ] Auto-pruning prevents overflow
- [ ] CLI commands work (`/status`, `/context`, `/compact`)
- [ ] API endpoints functional
- [ ] Integration with orchestration
- [ ] Test coverage >80%
- [ ] Documentation complete
- [ ] Performance acceptable (<100ms overhead)
- [ ] Code reviewed and approved

---

## 📊 Success Metrics

| Metric | Target |
|--------|--------|
| Token counting accuracy | >95% |
| Pruning latency | <50ms |
| Compaction ratio | >30% reduction |
| Test coverage | >80% |
| API response time | <100ms |
| Memory overhead | <50MB |

---

## 🚀 Getting Started

### Prerequisites

```bash
# Install dependencies
pip install tiktoken

# Check versions
python --version  # 3.10+
pytest --version  # 7.0+
```

### Run Tests

```bash
# Unit tests
pytest dashboard/backend/context/tests/ -v

# Integration tests
pytest dashboard/backend/tests/test_context_integration.py -v

# Coverage report
pytest --cov=dashboard/backend/context --cov-report=html
```

### Local Development

```bash
# 1. Create feature branch
git checkout -b feature/context-management

# 2. Start backend
cd dashboard/backend
uvicorn main:app --reload

# 3. Test CLI commands
curl http://localhost:1336/api/context/status

# 4. Run tests
pytest -v
```

---

## 📝 Notes

- **Token Counting:** Use tiktoken library for accuracy
- **Model Support:** Different models have different limits
  - Claude: 200k tokens (cl100k_base encoding)
  - Gemini: 1M-2M tokens (approximate)
  - GPT-4: 128k tokens
- **Pruning Strategy:** Start with simple time-based, add ML later
- **Compaction:** Use Claude/Gemini for summarization
- **Performance:** Cache token counts, optimize loops

---

## 🔗 Related Documents

- [OpenClaw Modernization Plan](OPENCLAW_MODERNIZATION_PLAN.md) - Full roadmap
- [System Architecture Summary](SYSTEM_ARCHITECTURE_SUMMARY.md) - Current architecture
- [Backend API Requirements](BACKEND_API_REQUIREMENTS.md) - API standards

---

**Status:** Ready to implement ✅  
**Next:** Create feature branch and start Day 1 tasks

**Questions?** Ask in the PR or GitHub Discussions!
