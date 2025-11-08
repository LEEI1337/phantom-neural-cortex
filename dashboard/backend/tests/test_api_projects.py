"""
Integration Tests for Projects API Endpoints
Tests CRUD operations, validation, and database interactions
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from main import app
from database import Base, get_db
from models import Project, ProjectType, ProjectStatus


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
def sample_project_data():
    """Sample project creation data."""
    return {
        "name": "Test Project",
        "description": "A test project for integration testing",
        "project_type": "typescript_fullstack",
        "repository_url": "https://github.com/test/repo",
        "config": {
            "priority": {
                "mode": "balanced",
                "custom_weights": None
            },
            "timeframe": {
                "max_minutes": 60,
                "preset": "standard"
            },
            "risk_tolerance": {
                "level": 50,
                "allow_experimental": False
            },
            "deployment": {
                "targets": ["linux"],
                "docker_enabled": True
            },
            "ml_components": {
                "adaptive_iterations": True,
                "latent_reasoning": True,
                "smart_agent_switching": True,
                "deep_supervision": True,
                "parallel_evaluation": True
            }
        }
    }


class TestProjectCreation:
    """Tests for POST /api/projects endpoint."""

    def test_create_project_success(self, client, sample_project_data):
        """Test successful project creation."""
        response = client.post("/api/projects", json=sample_project_data)

        assert response.status_code == 200
        data = response.json()

        assert data["name"] == "Test Project"
        assert data["project_type"] == "typescript_fullstack"
        assert data["status"] == "active"
        assert "id" in data
        assert "created_at" in data
        assert "slot" in data

    def test_create_project_assigns_slot(self, client, sample_project_data):
        """Test project gets assigned a slot (Projekt-A/B/C)."""
        response = client.post("/api/projects", json=sample_project_data)

        data = response.json()
        assert data["slot"] in ["Projekt-A", "Projekt-B", "Projekt-C"]

    def test_create_multiple_projects_different_slots(self, client, sample_project_data):
        """Test multiple projects get different slots."""
        # Create 3 projects
        slots = []
        for i in range(3):
            project_data = sample_project_data.copy()
            project_data["name"] = f"Project {i+1}"
            response = client.post("/api/projects", json=project_data)
            assert response.status_code == 200
            slots.append(response.json()["slot"])

        # All slots should be different
        assert len(set(slots)) == 3
        assert "Projekt-A" in slots
        assert "Projekt-B" in slots
        assert "Projekt-C" in slots

    def test_create_project_exceeds_slot_limit(self, client, sample_project_data):
        """Test creating 4th project fails (3 slot limit)."""
        # Create 3 projects
        for i in range(3):
            project_data = sample_project_data.copy()
            project_data["name"] = f"Project {i+1}"
            response = client.post("/api/projects", json=project_data)
            assert response.status_code == 200

        # 4th should fail
        project_data = sample_project_data.copy()
        project_data["name"] = "Project 4"
        response = client.post("/api/projects", json=project_data)

        assert response.status_code == 400
        assert "No available slots" in response.json()["detail"]

    def test_create_project_invalid_type(self, client, sample_project_data):
        """Test creating project with invalid type fails."""
        sample_project_data["project_type"] = "invalid_type"
        response = client.post("/api/projects", json=sample_project_data)

        assert response.status_code == 422  # Validation error

    def test_create_project_missing_required_fields(self, client):
        """Test creating project without required fields fails."""
        response = client.post("/api/projects", json={"name": "Test"})

        assert response.status_code == 422

    def test_create_project_default_config(self, client):
        """Test project creation with minimal data uses default config."""
        minimal_data = {
            "name": "Minimal Project",
            "project_type": "python_api"
        }
        response = client.post("/api/projects", json=minimal_data)

        assert response.status_code == 200
        data = response.json()

        # Should have default config
        assert "config" in data
        assert "priority" in data["config"]
        assert data["config"]["priority"]["mode"] == "balanced"


class TestProjectRetrieval:
    """Tests for GET /api/projects endpoints."""

    def test_get_all_projects_empty(self, client):
        """Test getting projects when none exist."""
        response = client.get("/api/projects")

        assert response.status_code == 200
        data = response.json()
        assert data == []

    def test_get_all_projects(self, client, sample_project_data):
        """Test getting all projects."""
        # Create 2 projects
        for i in range(2):
            project_data = sample_project_data.copy()
            project_data["name"] = f"Project {i+1}"
            client.post("/api/projects", json=project_data)

        response = client.get("/api/projects")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    def test_get_project_by_id(self, client, sample_project_data):
        """Test getting specific project by ID."""
        # Create project
        create_response = client.post("/api/projects", json=sample_project_data)
        project_id = create_response.json()["id"]

        # Get by ID
        response = client.get(f"/api/projects/{project_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == project_id
        assert data["name"] == "Test Project"

    def test_get_project_not_found(self, client):
        """Test getting non-existent project returns 404."""
        response = client.get("/api/projects/nonexistent-id")

        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()


class TestProjectUpdate:
    """Tests for PATCH/PUT /api/projects endpoints."""

    def test_update_project_config(self, client, sample_project_data):
        """Test updating project configuration."""
        # Create project
        create_response = client.post("/api/projects", json=sample_project_data)
        project_id = create_response.json()["id"]

        # Update config
        new_config = {
            "priority": {
                "mode": "performance",
                "custom_weights": {"quality": 0.8, "speed": 0.2}
            },
            "timeframe": {
                "max_minutes": 120,
                "preset": "deep_work"
            },
            "risk_tolerance": {
                "level": 75,
                "allow_experimental": True
            },
            "deployment": {
                "targets": ["linux", "windows"],
                "docker_enabled": True
            },
            "ml_components": {
                "adaptive_iterations": True,
                "latent_reasoning": True,
                "smart_agent_switching": False,
                "deep_supervision": True,
                "parallel_evaluation": True
            }
        }

        response = client.patch(
            f"/api/projects/{project_id}/config",
            json=new_config
        )

        assert response.status_code == 200
        data = response.json()
        assert data["config"]["priority"]["mode"] == "performance"
        assert data["config"]["timeframe"]["max_minutes"] == 120
        assert data["config"]["risk_tolerance"]["allow_experimental"] is True

    def test_update_project_status(self, client, sample_project_data):
        """Test updating project status."""
        # Create project
        create_response = client.post("/api/projects", json=sample_project_data)
        project_id = create_response.json()["id"]

        # Update to completed
        update_data = {"status": "completed"}
        response = client.patch(f"/api/projects/{project_id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "completed"


class TestProjectDeletion:
    """Tests for DELETE /api/projects endpoint."""

    def test_delete_project(self, client, sample_project_data):
        """Test deleting a project."""
        # Create project
        create_response = client.post("/api/projects", json=sample_project_data)
        project_id = create_response.json()["id"]

        # Delete
        response = client.delete(f"/api/projects/{project_id}")

        assert response.status_code == 200
        assert response.json()["message"] == "Project deleted successfully"

        # Verify deletion
        get_response = client.get(f"/api/projects/{project_id}")
        assert get_response.status_code == 404

    def test_delete_project_frees_slot(self, client, sample_project_data):
        """Test deleting project frees up its slot."""
        # Create 3 projects (fill all slots)
        project_ids = []
        for i in range(3):
            project_data = sample_project_data.copy()
            project_data["name"] = f"Project {i+1}"
            response = client.post("/api/projects", json=project_data)
            project_ids.append(response.json()["id"])

        # 4th should fail
        response = client.post("/api/projects", json=sample_project_data)
        assert response.status_code == 400

        # Delete first project
        client.delete(f"/api/projects/{project_ids[0]}")

        # Now 4th should succeed
        project_data = sample_project_data.copy()
        project_data["name"] = "Project 4"
        response = client.post("/api/projects", json=project_data)
        assert response.status_code == 200

    def test_delete_nonexistent_project(self, client):
        """Test deleting non-existent project returns 404."""
        response = client.delete("/api/projects/nonexistent-id")

        assert response.status_code == 404


class TestProjectValidation:
    """Tests for project data validation."""

    def test_validate_priority_mode(self, client, sample_project_data):
        """Test priority mode validation."""
        sample_project_data["config"]["priority"]["mode"] = "invalid_mode"
        response = client.post("/api/projects", json=sample_project_data)

        assert response.status_code == 422

    def test_validate_timeframe_range(self, client, sample_project_data):
        """Test timeframe validation (5-180 minutes)."""
        # Too low
        sample_project_data["config"]["timeframe"]["max_minutes"] = 3
        response = client.post("/api/projects", json=sample_project_data)
        assert response.status_code == 422

        # Too high
        sample_project_data["config"]["timeframe"]["max_minutes"] = 200
        response = client.post("/api/projects", json=sample_project_data)
        assert response.status_code == 422

        # Valid
        sample_project_data["config"]["timeframe"]["max_minutes"] = 90
        response = client.post("/api/projects", json=sample_project_data)
        assert response.status_code == 200

    def test_validate_risk_tolerance_range(self, client, sample_project_data):
        """Test risk tolerance validation (0-100)."""
        # Too low
        sample_project_data["config"]["risk_tolerance"]["level"] = -10
        response = client.post("/api/projects", json=sample_project_data)
        assert response.status_code == 422

        # Too high
        sample_project_data["config"]["risk_tolerance"]["level"] = 150
        response = client.post("/api/projects", json=sample_project_data)
        assert response.status_code == 422

    def test_validate_deployment_targets(self, client, sample_project_data):
        """Test deployment targets validation."""
        valid_targets = ["windows", "linux", "macos", "kubernetes"]

        # Valid targets
        sample_project_data["config"]["deployment"]["targets"] = ["linux", "windows"]
        response = client.post("/api/projects", json=sample_project_data)
        assert response.status_code == 200

        # Invalid target
        sample_project_data["config"]["deployment"]["targets"] = ["invalid_os"]
        response = client.post("/api/projects", json=sample_project_data)
        assert response.status_code == 422


class TestProjectTemplates:
    """Tests for project template functionality."""

    def test_template_speed_optimization(self, client):
        """Test creating project from 'speed' template."""
        template_data = {
            "name": "Speed Project",
            "project_type": "python_api",
            "template": "speed"
        }

        response = client.post("/api/projects", json=template_data)
        assert response.status_code == 200

        data = response.json()
        # Speed template should prioritize performance
        assert data["config"]["priority"]["mode"] in ["performance", "balanced"]
        assert data["config"]["timeframe"]["max_minutes"] <= 60

    def test_template_quality_focused(self, client):
        """Test creating project from 'quality' template."""
        template_data = {
            "name": "Quality Project",
            "project_type": "typescript_fullstack",
            "template": "quality"
        }

        response = client.post("/api/projects", json=template_data)
        assert response.status_code == 200

        data = response.json()
        # Quality template should have higher timeframe
        assert data["config"]["timeframe"]["max_minutes"] >= 60


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
