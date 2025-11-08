# Custom Agents for Claude Code & GitHub Copilot

This repository provides specialized AI agents for development tasks.

## Available Agents

### 1. Code Expert (@code-expert)
**Best for:** Code generation, refactoring, architecture decisions

**Capabilities:**
- TypeScript/JavaScript expertise (React, Next.js, Node.js)
- Python development (FastAPI, Django)
- System architecture & design patterns
- Code quality & security reviews
- Performance optimization

**Usage:**
```bash
# In Claude Code
"@code-expert review this React component"

# In Copilot CLI
copilot /agent code-expert
```

---

### 2. Debug Specialist (@debug-specialist)
**Best for:** Bug fixing, root cause analysis, performance issues

**Capabilities:**
- 4-Phase systematic debugging
- Root cause tracing
- Performance profiling
- Memory leak detection
- Error pattern recognition

**Methodology:**
1. **Investigation** - Reproduce & gather data
2. **Pattern Analysis** - Search for similar issues
3. **Hypothesis Testing** - Test systematically
4. **Implementation** - Fix & document

**Usage:**
```bash
# In Claude Code
"@debug-specialist this error keeps happening"

# In Copilot CLI
copilot /agent debug-specialist
```

---

### 3. API Tester (@api-tester)
**Best for:** API testing, integration testing, security testing

**Capabilities:**
- REST API testing with Postmancer
- GraphQL query testing
- WebSocket testing
- API security audits
- Performance & load testing

**Tools:**
- Postmancer for HTTP requests
- Playwright for browser-based tests
- Security vulnerability scanning
- Response time profiling

**Usage:**
```bash
# In Claude Code
"@api-tester test the /api/users endpoint"

# In Copilot CLI
copilot /agent api-tester
```

---

### 4. Gemini Specialist (@gemini-specialist)
**Best for:** Large-scale analysis, batch operations, documentation

**Capabilities:**
- **2M token context window** - Analyze entire codebases
- Large file/repository analysis
- Batch code generation
- Multi-file refactoring
- Comprehensive documentation generation

**Strengths:**
- Free tier: 1500 requests/day
- Ultra-fast responses (Gemini 2.0 Flash)
- Multimodal capabilities
- Cost-effective for large operations

**Usage:**
```bash
# In Claude Code
"@gemini-specialist analyze this entire repository structure"

# In Copilot CLI
copilot /agent gemini-specialist
```

---

## Agent Configuration

Agents are configured in:
- **Claude Code:** `.claude/` directory + this `AGENTS.md`
- **Copilot CLI:** `~/.copilot/agents/` directory

## MCP Servers Available

All agents have access to:
1. **filesystem** - File operations
2. **memory** - Context retention
3. **github** - Repository access
4. **brave-search** - Web research
5. **docs** - Framework documentation
6. **postmancer** - API testing
7. **playwright** - Browser automation
8. **time** - Timezone handling
9. **sqlite** - Local database
10. **sequential-thinking** - Complex reasoning

## Custom Instructions

### Code Quality Standards
- Follow DRY & SOLID principles
- Type safety (TypeScript preferred)
- Comprehensive error handling
- Security-first approach (OWASP Top 10)
- Test coverage for critical paths

### Documentation Requirements
- JSDoc for public APIs
- README for each module
- Examples for complex functions
- ADR (Architecture Decision Records) for major changes

### Testing Strategy
- **Unit Tests:** Jest + React Testing Library
- **Integration Tests:** Playwright
- **API Tests:** Postmancer
- **E2E Tests:** Playwright + Browser Tools

### Security Checklist
- [ ] No hardcoded secrets
- [ ] Input validation everywhere
- [ ] SQL injection prevention
- [ ] XSS protection
- [ ] CSRF tokens where needed
- [ ] Rate limiting implemented
- [ ] Authentication/Authorization proper

### Performance Guidelines
- Bundle size < 200KB (initial load)
- Time to Interactive < 3s
- Lighthouse score > 90
- Lazy load non-critical components
- Optimize images (WebP, lazy loading)
- Database queries optimized (use EXPLAIN)

## Agent Selection Guide

| Task | Recommended Agent |
|------|-------------------|
| Write new feature | @code-expert |
| Fix bug | @debug-specialist |
| Test API | @api-tester |
| Code review | @code-expert |
| Performance issue | @debug-specialist |
| Integration testing | @api-tester |
| Architecture design | @code-expert |
| Memory leak | @debug-specialist |
| Security audit | @api-tester |

## Environment Variables

Required in `.env`:
```env
GITHUB_TOKEN=ghp_xxx
BRAVE_API_KEY=BSA_xxx
GOOGLE_API_KEY=AIza_xxx
PERPLEXITY_API_KEY=pplx_xxx
```

## Repository Structure

```
.
├── .claude/              # Claude Code settings
├── .copilot/             # Copilot CLI config (user home)
├── AGENTS.md             # This file (repo-level)
├── .mcp.json             # MCP server config
├── .env                  # Environment variables
└── memory-bank/          # Persistent context
```

## Usage Examples

### Example 1: Code Review
```bash
# Claude Code
"@code-expert review src/components/UserProfile.tsx for security issues"

# Copilot CLI
copilot /agent code-expert
> Review the UserProfile component for security vulnerabilities
```

### Example 2: Debug Error
```bash
# Claude Code
"@debug-specialist I'm getting 'undefined is not a function' in production"

# Copilot CLI
copilot /agent debug-specialist
> Help me debug a production error
```

### Example 3: Test API
```bash
# Claude Code
"@api-tester create a test suite for POST /api/users endpoint"

# Copilot CLI
copilot /agent api-tester
> Test the users API endpoint
```

---

**Last Updated:** 2025-11-08
**Compatible with:** Claude Code CLI, Claude Code VSCode Extension, GitHub Copilot CLI
