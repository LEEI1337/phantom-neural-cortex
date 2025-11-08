#!/usr/bin/env python3
"""
Issue Watcher - GitHub issue monitoring and automation trigger

Polls GitHub repositories for issues with specific labels (e.g., "lazy-bird")
and triggers Rover tasks automatically.

Key Features:
- Polls GitHub API every 60 seconds
- Filters by label (e.g., "lazy-bird", "ready-for-implementation")
- Triggers RoverAdapter to create tasks
- Tracks issue → task mapping
- Handles multiple projects
"""

import os
import time
import json
import requests
from typing import List, Dict, Optional
from datetime import datetime
from pathlib import Path

from rover_adapter import RoverAdapter
from agent_selector import AgentSelector
from project_manager import ProjectManager


class IssueWatcher:
    """Watches GitHub issues and triggers automated workflows."""
    
    def __init__(
        self,
        github_token: str,
        poll_interval: int = 60,
        config_path: str = "../configs/projects.json"
    ):
        """
        Initialize issue watcher.
        
        Args:
            github_token: GitHub personal access token
            poll_interval: Seconds between GitHub API polls (default: 60)
            config_path: Path to projects.json configuration
        """
        self.github_token = github_token
        self.poll_interval = poll_interval
        self.headers = {
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        # Initialize components
        self.project_manager = ProjectManager(config_path)
        self.rover_adapter = RoverAdapter()
        self.agent_selector = AgentSelector()
        
        # Track processed issues to avoid duplicates
        self.processed_issues = set()
        self.active_tasks = {}  # issue_number → rover_task_id
    
    def start(self):
        """Start watching GitHub issues (blocking loop)."""
        print(f"🚀 Lazy Bird Issue Watcher started")
        print(f"📊 Monitoring {len(self.project_manager.projects)} projects")
        print(f"⏱️  Poll interval: {self.poll_interval}s\n")
        
        while True:
            try:
                self._poll_all_projects()
                time.sleep(self.poll_interval)
            except KeyboardInterrupt:
                print("\n👋 Shutting down gracefully...")
                break
            except Exception as e:
                print(f"❌ Error in main loop: {e}")
                time.sleep(self.poll_interval)
    
    def _poll_all_projects(self):
        """Poll all configured projects for new issues."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] Polling GitHub issues...")
        
        for project in self.project_manager.projects:
            if not project.get("rover_enabled", True):
                continue
            
            try:
                self._poll_project(project)
            except Exception as e:
                print(f"  ❌ Error polling {project['id']}: {e}")
    
    def _poll_project(self, project: Dict):
        """Poll a single project for issues."""
        # Parse repo URL to get owner/repo
        repo_url = project["repo"]
        owner, repo = self._parse_repo_url(repo_url)
        
        if not owner or not repo:
            return
        
        # Get watch label from config
        watch_label = project.get("labels", {}).get("watch", "lazy-bird")
        
        # Fetch open issues with watch label
        issues = self._fetch_issues(owner, repo, watch_label)
        
        new_issues = 0
        for issue in issues:
            issue_key = f"{owner}/{repo}#{issue['number']}"
            
            if issue_key not in self.processed_issues:
                self._process_issue(issue, project)
                new_issues += 1
        
        if new_issues > 0:
            print(f"  ✅ {project['id']}: {new_issues} new issue(s)")
    
    def _fetch_issues(
        self,
        owner: str,
        repo: str,
        label: str
    ) -> List[Dict]:
        """
        Fetch issues from GitHub API.
        
        Args:
            owner: Repository owner
            repo: Repository name
            label: Label to filter by
        
        Returns:
            List of issue dictionaries
        """
        url = f"https://api.github.com/repos/{owner}/{repo}/issues"
        params = {
            "labels": label,
            "state": "open",
            "per_page": 30
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"    ⚠️  Error fetching issues: {e}")
            return []
    
    def _process_issue(self, issue: Dict, project: Dict):
        """
        Process a new issue and create Rover task.
        
        Args:
            issue: GitHub issue data
            project: Project configuration
        """
        issue_number = issue["number"]
        issue_title = issue["title"]
        issue_labels = [label["name"] for label in issue.get("labels", [])]
        
        print(f"\n🎯 Processing Issue #{issue_number}: {issue_title}")
        print(f"   Labels: {', '.join(issue_labels)}")
        
        # Select appropriate AI agent
        agent = self.agent_selector.select_agent(
            issue_labels,
            project["id"],
            project.get("type")
        )
        print(f"   Agent: {agent}")
        
        # Create Rover task
        issue_data = {
            "title": issue_title,
            "body": issue.get("body", ""),
            "number": issue_number,
            "labels": issue_labels
        }
        
        task_id = self.rover_adapter.create_task(issue_data, project, agent)
        
        if task_id:
            # Track processed issue and active task
            issue_key = f"{self._parse_repo_url(project['repo'])}#{issue_number}"
            self.processed_issues.add(issue_key)
            self.active_tasks[issue_number] = task_id
            
            print(f"   ✅ Created Rover task: {task_id}\n")
            
            # Comment on issue with task info
            self._comment_on_issue(issue, project, task_id, agent)
        else:
            print(f"   ❌ Failed to create Rover task\n")
    
    def _comment_on_issue(
        self,
        issue: Dict,
        project: Dict,
        task_id: str,
        agent: str
    ):
        """Add comment to GitHub issue with task information."""
        owner, repo = self._parse_repo_url(project["repo"])
        if not owner or not repo:
            return
        
        comment_body = f"""🤖 **Lazy Bird Automation Started**

This issue has been picked up for automated implementation!

**Details:**
- 🔧 Rover Task: `{task_id}`
- 🤖 AI Agent: `{agent}`
- 📦 Project: `{project['id']}`
- ⏱️  Started: {datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")}

I'll update this issue with progress and create a PR when ready.

---
*Powered by [Lazy Bird](https://github.com/yusufkaraaslan/lazy-bird) + [Rover](https://github.com/endorhq/rover)*
"""
        
        url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue['number']}/comments"
        data = {"body": comment_body}
        
        try:
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()
        except Exception as e:
            print(f"    ⚠️  Could not comment on issue: {e}")
    
    def _parse_repo_url(self, repo_url: str) -> tuple:
        """
        Parse GitHub repo URL to extract owner and repo name.
        
        Args:
            repo_url: GitHub repo URL (https://github.com/owner/repo)
        
        Returns:
            Tuple of (owner, repo)
        """
        try:
            # Handle both HTTPS and SSH URLs
            if "github.com/" in repo_url:
                parts = repo_url.split("github.com/")[-1].rstrip("/").rstrip(".git")
                owner, repo = parts.split("/")
                return owner, repo
        except Exception:
            pass
        
        return None, None


def main():
    """Main entry point for issue watcher."""
    # Load GitHub token from environment
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        print("❌ Error: GITHUB_TOKEN environment variable not set")
        print("   Set it with: export GITHUB_TOKEN=your_token_here")
        return
    
    # Create and start watcher
    watcher = IssueWatcher(
        github_token=github_token,
        poll_interval=60  # Poll every 60 seconds
    )
    
    watcher.start()


if __name__ == "__main__":
    main()
