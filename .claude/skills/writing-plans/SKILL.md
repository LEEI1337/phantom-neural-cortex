---
name: writing-plans
description: Create detailed implementation plans before coding (saves tokens later)
trigger: auto
---

# Writing Implementation Plans

Create clear plans BEFORE coding to save time and tokens:

## Plan Structure

### 1. GOAL (1-2 sentences)
```
What are we building and why?
```

### 2. CONSTRAINTS
```
- Technology limits
- Time/resource constraints
- Compatibility requirements
- Performance targets
```

### 3. APPROACH (High-Level)
```
- Architecture pattern
- Key components
- Data flow
- Integration points
```

### 4. STEPS (Ordered Tasks)
```
1. [Component] - Brief description
2. [Component] - Brief description
   - Sub-task if needed
3. [Testing] - What to test
4. [Deployment] - How to deploy
```

### 5. RISKS & MITIGATIONS
```
Risk: Description
Mitigation: Solution
```

### 6. SUCCESS CRITERIA
```
- Measurable outcomes
- Test coverage targets
- Performance metrics
```

## Token Optimization
- Write plan ONCE, reference during implementation
- Clear steps prevent back-and-forth
- Catches issues early (cheaper to fix in planning)
- Team can review before coding starts

## Example Output Format
```
GOAL: Add user authentication with JWT

CONSTRAINTS:
- Must use existing DB schema
- Response time < 200ms
- Support OAuth2

APPROACH:
- Middleware-based auth layer
- JWT with refresh tokens
- Redis session cache

STEPS:
1. Create auth middleware
2. Implement token generation/validation
3. Add refresh token logic
4. Write integration tests
5. Update API docs

RISKS:
- Token expiry handling → Use refresh tokens
- Concurrency issues → Use Redis locks

SUCCESS:
- All endpoints secured
- 95%+ test coverage
- Load test passes (1000 req/s)
```
