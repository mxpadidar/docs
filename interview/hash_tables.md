# Hash Tables — Complete Guide

Purpose: Self-contained reference covering hash table concepts, common implementations, performance trade-offs, practical tips (including Python dict internals), example code, and interview prompts.

Contents

- What is a hash table?
- API and complexity
- Hash functions: properties and choices
- Collision resolution strategies
  - Separate chaining
  - Open addressing: linear probing, quadratic probing, double hashing
- Load factor, resizing and amortized costs
- Deletion and tombstones
- Python dict internals (CPython)
- Concurrency considerations
- Memory, cache behavior and practical trade-offs
- Simple implementations (Python example)
- Common pitfalls & debugging tips
- Interview prompts

## What is a hash table?

- A hash table (hash map) is a key-value store that maps keys to values using a hash function to compute an index into an underlying array.
- Goal: average O(1) time for lookup, insert, and delete.

## API and complexity

- Operations: get(key), set(key, value), delete(key), contains(key).
- Average complexity (with a good hash function and properly sized table): O(1) for lookup/insert/delete.
- Worst-case complexity: O(n) when many keys collide (e.g., degenerate hashing or adversarial input), but well-designed tables and hash functions make this rare.
- Space: O(n) for storing entries; plus overhead for the table array and metadata.

## Hash functions: properties and choices

