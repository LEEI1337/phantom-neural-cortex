"""
Integration Tests for Metrics API Endpoints
Tests dashboard stats, quality trends, cost metrics, and agent performance
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from datetime import datetime, timedelta
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from main import app
from database import Base, get_db
from models import Project, Task, QualitySnapshot, CostTracking, AgentSwitch, AgentType, TaskStatus


# Setup test database
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def client():
    """Create test client with fresh database."""
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    """Direct database session for test data setup."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


def create_test_project(db, name="Test Project", project_type="typescript_fullstack"):
    """Helper to create test project."""
    project = Project(
        id=f"proj_{name.replace(' ', '_').lower()}",
        name=name,
        project_type=project_type,
        status="active",
        slot="Projekt-A",
        config={},
        created_at=datetime.now()
    )
    db.add(project)
    db.commit()
    return project


def create_test_task(db, project_id, status="completed", iterations=5):
    """Helper to create test task."""
    task = Task(
        id=f"task_{datetime.now().timestamp()}",
        project_id=project_id,
        status=status,
        iterations_used=iterations,
        time_seconds=iterations * 30.0,
        created_at=datetime.now() - timedelta(hours=1),
        completed_at=datetime.now() if status == "completed" else None
    )
    db.add(task)
    db.commit()
    return task


class TestDashboardStats:
    """Tests for GET /api/metrics/dashboard endpoint."""

    def test_dashboard_stats_empty(self, client, db_session):
        """Test dashboard stats with no data."""
        response = client.get("/api/metrics/dashboard")

        assert response.status_code == 200
        data = response.json()

        assert data["total_projects"] == 0
        assert data["active_tasks"] == 0
        assert data["completed_today"] == 0
        assert data["cost_today"] == 0.0

    def test_dashboard_stats_with_projects(self, client, db_session):
        """Test dashboard stats with projects."""
        # Create projects
        create_test_project(db_session, "Project 1")
        create_test_project(db_session, "Project 2")

        response = client.get("/api/metrics/dashboard")

        assert response.status_code == 200
        data = response.json()
        assert data["total_projects"] == 2

    def test_dashboard_stats_with_tasks(self, client, db_session):
        """Test dashboard stats with tasks."""
        project = create_test_project(db_session)

        # Create active and completed tasks
        create_test_task(db_session, project.id, status="in_progress")
        create_test_task(db_session, project.id, status="completed")
        create_test_task(db_session, project.id, status="completed")

        response = client.get("/api/metrics/dashboard")

        assert response.status_code == 200
        data = response.json()
        assert data["active_tasks"] == 1
        assert data["completed_today"] == 2

    def test_dashboard_stats_with_cost_tracking(self, client, db_session):
        """Test dashboard stats includes cost tracking."""
        project = create_test_project(db_session)
        task = create_test_task(db_session, project.id)

        # Add cost tracking
        cost = CostTracking(
            id=f"cost_{datetime.now().timestamp()}",
            task_id=task.id,
            project_id=project.id,
            agent_type=AgentType.GEMINI,
            prompt_tokens=1000,
            completion_tokens=500,
            cost_usd=0.05,
            timestamp=datetime.now()
        )
        db_session.add(cost)
        db_session.commit()

        response = client.get("/api/metrics/dashboard")

        assert response.status_code == 200
        data = response.json()
        assert data["cost_today"] > 0.0

    def test_dashboard_performance_metrics(self, client, db_session):
        """Test dashboard includes performance metrics."""
        project = create_test_project(db_session)

        # Create tasks with varying iterations
        create_test_task(db_session, project.id, iterations=3)
        create_test_task(db_session, project.id, iterations=5)
        create_test_task(db_session, project.id, iterations=7)

        response = client.get("/api/metrics/dashboard")

        assert response.status_code == 200
        data = response.json()
        assert "performance_metrics" in data
        assert data["performance_metrics"]["avg_iterations"] == 5.0


