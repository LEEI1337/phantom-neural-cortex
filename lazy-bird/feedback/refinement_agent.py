#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Refinement Agent - L-Module (Low-Level)

Executes refinement iterations based on feedback.
"""

import sys
import io
import logging
from typing import Dict, List, Optional
from pathlib import Path

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

logger = logging.getLogger(__name__)


class RefinementAgent:
    """L-Module: Executes refinement iterations."""

    def __init__(self, agent_name: str = "gemini"):
        """Initialize refinement agent.

        Args:
            agent_name: Agent to use (claude/gemini/copilot)
        """
        self.agent_name = agent_name

    def refine_implementation(
        self,
        project_path: Path,
        feedback: List[str],
        previous_state: Dict,
        iteration: int
    ) -> Dict:
        """Execute one refinement iteration.

        Args:
            project_path: Path to project directory
            feedback: List of feedback strings from evaluator
            previous_state: Previous iteration state
            iteration: Current iteration number

        Returns:
            Dict with refinement results
        """
        logger.info(f"🔄 Iteration {iteration}: Refining with {self.agent_name}...")

        # Extract context from previous state
        quality_goals = previous_state.get("quality_goals", {})
        failed_tests = previous_state.get("failed_tests", [])

        # Build refinement prompt
        prompt = self._build_refinement_prompt(
            project_path=project_path,
            feedback=feedback,
            goals=quality_goals,
            failed_tests=failed_tests,
            iteration=iteration
        )

        # Execute refinement (via Rover or direct CLI)
        result = self._execute_refinement(
            project_path=project_path,
            prompt=prompt
        )

        # Run tests to evaluate refinement
        test_results = self._run_tests(project_path)

        # Run code analysis
        code_analysis = self._run_code_analysis(project_path)

        # Run security scan
        security = self._run_security_scan(project_path)

        return {
            "tests": test_results,
            "code_analysis": code_analysis,
            "security": security,
            "prompt": prompt,
            "agent": self.agent_name,
        }

    def _build_refinement_prompt(
        self,
        project_path: Path,
        feedback: List[str],
        goals: Dict,
        failed_tests: List[str],
        iteration: int
    ) -> str:
        """Build refinement prompt for agent.

        Args:
            project_path: Project path
            feedback: Feedback from evaluator
            goals: Quality goals
            failed_tests: List of failed test names
            iteration: Iteration number

        Returns:
            Refinement prompt string
        """
        prompt = f"""# Refinement Iteration {iteration}

## Quality Issues to Address

{chr(10).join(f"- {fb}" for fb in feedback)}

## Quality Goals

- Test Coverage: >= {goals.get('min_coverage', 0.60)*100:.0f}%
- Overall Quality: >= {goals.get('min_quality', 0.75)*100:.0f}%
- All Tests Passing: Required
- Security: No vulnerabilities

## Failed Tests

{chr(10).join(f"- {test}" for test in failed_tests) if failed_tests else "None"}

## Instructions

1. Analyze the feedback above
2. Fix all failing tests
3. Improve test coverage to meet goals
4. Address security issues
5. Improve code quality (readability, maintainability)
6. Update documentation if needed

## Important

- Make minimal, targeted changes (don't rewrite everything!)
- Focus on addressing feedback
- Ensure all tests pass before finishing
- Follow LAYER-0 to LAYER-4 guidelines

## Project Path

{project_path}
"""
        return prompt

    def _execute_refinement(
        self,
        project_path: Path,
        prompt: str
    ) -> Dict:
        """Execute refinement via agent.

        Args:
            project_path: Project path
            prompt: Refinement prompt

        Returns:
            Execution result
        """
        # TODO: Integrate with Rover or direct CLI
        # For now, return mock result
        logger.info(f"Executing refinement with {self.agent_name}...")

        # This would call:
        # - Rover CLI: rover task "{prompt}" --agent {self.agent_name}
        # - Or direct: claude/gemini/copilot CLI with prompt

        return {
            "status": "success",
            "message": f"Refinement executed with {self.agent_name}"
        }

    def _run_tests(self, project_path: Path) -> Dict:
        """Run tests and collect results.

        Args:
            project_path: Project path

        Returns:
            Test results dict
        """
        import subprocess
        import json

        logger.info("Running tests...")

        # Detect test framework
        if (project_path / "pytest.ini").exists() or \
           (project_path / "pyproject.toml").exists():
            # Python: pytest
            cmd = [
                "pytest",
                str(project_path / "tests"),
                "--cov=src",
                "--cov-report=json",
                "--json-report",
                "-v"
            ]
        elif (project_path / "package.json").exists():
            # TypeScript/JavaScript: npm test
            cmd = ["npm", "test", "--", "--coverage", "--json"]
        else:
            logger.warning("No test framework detected")
            return {
                "passing": True,
                "total": 0,
                "failed": 0,
                "coverage": 0.0,
                "errors": []
            }

        try:
            result = subprocess.run(
                cmd,
                cwd=project_path,
                capture_output=True,
                text=True,
                timeout=300  # 5 min timeout
            )

            # Parse coverage
            coverage = 0.0
            coverage_file = project_path / "coverage.json"
            if coverage_file.exists():
                with open(coverage_file) as f:
                    cov_data = json.load(f)
                    coverage = cov_data.get("totals", {}).get("percent_covered", 0.0) / 100.0

            # Parse test results
            passing = result.returncode == 0
            # TODO: Parse actual test counts and errors from output

            return {
                "passing": passing,
                "total": 0,  # TODO: Parse from output
                "failed": 0 if passing else 1,
                "coverage": coverage,
                "errors": [] if passing else ["Test failure - see logs"]
            }

        except subprocess.TimeoutExpired:
            logger.error("Tests timed out")
            return {
                "passing": False,
                "total": 0,
                "failed": 1,
                "coverage": 0.0,
                "errors": ["Tests timed out (5 min)"]
            }
        except Exception as e:
            logger.error(f"Test execution failed: {e}")
            return {
                "passing": False,
                "total": 0,
                "failed": 1,
                "coverage": 0.0,
                "errors": [str(e)]
            }

    def _run_code_analysis(self, project_path: Path) -> Dict:
        """Run code quality analysis.

        Args:
            project_path: Project path

        Returns:
            Code analysis results
        """
        # TODO: Integrate with ruff, pylint, eslint, etc.
        logger.info("Running code analysis...")

        return {
            "quality_score": 0.80,  # Mock score
            "complexity": 5,
            "duplications": 0.0
        }

    def _run_security_scan(self, project_path: Path) -> Dict:
        """Run security scan.

        Args:
            project_path: Project path

        Returns:
            Security scan results
        """
        # TODO: Integrate with bandit, semgrep, etc.
        logger.info("Running security scan...")

        return {
            "score": 1.0,  # Mock score
            "vulnerabilities": 0
        }
