#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Project Initializer - Automatic project folder assignment and scaffolding

Automatically assigns issues to available project folders (Projekt-A/B/C)
and creates standard project structure when a new project is started.

Features:
- Finds next available project folder (A → B → C → ...)
- Creates standard directory structure
- Initializes git repository
- Generates project-specific config files
- Updates projects.json automatically
"""

import os
import sys
import io
import json
import subprocess
from pathlib import Path
from typing import Dict, Optional, List
from datetime import datetime

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


class ProjectInitializer:
    """Manages automatic project folder assignment and initialization."""

    def __init__(
        self,
        projects_root: str = "../../projects",
        config_path: str = "../configs/projects.json"
    ):
        """
        Initialize project initializer.

        Args:
            projects_root: Root directory containing Projekt-A/B/C folders
            config_path: Path to projects.json configuration
        """
        self.projects_root = Path(projects_root).resolve()
        self.config_path = Path(config_path).resolve()
        self.project_slots = ["Projekt-A", "Projekt-B", "Projekt-C"]

    def find_available_slot(self) -> Optional[str]:
        """
        Find next available project slot.

        Returns:
            Project folder name (e.g., "Projekt-A") or None if all occupied
        """
        config = self._load_config()
        occupied_paths = set()

        # Get all currently used project paths
        for project in config.get("projects", []):
            project_path = Path(project.get("path", ""))
            if project_path.exists() and project_path.is_dir():
                # Check if it has actual project files (not just README.md)
                if self._is_project_occupied(project_path):
                    occupied_paths.add(project_path.name)

        # Find first available slot
        for slot in self.project_slots:
            if slot not in occupied_paths:
                return slot

        return None

    def _is_project_occupied(self, project_path: Path) -> bool:
        """
        Check if a project folder is actually being used.

        A project is considered occupied if it contains:
        - src/ or lib/ directory
        - package.json, requirements.txt, or similar
        - .git directory (excluding empty repos)

        Args:
            project_path: Path to project folder

        Returns:
            True if project is occupied, False if empty/template
        """
        # Check for source directories
        if (project_path / "src").exists():
            return True
        if (project_path / "lib").exists():
            return True
        if (project_path / "app").exists():
            return True

        # Check for package managers
        if (project_path / "package.json").exists():
            return True
        if (project_path / "requirements.txt").exists():
            return True
        if (project_path / "Cargo.toml").exists():
            return True
        if (project_path / "go.mod").exists():
            return True

        # Check for git with commits
        git_dir = project_path / ".git"
        if git_dir.exists():
            try:
                # Check if there are any commits
                result = subprocess.run(
                    ["git", "-C", str(project_path), "rev-list", "--count", "HEAD"],
                    capture_output=True,
                    text=True,
                    check=False
                )
                if result.returncode == 0 and int(result.stdout.strip()) > 0:
                    return True
            except:
                pass

        return False

    def initialize_project(
        self,
        issue_title: str,
        issue_number: int,
        project_type: str = "python",
        repo_url: str = "",
        agent: str = "gemini"
    ) -> Optional[Dict]:
        """
        Initialize a new project in the next available slot.

        Args:
            issue_title: GitHub issue title
            issue_number: GitHub issue number
            project_type: Type of project (python, typescript, react, etc.)
            repo_url: Optional GitHub repository URL
            agent: Default AI agent to use

        Returns:
            Project configuration dict or None if no slots available
        """
        # Find available slot
        slot = self.find_available_slot()
        if not slot:
            print("❌ No available project slots! All Projekt-A/B/C are occupied.")
            return None

        project_path = self.projects_root / slot
        print(f"✅ Assigning to: {slot}")
        print(f"   Path: {project_path}")

        # Create project structure
        self._create_project_structure(project_path, project_type)

        # Initialize git repository
        self._init_git_repo(project_path, issue_title, issue_number)

        # Create project-specific config
        project_config = self._create_project_config(
            slot=slot,
            path=str(project_path),
            project_type=project_type,
            repo_url=repo_url,
            agent=agent,
            issue_title=issue_title
        )

        # Update projects.json
        self._update_projects_json(project_config)

        print(f"🎉 Project initialized in {slot}!")
        return project_config

    def _create_project_structure(self, project_path: Path, project_type: str):
        """
        Create standard project directory structure.

        Args:
            project_path: Path to project folder
            project_type: Type of project (determines structure)
        """
        print(f"📁 Creating project structure for {project_type}...")

        # Common directories for all project types
        common_dirs = [
            "src",
            "tests",
            "docs",
            ".github/workflows"
        ]

        for dir_name in common_dirs:
            dir_path = project_path / dir_name
            dir_path.mkdir(parents=True, exist_ok=True)

        # Type-specific files
        if project_type == "python":
            self._create_python_structure(project_path)
        elif project_type in ["typescript", "javascript"]:
            self._create_node_structure(project_path, project_type)
        elif project_type in ["react", "nextjs"]:
            self._create_react_structure(project_path, project_type)
        else:
            # Generic structure
            (project_path / "src" / "__init__.py").touch()

        print("   ✅ Structure created")

    def _create_python_structure(self, project_path: Path):
        """Create Python project structure."""
        # Create setup files
        (project_path / "requirements.txt").write_text("")
        (project_path / "setup.py").write_text("""from setuptools import setup, find_packages

setup(
    name="project",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
)
""")
        (project_path / "src" / "__init__.py").touch()
        (project_path / "tests" / "__init__.py").touch()
        (project_path / "tests" / "test_example.py").write_text("""def test_example():
    assert True