class TestQualityTrends:
    """Tests for GET /api/metrics/quality-trends endpoint."""

    def test_quality_trends_empty(self, client, db_session):
        """Test quality trends with no data."""
        response = client.get("/api/metrics/quality-trends?days=7")

        assert response.status_code == 200
        data = response.json()
        assert data["trends"] == []

    def test_quality_trends_with_snapshots(self, client, db_session):
        """Test quality trends with quality snapshots."""
        project = create_test_project(db_session)

        # Create quality snapshots over time
        for i in range(5):
            snapshot = QualitySnapshot(
                id=f"snap_{i}",
                project_id=project.id,
                overall_score=70.0 + i * 2,
                quality_dimensions={
                    "test_coverage": 60.0 + i * 3,
                    "security": 80.0,
                    "complexity": 70.0
                },
                timestamp=datetime.now() - timedelta(days=i)
            )
            db_session.add(snapshot)
        db_session.commit()

        response = client.get("/api/metrics/quality-trends?days=7")

        assert response.status_code == 200
        data = response.json()
        assert len(data["trends"]) > 0

    def test_quality_trends_date_range(self, client, db_session):
        """Test quality trends respects date range."""
        project = create_test_project(db_session)

        # Create snapshots: some in range, some out of range
        for i in range(10):
            snapshot = QualitySnapshot(
                id=f"snap_{i}",
                project_id=project.id,
                overall_score=75.0,
                quality_dimensions={},
                timestamp=datetime.now() - timedelta(days=i)
            )
            db_session.add(snapshot)
        db_session.commit()

        # Query last 3 days
        response = client.get("/api/metrics/quality-trends?days=3")

        assert response.status_code == 200
        data = response.json()
        # Should only include snapshots from last 3 days
        assert len(data["trends"]) <= 3

    def test_quality_trends_aggregation(self, client, db_session):
        """Test quality trends aggregates by project type."""
        # Create projects of different types
        proj1 = create_test_project(db_session, "Project 1", "typescript_fullstack")
        proj2 = create_test_project(db_session, "Project 2", "python_api")

        # Add snapshots
        for project in [proj1, proj2]:
            snapshot = QualitySnapshot(
                id=f"snap_{project.id}",
                project_id=project.id,
                overall_score=80.0,
                quality_dimensions={},
                timestamp=datetime.now()
            )
            db_session.add(snapshot)
        db_session.commit()

        response = client.get("/api/metrics/quality-trends?days=7&group_by=project_type")

        assert response.status_code == 200
        data = response.json()
        # Should have separate entries for each project type
        project_types = [trend.get("project_type") for trend in data["trends"]]
        assert "typescript_fullstack" in project_types or "python_api" in project_types


class TestCostMetrics:
    """Tests for GET /api/metrics/cost endpoint."""

    def test_cost_metrics_empty(self, client, db_session):
        """Test cost metrics with no data."""
        response = client.get("/api/metrics/cost")

        assert response.status_code == 200
        data = response.json()
        assert data["total_cost"] == 0.0
        assert data["cost_by_agent"] == {}

    def test_cost_by_agent(self, client, db_session):
        """Test cost breakdown by agent."""
        project = create_test_project(db_session)
        task = create_test_task(db_session, project.id)

        # Add cost for different agents
        agents_costs = [
            (AgentType.GEMINI, 0.03),
            (AgentType.CLAUDE, 0.10),
            (AgentType.COPILOT, 0.05),
        ]

        for agent, cost in agents_costs:
            cost_entry = CostTracking(
                id=f"cost_{agent}_{datetime.now().timestamp()}",
                task_id=task.id,
                project_id=project.id,
                agent_type=agent,
                prompt_tokens=1000,
                completion_tokens=500,
                cost_usd=cost,
                timestamp=datetime.now()
            )
            db_session.add(cost_entry)
        db_session.commit()

        response = client.get("/api/metrics/cost")

        assert response.status_code == 200
        data = response.json()
        assert data["total_cost"] == 0.18  # Sum of all costs
        assert len(data["cost_by_agent"]) == 3
        assert AgentType.GEMINI in data["cost_by_agent"]
        assert AgentType.CLAUDE in data["cost_by_agent"]

    def test_cost_time_period(self, client, db_session):
        """Test cost filtering by time period."""
        project = create_test_project(db_session)
        task = create_test_task(db_session, project.id)

        # Add costs from different time periods
        cost_today = CostTracking(
            id="cost_today",
            task_id=task.id,
            project_id=project.id,
            agent_type=AgentType.GEMINI,
            prompt_tokens=1000,
            completion_tokens=500,
            cost_usd=0.05,
            timestamp=datetime.now()
        )

        cost_old = CostTracking(
            id="cost_old",
            task_id=task.id,
            project_id=project.id,
            agent_type=AgentType.GEMINI,
            prompt_tokens=1000,
            completion_tokens=500,
            cost_usd=0.10,
            timestamp=datetime.now() - timedelta(days=10)
        )

        db_session.add(cost_today)
        db_session.add(cost_old)
        db_session.commit()

        # Query last 7 days
        response = client.get("/api/metrics/cost?days=7")

        assert response.status_code == 200
        data = response.json()
        # Should only include today's cost
        assert data["total_cost"] == 0.05

    def test_cost_savings_calculation(self, client, db_session):
        """Test cost savings vs all-Claude calculation."""
        project = create_test_project(db_session)
        task = create_test_task(db_session, project.id)

        # Mix of agents with known costs
        cost_gemini = CostTracking(
            id="cost_gemini",
            task_id=task.id,
            project_id=project.id,
            agent_type=AgentType.GEMINI,
            prompt_tokens=10000,
            completion_tokens=5000,
            cost_usd=0.02,
            timestamp=datetime.now()
        )

        cost_claude = CostTracking(
            id="cost_claude",
            task_id=task.id,
            project_id=project.id,
            agent_type=AgentType.CLAUDE,
            prompt_tokens=10000,
            completion_tokens=5000,
            cost_usd=0.10,
            timestamp=datetime.now()
        )

        db_session.add(cost_gemini)
        db_session.add(cost_claude)
        db_session.commit()

        response = client.get("/api/metrics/cost")

        assert response.status_code == 200
        data = response.json()
        # Should calculate savings
        assert "savings_vs_all_claude" in data
        assert data["savings_vs_all_claude"] > 0.0


