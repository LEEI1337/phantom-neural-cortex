"""
3-Layer Caching System - Optimierung #8
========================================

Multi-tier Cache für maximale Performance.

Layer 1: Guideline Cache
    - TTL: 1 hour
    - Einsparung: 90% Disk I/O
    - Guidelines werden nur 1x pro Stunde geladen

Layer 2: GitHub API Cache
    - TTL: 5 minutes
    - Einsparung: 70% API Calls
    - Vermeidet Rate-Limiting

Layer 3: Quality Pattern Cache
    - TTL: Persistent
    - Einsparung: Wiederkehrende Code-Patterns
    - Ähnlicher Code → bekanntes Quality-Result

Erwartete Gesamtersparung:
- 90% weniger Guideline-Loads
- 70% weniger GitHub API Calls
- 30% schnellere Quality Evaluation (Pattern-Matching)

"""

import json
import hashlib
import time
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path
from datetime import datetime, timedelta
import pickle


@dataclass
class CacheEntry:
    """Ein Cache-Eintrag."""

    key: str
    value: Any
    created_at: datetime
    ttl: float  # Time to Live in seconds
    access_count: int = 0
    last_accessed: Optional[datetime] = None


class CacheLayer:
    """
    Einzelne Cache-Schicht mit TTL und Eviction.

    Base Class für alle Cache-Typen.
    """

    def __init__(
        self,
        name: str,
        default_ttl: float = 3600.0,
        max_size: int = 1000
    ):
        self.name = name
        self.default_ttl = default_ttl
        self.max_size = max_size

        # In-Memory Cache
        self.cache: Dict[str, CacheEntry] = {}

        # Statistics
        self.hits = 0
        self.misses = 0
        self.evictions = 0

    def get(self, key: str) -> Optional[Any]:
        """
        Holt Wert aus Cache.

        Returns:
            Value oder None wenn nicht gefunden/expired
        """
        if key not in self.cache:
            self.misses += 1
            return None

        entry = self.cache[key]

        # Check TTL
        if self._is_expired(entry):
            del self.cache[key]
            self.misses += 1
            return None

        # Update Access Stats
        entry.access_count += 1
        entry.last_accessed = datetime.now()
        self.hits += 1

        return entry.value

    def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[float] = None
    ):
        """
        Speichert Wert in Cache.

        Args:
            key: Cache Key
            value: Wert
            ttl: Optional Custom TTL (seconds)
        """
        # Check Size Limit
        if len(self.cache) >= self.max_size and key not in self.cache:
            self._evict_lru()

        ttl = ttl if ttl is not None else self.default_ttl

        entry = CacheEntry(
            key=key,
            value=value,
            created_at=datetime.now(),
            ttl=ttl,
            access_count=0,
            last_accessed=None
        )

        self.cache[key] = entry

    def invalidate(self, key: str):
        """Invalidiert einen Cache-Entry."""
        if key in self.cache:
            del self.cache[key]

    def clear(self):
        """Leert gesamten Cache."""
        self.cache.clear()

    def _is_expired(self, entry: CacheEntry) -> bool:
        """Prüft ob Entry expired."""
        age = (datetime.now() - entry.created_at).total_seconds()
        return age > entry.ttl

    def _evict_lru(self):
        """Evict Least Recently Used Entry."""
        if not self.cache:
            return

        # Finde LRU Entry
        lru_key = min(
            self.cache.keys(),
            key=lambda k: self.cache[k].last_accessed or self.cache[k].created_at
        )

        del self.cache[lru_key]
        self.evictions += 1

    def get_statistics(self) -> Dict[str, any]:
        """Gibt Cache-Statistiken zurück."""
        total_requests = self.hits + self.misses
        hit_rate = self.hits / total_requests if total_requests > 0 else 0.0

        return {
            'name': self.name,
            'size': len(self.cache),
            'max_size': self.max_size,
            'hits': self.hits,
            'misses': self.misses,
            'evictions': self.evictions,
            'hit_rate': hit_rate,
            'total_requests': total_requests
        }


class GuidelineCache(CacheLayer):
    """
    Cache für Guideline-Dokumente.

    TTL: 1 hour (Guidelines ändern sich selten)
    """

    def __init__(self):
        super().__init__(
            name='GuidelineCache',
            default_ttl=3600.0,  # 1 hour
            max_size=50  # Max 50 Guideline-Files
        )

    def get_guideline(self, file_path: Path) -> Optional[str]:
        """Holt Guideline aus Cache."""
        key = str(file_path)
        return self.get(key)

    def set_guideline(self, file_path: Path, content: str):
        """Speichert Guideline in Cache."""
        key = str(file_path)
        self.set(key, content)


