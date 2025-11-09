"""
Inference-Time Scaling - Optimierung #2
========================================

Inspiriert von HRM's Generalisierung zu höheren Rechenlimits während Deployment.
Lernt optimale Iterations-Limits basierend auf Task-Komplexität.

Key Features:
- ML-Modell (Random Forest) prediziert optimale Iteration-Count
- Features: Code complexity, file count, test count, label complexity
- Training auf historischen Daten
- Adaptive Max-Iteration statt fixe 5

Beispiel:
    Einfache Bugfix → 2 Iterationen predicted
    Komplexes Feature → 8 Iterationen predicted
    Statt IMMER 5 Iterationen

"""

import json
import pickle
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
from datetime import datetime
import numpy as np


@dataclass
class TaskComplexity:
    """Features für Task-Komplexität."""

    # Code-basierte Features
    total_files: int
    total_lines: int
    function_count: int
    class_count: int
    avg_cyclomatic_complexity: float

    # Test-basierte Features
    test_files: int
    test_count: int
    existing_coverage: float

    # Issue/Label-basierte Features
    label_count: int
    label_complexity_score: float  # 0-1, berechnet aus Labels
    issue_description_length: int

    # Historische Features (wenn verfügbar)
    similar_tasks_avg_iterations: Optional[float] = None

    # Ground Truth (für Training)
    actual_iterations_needed: Optional[int] = None
    final_quality_achieved: Optional[float] = None


