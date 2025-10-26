"""
Query Result Caching for GraphRAG

Implements simple in-memory caching to improve response times for frequently asked questions.
"""

import hashlib
import time
import logging
from typing import Dict, Any, Optional
from functools import lru_cache
from collections import OrderedDict

logger = logging.getLogger(__name__)


class QueryCache:
    """
    LRU cache for query results.

    Caches:
    - Vector search results (by question embedding)
    - Cypher query results (by query string + params)
    - Final answers (by question + query path)
    """

    def __init__(self, max_size: int = 100, ttl_seconds: int = 3600):
        """
        Initialize cache.

        Args:
            max_size: Maximum number of cached entries
            ttl_seconds: Time-to-live for cache entries (default 1 hour)
        """
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds

        # Separate caches for different data types
        self._vector_cache: OrderedDict = OrderedDict()
        self._cypher_cache: OrderedDict = OrderedDict()
        self._answer_cache: OrderedDict = OrderedDict()

        # Statistics
        self.stats = {
            "hits": 0,
            "misses": 0,
            "evictions": 0
        }

    def _make_key(self, data: Any) -> str:
        """
        Generate cache key from data.

        Args:
            data: Data to hash (question, query, etc.)

        Returns:
            Hash key
        """
        if isinstance(data, dict):
            # Sort dict for consistent hashing
            data_str = str(sorted(data.items()))
        elif isinstance(data, list):
            data_str = str(sorted(data))
        else:
            data_str = str(data)

        return hashlib.md5(data_str.encode()).hexdigest()

    def _is_expired(self, entry: Dict[str, Any]) -> bool:
        """
        Check if cache entry is expired.

        Args:
            entry: Cache entry with 'timestamp' field

        Returns:
            True if expired
        """
        age = time.time() - entry["timestamp"]
        return age > self.ttl_seconds

    def _evict_lru(self, cache: OrderedDict):
        """
        Evict least recently used entry if cache is full.

        Args:
            cache: Cache to evict from
        """
        if len(cache) >= self.max_size:
            cache.popitem(last=False)  # Remove oldest (FIFO)
            self.stats["evictions"] += 1

    def get_vector_results(self, question: str) -> Optional[list]:
        """
        Get cached vector search results.

        Args:
            question: User question

        Returns:
            Cached results or None
        """
        key = self._make_key(question)

        if key in self._vector_cache:
            entry = self._vector_cache[key]

            if not self._is_expired(entry):
                # Move to end (most recently used)
                self._vector_cache.move_to_end(key)
                self.stats["hits"] += 1
                logger.debug(f"Vector cache HIT for question: {question[:50]}...")
                return entry["data"]
            else:
                # Expired, remove
                del self._vector_cache[key]

        self.stats["misses"] += 1
        logger.debug(f"Vector cache MISS for question: {question[:50]}...")
        return None

    def set_vector_results(self, question: str, results: list):
        """
        Cache vector search results.

        Args:
            question: User question
            results: Vector search results
        """
        key = self._make_key(question)

        self._evict_lru(self._vector_cache)

        self._vector_cache[key] = {
            "data": results,
            "timestamp": time.time()
        }

        logger.debug(f"Vector results cached for: {question[:50]}...")

    def get_cypher_results(
        self,
        cypher_query: str,
        params: Optional[Dict] = None
    ) -> Optional[list]:
        """
        Get cached Cypher query results.

        Args:
            cypher_query: Cypher query string
            params: Query parameters

        Returns:
            Cached results or None
        """
        cache_key_data = {"query": cypher_query, "params": params or {}}
        key = self._make_key(cache_key_data)

        if key in self._cypher_cache:
            entry = self._cypher_cache[key]

            if not self._is_expired(entry):
                self._cypher_cache.move_to_end(key)
                self.stats["hits"] += 1
                logger.debug(f"Cypher cache HIT")
                return entry["data"]
            else:
                del self._cypher_cache[key]

        self.stats["misses"] += 1
        logger.debug(f"Cypher cache MISS")
        return None

    def set_cypher_results(
        self,
        cypher_query: str,
        params: Optional[Dict],
        results: list
    ):
        """
        Cache Cypher query results.

        Args:
            cypher_query: Cypher query string
            params: Query parameters
            results: Query results
        """
        cache_key_data = {"query": cypher_query, "params": params or {}}
        key = self._make_key(cache_key_data)

        self._evict_lru(self._cypher_cache)

        self._cypher_cache[key] = {
            "data": results,
            "timestamp": time.time()
        }

        logger.debug(f"Cypher results cached")

    def get_answer(
        self,
        question: str,
        query_path: str
    ) -> Optional[Dict[str, Any]]:
        """
        Get cached final answer.

        Args:
            question: User question
            query_path: Query path taken

        Returns:
            Cached answer dict or None
        """
        cache_key_data = {"question": question, "path": query_path}
        key = self._make_key(cache_key_data)

        if key in self._answer_cache:
            entry = self._answer_cache[key]

            if not self._is_expired(entry):
                self._answer_cache.move_to_end(key)
                self.stats["hits"] += 1
                logger.info(f"Answer cache HIT for: {question[:50]}...")
                return entry["data"]
            else:
                del self._answer_cache[key]

        self.stats["misses"] += 1
        logger.debug(f"Answer cache MISS for: {question[:50]}...")
        return None

    def set_answer(
        self,
        question: str,
        query_path: str,
        answer_data: Dict[str, Any]
    ):
        """
        Cache final answer.

        Args:
            question: User question
            query_path: Query path taken
            answer_data: Answer dict with 'final_answer' and 'citations'
        """
        cache_key_data = {"question": question, "path": query_path}
        key = self._make_key(cache_key_data)

        self._evict_lru(self._answer_cache)

        self._answer_cache[key] = {
            "data": answer_data,
            "timestamp": time.time()
        }

        logger.debug(f"Answer cached for: {question[:50]}...")

    def clear(self):
        """Clear all caches."""
        self._vector_cache.clear()
        self._cypher_cache.clear()
        self._answer_cache.clear()
        logger.info("All caches cleared")

    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.

        Returns:
            Statistics dict
        """
        total_requests = self.stats["hits"] + self.stats["misses"]
        hit_rate = (self.stats["hits"] / total_requests * 100) if total_requests > 0 else 0

        return {
            "hit_rate": round(hit_rate, 2),
            "hits": self.stats["hits"],
            "misses": self.stats["misses"],
            "evictions": self.stats["evictions"],
            "cache_sizes": {
                "vector": len(self._vector_cache),
                "cypher": len(self._cypher_cache),
                "answer": len(self._answer_cache)
            }
        }

    def print_stats(self):
        """Print cache statistics."""
        stats = self.get_stats()
        print("\n" + "="*50)
        print("Cache Statistics")
        print("="*50)
        print(f"Hit Rate: {stats['hit_rate']:.1f}%")
        print(f"Hits: {stats['hits']}")
        print(f"Misses: {stats['misses']}")
        print(f"Evictions: {stats['evictions']}")
        print(f"\nCache Sizes:")
        print(f"  Vector: {stats['cache_sizes']['vector']}")
        print(f"  Cypher: {stats['cache_sizes']['cypher']}")
        print(f"  Answer: {stats['cache_sizes']['answer']}")
        print("="*50)


# Singleton instance
_query_cache: Optional[QueryCache] = None


def get_query_cache(
    enabled: bool = True,
    max_size: int = 100,
    ttl_seconds: int = 3600
) -> QueryCache:
    """
    Get or create query cache singleton.

    Args:
        enabled: Whether caching is enabled (from env)
        max_size: Maximum cache size
        ttl_seconds: Time-to-live for entries

    Returns:
        QueryCache instance or None if disabled
    """
    global _query_cache

    if not enabled:
        return None

    if _query_cache is None:
        _query_cache = QueryCache(max_size=max_size, ttl_seconds=ttl_seconds)
        logger.info(f"Query cache initialized (max_size={max_size}, ttl={ttl_seconds}s)")

    return _query_cache


# Embedding cache using functools.lru_cache
@lru_cache(maxsize=1000)
def cache_embedding(text: str) -> str:
    """
    Cache embedding key for reuse.

    This is a placeholder - actual embedding caching should be done
    in the embedding generation function.

    Args:
        text: Text to embed

    Returns:
        Cache key
    """
    return hashlib.md5(text.encode()).hexdigest()