class GitHubAPICache(CacheLayer):
    """
    Cache für GitHub API Responses.

    TTL: 5 minutes (relativ kurz für aktuelle Daten)
    """

    def __init__(self):
        super().__init__(
            name='GitHubAPICache',
            default_ttl=300.0,  # 5 minutes
            max_size=200  # Max 200 API Responses
        )

    def get_issue(self, issue_number: int) -> Optional[Dict]:
        """Holt Issue aus Cache."""
        key = f"issue_{issue_number}"
        return self.get(key)

    def set_issue(self, issue_number: int, issue_data: Dict):
        """Speichert Issue in Cache."""
        key = f"issue_{issue_number}"
        self.set(key, issue_data)

    def get_pr(self, pr_number: int) -> Optional[Dict]:
        """Holt Pull Request aus Cache."""
        key = f"pr_{pr_number}"
        return self.get(key)

    def set_pr(self, pr_number: int, pr_data: Dict):
        """Speichert Pull Request in Cache."""
        key = f"pr_{pr_number}"
        self.set(key, pr_data)

    def get_repo_info(self, repo_name: str) -> Optional[Dict]:
        """Holt Repository Info aus Cache."""
        key = f"repo_{repo_name}"
        return self.get(key)

    def set_repo_info(self, repo_name: str, repo_data: Dict):
        """Speichert Repository Info in Cache."""
        key = f"repo_{repo_name}"
        self.set(key, repo_data)


class QualityPatternCache(CacheLayer):
    """
    Cache für wiederkehrende Code Quality Patterns.

    TTL: Persistent (bis manual invalidation)

    Idee: Ähnlicher Code → ähnliche Quality Issues
    """

    def __init__(self, cache_dir: Optional[Path] = None):
        super().__init__(
            name='QualityPatternCache',
            default_ttl=86400.0 * 30,  # 30 days
            max_size=500
        )

        self.cache_dir = cache_dir or Path(__file__).parent / "pattern_cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # Load from disk
        self._load_from_disk()

    def get_quality_for_code(
        self,
        code: str,
        similarity_threshold: float = 0.95
    ) -> Optional[Dict]:
        """
        Holt Quality-Result für ähnlichen Code.

        Args:
            code: Code Content
            similarity_threshold: Mindest-Ähnlichkeit (0-1)

        Returns:
            Quality Dict oder None
        """
        code_hash = self._hash_code(code)

        # Exact Match
        exact = self.get(code_hash)
        if exact is not None:
            return exact

        # Fuzzy Match (simplified - in production: use embeddings)
        # Hier nur über Code-Length Similarity
        code_length = len(code)

        for key, entry in self.cache.items():
            if self._is_expired(entry):
                continue

            # Check ob ähnliche Length
            cached_length = entry.value.get('code_length', 0)
            length_ratio = min(code_length, cached_length) / max(code_length, cached_length, 1)

            if length_ratio >= similarity_threshold:
                # Similar enough
                return entry.value.get('quality_result')

        return None

    def set_quality_for_code(
        self,
        code: str,
        quality_result: Dict
    ):
        """
        Speichert Quality-Result für Code.

        Args:
            code: Code Content
            quality_result: Quality Evaluation Result
        """
        code_hash = self._hash_code(code)

        # Store with metadata
        value = {
            'code_length': len(code),
            'code_hash': code_hash,
            'quality_result': quality_result,
            'cached_at': datetime.now().isoformat()
        }

        self.set(code_hash, value)

        # Persist to disk
        self._save_to_disk()

    def _hash_code(self, code: str) -> str:
        """Berechnet Hash für Code."""
        # Normalize Code (remove whitespace variations)
        normalized = ''.join(code.split())
        return hashlib.sha256(normalized.encode()).hexdigest()[:16]

    def _save_to_disk(self):
        """Speichert Cache zu Disk."""
        cache_file = self.cache_dir / "quality_patterns.pkl"

        # Serialize Cache
        cache_data = {}
        for key, entry in self.cache.items():
            if not self._is_expired(entry):
                cache_data[key] = {
                    'value': entry.value,
                    'created_at': entry.created_at.isoformat(),
                    'ttl': entry.ttl
                }

        with open(cache_file, 'wb') as f:
            pickle.dump(cache_data, f)

    def _load_from_disk(self):
        """Lädt Cache von Disk."""
        cache_file = self.cache_dir / "quality_patterns.pkl"

        if not cache_file.exists():
            return

        try:
            with open(cache_file, 'rb') as f:
                cache_data = pickle.load(f)

            for key, data in cache_data.items():
                entry = CacheEntry(
                    key=key,
                    value=data['value'],
                    created_at=datetime.fromisoformat(data['created_at']),
                    ttl=data['ttl']
                )

                if not self._is_expired(entry):
                    self.cache[key] = entry

            print(f"Loaded {len(self.cache)} quality patterns from disk")
        except Exception as e:
            print(f"Could not load quality patterns: {e}")


