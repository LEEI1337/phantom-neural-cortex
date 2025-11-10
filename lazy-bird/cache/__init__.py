"""
Three-Layer Caching System (ADR-007)

This package implements hierarchical caching:
1. Memory Cache (fastest, volatile)
2. Disk Cache (persistent, medium speed)
3. Remote Cache (distributed, slower)

Components:
- cache_manager.py: Unified cache interface

Usage:
    from lazy_bird.cache import CacheManager

    cache = CacheManager(
        memory_size_mb=100,
        disk_path='/var/cache/lazy-bird',
        remote_url='redis://localhost:6379'
    )

    # Store value
    await cache.set('key', value, ttl=300)

    # Retrieve (auto-fallback through layers)
    value = await cache.get('key')

    # Clear specific layer
    cache.clear_memory()

Performance:
- 90% I/O reduction vs no caching
- Memory: ~1ms access
- Disk: ~10ms access
- Remote: ~50ms access
"""

__version__ = "1.0.0"
__author__ = "Phantom Neural Cortex Team"

from .cache_manager import CacheManager, MemoryCache, DiskCache, RemoteCache

__all__ = ['CacheManager', 'MemoryCache', 'DiskCache', 'RemoteCache']
