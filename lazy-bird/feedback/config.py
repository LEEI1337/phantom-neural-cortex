#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Feedback Loop Configuration

Zentrale Konfiguration für Quality Weights und System-Parameter.
"""


class QualityWeights:
    """
    Zentrale Gewichtungs-Konfiguration für Q-Learning.

    Diese Gewichtungen werden sowohl in QualityMetrics als auch
    in QualityEvaluator verwendet, um Duplikation zu vermeiden.
    """

    # Core Metrics (Summe MUSS 1.0 sein!)
    TEST_COVERAGE = 0.25        # 25% - Test Abdeckung
    TESTS_PASSING = 0.30        # 30% - Tests bestehen (KRITISCH!)
    SECURITY = 0.20             # 20% - Sicherheit
    CODE_QUALITY = 0.15         # 15% - Code Qualität
    TYPE_SAFETY = 0.05          # 5%  - Type Coverage
    DOCUMENTATION = 0.05        # 5%  - Dokumentation

    @classmethod
    def as_dict(cls) -> dict[str, float]:
        """Gewichtungen als Dictionary."""
        return {
            "test_coverage": cls.TEST_COVERAGE,
            "tests_passing": cls.TESTS_PASSING,
            "security": cls.SECURITY,
            "code_quality": cls.CODE_QUALITY,
            "type_safety": cls.TYPE_SAFETY,
            "documentation": cls.DOCUMENTATION,
        }

    @classmethod
    def as_tuple(cls) -> tuple[float, ...]:
        """Gewichtungen als Tuple (für Performance)."""
        return (
            cls.TEST_COVERAGE,
            cls.TESTS_PASSING,
            cls.SECURITY,
            cls.CODE_QUALITY,
            cls.DOCUMENTATION,
            cls.TYPE_SAFETY,
        )

    @classmethod
    def validate(cls) -> None:
        """
        Validiere dass Gewichtungen = 1.0.

        Raises:
            AssertionError: Wenn Summe != 1.0
        """
        total = (
            cls.TEST_COVERAGE +
            cls.TESTS_PASSING +
            cls.SECURITY +
            cls.CODE_QUALITY +
            cls.TYPE_SAFETY +
            cls.DOCUMENTATION
        )

        tolerance = 0.0001
        assert abs(total - 1.0) < tolerance, (
            f"Quality weights must sum to 1.0, got {total:.4f}. "
            f"Difference: {abs(total - 1.0):.6f}"
        )


class CriticalPenalties:
    """
    Kritische Penalties für Quality Metrics.

    Diese werden multiplicativ auf den Q-Value angewendet,
    um kritische Issues härter zu bestrafen.
    """

    # Security: Jede Vulnerability reduziert Score um 10%
    SECURITY_VULNERABILITY_PENALTY = 0.10
    MAX_SECURITY_PENALTY = 0.50  # Max 50% Reduktion

    # Type Errors: Jeder Error reduziert Score um 5%
    TYPE_ERROR_PENALTY = 0.05
    MAX_TYPE_ERROR_PENALTY = 0.30  # Max 30% Reduktion

    # Failing Tests: Ab 3 failing tests → 50% Penalty
    CRITICAL_TEST_THRESHOLD = 3
    CRITICAL_TEST_PENALTY = 0.50  # Halbiere Score!

    # Complexity: Ab Complexity 15 → Penalty
    COMPLEXITY_THRESHOLD = 15
    COMPLEXITY_PENALTY_PER_UNIT = 0.02  # 2% pro Unit über Threshold
    MAX_COMPLEXITY_PENALTY = 0.20  # Max 20% Reduktion

    @classmethod
    def compute_security_penalty(cls, vulnerabilities: int) -> float:
        """
        Berechne Security Penalty.

        Args:
            vulnerabilities: Anzahl der Vulnerabilities

        Returns:
            Penalty factor (0.5 - 1.0)
        """
        if vulnerabilities == 0:
            return 1.0

        penalty = 1.0 - min(
            vulnerabilities * cls.SECURITY_VULNERABILITY_PENALTY,
            cls.MAX_SECURITY_PENALTY
        )

        return max(penalty, 0.5)  # Min 50% vom Score

    @classmethod
    def compute_type_error_penalty(cls, type_errors: int) -> float:
        """
        Berechne Type Error Penalty.

        Args:
            type_errors: Anzahl der Type Errors

        Returns:
            Penalty factor (0.7 - 1.0)
        """
        if type_errors == 0:
            return 1.0

        penalty = 1.0 - min(
            type_errors * cls.TYPE_ERROR_PENALTY,
            cls.MAX_TYPE_ERROR_PENALTY
        )

        return max(penalty, 0.7)  # Min 70% vom Score

    @classmethod
    def compute_failing_tests_penalty(cls, failed_count: int) -> float:
        """
        Berechne Failing Tests Penalty.

        Args:
            failed_count: Anzahl failing tests

        Returns:
            Penalty factor (0.5 - 1.0)
        """
        if failed_count == 0:
            return 1.0

        if failed_count >= cls.CRITICAL_TEST_THRESHOLD:
            return cls.CRITICAL_TEST_PENALTY  # 50% Penalty!

        # Linear: 1-2 tests → 10-20% Penalty
        return 1.0 - (failed_count * 0.10)

    @classmethod
    def compute_complexity_penalty(cls, complexity: int) -> float:
        """
        Berechne Complexity Penalty.

        Args:
            complexity: Cyclomatic complexity

        Returns:
            Penalty factor (0.8 - 1.0)
        """
        if complexity <= cls.COMPLEXITY_THRESHOLD:
            return 1.0

        excess = complexity - cls.COMPLEXITY_THRESHOLD
        penalty = 1.0 - min(
            excess * cls.COMPLEXITY_PENALTY_PER_UNIT,
            cls.MAX_COMPLEXITY_PENALTY
        )

        return max(penalty, 0.8)  # Min 80% vom Score


class AdaptiveLimits:
    """
    Adaptive Limits basierend auf Projekt-Komplexität.
    """

    SIMPLE = {
        "max_iterations": 3,
        "max_time": 600,        # 10 minutes
        "max_cost": 2.0,        # $2
        "min_quality": 0.70,    # 70% quality
        "stagnation_window": 2,
    }

    MEDIUM = {
        "max_iterations": 5,
        "max_time": 1800,       # 30 minutes
        "max_cost": 5.0,        # $5
        "min_quality": 0.75,    # 75% quality
        "stagnation_window": 3,
    }

    COMPLEX = {
        "max_iterations": 8,
        "max_time": 3600,       # 60 minutes
        "max_cost": 10.0,       # $10
        "min_quality": 0.80,    # 80% quality
        "stagnation_window": 4,
    }

    @classmethod
    def get_limits(cls, complexity: str) -> dict:
        """
        Get limits for complexity level.

        Args:
            complexity: "simple", "medium", or "complex"

        Returns:
            Dict with limits

        Raises:
            ValueError: If complexity unknown
        """
        limits = {
            "simple": cls.SIMPLE,
            "medium": cls.MEDIUM,
            "complex": cls.COMPLEX,
        }

        if complexity not in limits:
            raise ValueError(
                f"Unknown complexity: {complexity}. "
                f"Must be one of: {list(limits.keys())}"
            )

        return limits[complexity]


# Validate on import
QualityWeights.validate()