class CacheManager:
    """
    Central Cache Manager koordiniert alle 3 Layers.

    Provides unified interface für alle Caches.
    """

    def __init__(self):
        # Initialize all 3 Layers
        self.guideline_cache = GuidelineCache()
        self.github_cache = GitHubAPICache()
        self.quality_pattern_cache = QualityPatternCache()

    def get_all_statistics(self) -> Dict[str, any]:
        """Gibt Statistiken für alle Cache-Layers zurück."""
        return {
            'guideline_cache': self.guideline_cache.get_statistics(),
            'github_cache': self.github_cache.get_statistics(),
            'quality_pattern_cache': self.quality_pattern_cache.get_statistics(),
            'total_memory_entries': (
                len(self.guideline_cache.cache) +
                len(self.github_cache.cache) +
                len(self.quality_pattern_cache.cache)
            )
        }

    def clear_all(self):
        """Leert alle Caches."""
        self.guideline_cache.clear()
        self.github_cache.clear()
        self.quality_pattern_cache.clear()

    def clear_expired(self):
        """Entfernt expired Entries aus allen Caches."""
        for cache in [self.guideline_cache, self.github_cache, self.quality_pattern_cache]:
            expired_keys = [
                key for key, entry in cache.cache.items()
                if cache._is_expired(entry)
            ]
            for key in expired_keys:
                del cache.cache[key]

    def get_savings_report(self) -> Dict[str, any]:
        """
        Berechnet Einsparungs-Report.

        Estimiert wie viel Zeit/API Calls gespart wurden.
        """
        guideline_stats = self.guideline_cache.get_statistics()
        github_stats = self.github_cache.get_statistics()
        quality_stats = self.quality_pattern_cache.get_statistics()

        # Estimate Savings
        # Guideline: ~500ms pro Load
        guideline_time_saved = guideline_stats['hits'] * 0.5  # seconds

        # GitHub API: ~200ms pro Call
        github_time_saved = github_stats['hits'] * 0.2

        # Quality Pattern: ~20s pro Quality Evaluation
        quality_time_saved = quality_stats['hits'] * 20.0

        total_time_saved = guideline_time_saved + github_time_saved + quality_time_saved

        return {
            'guideline_cache': {
                'hits': guideline_stats['hits'],
                'time_saved_seconds': guideline_time_saved,
                'hit_rate': guideline_stats['hit_rate']
            },
            'github_cache': {
                'hits': github_stats['hits'],
                'api_calls_saved': github_stats['hits'],
                'time_saved_seconds': github_time_saved,
                'hit_rate': github_stats['hit_rate']
            },
            'quality_pattern_cache': {
                'hits': quality_stats['hits'],
                'evaluations_saved': quality_stats['hits'],
                'time_saved_seconds': quality_time_saved,
                'hit_rate': quality_stats['hit_rate']
            },
            'total': {
                'time_saved_seconds': total_time_saved,
                'time_saved_minutes': total_time_saved / 60.0,
                'time_saved_hours': total_time_saved / 3600.0
            }
        }


# Singleton Instance
_cache_manager_instance = None


def get_cache_manager() -> CacheManager:
    """Holt Singleton Cache-Manager-Instanz."""
    global _cache_manager_instance
    if _cache_manager_instance is None:
        _cache_manager_instance = CacheManager()
    return _cache_manager_instance


# Convenience Functions
def get_guideline_cache() -> GuidelineCache:
    """Holt Guideline Cache."""
    return get_cache_manager().guideline_cache


def get_github_cache() -> GitHubAPICache:
    """Holt GitHub API Cache."""
    return get_cache_manager().github_cache


def get_quality_pattern_cache() -> QualityPatternCache:
    """Holt Quality Pattern Cache."""
    return get_cache_manager().quality_pattern_cache


# Export
__all__ = [
    'CacheEntry',
    'CacheLayer',
    'GuidelineCache',
    'GitHubAPICache',
    'QualityPatternCache',
    'CacheManager',
    'get_cache_manager',
    'get_guideline_cache',
    'get_github_cache',
    'get_quality_pattern_cache'
]
