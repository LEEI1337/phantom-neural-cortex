# 🏗️ Complete System Architecture

**AI Development Orchestrator - Full Layer Stack (0-5)**

---

## 📊 Visual Overview

```mermaid
graph TB
    subgraph LAYER5["⚡ LAYER 5: FEEDBACK LOOP (UltraThink)"]
        direction TB
        H[H-Module: Quality Evaluator]
        L[L-Module: Refinement Agent]
        LP[Loop Prevention: 7 Strategies]
        QV[Q-Learning ACT: Adaptive Halting]

        H --> QV
        L --> H
        LP --> H

        style H fill:#ff6b6b
        style L fill:#ff6b6b
        style LP fill:#ff6b6b
        style QV fill:#ff6b6b
    end

    subgraph LAYER4["🐦 LAYER 4: LAZY BIRD (Automation)"]
        direction TB
        IW[Issue Watcher: GitHub Polling]
        PR[Project Manager: Slots A/B/C]
        AR[Agent Router: Cost-Optimized Selection]

        IW --> AR
        AR --> PR

        style IW fill:#feca57
        style PR fill:#feca57
        style AR fill:#feca57
    end

    subgraph LAYER3["🚀 LAYER 3: ROVER (Orchestration)"]
        direction TB
        RO[Rover Orchestrator: Parallel Tasks]
        GW[Git Worktrees: Isolation]
        DC[Docker Containers: Sandboxing]
        TM[Test Manager: Auto-validation]

        RO --> GW
        RO --> DC
        RO --> TM

        style RO fill:#48dbfb
        style GW fill:#48dbfb
        style DC fill:#48dbfb
        style TM fill:#48dbfb
    end

    subgraph LAYER2["🤖 LAYER 2: AI CLI TOOLS (Isolated)"]
        direction LR
        C[Claude: Expert<br/>$20/mo<br/>10-20%]
        G[Gemini: Worker<br/>FREE!<br/>60-70%]
        CP[Copilot: Specialist<br/>$0-10/mo<br/>20-30%]

        style C fill:#9b59b6
        style G fill:#3498db
        style CP fill:#e74c3c
    end

    subgraph LAYER1["🔧 LAYER 1: MCP SERVERS (18 Tools)"]
        direction TB
        FS[filesystem]
        GH[github]
        BR[brave-search]
        ST[sequential-thinking]
        PL[playwright]
        DB[sqlite/postgres]

        style FS fill:#2ecc71
        style GH fill:#2ecc71
        style BR fill:#2ecc71
        style ST fill:#2ecc71
        style PL fill:#2ecc71
        style DB fill:#2ecc71
    end

    subgraph LAYER0["⭐ LAYER 0: UNIVERSAL STANDARDS"]
        direction TB
        PS[Project Structure]
        NC[Naming Conventions]
        CQ[Code Quality & Security]
        TF[Testing Fundamentals]

        style PS fill:#95afc0
        style NC fill:#95afc0
        style CQ fill:#95afc0
        style TF fill:#95afc0
    end

    LAYER5 --> LAYER4
    LAYER4 --> LAYER3
    LAYER3 --> LAYER2
    LAYER2 --> LAYER1
    LAYER1 --> LAYER0

    L -.Feedback.-> LAYER4
    H -.Halt Decision.-> LAYER3
    AR -.Agent Selection.-> LAYER2
    RO -.Tool Calls.-> LAYER1

    classDef layer5 fill:#ff6b6b,stroke:#c92a2a,stroke-width:3px
    classDef layer4 fill:#feca57,stroke:#e67e22,stroke-width:3px
    classDef layer3 fill:#48dbfb,stroke:#0984e3,stroke-width:3px
    classDef layer2 fill:#a29bfe,stroke:#6c5ce7,stroke-width:3px
    classDef layer1 fill:#2ecc71,stroke:#27ae60,stroke-width:3px
    classDef layer0 fill:#95afc0,stroke:#535c68,stroke-width:3px
```

---

## 🔄 Feedback Loop Flow (Layer 5)

