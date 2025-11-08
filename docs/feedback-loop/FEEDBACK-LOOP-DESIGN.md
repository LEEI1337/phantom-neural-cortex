# 🔄 Feedback Loop Design - UltraThink Inspired

**Status:** Design Phase
**Inspired by:** [UltraThink - Hierarchical Reasoning Model](https://arxiv.org/html/2506.21734v3)
**Version:** 1.0
**Date:** 2025-11-08

---

## 🎯 Problem Statement

**Current System (Linear):**
```
Issue → Agent Selection → Implementation → PR → Done
```

**Problems:**
- ❌ No feedback if implementation is wrong
- ❌ No iterative refinement
- ❌ Agent learns nothing from failures
- ❌ Quality depends on first-try success
- ❌ No self-correction mechanism

**Goal:**
- ✅ Iterative refinement loop
- ✅ Self-correction on failures
- ✅ Learn from mistakes
- ✅ Prevent infinite loops
- ✅ Adaptive computation (stop when good enough)

---

## 📊 UltraThink Architecture (Adapted)

### Original Paper Concepts

**Hierarchical Two-Tier System:**
```
H-Module (High-Level) - Slow, Abstract Planning
    ↓ feedback
L-Module (Low-Level) - Fast, Detailed Execution
    ↑ state
H-Module updates when L-Module equilibrium reached
```

**Adaptive Halting (Q-Learning):**
```python
Q(state, action):
    action ∈ {HALT, CONTINUE}

    if Q(s, HALT) > Q(s, CONTINUE):
        stop_iteration()
    elif iterations >= MAX_ITERATIONS:
        force_halt()
    else:
        continue_refinement()
```

### Adapted to Lazy Bird

**Our Hierarchical System:**
```
H-Module: Lazy Bird (Strategy, Agent Selection, Quality Goals)
    ↓ feedback (quality metrics, test results, review comments)
L-Module: Agent (Implementation, Code Generation, Testing)
    ↑ state (code quality, test coverage, errors)
```

---

## 🏗️ Architecture Design

### Layer 5: Feedback Loop Orchestration (NEW!)

```
Layer 5: Feedback Loop Orchestration ⭐ NEW
   ↓ monitors & guides
Layer 4: Lazy Bird Automation
   ↓ orchestrates
Layer 3: Rover Orchestration
   ↓ uses
Layer 2: AI CLI (Claude/Gemini/Copilot)
   ↓ uses
Layer 1: MCP Servers
   ↓ built on
Layer 0: Universal Standards
```

### Components

**1. Quality Evaluator (H-Module)**
```python
class QualityEvaluator:
    """High-level module: Evaluates quality and decides next action."""

    def evaluate_implementation(self, pr_data: Dict) -> QualityMetrics:
        """Evaluate PR quality metrics."""
        return {
            "test_coverage": 0.85,        # 85%
            "tests_passing": True,
            "security_score": 0.92,       # 92/100
            "code_quality": 0.88,         # SonarQube score
            "documentation": 0.95,        # Completeness
            "type_safety": 1.0,          # TypeScript strict
        }

    def compute_halt_q_value(self, metrics: QualityMetrics) -> float:
        """Q-value for HALT action."""
        # Weighted average of metrics
        weights = {
            "test_coverage": 0.25,
            "tests_passing": 0.30,     # Critical!
            "security_score": 0.20,
            "code_quality": 0.15,
            "documentation": 0.05,
            "type_safety": 0.05,
        }

        q_halt = sum(metrics[k] * weights[k] for k in weights)
        return q_halt

    def should_halt(self, metrics: QualityMetrics, iteration: int) -> bool:
        """Adaptive halting decision."""
        q_halt = self.compute_halt_q_value(metrics)
        q_continue = 1.0 - q_halt  # Inverse

        # Halt conditions
        if q_halt > q_continue:
            return True  # Quality good enough

        if iteration >= MAX_ITERATIONS:
            return True  # Force halt (infinite loop prevention)

        if metrics["tests_passing"] and q_halt > 0.75:
            return True  # Good enough threshold

        return False  # Continue refinement
```

**2. Refinement Agent (L-Module)**
```python
class RefinementAgent:
    """Low-level module: Executes refinement iterations."""

    def refine_implementation(
        self,
        current_code: str,
        feedback: List[str],
        previous_state: Dict
    ) -> Dict:
        """Execute one refinement iteration."""

        # Context from H-module
        quality_goals = previous_state.get("quality_goals", {})
        failed_tests = previous_state.get("failed_tests", [])

        # Refine code based on feedback
        prompt = self._build_refinement_prompt(
            code=current_code,
            feedback=feedback,
            goals=quality_goals,
            failed_tests=failed_tests
        )

        # Call agent (Claude/Gemini/Copilot)
        refined_code = self.agent.generate(prompt)

        # Run tests
        test_results = self._run_tests(refined_code)

        return {
            "code": refined_code,
            "tests": test_results,
            "state": {
                "coverage": test_results["coverage"],
                "passing": test_results["passing"],
                "errors": test_results["errors"],
            }
        }
```

**3. Infinite Loop Prevention**
```python
class InfiniteLoopPrevention:
    """Prevents infinite feedback loops."""

    def __init__(self):
        self.MAX_ITERATIONS = 5           # Hard limit
        self.MIN_QUALITY_THRESHOLD = 0.60  # Must achieve 60%
        self.STAGNATION_WINDOW = 3         # Detect stagnation
        self.quality_history = []

    def is_stagnating(self) -> bool:
        """Detect if quality improvements have stalled."""
        if len(self.quality_history) < self.STAGNATION_WINDOW:
            return False

        recent = self.quality_history[-self.STAGNATION_WINDOW:]

        # Check if variance < threshold (no improvement)
        variance = np.var(recent)

        if variance < 0.001:  # Almost no change
            return True

        # Check if declining
        if all(recent[i] >= recent[i+1] for i in range(len(recent)-1)):
            return True  # Quality is getting worse!

        return False

    def should_abort(self, iteration: int, quality: float) -> bool:
        """Decide if loop should be aborted."""
        self.quality_history.append(quality)

        # Hard iteration limit
        if iteration >= self.MAX_ITERATIONS:
            return True

        # Quality not improving
        if self.is_stagnating():
            return True

        # Quality too low after multiple tries
        if iteration >= 3 and quality < self.MIN_QUALITY_THRESHOLD:
            return True  # Abort - quality too low

        return False
```

**4. Feedback Orchestrator**
```python
class FeedbackOrchestrator:
    """Orchestrates the feedback loop."""

    def __init__(self):
        self.evaluator = QualityEvaluator()
        self.refiner = RefinementAgent()
        self.loop_prevention = InfiniteLoopPrevention()

    def execute_feedback_loop(
        self,
        initial_implementation: Dict,
        quality_goals: Dict
    ) -> Dict:
        """Execute feedback loop until halt condition."""

        iteration = 0
        current_code = initial_implementation["code"]
        state = {"quality_goals": quality_goals}

        while True:
            iteration += 1

            # L-Module: Refine implementation
            logger.info(f"Iteration {iteration}: Refining...")
            result = self.refiner.refine_implementation(
                current_code=current_code,
                feedback=state.get("feedback", []),
                previous_state=state
            )

            current_code = result["code"]

            # H-Module: Evaluate quality
            logger.info(f"Iteration {iteration}: Evaluating quality...")
            metrics = self.evaluator.evaluate_implementation({
                "code": current_code,
                "tests": result["tests"]
            })

            # Update state
            state.update({
                "metrics": metrics,
                "iteration": iteration,
                "failed_tests": result["tests"]["errors"]
            })

            # Adaptive Halting Decision
            should_halt = self.evaluator.should_halt(metrics, iteration)
            should_abort = self.loop_prevention.should_abort(
                iteration,
                self.evaluator.compute_halt_q_value(metrics)
            )

            if should_halt:
                logger.info(f"✅ Halting: Quality sufficient ({metrics})")
                return {
                    "status": "success",
                    "code": current_code,
                    "metrics": metrics,
                    "iterations": iteration
                }

            if should_abort:
                logger.warning(f"⚠️ Aborting: Loop prevention triggered")
                return {
                    "status": "aborted",
                    "code": current_code,
                    "metrics": metrics,
                    "iterations": iteration,
                    "reason": "infinite_loop_prevention"
                }

            # Generate feedback for next iteration
            state["feedback"] = self._generate_feedback(metrics, result["tests"])

            logger.info(f"🔄 Continuing to iteration {iteration + 1}...")
```

---

## 🔄 Workflow Integration

### Updated Lazy Bird Workflow

**Before (Linear):**
```
1. Issue detected
2. Agent selected
3. Implementation
4. PR created
5. Done
```

**After (Feedback Loop):**
```
1. Issue detected
2. Agent selected
3. Initial implementation (L-Module)
4. Quality evaluation (H-Module)
5. ┌─> Refinement needed?
   │   ├─ Yes → Refine (L-Module) → Evaluate (H-Module) ─┐
   │   │                                                   │
   │   └─ No → Halt ─────────────────────────────────────┘
6. PR created with metrics
7. Done
```

### Feedback Sources

**Automatic Feedback:**
1. **Test Results** - Pytest output, coverage reports
2. **Linting** - Ruff, ESLint, Pylint
3. **Type Checking** - mypy, TypeScript compiler
4. **Security Scan** - Bandit, Semgrep
5. **Code Quality** - SonarQube, CodeClimate

**Manual Feedback (Optional):**
6. **Review Comments** - GitHub PR reviews
7. **User Feedback** - Issue comments

---

## 📊 Metrics & Monitoring

### Quality Metrics

```python
@dataclass
class QualityMetrics:
    # Testing
    test_coverage: float           # 0.0 - 1.0
    tests_passing: bool
    test_count: int

    # Code Quality
    code_quality_score: float      # SonarQube score
    complexity: int                # Cyclomatic complexity
    duplications: float            # % duplicated code

    # Security
    security_score: float          # Bandit/Semgrep score
    vulnerabilities: int

    # Type Safety
    type_coverage: float           # mypy coverage
    type_errors: int

    # Documentation
    doc_coverage: float            # Docstring coverage

    # Overall
    overall_quality: float         # Weighted average
```

### Loop Metrics

```python
@dataclass
class LoopMetrics:
    iterations: int
    total_time: float              # seconds
    quality_progression: List[float]  # Quality over iterations
    stagnation_detected: bool
    halt_reason: str               # "quality_sufficient" | "max_iterations" | "stagnation"
    cost: float                    # $
```

---

## 🛡️ Infinite Loop Prevention Strategies

### 1. Hard Iteration Limit
```python
MAX_ITERATIONS = 5  # Never exceed 5 refinements
```

### 2. Quality Stagnation Detection
```python
# If quality doesn't improve for 3 iterations → HALT
variance(quality_history[-3:]) < 0.001 → ABORT
```

### 3. Quality Degradation Detection
```python
# If quality is declining → HALT
if all(q[i] >= q[i+1] for i in range(len(recent)-1)):
    ABORT
```

### 4. Minimum Quality Gate
```python
# After 3 iterations, quality must be > 60%
if iteration >= 3 and quality < 0.60:
    ABORT  # Can't reach quality goals
```

### 5. Cost Limit
```python
# Don't spend more than $5 on refinements
if total_cost > 5.0:
    ABORT
```

### 6. Time Limit
```python
# Max 30 minutes total
if time.time() - start_time > 1800:
    ABORT
```

### 7. Feedback Hash Tracking
```python
# Detect if same feedback repeats (cycle detection)
feedback_hashes = []

def is_cycling(new_feedback: str) -> bool:
    h = hashlib.md5(new_feedback.encode()).hexdigest()

    if h in feedback_hashes[-2:]:  # Same feedback 2x in a row
        return True

    feedback_hashes.append(h)
    return False
```

---

## 💡 Implementation Plan

### Phase 1: Core Components (Week 1)
- [ ] Create `lazy-bird/feedback/` directory
- [ ] Implement `quality_evaluator.py`
- [ ] Implement `refinement_agent.py`
- [ ] Implement `loop_prevention.py`
- [ ] Implement `feedback_orchestrator.py`

### Phase 2: Integration (Week 2)
- [ ] Integrate with Rover
- [ ] Update `issue-watcher.py` to use feedback loop
- [ ] Add quality metrics collection
- [ ] Add monitoring/logging

### Phase 3: Testing (Week 3)
- [ ] Unit tests for each component
- [ ] Integration tests with real projects
- [ ] Stress testing (detect infinite loops)
- [ ] Cost analysis

### Phase 4: Optimization (Week 4)
- [ ] Tune Q-learning weights
- [ ] Optimize halting thresholds
- [ ] Add caching for repeated evaluations
- [ ] Performance profiling

---

## 📈 Expected Improvements

### Quality Improvements
```
Before (Single Pass):
- Test Coverage: 60-70% (Gemini) / 80-90% (Claude)
- Code Quality: 70-80%
- First-try Success: ~60%

After (Feedback Loop):
- Test Coverage: 75-85% (Gemini) / 85-95% (Claude)
- Code Quality: 85-95%
- Final Success: ~95% (after 2-3 iterations)
```

### Cost Analysis
```
Before:
- Gemini: $0 (1 pass)
- Claude: $2 (1 pass)

After (avg 2.5 iterations):
- Gemini: $0 (still free tier!)
- Claude: $5 (2.5x cost, but 95% success vs 60%)

ROI: Higher success rate = less manual fixes = worth it!
```

---

## 🔬 Example Scenario

### Scenario: E-Commerce API with Payment

**Initial Implementation (Iteration 0):**
```python
# Gemini generates code
# Quality: 65% (missing security checks)
# Tests: 12/15 passing (payment validation fails)
```

**Iteration 1 (Feedback Loop):**
```
Feedback:
- 3 tests failing (payment validation)
- Security scan: Missing input validation
- Coverage: 65% (below 75% target)

H-Module: Q(HALT) = 0.65, Q(CONTINUE) = 0.35 → CONTINUE

L-Module: Refine code
- Add input validation
- Fix payment tests
- Add edge case tests

Quality: 78%
Tests: 14/15 passing
```

**Iteration 2:**
```
Feedback:
- 1 test failing (edge case)
- Security scan: ✅ All checks pass
- Coverage: 78%

H-Module: Q(HALT) = 0.78, Q(CONTINUE) = 0.22 → CONTINUE (close!)

L-Module: Refine
- Fix edge case
- Add 2 more tests

Quality: 87%
Tests: 15/15 passing ✅
```

**Iteration 3:**
```
Feedback:
- All tests passing ✅
- Security: ✅
- Coverage: 87%
- Code quality: 90%

H-Module: Q(HALT) = 0.88, Q(CONTINUE) = 0.12 → HALT ✅

RESULT: PR created with 87% coverage, all tests passing!
```

**Cost:** Gemini FREE (3 iterations still within free tier)
**Time:** 8 minutes (vs 1 hour manual debugging)
**Quality:** 87% vs 65% initial

---

## 🚀 Next Steps

1. **Review this design document**
2. **Approve architecture**
3. **Implement Phase 1 components**
4. **Test with real scenarios**
5. **Iterate and optimize**

---

## 📚 References

- [UltraThink: Hierarchical Reasoning Model](https://arxiv.org/html/2506.21734v3)
- [Adaptive Computation Time (ACT)](https://arxiv.org/abs/1603.08983)
- [Q-Learning for Halting](https://arxiv.org/abs/1511.06279)

---

**Status:** ✅ Design Complete - Ready for Implementation

**Questions?** Open an issue or comment below!
