# Phantom Neural Cortex - Documentation Index

**Version:** 2.2.0
**Last Updated:** 2025-11-10

Complete documentation for the Enterprise-Grade Multi-Agent Orchestration System with Automatic Guideline Evolution.

---

## 🚀 Quick Start

**New to the project?** Start here:

1. [System Architecture Summary](SYSTEM_ARCHITECTURE_SUMMARY.md) - Complete system overview
2. [Langfuse Setup](LANGFUSE_SETUP.md) - **REQUIRED** - LLM observability
3. [Data Architecture](DATA_ARCHITECTURE.md) - How everything connects

**Ready to build?** Follow this path:

1. Setup environment (`.env.example`)
2. Install dependencies (`requirements.txt`)
3. Run database migrations (`alembic upgrade head`)
4. Start backend (`uvicorn main:app`)
5. Configure agents (Claude, Gemini, Ollama, Copilot)

---

## 📚 Core Documentation

### System Architecture

| Document | Description | Status |
|----------|-------------|--------|
| [System Architecture Summary](SYSTEM_ARCHITECTURE_SUMMARY.md) | 6-Layer orchestration architecture | ✅ Current |
| [Data Architecture](DATA_ARCHITECTURE.md) | Complete data flow and management | ✅ Current v2.1.0 |
| [Backend API Requirements](BACKEND_API_REQUIREMENTS.md) | Complete API reference (130+ pages) | ✅ Current |

### Guidelines Management **NEW!**

| Document | Description | Status |
|----------|-------------|--------|
| [Guidelines Management System](GUIDELINES_MANAGEMENT_SYSTEM.md) | Automatic guideline evolution system | ✅ NEW! Enterprise |

**Key Features:**
- **Error Analysis** - Automatic detection of quality issues
- **Meta-Agent Generation** - AI-powered guideline improvements
- **Version Control** - Git-like versioning for guidelines
- **Distribution Layer** - Flexible, hot-reload deployment
- **Evolution Loop** - Continuous learning and improvement

**Why Guidelines?**
- ✅ Free (vs. $1000+ for model fine-tuning)
- ✅ Instant (vs. days/weeks)
- ✅ Vendor-agnostic
- ✅ Easy to debug
- ✅ Versionable and rollback-capable

### Quality Assessment **NEW!**

| Document | Description | Status |
|----------|-------------|--------|
| [Quality Assessment System](QUALITY_ASSESSMENT_SYSTEM.md) | CodeAssist-inspired Reward/Penalty scoring | ✅ NEW! Production |

**Key Features:**
- **Real-Time Analysis** - Analyzes every agent output during execution
- **Reward/Penalty Scoring** - Quantifies quality from -1.0 to 1.0
- **Pattern Detection** - Identifies success patterns and anti-patterns
- **Multi-Language Support** - Python (AST), JavaScript, TypeScript
- **Security Analysis** - SQL injection, eval/exec, credential detection
- **Evolution Integration** - Feeds directly into Guidelines Management

**Reward Categories:** Best Practices (+0.1 to +0.3), Security (+0.1 to +0.4), Performance (+0.1 to +0.2), Readability (+0.05 to +0.15)

**Penalty Categories:** Anti-Patterns (-0.1 to -0.3), Security Risks (-0.5 to -1.0), Performance Issues (-0.1 to -0.3), Readability Issues (-0.05 to -0.2)

### Agent Integration

| Document | Description | Status |
|----------|-------------|--------|
| [Ollama Enterprise Integration](OLLAMA_ENTERPRISE_INTEGRATION.md) | Complete local AI setup with MCP | ✅ NEW! Enterprise |

**Ollama Features:**
- **ollama-code** - Claude Code-like CLI experience
- **ollmcp** - MCP server integration for skills/subagents
- **Multiple Models** - qwen2.5-coder, deepseek-coder, phi3.5
- **100% Local** - Complete privacy, zero API costs
- **Enterprise Grade** - Production-ready with MCP support

**Supported CLI Tools:**
- `ollama-code` - Terminal-based coding assistant
- `opencode` - Open-source Claude Code alternative
- `ollmcp` - MCP client with multi-server support
- `aider` - Git-aware pair programmer

### Production Requirements