```mermaid
sequenceDiagram
    participant User
    participant H as H-Module<br/>(Quality Evaluator)
    participant L as L-Module<br/>(Refinement Agent)
    participant LP as Loop Prevention

    User->>H: Initial implementation

    loop Refinement Iterations (max 5)
        H->>H: Evaluate Quality Metrics
        H->>H: Compute Q(HALT) vs Q(CONTINUE)

        alt Critical Issues
            H->>H: Apply Penalties:<br/>- Security: -10%/vuln<br/>- Tests Failing (3+): -50%!<br/>- Type Errors: -5%/error<br/>- Complexity: -2%/unit
        end

        H->>LP: Check abort conditions

        alt Should Abort
            LP-->>User: ABORT (reason: cost/time/stagnation)
        else Should Halt
            H-->>User: HALT (Q(HALT) > Q(CONTINUE))
        else Should Continue
            H->>L: Generate prioritized feedback
            L->>L: Refine implementation
            L->>H: New implementation
        end
    end

    H-->>User: Final result + metrics
```

---

## 🐦 Lazy Bird Workflow (Layer 4)

```mermaid
flowchart TD
    Start([GitHub Issue Created]) --> Check{Has 'lazy-bird' label?}

    Check -->|No| Ignore[Ignore]
    Check -->|Yes| Labels{Check Labels}

    Labels -->|security,<br/>architecture,<br/>complex| AgentC[Select: Claude<br/>Expert<br/>Cost: ~$1]
    Labels -->|documentation,<br/>bulk-refactor,<br/>large-scale| AgentG[Select: Gemini<br/>Worker<br/>Cost: $0 FREE!]
    Labels -->|github-workflow,<br/>quick-fix,<br/>pr| AgentCP[Select: Copilot<br/>Specialist<br/>Cost: $0-0.10]
    Labels -->|No specific| AgentG

    AgentC --> Slot{Find Free Slot}
    AgentG --> Slot
    AgentCP --> Slot

    Slot -->|Projekt-A| SlotA[Use Slot A]
    Slot -->|Projekt-B| SlotB[Use Slot B]
    Slot -->|Projekt-C| SlotC[Use Slot C]
    Slot -->|All busy| Queue[Add to Queue]

    SlotA --> Rover[Create Rover Task]
    SlotB --> Rover
    SlotC --> Rover

    Rover --> Worktree[Create Git Worktree]
    Worktree --> Docker[Spin up Docker Container]
    Docker --> Implement[AI implements solution]

    Implement --> Tests{Run Tests}
    Tests -->|Pass| FeedbackLoop[Enter Feedback Loop]
    Tests -->|Fail| Refine[Refine & Re-test]
    Refine --> Tests

    FeedbackLoop --> Quality{Quality >= 75%?}
    Quality -->|Yes| PR[Create Pull Request]
    Quality -->|No & Iter < 5| Iterate[L-Module Refines]
    Quality -->|No & Iter >= 5| Abort[Abort with Report]

    Iterate --> Tests

    PR --> Comment[Comment on Issue:<br/>PR #123 ready!]
    Abort --> Comment2[Comment on Issue:<br/>Failed - see logs]

    Comment --> Cleanup[Cleanup: Docker + Worktree]
    Comment2 --> Cleanup

    Cleanup --> End([Done])

    style AgentC fill:#9b59b6
    style AgentG fill:#3498db
    style AgentCP fill:#e74c3c
    style FeedbackLoop fill:#ff6b6b
    style PR fill:#2ecc71
```

---

## 🚀 Rover Parallel Execution (Layer 3)

