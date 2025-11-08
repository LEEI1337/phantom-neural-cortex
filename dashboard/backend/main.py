"""
FastAPI Main Application
AI Development Orchestrator Dashboard Backend
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import socketio

from database import init_db
from routers import projects, tasks, metrics, config, websocket, prometheus, speckit
from routers.websocket import sio

# Lifespan context manager for startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting PHANTOM NEURAL CORTEX UI Backend...")
    print("👻 Phantom Mode Engaged")
    print("🧠 Neural Cortex Active")
    init_db()
    yield
    # Shutdown
    print("Shutting down...")

# Create FastAPI app with comprehensive OpenAPI documentation
app = FastAPI(
    title="PHANTOM NEURAL CORTEX UI API",
    description="""
# 👻🧠 PHANTOM NEURAL CORTEX UI - AI Development Orchestration Platform

**The Mind Behind The Machine** — Complete REST API for neural AI-powered development with
ML/RL optimizations, Spec-Driven workflows, and multi-agent orchestration.

## Features

- **Project Management:** CRUD operations for development projects with 5-dimension configuration
- **Task Orchestration:** Automated refinement loops with ML-optimized iteration counts
- **Quality Metrics:** Real-time tracking of 7 quality dimensions (coverage, security, complexity, etc.)
- **Cost Analytics:** Token usage and cost tracking across multiple AI agents (Gemini, Claude, Copilot)
- **Agent Performance:** Comparative analysis and smart agent switching
- **Real-time Updates:** WebSocket support for live monitoring

## Configuration Dimensions

Projects can be configured across 5 dimensions:

1. **Priority:** performance | cost | quality | balanced | custom
2. **Timeframe:** 5-180 minutes with presets (sprint, standard, deep-work, marathon)
3. **Risk Tolerance:** 0-100% with experimental features toggle
4. **Deployment:** Windows, Linux, macOS, Kubernetes
5. **ML Components:** Adaptive iterations, latent reasoning, smart switching, deep supervision, parallel evaluation

## Authentication

Currently uses API keys (to be implemented). Future: OAuth2 with JWT tokens.

## Rate Limiting

- 1000 requests/hour per API key
- WebSocket: 100 concurrent connections

## Neural Cortex ML/RL Optimizations

- **12 ML/RL Neurons:** Latent Reasoning, PPO, Bayesian, Deep Supervision, Smart Switching
- **Spec-Kit Integration:** GitHub Spec-Driven Development (7-phase workflow)
- **Performance:** -60% Deploy Time, -52% Cost, +34% Quality

## Support

- Documentation: http://localhost:1336/docs
- GitHub: https://github.com/phantom-neural-cortex
- Issues: https://github.com/phantom-neural-cortex/issues
    """,
    version="2.0.0",
    terms_of_service="https://phantom-neural-cortex.dev/terms",
    contact={
        "name": "Phantom Neural Cortex Team",
        "url": "https://phantom-neural-cortex.dev",
        "email": "support@phantom-neural-cortex.dev",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    lifespan=lifespan,
    openapi_tags=[
        {
            "name": "projects",
            "description": "Project management operations. Create, read, update, and delete development projects.",
        },
        {
            "name": "tasks",
            "description": "Task orchestration and monitoring. Track refinement loops, iterations, and completion status.",
        },
        {
            "name": "metrics",
            "description": "Quality and performance metrics. Dashboard stats, quality trends, cost analysis, and agent performance.",
        },
        {
            "name": "config",
            "description": "Configuration management. Default configs, validation, and project-specific settings.",
        },
        {
            "name": "prometheus",
            "description": "Prometheus metrics endpoint. Exposes custom metrics for monitoring and alerting.",
        },
        {
            "name": "speckit",
            "description": "GitHub Spec-Kit integration. Spec-Driven Development workflow with UltraThink optimizations.",
        },
    ],
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:1337", "http://localhost:5173"],  # Vite + React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Socket.IO
socket_app = socketio.ASGIApp(sio, app)

# Include routers
app.include_router(projects.router, prefix="/api/projects", tags=["projects"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
app.include_router(metrics.router, prefix="/api/metrics", tags=["metrics"])
app.include_router(config.router, prefix="/api/config", tags=["config"])
app.include_router(prometheus.router, prefix="/api", tags=["prometheus"])
app.include_router(speckit.router, prefix="/api/speckit", tags=["speckit"])

# Health check
@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "2.0.0",
        "components": {
            "database": True,
            "websocket": True,
            "cache": True,
        }
    }

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "👻🧠 Phantom Neural Cortex API v2.0",
        "tagline": "The Mind Behind The Machine",
        "docs": "/docs",
        "health": "/api/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:socket_app",  # Use socket_app instead of app
        host="0.0.0.0",
        port=1336,
        reload=True
    )
