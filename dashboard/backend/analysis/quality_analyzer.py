"""
CodeAssist-Inspired Quality Analyzer

Real-time code quality assessment with Reward/Penalty scoring system.
Inspired by CodeAssist's keystroke-level feedback mechanism, but integrated
directly into the orchestration layer.
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import re
import ast
import logging

logger = logging.getLogger(__name__)


@dataclass
class QualityReward:
    """A positive quality signal."""
    category: str  # "best_practice", "security", "performance", "readability"
    score: float  # 0.0 - 1.0
    description: str
    code_snippet: Optional[str] = None


@dataclass
class QualityPenalty:
    """A negative quality signal."""
    category: str  # "anti_pattern", "security_risk", "performance_issue", "readability_issue"
    score: float  # -1.0 - 0.0
    description: str
    code_snippet: Optional[str] = None
    suggestion: Optional[str] = None


@dataclass
class QualityAnalysis:
    """Complete quality analysis result."""
    overall_score: float  # -1.0 to 1.0
    rewards: List[QualityReward]
    penalties: List[QualityPenalty]
    detected_patterns: List[str]
    language: str
    timestamp: datetime


class QualityAnalyzer:
    """
    Analyzes code quality and provides reward/penalty feedback.

    Inspired by CodeAssist's continuous learning approach, but designed
    for batch analysis of agent outputs rather than keystroke tracking.
    """

    def __init__(self):
        self.language_detectors = {
            "python": self._detect_python,
            "javascript": self._detect_javascript,
            "typescript": self._detect_typescript,
        }

    async def analyze(
        self,
        code: str,
        context: str,
        task_type: str,
        language: Optional[str] = None
    ) -> QualityAnalysis:
        """
        Analyze code quality and return reward/penalty breakdown.

        Args:
            code: The code to analyze
            context: Task context/prompt
            task_type: Type of task (security, refactoring, etc.)
            language: Programming language (auto-detected if None)

        Returns:
            QualityAnalysis with detailed feedback
        """
        # Auto-detect language if not provided
        if not language:
            language = self._detect_language(code)

        rewards = []
        penalties = []
        patterns = []

        # Run language-specific analysis
        if language == "python":
            lang_rewards, lang_penalties, lang_patterns = await self._analyze_python(
                code, context, task_type
            )
            rewards.extend(lang_rewards)
            penalties.extend(lang_penalties)
            patterns.extend(lang_patterns)

        # Run universal code quality checks
        universal_rewards, universal_penalties = self._analyze_universal(code)
        rewards.extend(universal_rewards)
        penalties.extend(universal_penalties)

        # Calculate overall score
        total_reward = sum(r.score for r in rewards)
        total_penalty = sum(p.score for p in penalties)
        overall_score = max(-1.0, min(1.0, total_reward + total_penalty))

        return QualityAnalysis(
            overall_score=overall_score,
            rewards=rewards,
            penalties=penalties,
            detected_patterns=patterns,
            language=language,
            timestamp=datetime.utcnow()
        )

    def _detect_language(self, code: str) -> str:
        """Auto-detect programming language."""
        # Simple heuristics
        if "def " in code or "import " in code or "class " in code:
            return "python"
        elif "function" in code or "const " in code or "let " in code:
            if ": " in code and "interface" in code:
                return "typescript"
            return "javascript"
        return "unknown"

    async def _analyze_python(
        self,
        code: str,
        context: str,
        task_type: str
    ) -> Tuple[List[QualityReward], List[QualityPenalty], List[str]]:
        """Python-specific analysis."""
        rewards = []
        penalties = []
        patterns = []

        # Try to parse as AST
        try:
            tree = ast.parse(code)

            # Reward: Has docstrings
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                    if ast.get_docstring(node):
                        rewards.append(QualityReward(
                            category="readability",
                            score=0.15,
                            description=f"Docstring present for {node.name}",
                            code_snippet=ast.get_docstring(node)[:100]
                        ))
                        patterns.append("documented_functions")

            # Reward: Type hints
            type_hint_count = 0
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if node.returns is not None:
                        type_hint_count += 1
                    if any(arg.annotation for arg in node.args.args):
                        type_hint_count += 1

            if type_hint_count > 0:
                rewards.append(QualityReward(
                    category="best_practice",
                    score=0.2,
                    description=f"Type hints used ({type_hint_count} locations)",
                ))
                patterns.append("type_hints")

            # Reward: Error handling
            for node in ast.walk(tree):
                if isinstance(node, ast.Try):
                    rewards.append(QualityReward(
                        category="best_practice",
                        score=0.15,
                        description="Error handling with try/except",
                    ))
                    patterns.append("error_handling")
                    break

            # Penalty: Very long functions
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func_lines = len(ast.unparse(node).split('\n'))
                    if func_lines > 50:
                        penalties.append(QualityPenalty(
                            category="readability_issue",
                            score=-0.2,
                            description=f"Function {node.name} is very long ({func_lines} lines)",
                            suggestion="Consider breaking into smaller functions"
                        ))
                        patterns.append("long_functions")

        except SyntaxError as e:
            penalties.append(QualityPenalty(
                category="syntax_error",
                score=-0.5,
                description=f"Syntax error: {str(e)}",
                suggestion="Fix syntax errors before proceeding"
            ))

        # Security checks
        if "eval(" in code or "exec(" in code:
            penalties.append(QualityPenalty(
                category="security_risk",
                score=-0.8,
                description="Use of eval() or exec() detected",
                suggestion="Avoid eval/exec - major security risk"
            ))
            patterns.append("security_risk_eval")

        # Check for SQL injection vulnerability patterns
        if re.search(r'execute\s*\(\s*["\'].*%s.*["\']', code):
            penalties.append(QualityPenalty(
                category="security_risk",
                score=-0.9,
                description="Potential SQL injection vulnerability",
                suggestion="Use parameterized queries"
            ))
            patterns.append("sql_injection_risk")

        # Reward: Async/await usage (for async tasks)
        if "async def" in code and "await" in code:
            rewards.append(QualityReward(
                category="best_practice",
                score=0.2,
                description="Proper async/await usage",
            ))
            patterns.append("async_pattern")

        return rewards, penalties, patterns

    def _analyze_universal(self, code: str) -> Tuple[List[QualityReward], List[QualityPenalty]]:
        """Universal code quality checks (any language)."""
        rewards = []
        penalties = []

        # Reward: Has comments
        comment_lines = len([line for line in code.split('\n') if line.strip().startswith('#')])
        if comment_lines > 0:
            rewards.append(QualityReward(
                category="readability",
                score=min(0.15, comment_lines * 0.03),
                description=f"Code has {comment_lines} comment lines",
            ))

        # Penalty: Very long lines
        long_lines = [i for i, line in enumerate(code.split('\n'), 1) if len(line) > 120]
        if long_lines:
            penalties.append(QualityPenalty(
                category="readability_issue",
                score=-0.1,
                description=f"{len(long_lines)} lines exceed 120 characters",
                suggestion="Break long lines for better readability"
            ))

        # Reward: Consistent indentation
        lines = [line for line in code.split('\n') if line.strip()]
        if lines:
            indent_chars = set()
            for line in lines:
                if line[0] in (' ', '\t'):
                    indent_chars.add(line[0])

            if len(indent_chars) <= 1:  # Consistent
                rewards.append(QualityReward(
                    category="readability",
                    score=0.1,
                    description="Consistent indentation",
                ))

        # Penalty: Hardcoded credentials patterns
        credential_patterns = [
            r'password\s*=\s*["\'][^"\']+["\']',
            r'api[_-]?key\s*=\s*["\'][^"\']+["\']',
            r'secret\s*=\s*["\'][^"\']+["\']',
            r'token\s*=\s*["\'][^"\']+["\']',
        ]

        for pattern in credential_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                penalties.append(QualityPenalty(
                    category="security_risk",
                    score=-0.7,
                    description="Hardcoded credentials detected",
                    suggestion="Use environment variables or secure vaults"
                ))
                break

        return rewards, penalties

    async def _detect_python(self, code: str) -> bool:
        """Detect if code is Python."""
        try:
            ast.parse(code)
            return True
        except:
            return False

    async def _detect_javascript(self, code: str) -> bool:
        """Detect if code is JavaScript."""
        # Simple heuristics
        js_keywords = ["function", "const", "let", "var", "=>"]
        return any(kw in code for kw in js_keywords)

    async def _detect_typescript(self, code: str) -> bool:
        """Detect if code is TypeScript."""
        # TypeScript-specific patterns
        ts_patterns = [": ", "interface ", "type ", "<", ">"]
        return await self._detect_javascript(code) and any(p in code for p in ts_patterns)


# Global analyzer instance
_analyzer: Optional[QualityAnalyzer] = None


def get_quality_analyzer() -> QualityAnalyzer:
    """Get global quality analyzer instance."""
    global _analyzer

    if _analyzer is None:
        _analyzer = QualityAnalyzer()

    return _analyzer
