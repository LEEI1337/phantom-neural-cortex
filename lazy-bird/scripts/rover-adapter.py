#!/usr/bin/env python3
"""
Rover Adapter - Bridge between Lazy Bird and Rover CLI

This module translates Lazy Bird issue tasks into Rover CLI commands,
enabling autonomous GitHub issue → implementation → PR workflows.

Architecture:
    Lazy Bird (Layer 4) → RoverAdapter → Rover CLI (Layer 3) → AI Agents (Layer 2)
"""

import subprocess
import json
import time
from typing import Dict, Optional, List
from pathlib import Path


class RoverAdapter:
    """Adapter for integrating Lazy Bird with Rover orchestration."""
    
    def __init__(self, rover_cli_path: str = "rover"):
        """
        Initialize Rover adapter.
        
        Args:
            rover_cli_path: Path to rover CLI executable (default: "rover" in PATH)
        """
        self.rover_cli = rover_cli_path
        self.tasks = {}  # Track active Rover tasks
    
    def create_task(self, issue_data: Dict, project_config: Dict, agent: str) -> Optional[str]:
        """
        Create a Rover task from a GitHub issue.
        
        Args:
            issue_data: GitHub issue details (title, body, labels, number)
            project_config: Project configuration (path, repo, test_command, etc.)
            agent: AI agent to use (claude, gemini, copilot)
        
        Returns:
            Rover task ID if successful, None otherwise
        
        Example:
            >>> issue = {
            ...     "title": "Add login feature",
            ...     "body": "Implement OAuth login...",
            ...     "number": 42
            ... }
            >>> config = {
            ...     "path": "/workspace/my-project",
            ...     "repo": "https://github.com/user/repo"
            ... }
            >>> task_id = adapter.create_task(issue, config, "gemini")
        """
        # Build Rover command
        task_description = f"{issue_data['title']}\n\n{issue_data['body']}"
        
        cmd = [
            self.rover_cli,
            "task",
            task_description,
            "--agent", agent,
            "--project", project_config["path"],
            "--issue", str(issue_data["number"])
        ]
        
        try:
            # Execute Rover command
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                # Extract task ID from Rover output
                task_id = self._extract_task_id(result.stdout)
                
                # Store task metadata
                self.tasks[task_id] = {
                    "issue_number": issue_data["number"],
                    "agent": agent,
                    "project": project_config["id"],
                    "status": "created",
                    "created_at": time.time()
                }
                
                return task_id
            else:
                print(f"Error creating Rover task: {result.stderr}")
                return None
                
        except subprocess.TimeoutExpired:
            print("Rover command timed out")
            return None
        except Exception as e:
            print(f"Exception creating Rover task: {e}")
            return None
    
    def monitor_task(self, rover_task_id: str) -> Dict:
        """
        Poll Rover task status.
        
        Args:
            rover_task_id: Rover task identifier
        
        Returns:
            Task status dictionary with keys: status, progress, error
        
        Example:
            >>> status = adapter.monitor_task("task-123")
            >>> print(status["status"])  # "running", "completed", "failed"
        """
        cmd = [self.rover_cli, "status", rover_task_id, "--json"]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                return json.loads(result.stdout)
            else:
                return {"status": "error", "error": result.stderr}
                
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def get_test_results(self, rover_task_id: str) -> Dict:
        """
        Extract test results from Rover workspace.
        
        Args:
            rover_task_id: Rover task identifier
        
        Returns:
            Test results dictionary with keys: passed, failed, total, output
        
        Example:
            >>> results = adapter.get_test_results("task-123")
            >>> if results["passed"] == results["total"]:
            ...     print("All tests passed!")
        """
        # Get Rover workspace path
        workspace = self._get_workspace_path(rover_task_id)
        if not workspace:
            return {"error": "Workspace not found"}
        
        # Look for test result files (pytest, jest, etc.)
        test_files = [
            "test-results.json",
            "junit.xml",
            ".pytest_cache/v/cache/lastfailed"
        ]
        
        for test_file in test_files:
            test_path = Path(workspace) / test_file
            if test_path.exists():
                return self._parse_test_results(test_path)
        
        return {"error": "No test results found"}
    
    def merge_or_retry(self, rover_task_id: str, test_status: Dict) -> str:
        """
        Decision logic for merging PR or retrying on failure.
        
        Args:
            rover_task_id: Rover task identifier
            test_status: Test results from get_test_results()
        
        Returns:
            Action taken: "merged", "retried", "failed"
        
        Example:
            >>> test_status = {"passed": 10, "failed": 0, "total": 10}
            >>> action = adapter.merge_or_retry("task-123", test_status)
        """
        if test_status.get("error"):
            print(f"Test error: {test_status['error']}")
            return "failed"
        
        # Check if all tests passed
        passed = test_status.get("passed", 0)
        total = test_status.get("total", 1)
        
        if passed == total and total > 0:
            # All tests passed - merge
            return self._merge_task(rover_task_id)
        elif self._should_retry(rover_task_id):
            # Some tests failed - retry with different agent or approach
            return self._retry_task(rover_task_id)
        else:
            # Max retries reached - fail
            return "failed"
    
    def _extract_task_id(self, rover_output: str) -> str:
        """Extract task ID from Rover CLI output."""
        # Parse Rover output for task ID
        # Example output: "Created task: task-abc123"
        for line in rover_output.split("\n"):
            if "task" in line.lower() and ":" in line:
                return line.split(":")[-1].strip()
        return f"task-{int(time.time())}"
    
    def _get_workspace_path(self, rover_task_id: str) -> Optional[str]:
        """Get filesystem path to Rover task workspace."""
        cmd = [self.rover_cli, "workspace", rover_task_id]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                return result.stdout.strip()
        except Exception:
            pass
        return None
    
    def _parse_test_results(self, test_file: Path) -> Dict:
        """Parse test results from file (pytest, jest, junit)."""
        # Placeholder - implement actual parsing based on test framework
        return {
            "passed": 0,
            "failed": 0,
            "total": 0,
            "output": ""
        }
    
    def _merge_task(self, rover_task_id: str) -> str:
        """Merge Rover task (create PR and merge)."""
        cmd = [self.rover_cli, "merge", rover_task_id]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                return "merged"
        except Exception:
            pass
        return "failed"
    
    def _should_retry(self, rover_task_id: str) -> bool:
        """Check if task should be retried based on retry count."""
        task_meta = self.tasks.get(rover_task_id, {})
        retries = task_meta.get("retries", 0)
        max_retries = 3
        return retries < max_retries
    
    def _retry_task(self, rover_task_id: str) -> str:
        """Retry task with different agent or approach."""
        task_meta = self.tasks.get(rover_task_id, {})
        task_meta["retries"] = task_meta.get("retries", 0) + 1
        
        # Switch to more powerful agent on retry
        current_agent = task_meta.get("agent", "gemini")
        next_agent = self._get_escalated_agent(current_agent)
        
        print(f"Retrying task {rover_task_id} with agent: {next_agent}")
        
        # Trigger new Rover task with same issue but different agent
        # This would need issue data stored in task_meta
        
        return "retried"
    
    def _get_escalated_agent(self, current_agent: str) -> str:
        """Get more powerful agent for retry (escalation path)."""
        escalation = {
            "gemini": "claude",  # Free → Paid expert
            "copilot": "claude",  # GitHub specialist → Expert
            "claude": "claude"  # Already using best
        }
        return escalation.get(current_agent, "claude")


if __name__ == "__main__":
    # Example usage
    adapter = RoverAdapter()
    
    # Example issue
    issue = {
        "title": "Add user authentication",
        "body": "Implement JWT-based authentication with refresh tokens",
        "number": 42,
        "labels": ["feature", "security"]
    }
    
    # Example project config
    project = {
        "id": "my-app",
        "path": "/workspace/my-app",
        "repo": "https://github.com/user/my-app"
    }
    
    # Create task
    task_id = adapter.create_task(issue, project, "gemini")
    print(f"Created Rover task: {task_id}")
    
    # Monitor task
    status = adapter.monitor_task(task_id)
    print(f"Task status: {status}")