| Document | Description | Status |
|----------|-------------|--------|
| [Langfuse Setup](LANGFUSE_SETUP.md) | **REQUIRED** - LLM observability | ✅ Critical |
| [Schema Migrations](SCHEMA_MIGRATIONS.md) | Database migrations with Alembic | ✅ Production |
| [API Key Encryption](API_KEY_ENCRYPTION.md) | Secure credential management (Fernet) | ✅ Production |
| [Error Handling & Retry](ERROR_HANDLING_RETRY_STRATEGY.md) | Resilience patterns and error handling | ✅ Production |
| [Testing Strategy](TESTING_STRATEGY.md) | Comprehensive testing guide (80% coverage) | ✅ Production |

**Production Checklist:**
- [x] Langfuse configured (NO COMPROMISES!)
- [x] Database migrations (Alembic)
- [x] API keys encrypted (Fernet)
- [x] Error handling (Circuit breakers, retries)
- [x] Test coverage (80% minimum)
- [x] WebSocket reliability (Acknowledgements)

---

## 🎯 By Use Case

### "I want to understand the system"
1. [System Architecture Summary](SYSTEM_ARCHITECTURE_SUMMARY.md)
2. [Data Architecture](DATA_ARCHITECTURE.md)

### "I want to set up Langfuse" **(REQUIRED!)**
1. [Langfuse Setup](LANGFUSE_SETUP.md)

### "I want to add local AI (Ollama)"
1. [Ollama Enterprise Integration](OLLAMA_ENTERPRISE_INTEGRATION.md)

### "I want to improve guidelines automatically"
1. [Guidelines Management System](GUIDELINES_MANAGEMENT_SYSTEM.md)
2. [Quality Assessment System](QUALITY_ASSESSMENT_SYSTEM.md) - Provides feedback for evolution

### "I want to understand code quality analysis"
1. [Quality Assessment System](QUALITY_ASSESSMENT_SYSTEM.md)

### "I want to deploy to production"
1. [Langfuse Setup](LANGFUSE_SETUP.md) ← **Start here!**
2. [Schema Migrations](SCHEMA_MIGRATIONS.md)
3. [API Key Encryption](API_KEY_ENCRYPTION.md)
4. [Error Handling & Retry](ERROR_HANDLING_RETRY_STRATEGY.md)
5. [Testing Strategy](TESTING_STRATEGY.md)
6. [Data Architecture § 11](DATA_ARCHITECTURE.md#11-production-enhancements) - Deployment checklist

### "I want to integrate new APIs"
1. [Backend API Requirements](BACKEND_API_REQUIREMENTS.md)

### "I want to understand the database"
1. [Data Architecture § 1](DATA_ARCHITECTURE.md#1-database-schema) - Complete schema
2. [Schema Migrations](SCHEMA_MIGRATIONS.md) - Managing changes

### "I want to write tests"
1. [Testing Strategy](TESTING_STRATEGY.md)

---

## 🔄 Version History

### v2.2.0 (2025-11-10) - **Current**

**Major Features:**
- ⭐ **Quality Assessment System** - CodeAssist-inspired Reward/Penalty scoring
- ✨ **Guidelines Management System** - Automatic guideline evolution
- ✨ **Ollama Enterprise Integration** - Complete local AI with MCP
- ✨ **Production Enhancements** - 6 critical systems documented

**New Documents:**
- `QUALITY_ASSESSMENT_SYSTEM.md` - Real-time code quality analysis
- `GUIDELINES_MANAGEMENT_SYSTEM.md` - Automated fine-tuning via guidelines
- `OLLAMA_ENTERPRISE_INTEGRATION.md` - Enterprise-grade local AI
- `LANGFUSE_SETUP.md` - LLM observability (REQUIRED)
- `SCHEMA_MIGRATIONS.md` - Database migrations with Alembic
- `API_KEY_ENCRYPTION.md` - Secure credential management
- `ERROR_HANDLING_RETRY_STRATEGY.md` - Resilience patterns
- `TESTING_STRATEGY.md` - Comprehensive testing guide

**New Implementation:**
- `dashboard/backend/analysis/quality_analyzer.py` - Complete quality analyzer
- `dashboard/backend/analysis/feedback_aggregator.py` - Feedback aggregation
- `CHANGELOG.md` - Version history tracking

### v2.1.0 (2025-11-09)

**Focus:** Production infrastructure and documentation

**Added:**
- Initial Guidelines Management System design
- Ollama integration planning
- Production enhancement documentation

### v2.0.0 (2025-11-08)

**Focus:** Initial multi-agent orchestration release

**Core Features:**
- Multi-agent orchestration (Claude, Gemini, Ollama, Copilot)
- Intelligent agent routing
- Cost optimization strategies
- WebSocket real-time updates

---

**Maintained by:** LEEI1337
**License:** MIT
**Last Updated:** 2025-11-10
