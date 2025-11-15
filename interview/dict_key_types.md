# Dict Key Types — What Can Be Used as Keys and Why

Purpose: Explain, with examples and caveats, which Python objects can be dictionary keys and the rationale (hashability, equality, immutability).

Core rule

- A dict key must be hashable. Concretely, an object is usable as a dict key if:
  1. It implements **hash**() returning an integer.
  2. It implements **eq**() for equality comparisons.
  3. Its hash value does not change while it is used as a key (i.e., it behaves effectively immutable for hashing/equality).

Why hashability?

- Dicts use a hash table internally: hash(key) -> bucket index. If the hash or equality semantics change after insertion, lookups can fail or return wrong values.

Common built-in hashable types

- Immutable scalars: int, float, bool, complex (hashable; note numeric equivalence rules below).
- str, bytes, frozenset, range, types like datetime.datetime (immutable-semantics overall).
- tuple is hashable if and only if all its elements are hashable.

- user-defined objects (instances) are hashable by default (object.**hash** uses identity) unless **eq** is overridden without reintroducing **hash**.

Common unhashable/mutable types

- list, dict, set, bytearray, and other mutable containers are unhashable (TypeError if used as key).
- Instances of classes that define **eq** but do not define **hash** become unhashable (to avoid inconsistent hashing).

Tuple & frozenset nuances

- tuple: hashable only when every contained element is hashable; nested structures must also satisfy this.
- frozenset: immutable set; hashable if elements are hashable. Useful when you need a set-like key.

Numeric key equivalence and hashing

- Python considers numeric types with equal values as equal keys:
  - 1 and 1.0 are considered equal keys (1 == 1.0 is True) and have equal hashes (hash(1) == hash(1.0)), so they collide and behave as the same key.
- Be aware when mixing int/float keys.

NaN (float('nan')) behavior

- NaN compares unequal to itself (float('nan') != float('nan')) and hashing multiple NaNs can be surprising.
- Using NaN as a dict key is allowed (it is hashable), but equality semantics mean lookups by "another NaN" will not match; avoid using NaN as key.

Custom objects as keys

- Default: object instances are hashable by identity (id-based), so two distinct instances are different keys even if they carry same data.
- If you implement **eq** to compare by value, you must also implement **hash** to ensure consistent hashing:
  - Python rule: if **eq** is provided and **hash** is not, the object becomes unhashable.
  - Ensure **hash** returns stable value based on immutable fields used in equality.
- Example safe pattern:
  - Use dataclasses.dataclass(frozen=True) or implement **eq** + **hash** consistently.

Mutability pitfalls

- Never use a mutable object as a key (like list) because its hash cannot be computed or will change.
- Do not mutate the contents of an object used as a key if that mutation affects its hash/eq; doing so makes the dict inconsistent (item may become unreachable).

Examples

Valid keys

- "hello", 42, (1, 2, "a"), frozenset({1,2}), dataclasses.dataclass(frozen=True) instances

Invalid keys (will raise TypeError)

- ["a", "b"], {"x":1}, {1,2}

Custom class example

```python
# filepath: /home/mxpadidar/Documents/docs/interview/dict_key_types.md

from dataclasses import dataclass

@dataclass(frozen=True)
class Point:
    x: int
    y: int


p = Point(1, 2)
d = {p: "origin"}  # safe: dataclass frozen => hashable
```

Pitfalls & gotchas

- Mixing numeric types: 1 and 1.0 collide — be explicit about key types where it matters.
- Mutable elements inside a tuple: tuple(([],)) is unhashable because inner list is unhashable.
- Overriding **eq** without **hash**: instances become unhashable (TypeError on dict insertion) — implement both or use frozen dataclass.
- Using NaN as key: unpredictable for equality-based lookups.
- Identity vs value-based keys: default instances are identity-based keys; two objects with same data but different instances remain distinct keys unless equality/hash are overridden.

Best practices

- Prefer built-in immutable types (str, int, tuple of immutables, frozenset) as keys.
- For composite keys, use tuple or a frozen dataclass with stable fields.

- If you need mutable semantics, use mapping from an immutable identifier (id, UUID) to mutable state.
- Document key semantics clearly in APIs and avoid relying on ambiguous equality (e.g., int vs float).

Interview prompts

- Why must dict keys be hashable? Explain the relationship between **hash** and **eq**.
- What happens if you override **eq** but not **hash** on a custom class?
- Why are tuples only sometimes hashable? Give an example of an unhashable tuple.
- How does Python treat 1 and 1.0 as dict keys?

Further reading / exercises

- Inspect behavior: try inserting (1, 1.0, "1") as keys into a dict and observe collisions.
- Implement a custom immutable key class with correct **eq** and **hash** and show two instances representing same logical key behave as the same dict key.

Notes

- This doc is intended to be a concise, standalone reference for interview prep and practical coding decisions regarding dict keys.
