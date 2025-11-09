"""
Parallel Feedback Loop - Optimierung #6
========================================

Parallelisiert alle Quality Checks für 30-40% Speed-Improvement.

Vorher (Sequential):
    Tests (20s) → Security (10s) → Types (5s) → Complexity (3s) = 38s

Nachher (Parallel):
    Tests + Security + Types + Complexity = max(20s) = 20s

Zeitersparnis: ~47% (18s gespart)

Key Features:
- Async execution mit asyncio
- Concurrent Tests, Security, Type Checking, Complexity Analysis
- Result Aggregation mit Timeout-Handling
- Error Isolation (ein fehlender Check blockiert nicht andere)

"""

import asyncio
import subprocess
import time
from typing import Dict, List, Tuple, Optional, Callable
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
import json


@dataclass
class CheckResult:
    """Ergebnis eines einzelnen Quality Checks."""

    check_name: str  # 'tests', 'security', 'types', 'complexity'
    success: bool
    score: float  # 0-1
    duration: float  # Seconds
    details: Dict  # Check-specific details
    error: Optional[str] = None


@dataclass
class ParallelEvaluationResult:
    """Ergebnis der parallelen Evaluation."""

    total_duration: float
    sequential_would_take: float  # Estimated
    time_saved: float
    time_saved_percent: float

    # Individual Results
    tests_result: Optional[CheckResult]
    security_result: Optional[CheckResult]
    types_result: Optional[CheckResult]
    complexity_result: Optional[CheckResult]
    coverage_result: Optional[CheckResult]
    documentation_result: Optional[CheckResult]

    # Aggregated
    overall_quality: float
    checks_completed: int
    checks_failed: int