""")

    def _create_node_structure(self, project_path: Path, project_type: str):
        """Create Node.js/TypeScript project structure."""
        package_json = {
            "name": project_path.name.lower(),
            "version": "0.1.0",
            "description": "Auto-generated project",
            "main": "src/index.js" if project_type == "javascript" else "dist/index.js",
            "scripts": {
                "test": "jest",
                "build": "tsc" if project_type == "typescript" else "echo 'No build needed'",
                "start": "node src/index.js"
            },
            "keywords": [],
            "author": "",
            "license": "MIT"
        }

        (project_path / "package.json").write_text(
            json.dumps(package_json, indent=2)
        )

        if project_type == "typescript":
            (project_path / "tsconfig.json").write_text("""{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true
  }
}
""")
            (project_path / "src" / "index.ts").write_text("console.log('Hello World!');\n")
        else:
            (project_path / "src" / "index.js").write_text("console.log('Hello World!');\n")

    def _create_react_structure(self, project_path: Path, project_type: str):
        """Create React/Next.js project structure."""
        # Will be created by create-react-app or create-next-app
        # Just create placeholder
        (project_path / "SETUP.md").write_text(f"""# Setup Required

Run one of these commands to initialize the {project_type} project:

```bash
# For React:
npx create-react-app .

# For Next.js:
npx create-next-app .
```
""")

    def _init_git_repo(self, project_path: Path, issue_title: str, issue_number: int):
        """
        Initialize git repository with initial commit.

        Args:
            project_path: Path to project folder
            issue_title: GitHub issue title
            issue_number: GitHub issue number
        """
        print(f"🔧 Initializing git repository...")

        try:
            # Initialize repo
            subprocess.run(
                ["git", "init"],
                cwd=project_path,
                check=True,
                capture_output=True
            )

            # Create .gitignore
            gitignore_content = """# Dependencies
node_modules/
venv/
env/

# Build outputs
dist/
build/
*.pyc
__pycache__/

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
"""
            (project_path / ".gitignore").write_text(gitignore_content)

            # Initial commit
            subprocess.run(
                ["git", "add", "."],
                cwd=project_path,
                check=True,
                capture_output=True
            )

            commit_message = f"Initial project setup for issue #{issue_number}: {issue_title}"
            subprocess.run(
                ["git", "commit", "-m", commit_message],
                cwd=project_path,
                check=True,
                capture_output=True
            )

            print("   ✅ Git repository initialized")
        except Exception as e:
            print(f"   ⚠️  Git initialization failed: {e}")

    def _create_project_config(
        self,
        slot: str,
        path: str,
        project_type: str,
        repo_url: str,
        agent: str,
        issue_title: str
    ) -> Dict:
        """
        Create project configuration dictionary.

        Returns:
            Project config dict for projects.json
        """
        # Determine test/build commands based on type
        commands = self._get_type_commands(project_type)

        project_id = slot.lower()

        return {
            "id": project_id,
            "name": issue_title[:50],  # Use issue title as project name
            "type": project_type,
            "path": path,
            "repo": repo_url,
            "branch": "main",
            "rover_enabled": True,
            "settings": {
                "test_command": commands["test"],
                "build_command": commands["build"],
                "lint_command": commands["lint"],
                "default_agent": agent,
                "max_retries": 3,
                "timeout_minutes": 30
            },
            "labels": {
                "watch": "lazy-bird",
                "ready": "ready-for-implementation"
            },
            "created_at": datetime.now().isoformat()
        }

    def _get_type_commands(self, project_type: str) -> Dict[str, str]:
        """Get test/build/lint commands for project type."""
        commands_map = {
            "python": {
                "test": "pytest tests/ -v",
                "build": "python -m build",
                "lint": "ruff check ."
            },
            "typescript": {
                "test": "npm test",
                "build": "npm run build",
                "lint": "npm run lint"
            },
            "javascript": {
                "test": "npm test",
                "build": "npm run build",
                "lint": "eslint ."
            },
            "react": {
                "test": "npm test",
                "build": "npm run build",
                "lint": "npm run lint"
            },
            "nextjs": {
                "test": "npm test",
                "build": "npm run build",
                "lint": "next lint"
            }
        }

        return commands_map.get(project_type, {
            "test": "echo 'No tests configured'",
            "build": "echo 'No build configured'",
            "lint": "echo 'No linting configured'"
        })

    def _update_projects_json(self, new_project: Dict):
        """
        Update projects.json with new project configuration.

        Args:
            new_project: New project configuration to add
        """
        config = self._load_config()

        # Remove placeholder entry if exists
        projects = [
            p for p in config.get("projects", [])
            if p["id"] != new_project["id"] or p["type"] != "placeholder"
        ]

        # Add new project
        projects.append(new_project)

        # Save back
        config["projects"] = projects

        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)

        print(f"   ✅ Updated {self.config_path}")

    def _load_config(self) -> Dict:
        """Load current projects.json configuration."""
        if not self.config_path.exists():
            return {"projects": []}

        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️  Error loading config: {e}")
            return {"projects": []}


def main():
    """Demo: Initialize a test project."""
    initializer = ProjectInitializer()

    print("=" * 60)
    print("🤖 Project Initializer Demo")
    print("=" * 60)

    # Find available slot
    slot = initializer.find_available_slot()
    print(f"\n📊 Next available slot: {slot}")

    # Initialize test project
    if slot:
        print(f"\n🚀 Initializing test project...")
        project = initializer.initialize_project(
            issue_title="Test Project Setup",
            issue_number=999,
            project_type="python",
            repo_url="",
            agent="gemini"
        )

        if project:
            print(f"\n✅ Project created:")
            print(f"   ID: {project['id']}")
            print(f"   Path: {project['path']}")
            print(f"   Type: {project['type']}")


if __name__ == "__main__":
    main()