```mermaid
graph LR
    subgraph Main["Main Repository"]
        Master[master branch]
    end

    subgraph Parallel["Parallel Tasks via Rover"]
        Task1[Task 1: Design<br/>Agent: Claude<br/>Worktree: design-feature]
        Task2[Task 2: Implement<br/>Agent: Gemini<br/>Worktree: impl-feature]
        Task3[Task 3: Tests<br/>Agent: Gemini<br/>Worktree: test-feature]
        Task4[Task 4: GitHub<br/>Agent: Copilot<br/>Worktree: gh-workflow]
    end

    Master -.->|git worktree add| Task1
    Master -.->|git worktree add| Task2
    Master -.->|git worktree add| Task3
    Master -.->|git worktree add| Task4

    subgraph Docker1["Docker Container 1"]
        T1[Claude: Security Review]
    end

    subgraph Docker2["Docker Container 2"]
        T2[Gemini: Bulk Refactor]
    end

    subgraph Docker3["Docker Container 3"]
        T3[Gemini: E2E Tests]
    end

    subgraph Docker4["Docker Container 4"]
        T4[Copilot: PR Template]
    end

    Task1 --> T1
    Task2 --> T2
    Task3 --> T3
    Task4 --> T4

    T1 -->|Tests Pass| Merge1[Merge to master]
    T2 -->|Tests Pass| Merge2[Merge to master]
    T3 -->|Tests Pass| Merge3[Merge to master]
    T4 -->|Tests Pass| Merge4[Merge to master]

    Merge1 --> Master
    Merge2 --> Master
    Merge3 --> Master
    Merge4 --> Master
```

---

## 🤖 AI Agent Selection Logic (Layer 2)

```mermaid
flowchart TD
    Start([Task Received]) --> TaskType{Task Type?}

    TaskType -->|Security Audit| Security[Check: Vulnerabilities?<br/>Code Injection?<br/>Auth Patterns?]
    TaskType -->|Architecture| Arch[Check: System Design?<br/>Scalability?<br/>Complex Logic?]
    TaskType -->|Bulk Operations| Bulk[Check: Large codebase?<br/>Docs generation?<br/>Repetitive?]
    TaskType -->|GitHub Ops| GitHub[Check: PR creation?<br/>Issue management?<br/>Workflows?]
    TaskType -->|Quick Fix| Quick[Check: Small scope?<br/>Low complexity?<br/>Fast turnaround?]

    Security --> Claude1[Use: Claude<br/>Reason: Expert security<br/>Cost: ~$0.50]
    Arch --> Claude2[Use: Claude<br/>Reason: Architecture expertise<br/>Cost: ~$0.50]

    Bulk --> Context{Context Size?}
    Context -->|> 100k tokens| Gemini1[Use: Gemini<br/>Reason: 2M context<br/>Cost: $0 FREE!]
    Context -->|< 100k tokens| Gemini2[Use: Gemini<br/>Reason: Cost-optimized<br/>Cost: $0 FREE!]

    GitHub --> Copilot1[Use: Copilot<br/>Reason: GitHub native<br/>Cost: $0-0.10]
    Quick --> Copilot2[Use: Copilot<br/>Reason: Fast iteration<br/>Cost: $0-0.10]

    Claude1 --> Budget{Within Budget?}
    Claude2 --> Budget

    Budget -->|Yes| Execute[Execute Task]
    Budget -->|No| Fallback[Fallback: Gemini<br/>Add warning]

    Gemini1 --> RateLimit{Rate Limit?}
    Gemini2 --> RateLimit

    RateLimit -->|< 1000/day| Execute
    RateLimit -->|>= 1000/day| Wait[Wait or Use Copilot]

    Copilot1 --> Execute
    Copilot2 --> Execute
    Fallback --> Execute
    Wait --> Execute

    Execute --> End([Task Complete])

    style Claude1 fill:#9b59b6
    style Claude2 fill:#9b59b6
    style Gemini1 fill:#3498db
    style Gemini2 fill:#3498db
    style Copilot1 fill:#e74c3c
    style Copilot2 fill:#e74c3c
```

---

## 📊 Cost Optimization Strategy

```mermaid
pie title Monthly Task Distribution (500 tasks)
    "Gemini (FREE)" : 350
    "Copilot (FREE/$10)" : 100
    "Claude ($20)" : 50
```

**Target Breakdown:**
- **Gemini:** 60-70% (300-350 tasks) = **$0** ✨
- **Copilot:** 20-30% (100-150 tasks) = **$0-10**
- **Claude:** 10-20% (50-100 tasks) = **$20** (Pro subscription)

**Total: $20-30/month** for ~500 tasks!

---

## 🔧 MCP Server Integration (Layer 1)