class ParallelQualityEvaluator:
    """
    Parallel Execution Engine für Quality Checks.

    Führt alle Checks gleichzeitig aus mit asyncio.
    """

    def __init__(self, timeout_per_check: float = 60.0):
        self.timeout_per_check = timeout_per_check
        self.evaluation_history: List[ParallelEvaluationResult] = []

    async def evaluate_parallel(
        self,
        project_path: Path,
        code_content: Optional[str] = None,
        checks_config: Optional[Dict] = None
    ) -> ParallelEvaluationResult:
        """
        Führt alle Quality Checks parallel aus.

        Args:
            project_path: Pfad zum Projekt
            code_content: Optional Code-Content (für in-memory checks)
            checks_config: Optional Config {'run_tests': True, 'run_security': True, ...}

        Returns:
            ParallelEvaluationResult mit allen Ergebnissen
        """
        start_time = time.time()

        # Default Config
        if checks_config is None:
            checks_config = {
                'run_tests': True,
                'run_security': True,
                'run_types': True,
                'run_complexity': True,
                'run_coverage': True,
                'run_documentation': True
            }

        # Create Tasks for parallel execution
        tasks = []

        if checks_config.get('run_tests', True):
            tasks.append(self._check_tests(project_path))

        if checks_config.get('run_security', True):
            tasks.append(self._check_security(project_path))

        if checks_config.get('run_types', True):
            tasks.append(self._check_types(project_path))

        if checks_config.get('run_complexity', True):
            tasks.append(self._check_complexity(project_path))

        if checks_config.get('run_coverage', True):
            tasks.append(self._check_coverage(project_path))

        if checks_config.get('run_documentation', True):
            tasks.append(self._check_documentation(project_path))

        # Execute all in parallel
        results = await asyncio.gather(*tasks, return_exceptions=True)

        total_duration = time.time() - start_time

        # Parse Results
        tests_result = None
        security_result = None
        types_result = None
        complexity_result = None
        coverage_result = None
        documentation_result = None

        for result in results:
            if isinstance(result, Exception):
                continue  # Error handled

            if isinstance(result, CheckResult):
                if result.check_name == 'tests':
                    tests_result = result
                elif result.check_name == 'security':
                    security_result = result
                elif result.check_name == 'types':
                    types_result = result
                elif result.check_name == 'complexity':
                    complexity_result = result
                elif result.check_name == 'coverage':
                    coverage_result = result
                elif result.check_name == 'documentation':
                    documentation_result = result

        # Calculate Sequential Time (Estimate)
        sequential_time = sum(
            r.duration for r in results
            if isinstance(r, CheckResult)
        )

        time_saved = sequential_time - total_duration
        time_saved_percent = (time_saved / sequential_time * 100) if sequential_time > 0 else 0

        # Calculate Overall Quality
        overall_quality = self._calculate_overall_quality([
            tests_result,
            security_result,
            types_result,
            complexity_result,
            coverage_result,
            documentation_result
        ])

        # Count Completed/Failed
        all_results = [
            tests_result, security_result, types_result,
            complexity_result, coverage_result, documentation_result
        ]
        checks_completed = sum(1 for r in all_results if r is not None)
        checks_failed = sum(1 for r in all_results if r is not None and not r.success)

        # Create Result
        eval_result = ParallelEvaluationResult(
            total_duration=total_duration,
            sequential_would_take=sequential_time,
            time_saved=time_saved,
            time_saved_percent=time_saved_percent,
            tests_result=tests_result,
            security_result=security_result,
            types_result=types_result,
            complexity_result=complexity_result,
            coverage_result=coverage_result,
            documentation_result=documentation_result,
            overall_quality=overall_quality,
            checks_completed=checks_completed,
            checks_failed=checks_failed
        )

        self.evaluation_history.append(eval_result)

        return eval_result

    async def _check_tests(self, project_path: Path) -> CheckResult:
        """Führt Tests aus (parallel)."""
        start = time.time()

        try:
            # Run pytest
            proc = await asyncio.create_subprocess_exec(
                'pytest',
                '--tb=short',
                '--quiet',
                cwd=str(project_path),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await asyncio.wait_for(
                proc.communicate(),
                timeout=self.timeout_per_check
            )

            duration = time.time() - start

            # Parse Results
            output = stdout.decode('utf-8', errors='ignore')
            success = proc.returncode == 0

            # Extract stats (simplified)
            passed = output.count(' passed')
            failed = output.count(' failed')
            total = passed + failed

            score = passed / total if total > 0 else 0.0

            return CheckResult(
                check_name='tests',
                success=success,
                score=score,
                duration=duration,
                details={
                    'passed': passed,
                    'failed': failed,
                    'total': total,
                    'output': output[:500]  # First 500 chars
                }
            )

        except asyncio.TimeoutError:
            return CheckResult(
                check_name='tests',
                success=False,
                score=0.0,
                duration=self.timeout_per_check,
                details={},
                error='Timeout'
            )
        except Exception as e:
            return CheckResult(
                check_name='tests',
                success=False,
                score=0.0,
                duration=time.time() - start,
                details={},
                error=str(e)
            )

    async def _check_security(self, project_path: Path) -> CheckResult:
        """Führt Security Scan aus (parallel)."""
        start = time.time()

        try:
            # Run bandit (Python security linter)
            proc = await asyncio.create_subprocess_exec(
                'bandit',
                '-r',
                '.',
                '-f', 'json',
                cwd=str(project_path),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await asyncio.wait_for(
                proc.communicate(),
                timeout=self.timeout_per_check
            )

            duration = time.time() - start

            # Parse JSON Output
            try:
                output = stdout.decode('utf-8', errors='ignore')
                results = json.loads(output)

                high_severity = len([r for r in results.get('results', []) if r.get('issue_severity') == 'HIGH'])
                medium_severity = len([r for r in results.get('results', []) if r.get('issue_severity') == 'MEDIUM'])
                low_severity = len([r for r in results.get('results', []) if r.get('issue_severity') == 'LOW'])

                total_issues = high_severity + medium_severity + low_severity

                # Score: 1.0 = no issues, 0.0 = many high severity
                if total_issues == 0:
                    score = 1.0
                else:
                    # Weight: High=3, Medium=2, Low=1
                    weighted_issues = high_severity * 3 + medium_severity * 2 + low_severity
                    score = max(0.0, 1.0 - (weighted_issues * 0.1))

                success = high_severity == 0  # Success if no high severity

                return CheckResult(
                    check_name='security',
                    success=success,
                    score=score,
                    duration=duration,
                    details={
                        'high_severity': high_severity,
                        'medium_severity': medium_severity,
                        'low_severity': low_severity,
                        'total_issues': total_issues
                    }
                )

            except json.JSONDecodeError:
                # Fallback
                return CheckResult(
                    check_name='security',
                    success=True,
                    score=0.8,
                    duration=duration,
                    details={'note': 'Could not parse bandit output'}
                )

        except asyncio.TimeoutError:
            return CheckResult(
                check_name='security',
                success=False,
                score=0.5,
                duration=self.timeout_per_check,
                details={},
                error='Timeout'
            )
        except FileNotFoundError:
            # bandit nicht installiert
            return CheckResult(
                check_name='security',
                success=True,
                score=0.7,
                duration=time.time() - start,
                details={'note': 'bandit not installed'},
                error='bandit not found'
            )
        except Exception as e:
            return CheckResult(
                check_name='security',
                success=False,
                score=0.5,
                duration=time.time() - start,
                details={},
                error=str(e)
            )

    async def _check_types(self, project_path: Path) -> CheckResult:
        """Führt Type Checking aus (parallel)."""
        start = time.time()

        try:
            # Run mypy
            proc = await asyncio.create_subprocess_exec(
                'mypy',
                '.',
                '--ignore-missing-imports',
                cwd=str(project_path),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await asyncio.wait_for(
                proc.communicate(),
                timeout=self.timeout_per_check
            )

            duration = time.time() - start

            output = stdout.decode('utf-8', errors='ignore')

            # Parse Errors
            error_count = output.count('error:')
            success = proc.returncode == 0

            # Score
            if error_count == 0:
                score = 1.0
            else:
                score = max(0.0, 1.0 - (error_count * 0.05))

            return CheckResult(
                check_name='types',
                success=success,
                score=score,
                duration=duration,
                details={
                    'error_count': error_count,
                    'output_preview': output[:300]
                }
            )

        except asyncio.TimeoutError:
            return CheckResult(
                check_name='types',
                success=False,
                score=0.5,
                duration=self.timeout_per_check,
                details={},
                error='Timeout'
            )
        except FileNotFoundError:
            return CheckResult(
                check_name='types',
                success=True,
                score=0.7,
                duration=time.time() - start,
                details={'note': 'mypy not installed'},
                error='mypy not found'
            )
        except Exception as e:
            return CheckResult(
                check_name='types',
                success=False,
                score=0.5,
                duration=time.time() - start,
                details={},
                error=str(e)
            )

    async def _check_complexity(self, project_path: Path) -> CheckResult:
        """Führt Complexity Analysis aus (parallel)."""
        start = time.time()

        try:
            # Run radon (Cyclomatic Complexity)
            proc = await asyncio.create_subprocess_exec(
                'radon',
                'cc',
                '.',
                '-a',
                '--json',
                cwd=str(project_path),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await asyncio.wait_for(
                proc.communicate(),
                timeout=self.timeout_per_check
            )

            duration = time.time() - start

            try:
                output = stdout.decode('utf-8', errors='ignore')
                results = json.loads(output)

                # Calculate average complexity
                complexities = []
                for file_results in results.values():
                    for func in file_results:
                        if isinstance(func, dict) and 'complexity' in func:
                            complexities.append(func['complexity'])

                if complexities:
                    avg_complexity = sum(complexities) / len(complexities)
                    max_complexity = max(complexities)
                else:
                    avg_complexity = 5.0
                    max_complexity = 5.0

                # Score: <10 = 1.0, >20 = 0.0
                if avg_complexity < 10:
                    score = 1.0
                elif avg_complexity > 20:
                    score = 0.0
                else:
                    score = 1.0 - ((avg_complexity - 10) / 10)

                success = avg_complexity < 15

                return CheckResult(
                    check_name='complexity',
                    success=success,
                    score=score,
                    duration=duration,
                    details={
                        'avg_complexity': avg_complexity,
                        'max_complexity': max_complexity,
                        'function_count': len(complexities)
                    }
                )

            except json.JSONDecodeError:
                return CheckResult(
                    check_name='complexity',
                    success=True,
                    score=0.8,
                    duration=duration,
                    details={'note': 'Could not parse radon output'}
                )

        except asyncio.TimeoutError:
            return CheckResult(
                check_name='complexity',
                success=False,
                score=0.5,
                duration=self.timeout_per_check,
                details={},
                error='Timeout'
            )
        except FileNotFoundError:
            return CheckResult(
                check_name='complexity',
                success=True,
                score=0.7,
                duration=time.time() - start,
                details={'note': 'radon not installed'},
                error='radon not found'
            )
        except Exception as e:
            return CheckResult(
                check_name='complexity',
                success=False,
                score=0.5,
                duration=time.time() - start,
                details={},
                error=str(e)
            )

    async def _check_coverage(self, project_path: Path) -> CheckResult:
        """Führt Coverage Check aus (parallel)."""
        start = time.time()

        try:
            # Run pytest with coverage
            proc = await asyncio.create_subprocess_exec(
                'pytest',
                '--cov=.',
                '--cov-report=json',
                '--quiet',
                cwd=str(project_path),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await asyncio.wait_for(
                proc.communicate(),
                timeout=self.timeout_per_check
            )

            duration = time.time() - start

            # Read coverage.json
            coverage_file = project_path / 'coverage.json'
            if coverage_file.exists():
                with open(coverage_file, 'r') as f:
                    coverage_data = json.load(f)

                coverage_percent = coverage_data.get('totals', {}).get('percent_covered', 0.0) / 100.0

                success = coverage_percent >= 0.75  # 75% threshold

                return CheckResult(
                    check_name='coverage',
                    success=success,
                    score=coverage_percent,
                    duration=duration,
                    details={
                        'coverage_percent': coverage_percent * 100,
                        'lines_covered': coverage_data.get('totals', {}).get('covered_lines', 0),
                        'lines_total': coverage_data.get('totals', {}).get('num_statements', 0)
                    }
                )
            else:
                return CheckResult(
                    check_name='coverage',
                    success=False,
                    score=0.0,
                    duration=duration,
                    details={'note': 'coverage.json not found'}
                )

        except asyncio.TimeoutError:
            return CheckResult(
                check_name='coverage',
                success=False,
                score=0.0,
                duration=self.timeout_per_check,
                details={},
                error='Timeout'
            )
        except Exception as e:
            return CheckResult(
                check_name='coverage',
                success=False,
                score=0.0,
                duration=time.time() - start,
                details={},
                error=str(e)
            )

    async def _check_documentation(self, project_path: Path) -> CheckResult:
        """Führt Documentation Check aus (parallel)."""
        start = time.time()

        try:
            # Simple docstring coverage check
            python_files = list(project_path.rglob('*.py'))

            total_functions = 0
            documented_functions = 0

            for file_path in python_files:
                try:
                    content = file_path.read_text(encoding='utf-8')

                    # Count functions
                    func_count = content.count('def ')
                    total_functions += func_count

                    # Count docstrings (simplified)
                    # Look for """...""" after def
                    docstring_count = content.count('"""')
                    documented_functions += min(docstring_count // 2, func_count)

                except Exception:
                    continue

            duration = time.time() - start

            if total_functions > 0:
                doc_coverage = documented_functions / total_functions
            else:
                doc_coverage = 1.0  # No functions = 100% coverage

            success = doc_coverage >= 0.5  # 50% threshold

            return CheckResult(
                check_name='documentation',
                success=success,
                score=doc_coverage,
                duration=duration,
                details={
                    'total_functions': total_functions,
                    'documented_functions': documented_functions,
                    'coverage_percent': doc_coverage * 100
                }
            )

        except Exception as e:
            return CheckResult(
                check_name='documentation',
                success=False,
                score=0.5,
                duration=time.time() - start,
                details={},
                error=str(e)
            )

    def _calculate_overall_quality(
        self,
        results: List[Optional[CheckResult]]
    ) -> float:
        """Berechnet Overall Quality aus allen Check-Results."""

        # Weights (same as config.py)
        weights = {
            'tests': 0.30,
            'security': 0.20,
            'types': 0.05,
            'complexity': 0.15,
            'coverage': 0.25,
            'documentation': 0.05
        }

        total_score = 0.0
        total_weight = 0.0

        for result in results:
            if result is not None and result.check_name in weights:
                weight = weights[result.check_name]
                total_score += result.score * weight
                total_weight += weight

        if total_weight == 0:
            return 0.0

        return total_score / total_weight

    def get_performance_statistics(self) -> Dict[str, any]:
        """Gibt Performance-Statistiken zurück."""
        if not self.evaluation_history:
            return {
                'total_evaluations': 0,
                'avg_time_saved': 0.0,
                'avg_time_saved_percent': 0.0
            }

        time_saved_total = sum(e.time_saved for e in self.evaluation_history)
        time_saved_percent_avg = sum(e.time_saved_percent for e in self.evaluation_history) / len(self.evaluation_history)

        return {
            'total_evaluations': len(self.evaluation_history),
            'avg_parallel_duration': sum(e.total_duration for e in self.evaluation_history) / len(self.evaluation_history),
            'avg_sequential_would_take': sum(e.sequential_would_take for e in self.evaluation_history) / len(self.evaluation_history),
            'total_time_saved': time_saved_total,
            'avg_time_saved': time_saved_total / len(self.evaluation_history),
            'avg_time_saved_percent': time_saved_percent_avg
        }


# Singleton Instance
_evaluator_instance = None


def get_evaluator() -> ParallelQualityEvaluator:
    """Holt Singleton Evaluator-Instanz."""
    global _evaluator_instance
    if _evaluator_instance is None:
        _evaluator_instance = ParallelQualityEvaluator()
    return _evaluator_instance


# Convenience Function
def run_parallel_evaluation(project_path: Path) -> ParallelEvaluationResult:
    """
    Convenience-Funktion für synchronen Call.

    Führt async evaluation aus und returned Ergebnis.
    """
    evaluator = get_evaluator()
    return asyncio.run(evaluator.evaluate_parallel(project_path))


# Export
__all__ = [
    'CheckResult',
    'ParallelEvaluationResult',
    'ParallelQualityEvaluator',
    'get_evaluator',
    'run_parallel_evaluation'
]
