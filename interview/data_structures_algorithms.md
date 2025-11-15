# Data Structures & Algorithms — Backend Practical Guide

Purpose: Rapid reference to common data structures, complexity, and when to use them in backend systems.

## Time & space complexity

- Big-O notation for worst-case; O(1), O(log n), O(n), O(n log n), O(n^2).
- Understand amortized complexity: e.g., dynamic array append is amortized O(1).
- Space complexity: when RAM is limited prefer streaming/iterators and external sorting.

## Key data structures

- Hash map (dict): O(1) average lookup/insert/delete. Best for membership and caches. Watch for memory overhead and collision attacks — use size limits and TTL in caches.
- Heap (priority queue): O(log n) insert/pop. Use for scheduling, k-largest problems (heapq in Python).
- Trees:
  - Binary search trees (balanced): O(log n) lookup/insert. Use e.g., btree indexes in DBs for disk-friendly ordered storage.
  - Tries: prefix-based searches (autocomplete).
- Graphs: adjacency list for sparse graphs, matrix for dense. BFS for shortest path in unweighted graphs, Dijkstra for weighted positive edges.
- Queue: FIFO processing for task pipelines. Use deque for in-memory queue or external queues (RabbitMQ/Kafka) for persistence.

## Practical trade-offs

- Use hash maps for O(1) lookups; use ordered structures if you need range queries or sorted iteration.
- For large datasets, use streaming algorithms (one-pass), approximate algorithms (HyperLogLog, Bloom filters) to save memory.
- For top-k in streaming: use bounded heap of size k; complexity O(n log k).

## Example problems & solutions

- Top-k users in a stream: maintain a min-heap of size k keyed by activity count; update and pop as needed.
- Deduplicate large dataset larger than memory: use external sort or Bloom filter + disk-backed set.

## Interview prompts

- Explain when you'd pick a heap vs a sorted tree structure for a scheduling system.
- What is amortized complexity and give an example.

Cheat sheet:

- dict lookup: O(1) average
- list append: O(1) amortized
- sorted insert: O(n)
- heap push/pop: O(log n)