```mermaid
graph TB
    subgraph AI["AI Agents (Layer 2)"]
        C[Claude]
        G[Gemini]
        CP[Copilot]
    end

    subgraph MCP["MCP Servers (Layer 1)"]
        direction TB

        subgraph Core["Core Servers"]
            FS[filesystem<br/>File ops]
            MEM[memory<br/>Knowledge persistence]
            GH[github<br/>GitHub integration]
        end

        subgraph Search["Search & Web"]
            BR[brave-search<br/>Web search]
            PERP[perplexity<br/>AI search]
        end

        subgraph Development["Development Tools"]
            ST[sequential-thinking<br/>Reasoning]
            PL[playwright<br/>Browser automation]
            DOCS[docs<br/>Documentation]
        end

        subgraph Data["Data & Storage"]
            SQL[sqlite<br/>Database]
            PG[postgres<br/>PostgreSQL]
        end

        subgraph Testing["Testing & Debug"]
            POST[postmancer<br/>API testing]
            INSP[inspector<br/>Debugging]
        end

        subgraph Utilities["Utilities"]
            TIME[time<br/>Timezone]
            RVMCP[rover-mcp<br/>Rover integration]
        end
    end

    C --> Core
    C --> Search
    C --> Development
    C --> Data
    C --> Testing
    C --> Utilities

    G --> Core
    G --> Search
    G --> Development
    G --> Data

    CP --> Core
    CP --> GH
    CP --> Development

    style C fill:#9b59b6
    style G fill:#3498db
    style CP fill:#e74c3c
```

---

## 🎯 Complete Request Flow

```mermaid
sequenceDiagram
    participant U as User
    participant GH as GitHub
    participant LB as Lazy Bird<br/>(Layer 4)
    participant R as Rover<br/>(Layer 3)
    participant AI as AI Agent<br/>(Layer 2)
    participant MCP as MCP Servers<br/>(Layer 1)
    participant FL as Feedback Loop<br/>(Layer 5)

    U->>GH: Create issue with label
    GH-->>LB: Webhook notification

    LB->>LB: Parse issue
    LB->>LB: Select optimal agent
    LB->>R: Create task

    R->>R: Create git worktree
    R->>R: Spin up Docker container
    R->>AI: Execute task

    AI->>MCP: Request tools (filesystem, github, etc.)
    MCP-->>AI: Tool responses

    AI->>AI: Generate implementation
    AI-->>R: Implementation complete

    R->>R: Run tests

    alt Tests Pass
        R->>FL: Send for quality check
        FL->>FL: Evaluate metrics
        FL->>FL: Compute Q(HALT) vs Q(CONTINUE)

        alt Quality >= 75%
            FL-->>R: Approved
            R->>GH: Create Pull Request
            GH-->>U: PR notification
        else Quality < 75% AND Iterations < 5
            FL->>AI: Refine with feedback
            AI->>MCP: Request tools
            MCP-->>AI: Tool responses
            AI-->>FL: Refined implementation
            FL->>FL: Re-evaluate (loop)
        else Quality < 75% AND Iterations >= 5
            FL-->>R: Abort (max iterations)
            R->>GH: Comment: Quality insufficient
            GH-->>U: Notification
        end
    else Tests Fail
        R->>AI: Request fix
        AI->>MCP: Request tools
        MCP-->>AI: Tool responses
        AI-->>R: Fixed implementation
        R->>R: Re-run tests
    end

    R->>R: Cleanup Docker & worktree
```

---

## 📈 Performance Metrics

| Metric | Value | Notes |
|--------|-------|-------|
| **Setup Time** | ~45 min | One-time initial setup |
| **MCP Start** | ~10-15s | Server initialization |
| **Agent Response** | <3s | Average task pickup time |
| **Parallel Speedup** | 3-5x | vs. sequential execution |
| **Context Window** | Up to 2M | Gemini's massive context |
| **Daily Free Requests** | 1000 | Gemini API limit |
| **Monthly Cost** | $20-30 | With strategic free tier usage |
| **Q-Value Computation** | 0.0001ms | Feedback loop overhead |
| **Feedback Generation** | 0.0005ms | Per iteration |

---

## 🔒 Security & Isolation