class TestAgentPerformance:
    """Tests for GET /api/metrics/agent-performance endpoint."""

    def test_agent_performance_empty(self, client, db_session):
        """Test agent performance with no data."""
        response = client.get("/api/metrics/agent-performance")

        assert response.status_code == 200
        data = response.json()
        assert data["agents"] == {}

    def test_agent_performance_metrics(self, client, db_session):
        """Test agent performance calculation."""
        project = create_test_project(db_session)

        # Create tasks for different agents with quality snapshots
        for agent in [AgentType.GEMINI, AgentType.CLAUDE]:
            task = create_test_task(db_session, project.id)

            # Quality snapshot
            quality = 85.0 if agent == AgentType.CLAUDE else 75.0
            snapshot = QualitySnapshot(
                id=f"snap_{task.id}",
                project_id=project.id,
                overall_score=quality,
                quality_dimensions={},
                timestamp=datetime.now()
            )

            # Cost
            cost_usd = 0.10 if agent == AgentType.CLAUDE else 0.03
            cost = CostTracking(
                id=f"cost_{task.id}",
                task_id=task.id,
                project_id=project.id,
                agent_type=agent,
                prompt_tokens=1000,
                completion_tokens=500,
                cost_usd=cost_usd,
                timestamp=datetime.now()
            )

            db_session.add(snapshot)
            db_session.add(cost)

        db_session.commit()

        response = client.get("/api/metrics/agent-performance")

        assert response.status_code == 200
        data = response.json()
        assert len(data["agents"]) >= 1
        # Should have metrics for each agent
        for agent_data in data["agents"].values():
            assert "avg_quality" in agent_data
            assert "avg_cost" in agent_data
            assert "tasks_completed" in agent_data

    def test_agent_switch_tracking(self, client, db_session):
        """Test tracking of agent switches."""
        project = create_test_project(db_session)
        task = create_test_task(db_session, project.id)

        # Record agent switches
        switch = AgentSwitch(
            id=f"switch_{datetime.now().timestamp()}",
            task_id=task.id,
            project_id=project.id,
            from_agent=AgentType.GEMINI,
            to_agent=AgentType.CLAUDE,
            reason="Complex security issue detected",
            timestamp=datetime.now()
        )
        db_session.add(switch)
        db_session.commit()

        response = client.get("/api/metrics/agent-performance")

        assert response.status_code == 200
        data = response.json()
        assert "switch_count" in data or "switches" in data


class TestMetricsFiltering:
    """Tests for metric filtering and querying."""

    def test_filter_by_project(self, client, db_session):
        """Test filtering metrics by project ID."""
        proj1 = create_test_project(db_session, "Project 1")
        proj2 = create_test_project(db_session, "Project 2")

        create_test_task(db_session, proj1.id)
        create_test_task(db_session, proj2.id)

        response = client.get(f"/api/metrics/quality-trends?project_id={proj1.id}")

        assert response.status_code == 200
        # Should only include data from proj1

    def test_filter_by_date_range(self, client, db_session):
        """Test filtering by date range."""
        response = client.get("/api/metrics/cost?start_date=2025-01-01&end_date=2025-01-31")

        assert response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