class IterationPredictor:
    """
    ML-Modell für Prediction optimaler Iteration-Counts.

    Verwendet Random Forest für robuste Predictions.
    """

    def __init__(self, model_path: Optional[Path] = None):
        self.model_path = model_path or Path(__file__).parent / "models" / "iteration_predictor.pkl"
        self.model = None
        self.feature_scaler = None
        self.training_history: List[TaskComplexity] = []

        # Label Complexity Mapping
        self.label_weights = {
            # High complexity
            'security': 1.0,
            'architecture': 0.9,
            'refactoring': 0.8,
            'performance': 0.8,

            # Medium complexity
            'feature': 0.6,
            'enhancement': 0.5,
            'api': 0.5,

            # Low complexity
            'bug': 0.3,
            'documentation': 0.2,
            'style': 0.1,
            'typo': 0.1
        }

        # Load existierendes Modell wenn vorhanden
        if self.model_path.exists():
            self._load_model()

    def extract_features(
        self,
        code_stats: Dict,
        test_stats: Dict,
        issue_info: Dict
    ) -> TaskComplexity:
        """
        Extrahiert Features aus Task-Information.

        Args:
            code_stats: {'files': int, 'lines': int, 'functions': int, ...}
            test_stats: {'test_files': int, 'test_count': int, 'coverage': float}
            issue_info: {'labels': List[str], 'description': str}

        Returns:
            TaskComplexity Objekt mit allen Features
        """
        # Label Complexity berechnen
        labels = issue_info.get('labels', [])
        label_complexity = self._calculate_label_complexity(labels)

        # Cyclomatic Complexity schätzen (vereinfacht)
        avg_complexity = self._estimate_cyclomatic_complexity(code_stats)

        # Ähnliche Tasks finden (wenn Trainingshistorie vorhanden)
        similar_avg = self._find_similar_tasks_avg(code_stats, test_stats)

        return TaskComplexity(
            total_files=code_stats.get('files', 1),
            total_lines=code_stats.get('lines', 100),
            function_count=code_stats.get('functions', 5),
            class_count=code_stats.get('classes', 1),
            avg_cyclomatic_complexity=avg_complexity,
            test_files=test_stats.get('test_files', 0),
            test_count=test_stats.get('test_count', 0),
            existing_coverage=test_stats.get('coverage', 0.0),
            label_count=len(labels),
            label_complexity_score=label_complexity,
            issue_description_length=len(issue_info.get('description', '')),
            similar_tasks_avg_iterations=similar_avg
        )

    def predict_optimal_iterations(
        self,
        task_complexity: TaskComplexity
    ) -> Dict[str, any]:
        """
        Prediziert optimale Iterations-Count.

        Args:
            task_complexity: Extrahierte Features

        Returns:
            {
                'predicted_iterations': int,
                'confidence': float,
                'min_iterations': int,
                'max_iterations': int,
                'reasoning': str
            }
        """
        # Fallback auf Heuristik wenn kein trainiertes Modell
        if self.model is None:
            return self._heuristic_prediction(task_complexity)

        # ML-basierte Prediction
        features = self._task_to_feature_vector(task_complexity)
        features_scaled = self.feature_scaler.transform([features])

        # Random Forest gibt Predictions für jeden Tree
        predictions = []
        for tree in self.model.estimators_:
            pred = tree.predict(features_scaled)[0]
            predictions.append(pred)

        # Statistiken über alle Trees
        mean_pred = np.mean(predictions)
        std_pred = np.std(predictions)
        confidence = 1.0 - min(std_pred / mean_pred, 0.5) if mean_pred > 0 else 0.5

        # Runde auf Integer und clamp
        predicted = int(round(mean_pred))
        min_iter = max(1, int(mean_pred - std_pred))
        max_iter = min(12, int(mean_pred + std_pred))

        predicted = max(min_iter, min(predicted, max_iter))

        reasoning = self._generate_reasoning(task_complexity, predicted)

        return {
            'predicted_iterations': predicted,
            'confidence': confidence,
            'min_iterations': min_iter,
            'max_iterations': max_iter,
            'reasoning': reasoning
        }

    def _heuristic_prediction(self, task: TaskComplexity) -> Dict[str, any]:
        """
        Heuristische Prediction wenn noch kein trainiertes Modell.

        Basiert auf einfachen Regeln aus Task-Eigenschaften.
        """
        score = 0.0

        # Code Complexity Faktoren
        if task.total_lines > 1000:
            score += 2.0
        elif task.total_lines > 500:
            score += 1.0
        elif task.total_lines > 200:
            score += 0.5

        if task.avg_cyclomatic_complexity > 15:
            score += 1.5
        elif task.avg_cyclomatic_complexity > 10:
            score += 0.8

        # Test Faktoren
        if task.existing_coverage < 0.5:
            score += 1.0
        if task.test_count == 0:
            score += 1.5

        # Label Faktoren
        score += task.label_complexity_score * 2.0

        # Baseline
        base_iterations = 3

        # Kombiniere
        predicted = base_iterations + int(round(score))
        predicted = max(2, min(predicted, 10))

        return {
            'predicted_iterations': predicted,
            'confidence': 0.6,  # Mittlere Confidence für Heuristik
            'min_iterations': max(2, predicted - 1),
            'max_iterations': min(10, predicted + 2),
            'reasoning': f'Heuristic prediction based on complexity score: {score:.1f}'
        }

    def record_actual_result(
        self,
        task_complexity: TaskComplexity,
        actual_iterations: int,
        final_quality: float
    ):
        """
        Speichert tatsächliches Ergebnis für zukünftiges Training.

        Args:
            task_complexity: Features der Task
            actual_iterations: Tatsächlich benötigte Iterationen
            final_quality: Erreichte finale Qualität
        """
        task_complexity.actual_iterations_needed = actual_iterations
        task_complexity.final_quality_achieved = final_quality

        self.training_history.append(task_complexity)

        # Auto-Retrain alle 20 Samples
        if len(self.training_history) >= 20 and len(self.training_history) % 20 == 0:
            self.train_model()

        # Speichere Training History
        self._save_training_history()

    def train_model(self, min_samples: int = 20):
        """
        Trainiert Random Forest Modell auf gesammelten Daten.

        Args:
            min_samples: Minimum Samples vor Training
        """
        if len(self.training_history) < min_samples:
            print(f"Not enough samples for training: {len(self.training_history)}/{min_samples}")
            return

        # Lazy import (sklearn nur wenn wirklich gebraucht)
        try:
            from sklearn.ensemble import RandomForestRegressor
            from sklearn.preprocessing import StandardScaler
            from sklearn.model_selection import train_test_split
        except ImportError:
            print("scikit-learn not installed. Install with: pip install scikit-learn")
            return

        # Prepare training data
        X = []
        y = []

        for task in self.training_history:
            if task.actual_iterations_needed is not None:
                features = self._task_to_feature_vector(task)
                X.append(features)
                y.append(task.actual_iterations_needed)

        X = np.array(X)
        y = np.array(y)

        # Split train/test
        if len(X) > 40:
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
        else:
            X_train, y_train = X, y
            X_test, y_test = None, None

        # Feature Scaling
        self.feature_scaler = StandardScaler()
        X_train_scaled = self.feature_scaler.fit_transform(X_train)

        # Train Random Forest
        self.model = RandomForestRegressor(
            n_estimators=50,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42
        )
        self.model.fit(X_train_scaled, y_train)

        # Evaluate if test set available
        if X_test is not None:
            X_test_scaled = self.feature_scaler.transform(X_test)
            score = self.model.score(X_test_scaled, y_test)
            print(f"Model trained! R² Score: {score:.3f}")

        # Save model
        self._save_model()

    def _task_to_feature_vector(self, task: TaskComplexity) -> np.ndarray:
        """Konvertiert TaskComplexity zu Feature-Vektor für ML."""
        features = [
            task.total_files,
            task.total_lines,
            task.function_count,
            task.class_count,
            task.avg_cyclomatic_complexity,
            task.test_files,
            task.test_count,
            task.existing_coverage,
            task.label_count,
            task.label_complexity_score,
            task.issue_description_length,
            task.similar_tasks_avg_iterations or 3.0  # Default 3
        ]
        return np.array(features, dtype=np.float32)

    def _calculate_label_complexity(self, labels: List[str]) -> float:
        """
        Berechnet Complexity-Score aus Issue-Labels.

        Returns:
            Float 0-1 (0=simple, 1=complex)
        """
        if not labels:
            return 0.3  # Default moderate complexity

        # Normalisiere Labels
        labels_lower = [l.lower() for l in labels]

        # Berechne gewichteten Score
        total_weight = 0.0
        for label in labels_lower:
            for key, weight in self.label_weights.items():
                if key in label:
                    total_weight += weight
                    break

        # Normalisiere auf 0-1 (max 2 Labels mit weight=1.0 => cap bei 2)
        normalized = min(total_weight / 2.0, 1.0)

        return normalized

    def _estimate_cyclomatic_complexity(self, code_stats: Dict) -> float:
        """
        Schätzt durchschnittliche Cyclomatic Complexity.

        Vereinfachte Schätzung basierend auf Code-Statistiken.
        """
        lines = code_stats.get('lines', 100)
        functions = code_stats.get('functions', 5)

        # Heuristik: Mehr Lines pro Function = höhere Complexity
        if functions == 0:
            return 5.0

        lines_per_function = lines / functions

        # Mapping
        if lines_per_function > 100:
            return 20.0
        elif lines_per_function > 50:
            return 15.0
        elif lines_per_function > 30:
            return 10.0
        elif lines_per_function > 15:
            return 7.0
        else:
            return 5.0

    def _find_similar_tasks_avg(
        self,
        code_stats: Dict,
        test_stats: Dict
    ) -> Optional[float]:
        """
        Findet ähnliche Tasks in History und averaged deren Iterations.

        Ähnlichkeit basierend auf Code/Test-Stats.
        """
        if not self.training_history:
            return None

        current_lines = code_stats.get('lines', 100)
        current_tests = test_stats.get('test_count', 0)

        similar_tasks = []

        for task in self.training_history:
            # Ähnlichkeit: ±50% Lines, ±50% Tests
            line_ratio = task.total_lines / max(current_lines, 1)
            test_ratio = task.test_count / max(current_tests, 1) if current_tests > 0 else 1.0

            if (0.5 <= line_ratio <= 2.0) and (0.5 <= test_ratio <= 2.0):
                if task.actual_iterations_needed is not None:
                    similar_tasks.append(task.actual_iterations_needed)

        if similar_tasks:
            return np.mean(similar_tasks)

        return None

    def _generate_reasoning(self, task: TaskComplexity, predicted: int) -> str:
        """Generiert menschenlesbare Begründung für Prediction."""
        reasons = []

        if task.total_lines > 500:
            reasons.append(f"Large codebase ({task.total_lines} lines)")
        if task.avg_cyclomatic_complexity > 10:
            reasons.append(f"High complexity (CCN: {task.avg_cyclomatic_complexity:.1f})")
        if task.existing_coverage < 0.5:
            reasons.append(f"Low test coverage ({task.existing_coverage*100:.0f}%)")
        if task.label_complexity_score > 0.7:
            reasons.append("Complex issue labels")

        if not reasons:
            reasons.append("Standard complexity task")

        reason_text = ", ".join(reasons)
        return f"Predicted {predicted} iterations. Factors: {reason_text}"

    def _save_model(self):
        """Speichert trainiertes Modell."""
        self.model_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.model_path, 'wb') as f:
            pickle.dump({
                'model': self.model,
                'scaler': self.feature_scaler,
                'label_weights': self.label_weights
            }, f)

        print(f"Model saved to {self.model_path}")

    def _load_model(self):
        """Lädt gespeichertes Modell."""
        try:
            with open(self.model_path, 'rb') as f:
                data = pickle.load(f)
                self.model = data['model']
                self.feature_scaler = data['scaler']
                self.label_weights = data.get('label_weights', self.label_weights)

            print(f"Model loaded from {self.model_path}")
        except Exception as e:
            print(f"Could not load model: {e}")

    def _save_training_history(self):
        """Speichert Training History als JSON."""
        history_path = self.model_path.parent / "training_history.json"
        history_path.parent.mkdir(parents=True, exist_ok=True)

        # Konvertiere zu JSON-serializable format
        history_data = []
        for task in self.training_history:
            task_dict = asdict(task)
            history_data.append(task_dict)

        with open(history_path, 'w', encoding='utf-8') as f:
            json.dump(history_data, f, indent=2, default=str)

    def _load_training_history(self):
        """Lädt Training History."""
        history_path = self.model_path.parent / "training_history.json"

        if not history_path.exists():
            return

        try:
            with open(history_path, 'r', encoding='utf-8') as f:
                history_data = json.load(f)

            self.training_history = []
            for task_dict in history_data:
                # Reconstruct TaskComplexity
                task = TaskComplexity(**task_dict)
                self.training_history.append(task)

            print(f"Loaded {len(self.training_history)} historical tasks")
        except Exception as e:
            print(f"Could not load training history: {e}")

    def get_statistics(self) -> Dict[str, any]:
        """Gibt Statistiken über Predictions zurück."""
        if not self.training_history:
            return {
                'total_tasks': 0,
                'avg_iterations': 0.0,
                'model_trained': self.model is not None
            }

        tasks_with_results = [
            t for t in self.training_history
            if t.actual_iterations_needed is not None
        ]

        if not tasks_with_results:
            return {
                'total_tasks': len(self.training_history),
                'avg_iterations': 0.0,
                'model_trained': self.model is not None
            }

        iterations = [t.actual_iterations_needed for t in tasks_with_results]
        qualities = [
            t.final_quality_achieved for t in tasks_with_results
            if t.final_quality_achieved is not None
        ]

        return {
            'total_tasks': len(self.training_history),
            'tasks_with_results': len(tasks_with_results),
            'avg_iterations': np.mean(iterations),
            'median_iterations': np.median(iterations),
            'min_iterations': np.min(iterations),
            'max_iterations': np.max(iterations),
            'avg_quality': np.mean(qualities) if qualities else 0.0,
            'model_trained': self.model is not None
        }


# Singleton Instanz
_predictor_instance = None


def get_predictor() -> IterationPredictor:
    """Holt Singleton Predictor-Instanz."""
    global _predictor_instance
    if _predictor_instance is None:
        _predictor_instance = IterationPredictor()
        _predictor_instance._load_training_history()
    return _predictor_instance


# Export
__all__ = [
    'TaskComplexity',
    'IterationPredictor',
    'get_predictor'
]