```mermaid
graph TB
    subgraph Isolation["Isolation Layers"]
        direction TB

        W1[Worktree 1<br/>design-feature]
        W2[Worktree 2<br/>impl-feature]
        W3[Worktree 3<br/>test-feature]

        D1[Docker Container 1<br/>Network: isolated<br/>Volume: read-only]
        D2[Docker Container 2<br/>Network: isolated<br/>Volume: read-only]
        D3[Docker Container 3<br/>Network: isolated<br/>Volume: read-only]

        W1 --> D1
        W2 --> D2
        W3 --> D3
    end

    subgraph Secrets["Secret Management"]
        ENV[.env files<br/>Git-ignored]
        API[API keys<br/>Environment vars]
        CREDS[OAuth credentials<br/>Encrypted storage]
    end

    subgraph Validation["Validation Gates"]
        PRE[Pre-commit hooks<br/>Code quality]
        TESTS[Test suite<br/>100% must pass]
        SEC[Security scan<br/>Bandit/Semgrep]
    end

    D1 --> Validation
    D2 --> Validation
    D3 --> Validation

    Validation --> Secrets

    style D1 fill:#e74c3c
    style D2 fill:#e74c3c
    style D3 fill:#e74c3c
    style SEC fill:#c0392b
```

---

## 📚 Documentation Structure

```
docs/
├── INDEX.md                          # Main documentation index
│
├── Quick Start (5 minutes)
│   ├── QUICKSTART-EN.md              # English setup guide
│   └── QUICKSTART-DE.md              # German setup guide
│
├── Architecture
│   ├── ARCHITECTURE-EN.md            # English architecture overview
│   ├── ARCHITECTURE-DE.md            # German architecture overview
│   ├── SYSTEM-ARCHITECTURE.md        # This file (visual diagrams)
│   └── architecture/
│       ├── ARCHITECTURE.md           # Detailed system design
│       ├── AI-CAPABILITY-MATRIX.md   # AI comparison matrix
│       └── CLAUDE-VS-COPILOT.md      # Detailed AI comparison
│
├── Lazy Bird (Layer 4 Automation)
│   ├── LAZY-BIRD-ARCHITECTURE.md     # Layer 0-4 design
│   ├── LAZY-BIRD-SETUP-EN.md         # English setup guide
│   ├── LAZY-BIRD-SETUP-DE.md         # German setup guide
│   └── LAZY-BIRD-SUMMARY.md          # Quick reference
│
├── Feedback Loop (Layer 5 UltraThink)
│   └── feedback-loop/
│       ├── FEEDBACK-LOOP-DESIGN.md   # System design
│       ├── FEEDBACK-LOOP-ANALYSIS.md # Critical analysis
│       └── OPTIMIZATION-SUMMARY.md   # Phase 1 improvements
│
├── Guides
│   ├── HOW-TO-CREATE-PROJECT.md      # Project creation guide
│   └── guides/
│       ├── BRANCH_PROTECTION.md      # GitHub branch protection
│       ├── ROVER-GUIDE.md            # Rover usage guide
│       └── ROVER-AI-SELECTOR.md      # AI selection logic
│
├── Setup & Verification
│   └── setup/
│       ├── SETUP-GUIDE.md            # Detailed setup steps
│       ├── SETUP-VERIFICATION.md     # Verification checklist
│       └── OPENHANDS-SETUP.md        # OpenHands setup
│
└── Reference
    └── MCP-SERVERS.md                # All 18 MCP servers
```

---

## 🎓 Next Steps

1. **Getting Started:** [QUICKSTART-EN.md](QUICKSTART-EN.md) or [QUICKSTART-DE.md](QUICKSTART-DE.md)
2. **Understand Architecture:** [ARCHITECTURE-EN.md](ARCHITECTURE-EN.md) or [ARCHITECTURE-DE.md](ARCHITECTURE-DE.md)
3. **Setup Lazy Bird:** [LAZY-BIRD-SETUP-EN.md](LAZY-BIRD-SETUP-EN.md)
4. **Explore Feedback Loop:** [feedback-loop/FEEDBACK-LOOP-DESIGN.md](feedback-loop/FEEDBACK-LOOP-DESIGN.md)
5. **Browse All Docs:** [INDEX.md](INDEX.md)

---

**Made with ❤️ by developers, for developers in Austria 🇦🇹**
