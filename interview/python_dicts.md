# Python dicts — Keys, Copies, Methods, and Internals (Complete Guide)

Purpose: A complete, standalone reference about Python dictionaries: key rules (hashability), full set of dict behaviors, shallow vs deep copying, common methods, iteration semantics, performance characteristics, implementation notes, and best practices for interviews and production code.

Contents

- Core rule for keys
- What types can be keys (summary)
- Deep vs shallow copy for dicts (detailed)
- Common dict methods and behaviors
- Views (keys(), values(), items()) and mutability
- Dict comprehensions and creation patterns
- Merging and update semantics (including Python 3.9 | operator)
- Performance characteristics and complexity
- CPython implementation notes (high-level)
- Mapping protocol and subclassing
- Common pitfalls & best practices
- Interview prompts

Core rule for keys

- A dict key must be hashable: implement **hash**() and **eq**() consistently and have a stable hash while used as key.
- Immutable built-ins (str, int, tuple of immutables, frozenset) are typical safe keys. Mutable containers (list, dict, set) are unhashable.

What types can be keys (quick)

- Valid: int, float (beware 1 == 1.0), str, bytes, frozenset, tuple (only if all elements are hashable), user-defined objects with consistent **hash**/**eq**, dataclasses with frozen=True.
- Invalid: list, dict, set, bytearray, most mutable containers.
- Special: NaN is hashable but NaN != NaN complicates lookups—avoid as keys.

Deep vs shallow copy (for dicts)

- Shallow copy:
  - Creates a new dict object but references the same key and value objects.
  - Methods: new = old.copy(), new = dict(old), or use copy.copy(old).
  - Cost: O(n) to copy references; values are not cloned.
  - Use when you want a new mapping but are okay sharing the same value objects.
- Deep copy:
  - Recursively copies the dict and all nested objects (values and containers).
  - Use copy.deepcopy(old).
  - Cost: potentially expensive (time and memory), but yields independent nested structures.
- Example:

```python
# filepath: /home/mxpadidar/Documents/docs/interview/python_dicts.md
# Shallow vs Deep copy examples
import copy

orig = {"a": [1, 2], "b": {"x": 10}}
shallow = orig.copy()
deep = copy.deepcopy(orig)

orig["a"].append(3)
orig["b"]["x"] = 99

# Effects:
# shallow["a"] reflects appended 3 (shared list)
# shallow["b"]["x"] reflects 99 (shared nested dict)
# deep remains unaffected
```

- Practical guidance:
  - Prefer shallow copy for speed when values are immutable or shared mutation is acceptable.
  - Use deep copy cautiously for complex nested mutable state; consider explicit transformation/serialization instead of deepcopy for production data migrations.

Common dict methods and behaviors

- Creation:
  - d = {} ; d = dict() ; d = dict(a=1, b=2) ; d = dict([("a",1), ("b",2)]) ; {k: v for ...}
- Access & safe access:
  - d[key]
  - d.get(key, default)
  - d.setdefault(key, default) — mutates if absent
- Mutation:
  - d[key] = value ; d.update(other) ; d.pop(key[, default]) ; d.popitem() (LIFO in 3.7+) ; d.clear()
- Copying:
  - shallow via d.copy(); deep via copy.deepcopy(d)
- Other:
  - d.keys(), d.values(), d.items() return view objects (see below)
  - d.fromkeys(seq, value=None) creates new dict with keys from seq

Views (keys(), values(), items())

- These return dynamic view objects that reflect changes to the dict:
  - Example: v = d.values(); d["x"] = 10; now x appears in v
- They are not lists (convert if you need a stable snapshot): list(d.items()).
- Iterating d yields keys by default (same as iter(d)).

Iteration order and insertion-order guarantee

- Since CPython 3.6 (implementation detail) and guaranteed in the language from 3.7, dict preserves insertion order.
- Implementation stores entries in a way that keeps iteration order stable; do not rely on ordering in earlier versions.

Dict comprehensions & creation patterns

- Comprehension: {k: v for k, v in iterable}
- Use dict.fromkeys(iterable, value) for uniform value mapping.
- Efficient bulk updates: d.update({...}) or for small-known static mappings prefer a literal { }.

Merging & update semantics

- d.update(other) modifies d in place: keys from other overwrite existing keys.
- Python 3.9+: new = d1 | d2 (both dicts) returns merged dict; d1 |= d2 updates in-place.
- When merging, later mappings overwrite earlier ones for overlapping keys.

Performance characteristics and complexity

- Average-case time complexity: O(1) for lookup, insert, delete (amortized).
- Worst-case: O(n) in pathological collision scenarios (rare with good hash functions).
- Iteration: O(n).
- Memory: dicts trade memory for speed (sparse tables, resizing).
- Growth/resizing: dicts grow with amortized constant cost; resizing rehashes entries and is O(n) at resize time.

CPython implementation notes (high-level)

- CPython uses an optimized open-addressing scheme with a compact entry array and an index table, plus insertion-order preservation.
- Hash randomization (per-process) mitigates hash collision DoS attacks.
- For large dicts, consider memory overhead and occasional resizing pauses.

Mapping protocol and subclassing

- The Mapping and MutableMapping ABCs live in collections.abc. Implementing these lets custom objects behave like mappings.
- Subclassing dict: override **missing**, **setitem**, **getitem**, and consider dict.**init** signature.
- Alternative: wrap dict inside a class rather than subclass when behavior is different.

Common pitfalls & best practices

- Avoid using mutable objects as keys.
- Beware of mixing numeric types as keys (1 and 1.0 are treated equal).
- Using d.setdefault in loops may inadvertently mutate dict; prefer explicit checks if needed.
- Avoid relying on view objects as snapshots — convert to list when snapshot required.
- For nested mutable values, document whether functions mutate in-place or return new dicts.
- For concurrency: plain dict is not thread-safe for concurrent mutations; use threading.Lock, concurrent maps, or process-based separation.

Advanced tips

- Use dict comprehensions for clarity and performance over manual loops when appropriate.
- For high-performance large mappings, consider specialized structures (e.g., sortedcontainers for order queries, or databases for persistence).
- Use mapping views for membership tests: if k in d is O(1).

Interview prompts

- Explain shallow vs deep copy for dicts with an example.
- Why must dict keys be hashable and what happens if you override **eq** without **hash**?
- How do dict views behave when the dict is mutated during iteration?
- Describe insertion-order guarantee and its implications.
- When would you choose dict.update vs the new | operator?

Further reading / exercises

- Inspect performance: compare repeated insertion and lookup times for dict vs other mapping types.
- Implement transformations that produce a deep copy using functional transformations instead of copy.deepcopy for predictable behavior.

Notes

- This doc supplements other notes about hash tables and Python data structures; use shallow copying for speed and deep copying only when you need full isolation of nested mutable structures.
