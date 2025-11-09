"""
Project Templates and Guideline System
Predefined templates for common project types with best-practice guidelines
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from enum import Enum

router = APIRouter()

class ProjectType(str, Enum):
    """Supported project types"""
    WEB_APP = "web_app"
    DATA_SCIENCE = "data_science"
    MICROSERVICES = "microservices"
    MOBILE_APP = "mobile_app"
    CLI_TOOL = "cli_tool"
    CUSTOM = "custom"

class TemplateResponse(BaseModel):
    """Project template"""
    id: str
    name: str
    type: ProjectType
    description: str
    icon: str
    guidelines: List[str]
    prerequisites: List[str]
    tech_stack: List[str]
    estimated_duration: str
    complexity: str
    config_preset: Dict

# Predefined Templates
TEMPLATES = {
    "production_web_app": TemplateResponse(
        id="production_web_app",
        name="Production-Ready Web Application",
        type=ProjectType.WEB_APP,
        description="Full-stack web application with modern best practices, testing, CI/CD, and monitoring",
        icon="🌐",
        guidelines=[
            "# Architecture Guidelines\n\n## Frontend\n- Use React 18+ with TypeScript\n- Implement proper state management (Zustand or Redux Toolkit)\n- Follow component-driven development with Storybook\n- Use TailwindCSS for styling with design system\n- Implement lazy loading and code splitting\n\n## Backend\n- Use FastAPI or Next.js API routes\n- Implement proper authentication (JWT + refresh tokens)\n- Use PostgreSQL with migrations (Alembic/Prisma)\n- Implement request validation with Pydantic/Zod\n- Add rate limiting and CORS properly\n\n## Testing\n- Unit tests: 80%+ coverage (Jest/Pytest)\n- Integration tests for API endpoints\n- E2E tests for critical paths (Playwright)\n- Component tests with React Testing Library\n\n## Security\n- Never store secrets in code\n- Use environment variables\n- Implement HTTPS only\n- Add CSRF protection\n- Sanitize all user inputs\n- Use prepared statements for SQL\n\n## Performance\n- Optimize bundle size < 200KB gzipped\n- Implement caching strategies\n- Use CDN for static assets\n- Optimize images (WebP, lazy loading)\n- Implement database indexing\n\n## Deployment\n- Use Docker for consistent environments\n- Implement health checks\n- Use GitHub Actions for CI/CD\n- Deploy to Vercel/Railway/AWS\n- Set up monitoring (Sentry, Grafana)",
        ],
        prerequisites=[
            "Node.js 20+ installed",
            "Python 3.11+ (if using FastAPI backend)",
            "PostgreSQL 15+ database",
            "Docker Desktop",
            "Git configured",
            "Environment variables configured (.env file)",
        ],
        tech_stack=[
            "React 18",
            "TypeScript 5",
            "TailwindCSS 4",
            "FastAPI / Next.js",
            "PostgreSQL",
            "Redis (caching)",
            "Docker",
            "GitHub Actions",
        ],
        estimated_duration="2-4 weeks",
        complexity="Medium-High",
        config_preset={
            "priority": "balanced",
            "timeframe": 120,
            "risk_tolerance": 0.3,
            "deployment_target": ["linux", "docker"],
            "ml_config": {
                "adaptive_iterations": True,
                "use_latent_reasoning": True,
                "smart_switching": True,
                "deep_supervision": True,
            },
        },
    ),
    "data_science_pipeline": TemplateResponse(
        id="data_science_pipeline",
        name="Data Science Pipeline",
        type=ProjectType.DATA_SCIENCE,
        description="Production-grade data science pipeline with ML models, feature engineering, and deployment",
        icon="📊",
        guidelines=[
            "# Data Science Pipeline Guidelines\n\n## Data Processing\n- Use Pandas/Polars for data manipulation\n- Implement proper data validation\n- Handle missing data systematically\n- Document data transformations\n- Version control datasets (DVC)\n\n## Feature Engineering\n- Create feature engineering pipeline\n- Document feature importance\n- Handle categorical variables properly\n- Scale numerical features\n- Create time-based features if needed\n\n## Model Development\n- Try multiple algorithms\n- Use cross-validation (k-fold)\n- Track experiments with MLflow/Wandb\n- Optimize hyperparameters systematically\n- Document model assumptions\n\n## Model Evaluation\n- Use appropriate metrics for problem type\n- Test on held-out test set\n- Check for data leakage\n- Analyze error patterns\n- Create confusion matrix/ROC curves\n\n## Deployment\n- Serialize models properly (pickle/joblib)\n- Create FastAPI endpoint for predictions\n- Implement input validation\n- Add monitoring for model drift\n- Set up A/B testing framework\n\n## Reproducibility\n- Pin all dependencies\n- Set random seeds\n- Document hardware used\n- Save training configurations\n- Use Docker for consistency",
        ],
        prerequisites=[
            "Python 3.11+ with scientific stack",
            "Jupyter Lab / VSCode with extensions",
            "Dataset prepared and cleaned",
            "GPU access (optional, for deep learning)",
            "MLflow or Weights & Biases account",
        ],
        tech_stack=[
            "Python 3.11",
            "Pandas / Polars",
            "Scikit-learn",
            "XGBoost / LightGBM",
            "TensorFlow / PyTorch (optional)",
            "MLflow / Weights & Biases",
            "FastAPI (for serving)",
            "Docker",
        ],
        estimated_duration="3-6 weeks",
        complexity="High",
        config_preset={
            "priority": "quality",
            "timeframe": 180,
            "risk_tolerance": 0.2,
            "deployment_target": ["linux"],
            "ml_config": {
                "adaptive_iterations": True,
                "use_latent_reasoning": True,
                "smart_switching": True,
                "deep_supervision": True,
                "parallel_evaluation": True,
            },
        },
    ),
    "microservices_api": TemplateResponse(
        id="microservices_api",
        name="Microservices API Platform",
        type=ProjectType.MICROSERVICES,
        description="Scalable microservices architecture with API gateway, service mesh, and observability",
        icon="🔧",
        guidelines=[
            "# Microservices Architecture Guidelines\n\n## Service Design\n- Follow single responsibility principle\n- Design for failure (circuit breakers)\n- Implement proper service boundaries\n- Use asynchronous communication where possible\n- Version your APIs (/v1/, /v2/)\n\n## Communication\n- REST APIs with OpenAPI/Swagger docs\n- Use gRPC for inter-service communication\n- Implement message queues (RabbitMQ/Kafka)\n- Add retry logic with exponential backoff\n- Use service discovery (Consul/Kubernetes)\n\n## Data Management\n- Database per service pattern\n- Implement event sourcing if needed\n- Use distributed transactions carefully (SAGA)\n- Cache frequently accessed data (Redis)\n- Implement data replication strategy\n\n## Security\n- Implement OAuth2/JWT authentication\n- Use API gateway for central auth\n- Service-to-service authentication (mTLS)\n- Implement rate limiting per service\n- Audit logging for all operations\n\n## Observability\n- Distributed tracing (Jaeger/Zipkin)\n- Centralized logging (ELK stack)\n- Metrics collection (Prometheus)\n- Health checks for each service\n- Create service dependency map\n\n## Deployment\n- Containerize all services (Docker)\n- Orchestrate with Kubernetes\n- Implement rolling deployments\n- Use Helm charts for configuration\n- Set up auto-scaling\n\n## Testing\n- Unit tests per service\n- Contract testing between services\n- Integration tests for workflows\n- Chaos engineering (simulate failures)\n- Load testing entire platform",
        ],
        prerequisites=[
            "Docker and Kubernetes knowledge",
            "Multiple services designed",
            "Message queue system ready",
            "Monitoring infrastructure",
            "CI/CD pipeline configured",
        ],
        tech_stack=[
            "FastAPI / Go / Node.js",
            "PostgreSQL / MongoDB",
            "Redis",
            "RabbitMQ / Kafka",
            "Docker & Kubernetes",
            "Nginx / Traefik (API Gateway)",
            "Prometheus & Grafana",
            "Jaeger (tracing)",
        ],
        estimated_duration="6-12 weeks",
        complexity="Very High",
        config_preset={
            "priority": "performance",
            "timeframe": 90,
            "risk_tolerance": 0.4,
            "deployment_target": ["kubernetes"],
            "ml_config": {
                "adaptive_iterations": True,
                "use_latent_reasoning": False,
                "smart_switching": True,
                "deep_supervision": False,
                "parallel_evaluation": True,
            },
        },
    ),
}

# Endpoints

@router.get("/")
async def list_templates():
    """
    List all available project templates.
    """
    return {
        "templates": [
            {
                "id": t.id,
                "name": t.name,
                "description": t.description,
                "icon": t.icon
            }
            for t in TEMPLATES.values()
        ]
    }

@router.get("/{template_id}")
async def get_template(template_id: str):
    """
    Get details of a specific template.
    """
    if template_id not in TEMPLATES:
        raise HTTPException(status_code=404, detail="Template not found")

    t = TEMPLATES[template_id]
    return {
        "name": t.name,
        "description": t.description,
        "guidelines": t.guidelines,
        "prerequisites": t.prerequisites,
        "tech_stack": t.tech_stack,
        "estimated_duration": t.estimated_duration,
        "complexity": t.complexity
    }

@router.post("/{template_id}/apply")
async def apply_template(template_id: str, project_name: str, customizations: Optional[Dict] = None):
    """
    Apply a template to create a new project with preset configuration.
    """
    if template_id not in TEMPLATES:
        raise HTTPException(status_code=404, detail="Template not found")

    template = TEMPLATES[template_id]

    # Merge template preset with customizations
    config = template.config_preset.copy()
    if customizations:
        config.update(customizations)

    return {
        "project_name": project_name,
        "template_id": template_id,
        "template_name": template.name,
        "applied_config": config,
        "guidelines": template.guidelines,
        "prerequisites": template.prerequisites,
        "next_steps": [
            f"Review the {len(template.guidelines)} guideline sections",
            f"Ensure all {len(template.prerequisites)} prerequisites are met",
            "Customize the configuration if needed",
            "Start development with the preset configuration",
        ],
    }

@router.get("/guidelines/best-practices")
async def get_best_practices(category: Optional[str] = None):
    """
    Get general best practices and guidelines.
    """
    best_practices = {
        "security": [
            "Never commit secrets to version control",
            "Use environment variables for sensitive data",
            "Implement proper authentication and authorization",
            "Validate and sanitize all user inputs",
            "Use HTTPS for all communications",
            "Implement rate limiting to prevent abuse",
            "Keep dependencies updated",
            "Use security headers (CSP, HSTS, etc.)",
        ],
        "testing": [
            "Aim for 80%+ code coverage",
            "Write tests before fixing bugs (TDD)",
            "Test edge cases and error conditions",
            "Use integration tests for critical paths",
            "Implement E2E tests for user flows",
            "Run tests in CI/CD pipeline",
            "Keep tests fast and independent",
            "Use test fixtures and mocks appropriately",
        ],
        "performance": [
            "Optimize database queries (use indexes)",
            "Implement caching strategies",
            "Use lazy loading for resources",
            "Minimize bundle sizes",
            "Optimize images and assets",
            "Use CDN for static content",
            "Implement pagination for large datasets",
            "Profile and monitor performance regularly",
        ],
        "code_quality": [
            "Follow consistent code style (use linters)",
            "Write self-documenting code",
            "Keep functions small and focused",
            "Use meaningful variable names",
            "Comment complex logic",
            "Refactor regularly",
            "Follow DRY principle",
            "Conduct code reviews",
        ],
    }

    if category:
        if category not in best_practices:
            raise HTTPException(status_code=404, detail="Category not found")
        return {category: best_practices[category]}

    return best_practices
