#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quality Evaluator - H-Module (High-Level)

Evaluates implementation quality and makes adaptive halting decisions.
"""

import sys
import io
from dataclasses import dataclass
from typing import Dict, Optional
import logging

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

logger = logging.getLogger(__name__)


@dataclass
class QualityMetrics:
    """Quality metrics for code evaluation."""

    # Testing
    test_coverage: float  # 0.0 - 1.0
    tests_passing: bool
    test_count: int
    failed_test_count: int = 0

    # Code Quality
    code_quality_score: float = 0.0  # 0.0 - 1.0 (SonarQube-like)
    complexity: int = 0  # Cyclomatic complexity
    duplications: float = 0.0  # % duplicated code

    # Security
    security_score: float = 1.0  # 0.0 - 1.0 (Bandit/Semgrep)
    vulnerabilities: int = 0

    # Type Safety
    type_coverage: float = 1.0  # mypy coverage
    type_errors: int = 0

    # Documentation
    doc_coverage: float = 0.0  # Docstring coverage

    # Overall
    overall_quality: float = 0.0  # Weighted average

    def __post_init__(self):
        """Calculate overall quality if not provided."""
        if self.overall_quality == 0.0:
            self.overall_quality = self._calculate_overall()

    def _calculate_overall(self) -> float:
        """Calculate weighted overall quality."""
        weights = {
            "test_coverage": 0.25,
            "tests_passing": 0.30,  # Critical!
            "code_quality_score": 0.15,
            "security_score": 0.20,
            "type_coverage": 0.05,
            "doc_coverage": 0.05,
        }

        score = 0.0
        score += self.test_coverage * weights["test_coverage"]
        score += (1.0 if self.tests_passing else 0.0) * weights["tests_passing"]
        score += self.code_quality_score * weights["code_quality_score"]
        score += self.security_score * weights["security_score"]
        score += self.type_coverage * weights["type_coverage"]
        score += self.doc_coverage * weights["doc_coverage"]

        return score


class QualityEvaluator:
    """H-Module: Evaluates quality and decides halting."""

    def __init__(
        self,
        min_coverage: float = 0.60,
        min_quality: float = 0.75,
        max_iterations: int = 5
    ):
        """Initialize quality evaluator.

        Args:
            min_coverage: Minimum acceptable test coverage
            min_quality: Minimum acceptable overall quality
            max_iterations: Maximum refinement iterations
        """
        self.min_coverage = min_coverage
        self.min_quality = min_quality
        self.max_iterations = max_iterations

        # Q-learning weights (can be tuned)
        self.weights = {
            "test_coverage": 0.25,
            "tests_passing": 0.30,
            "security_score": 0.20,
            "code_quality": 0.15,
            "documentation": 0.05,
            "type_safety": 0.05,
        }

    def evaluate_implementation(self, pr_data: Dict) -> QualityMetrics:
        """Evaluate PR quality metrics.

        Args:
            pr_data: Dict containing code, tests, and analysis results

        Returns:
            QualityMetrics object
        """
        # Extract test results
        test_results = pr_data.get("tests", {})
        test_coverage = test_results.get("coverage", 0.0)
        tests_passing = test_results.get("passing", False)
        test_count = test_results.get("total", 0)
        failed_count = test_results.get("failed", 0)

        # Extract code quality
        code_analysis = pr_data.get("code_analysis", {})
        code_quality = code_analysis.get("quality_score", 0.0)
        complexity = code_analysis.get("complexity", 0)
        duplications = code_analysis.get("duplications", 0.0)

        # Extract security
        security = pr_data.get("security", {})
        security_score = security.get("score", 1.0)
        vulnerabilities = security.get("vulnerabilities", 0)

        # Extract type checking
        type_check = pr_data.get("type_check", {})
        type_coverage = type_check.get("coverage", 1.0)
        type_errors = type_check.get("errors", 0)

        # Extract documentation
        doc_analysis = pr_data.get("documentation", {})
        doc_coverage = doc_analysis.get("coverage", 0.0)

        return QualityMetrics(
            test_coverage=test_coverage,
            tests_passing=tests_passing,
            test_count=test_count,
            failed_test_count=failed_count,
            code_quality_score=code_quality,
            complexity=complexity,
            duplications=duplications,
            security_score=security_score,
            vulnerabilities=vulnerabilities,
            type_coverage=type_coverage,
            type_errors=type_errors,
            doc_coverage=doc_coverage,
        )

    def compute_halt_q_value(self, metrics: QualityMetrics) -> float:
        """Compute Q-value for HALT action.

        Args:
            metrics: Quality metrics

        Returns:
            Q-value between 0.0 and 1.0
        """
        q_halt = sum([
            metrics.test_coverage * self.weights["test_coverage"],
            (1.0 if metrics.tests_passing else 0.0) * self.weights["tests_passing"],
            metrics.security_score * self.weights["security_score"],
            metrics.code_quality_score * self.weights["code_quality"],
            metrics.doc_coverage * self.weights["documentation"],
            metrics.type_coverage * self.weights["type_safety"],
        ])

        return q_halt

    def should_halt(
        self,
        metrics: QualityMetrics,
        iteration: int
    ) -> bool:
        """Adaptive halting decision (UltraThink ACT mechanism).

        Args:
            metrics: Current quality metrics
            iteration: Current iteration number

        Returns:
            True if should halt, False to continue
        """
        q_halt = self.compute_halt_q_value(metrics)
        q_continue = 1.0 - q_halt

        logger.info(f"Iteration {iteration}: Q(HALT)={q_halt:.3f}, Q(CONTINUE)={q_continue:.3f}")

        # Condition 1: Q(HALT) > Q(CONTINUE)
        if q_halt > q_continue:
            logger.info(f"✅ Halting: Q(HALT) > Q(CONTINUE)")
            return True

        # Condition 2: Force halt at max iterations
        if iteration >= self.max_iterations:
            logger.warning(f"⚠️ Halting: Max iterations reached ({self.max_iterations})")
            return True

        # Condition 3: Tests passing + good enough quality
        if metrics.tests_passing and q_halt >= self.min_quality:
            logger.info(f"✅ Halting: Tests passing & quality >= {self.min_quality}")
            return True

        # Condition 4: Perfect scores
        if metrics.overall_quality >= 0.95:
            logger.info(f"✅ Halting: Excellent quality ({metrics.overall_quality:.2f})")
            return True

        logger.info(f"🔄 Continuing refinement (quality={q_halt:.3f})")
        return False

    def generate_feedback(
        self,
        metrics: QualityMetrics,
        test_results: Dict
    ) -> list[str]:
        """Generate actionable feedback for refinement.

        Args:
            metrics: Current quality metrics
            test_results: Test execution results

        Returns:
            List of feedback strings
        """
        feedback = []

        # Test coverage feedback
        if metrics.test_coverage < self.min_coverage:
            feedback.append(
                f"Test coverage too low: {metrics.test_coverage*100:.1f}% "
                f"(target: {self.min_coverage*100:.1f}%)"
            )

        # Failing tests
        if not metrics.tests_passing:
            failed_tests = test_results.get("errors", [])
            feedback.append(
                f"{metrics.failed_test_count} tests failing: {', '.join(failed_tests[:3])}"
            )

        # Security issues
        if metrics.vulnerabilities > 0:
            feedback.append(
                f"{metrics.vulnerabilities} security vulnerabilities detected"
            )

        # Code quality
        if metrics.code_quality_score < 0.70:
            feedback.append(
                f"Code quality low: {metrics.code_quality_score*100:.1f}/100"
            )

        # Type errors
        if metrics.type_errors > 0:
            feedback.append(
                f"{metrics.type_errors} type errors detected"
            )

        # Documentation
        if metrics.doc_coverage < 0.50:
            feedback.append(
                f"Documentation incomplete: {metrics.doc_coverage*100:.1f}% coverage"
            )

        return feedback
