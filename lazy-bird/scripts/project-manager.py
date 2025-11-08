#!/usr/bin/env python3
"""
Project Manager - Multi-project configuration and coordination

Manages configuration for multiple projects that Lazy Bird monitors.
Each project can have custom settings for:
- Repository location
- Test commands
- Default AI agent
- Rover settings
- Label filters
"""

import json
from typing import List, Dict, Optional
from pathlib import Path


class ProjectManager:
    """Manages multi-project configuration for Lazy Bird."""
    
    def __init__(self, config_path: str = "../configs/projects.json"):
        """
        Initialize project manager.
        
        Args:
            config_path: Path to projects.json configuration file
        """
        self.config_path = Path(config_path)
        self.projects = self._load_projects()
    
    def _load_projects(self) -> List[Dict]:
        """Load project configurations from JSON file."""
        if not self.config_path.exists():
            print(f"⚠️  Config file not found: {self.config_path}")
            print("   Using default configuration")
            return self._get_default_config()
        
        try:
            with open(self.config_path, 'r') as f:
                data = json.load(f)
                return data.get("projects", [])
        except Exception as e:
            print(f"❌ Error loading config: {e}")
            return []
    
    def _get_default_config(self) -> List[Dict]:
        """Return default project configuration."""
        return [
            {
                "id": "ai-orchestrator",
                "name": "AI Development Orchestrator",
                "type": "python",
                "path": "/workspace/ai-dev-orchestrator",
                "repo": "https://github.com/LEEI1337/ai-dev-orchestrator",
                "branch": "master",
                "rover_enabled": True,
                "settings": {
                    "test_command": "pytest tests/ -v",
                    "build_command": "python -m build",
                    "lint_command": "ruff check .",
                    "default_agent": "gemini",
                    "max_retries": 3,
                    "timeout_minutes": 30
                },
                "labels": {
                    "watch": "lazy-bird",
                    "ready": "ready-for-implementation"
                }
            }
        ]
    
    def get_project(self, project_id: str) -> Optional[Dict]:
        """
        Get project configuration by ID.
        
        Args:
            project_id: Project identifier
        
        Returns:
            Project configuration dictionary or None
        """
        for project in self.projects:
            if project["id"] == project_id:
                return project
        return None
    
    def get_project_by_repo(self, repo_url: str) -> Optional[Dict]:
        """
        Get project configuration by repository URL.
        
        Args:
            repo_url: GitHub repository URL
        
        Returns:
            Project configuration dictionary or None
        """
        # Normalize repo URL for comparison
        normalized = repo_url.rstrip("/").rstrip(".git").lower()
        
        for project in self.projects:
            project_repo = project["repo"].rstrip("/").rstrip(".git").lower()
            if project_repo == normalized:
                return project
        
        return None
    
    def get_enabled_projects(self) -> List[Dict]:
        """
        Get all projects with Rover integration enabled.
        
        Returns:
            List of enabled project configurations
        """
        return [p for p in self.projects if p.get("rover_enabled", True)]
    
    def validate_project(self, project: Dict) -> tuple:
        """
        Validate project configuration.
        
        Args:
            project: Project configuration dictionary
        
        Returns:
            Tuple of (is_valid: bool, errors: List[str])
        """
        errors = []
        required_fields = ["id", "name", "type", "path", "repo"]
        
        for field in required_fields:
            if field not in project:
                errors.append(f"Missing required field: {field}")
        
        # Validate path exists
        if "path" in project:
            path = Path(project["path"])
            if not path.exists():
                errors.append(f"Project path does not exist: {project['path']}")
        
        return len(errors) == 0, errors
    
    def add_project(self, project: Dict) -> bool:
        """
        Add a new project to configuration.
        
        Args:
            project: Project configuration dictionary
        
        Returns:
            True if added successfully, False otherwise
        """
        is_valid, errors = self.validate_project(project)
        
        if not is_valid:
            print("❌ Invalid project configuration:")
            for error in errors:
                print(f"   - {error}")
            return False
        
        # Check for duplicate ID
        if self.get_project(project["id"]):
            print(f"❌ Project with ID '{project['id']}' already exists")
            return False
        
        self.projects.append(project)
        return self._save_projects()
    
    def remove_project(self, project_id: str) -> bool:
        """
        Remove a project from configuration.
        
        Args:
            project_id: Project identifier
        
        Returns:
            True if removed successfully, False otherwise
        """
        project = self.get_project(project_id)
        if not project:
            print(f"❌ Project not found: {project_id}")
            return False
        
        self.projects.remove(project)
        return self._save_projects()
    
    def _save_projects(self) -> bool:
        """Save projects configuration to JSON file."""
        try:
            # Ensure config directory exists
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            
            data = {"projects": self.projects}
            
            with open(self.config_path, 'w') as f:
                json.dump(data, f, indent=2)
            
            print(f"✅ Saved configuration to {self.config_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error saving config: {e}")
            return False


def main():
    """Example usage and testing."""
    manager = ProjectManager()
    
    print("=== Project Manager ===\n")
    
    print(f"Loaded {len(manager.projects)} project(s):\n")
    
    for project in manager.projects:
        print(f"📦 {project['name']}")
        print(f"   ID: {project['id']}")
        print(f"   Type: {project['type']}")
        print(f"   Repo: {project['repo']}")
        print(f"   Rover: {'✅ Enabled' if project.get('rover_enabled') else '❌ Disabled'}")
        
        settings = project.get('settings', {})
        if settings:
            print(f"   Default Agent: {settings.get('default_agent', 'N/A')}")
            print(f"   Test Command: {settings.get('test_command', 'N/A')}")
        
        print()
    
    # Test validation
    print("=== Validation Test ===\n")
    test_project = {
        "id": "test-project",
        "name": "Test Project",
        "type": "javascript",
        "path": "/tmp/test",
        "repo": "https://github.com/user/test"
    }
    
    is_valid, errors = manager.validate_project(test_project)
    if is_valid:
        print("✅ Test project configuration is valid")
    else:
        print("❌ Test project has errors:")
        for error in errors:
            print(f"   - {error}")


if __name__ == "__main__":
    main()