- Deterministic and fast.
- Uniform distribution across buckets to avoid clustering.
- Low collision probability for expected inputs.
- Not necessarily cryptographic: prefer non-cryptographic hashes (e.g., MurmurHash, xxHash) for speed in in-memory hash tables; use cryptographic hashes only when security properties needed.
- In practice: use builtin language hash (Python's hash()) but be aware of seedization/randomization and collision attacks.

## Collision resolution strategies

1. Separate chaining

   - Each bucket holds a linked list (or vector) of entries.
   - Insert: append to list at bucket index.
   - Lookup: scan bucket list for matching key.
   - Pros: simple, robust under load; easier deletion; table resizing cheaper (no need to re-place tombstones).
   - Cons: extra memory for pointers; may degrade cache usage.

2. Open addressing
   - All entries stored directly in table array; collisions resolved by probing sequence until empty slot found.
   - Linear probing:
     - Probe sequence: (h + i) % m
     - Tends to cluster (primary clustering), but offers excellent cache locality.
   - Quadratic probing:
     - Probe: (h + c1*i + c2*i^2) % m
     - Reduces primary clustering but may still suffer secondary clustering; requires careful choice of table size (often power-of-two).
   - Double hashing:
     - Probe: (h1 + i \* h2) % m
     - Uses a second hash for step size; reduces clustering and generally has good distribution.
   - Pros: lower memory overhead; excellent cache locality.
   - Cons: deletion complexity (need tombstones), performance degrades as load factor approaches 1.

## Load factor, resizing and amortized costs

- Load factor α = n / m (entries / number of buckets).
- Performance sensitive to α; typical thresholds:
  - Separate chaining: keep α ≲ 1 (or slightly larger).
  - Open addressing: keep α ≲ 0.5–0.7 depending on probe scheme.
- Resizing policy:
  - Grow (e.g., double size) when α exceeds threshold; rehash all entries into new table.
  - Shrinking sometimes applied when α falls below lower threshold.
- Cost: resizing is O(n) but amortized cost per insertion remains O(1) if growth factor constant (e.g., 2x).

## Deletion and tombstones

- Separate chaining: delete by removing from bucket list.
- Open addressing: cannot simply clear a slot — doing so breaks probe chains; use tombstone markers to indicate deleted slots so lookups don't terminate early.
- Tombstones accumulate and degrade performance; periodic rehash can clean them.

## Python dict internals (CPython)

- CPython dict is a highly optimized hash table using open addressing with perturbation and insertion-order preservation (since Python 3.7).
- Key facts:
  - Uses open addressing, sparse table, and a scheme optimized for memory and speed.
  - Maintains a compact array (entries) and an index table; resizing strategy doubles size and re-inserts entries.
  - Hash randomization: Python can randomized hash seed per process to mitigate hash-flooding DoS.
  - Since 3.6 (implementation detail) and guaranteed in 3.7+, dict preserves insertion order — implemented without linked lists by keeping entries in a compact array.
- Practical note: Python dicts are highly optimized; for general use prefer dict unless specific constraints demand custom structure.

## Concurrency considerations

- Hash tables are not inherently thread-safe.
- Strategies for concurrent access:
  - Coarse-grained lock: single mutex around table (simple but limits parallelism).
  - Sharding/striping: partition key space into multiple sub-tables each with its own lock to increase parallelism.
  - Lock-free or concurrent hash tables: more complex; e.g., Java ConcurrentHashMap uses segmented locking / optimistic techniques.
- Consider immutability or copy-on-write for read-heavy workloads to avoid locking.

## Memory, cache behavior and practical trade-offs

- Cache locality matters: open addressing often faster due to contiguous memory access; separate chaining may have pointer-chasing overhead.
- Memory overhead: pointer-based chain nodes add overhead; open addressing stores entries directly but may require larger table to keep low α.
- Choice depends on data size, expected load factor, and operation mix.

## Simple implementations (Python example)

- Chaining example (educational):
  - Implementation shows concepts; not production-optimized.

Example (conceptual):

```python
# filepath: /home/mxpadidar/Documents/docs/interview/hash_tables.md
# ...existing code...
class HashTableChaining:
    def __init__(self, capacity=8):
        self.capacity = capacity
        self.size = 0
        self.buckets = [[] for _ in range(capacity)]

    def _bucket_index(self, key):
        return hash(key) % self.capacity

    def set(self, key, value):
        idx = self._bucket_index(key)
        bucket = self.buckets[idx]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self.size += 1
        if self.size / self.capacity > 0.75:
            self._resize(self.capacity * 2)

    def get(self, key, default=None):
        idx = self._bucket_index(key)
        bucket = self.buckets[idx]
        for k, v in bucket:
            if k == key:
                return v
        return default

    def delete(self, key):
        idx = self._bucket_index(key)
        bucket = self.buckets[idx]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                self.size -= 1
                return True
        return False

    def _resize(self, new_capacity):
        old = self.buckets
        self.capacity = new_capacity
        self.buckets = [[] for _ in range(new_capacity)]
        self.size = 0
        for bucket in old:
            for k, v in bucket:
                self.set(k, v)
# ...existing code...
```

## Common pitfalls & debugging tips

- Poor hash functions or adversarial inputs lead to clustering and degraded performance.
- Using high-cardinality labels (e.g., user IDs) as metric labels in monitoring resembles high-collision thinking — avoid misuse of high-cardinality keys in systems expecting low cardinality.
- When testing performance, benchmark with realistic key distributions and load factors.
- Watch for resizing pauses in latency-sensitive systems; consider incremental resizing or pre-sizing.

## When not to use hash tables

- Need for ordered iteration by key range (use balanced trees).
- Need for range queries or ordered scans (use trees or specialized indexes).
- Strong transactions/ACID across many keys (use database or specialized index).

## Interview prompts

- Explain how a hash table works and why average-case lookup is O(1).
- Compare separate chaining vs open addressing and when you’d choose one over the other.
- Describe how Python dict works at a high level and why it's efficient.
- Design a concurrent hash map for a read-heavy workload: how would you shard/lock?
- Explain resizing cost and why average insertion remains O(1).

## Further reading / practice

- Implement both a chaining and an open addressing hash table; benchmark inserts/gets/deletes with different load factors and key distributions.
- Inspect CPython dict source or high-level docs to understand production optimizations.

## Notes

- This doc aims to be self-contained for interview prep and practical understanding. For production systems, rely on well-tested libraries and consider workload-specific trade-offs.
