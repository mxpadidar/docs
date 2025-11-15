# Python Data Structures — Mutability, Immutability, and Parameter Passing (In-Depth)

Purpose: A focused, self-contained reference covering mutability vs immutability in Python, how Python passes arguments, copying semantics, common pitfalls (default mutable args), and practical patterns for safe code.

Contents

- Overview: mutable vs immutable
- Built-in immutable types
- Built-in mutable types
- Python's parameter passing model (pass-by-assignment)
- Examples showing mutation across function boundaries
- Shallow vs deep copy
- Hashing, dict/set keys and immutability
- Default mutable argument pitfall
- Immutability patterns and tools
- Concurrency and mutability considerations
- Performance/memory notes
- Interview prompts

Overview: mutable vs immutable

- Immutable: object state cannot change after creation. Example: int, float, str, tuple, frozenset, bytes.
- Mutable: object state can be modified. Example: list, dict, set, bytearray, custom mutable classes.
- Immutability simplifies reasoning, sharing without defensive copies, and allows safe use as dict/set keys.

Built-in immutable types

- int, float, bool, str, tuple (if its elements are immutable), frozenset, bytes, range, NoneType.
- Many immutable types are hashable (hash(x) defined) and can be used as dict keys or set members (if their contents are also immutable).

Built-in mutable types

- list, dict, set, bytearray, user-defined classes with mutable attributes.
- Mutable containers are unhashable by default and cannot be dict keys.

Python's parameter passing model

- Python uses "pass-by-assignment" (aka pass-by-object-reference): function arguments are references to objects. The reference is passed by value.
- Result: rebinding a parameter name inside the function does not affect caller; mutating the referenced object does affect caller if object is mutable.

Examples

Rebinding vs mutating:

```python
# filepath: /home/mxpadidar/Documents/docs/interview/python_data_structures_in_depth.md
# Rebinding a name doesn't change the caller's binding
def reassign(x):
    x = [1, 2, 3]  # local rebind only

a = [0]
reassign(a)
assert a == [0]  # unchanged

# Mutating the object affects the caller
def mutate(x):
    x.append(2)

b = [0]
mutate(b)
assert b == [0, 2]  # mutated
```

Shallow vs deep copy

- Shallow copy: creates a new container, but references the same elements. Use copy.copy() or container-specific methods (list.copy(), dict.copy()).
- Deep copy: recursively copies nested objects. Use copy.deepcopy().
- Example:

```python
from copy import copy, deepcopy

orig = [[1], [2]]
sh = copy(orig)
dp = deepcopy(orig)
orig[0].append(99)
# sh[0] reflects change (shared inner list), dp[0] does not
```

Hashing, dict/set keys and immutability

- Keys in dicts and members of sets must be hashable: their hash must not change during their lifetime.
- Mutable objects are usually unhashable (list, dict, set). If you mutate an object used as a key and its hash changes, lookups break.
- Use tuples or frozenset for compound immutable keys. For composite keys consider using a canonical serialization or a stable tuple.

Default mutable argument pitfall

- Common bug:

```python
def f(a, memo=[]):
    memo.append(a)
    return memo

# Each call reuses same list
```

- Fix: use None sentinel and allocate inside function:

```python
def f(a, memo=None):
    if memo is None:
        memo = []
    memo.append(a)
    return memo
```

Immutability patterns and tools

- Use tuple/frozenset or immutable dataclasses (dataclasses.dataclass(frozen=True)) for value objects.
- typing.Final to mark variables intended as constants (static analysis only).
- Namedtuple / typing.NamedTuple for lightweight immutable records.
- attrs library and pydantic provide frozen/dataclass-like capabilities.
- For read-heavy workloads consider copy-on-write patterns or persistent immutable data structures (third-party libs).

Concurrency and mutability

- Mutable shared state requires synchronization (locks, RLock, threading primitives) or actor/message-passing to avoid races.
- Prefer immutable messages passed between threads/processes. Immutability reduces need for locking.
- For multiprocessing, use multiprocessing-safe constructs (Queues) or share immutable data via shared memory/read-only mapping.

Performance and memory notes

- Immutables can be interned (small ints, short strings) saving memory and improving comparisons.
- Mutable containers have overhead for dynamic resizing; e.g., list growth amortized O(1) append.
- Copying large structures is expensive; prefer views, generators, or structural sharing when possible.

Practical rules of thumb

- Use immutable types for keys and values that should not change.
- Avoid exposing internal mutable structures directly; return copies or read-only views if necessary.
- Prefer explicit contracts: document whether functions modify inputs.
- For libraries, avoid mutating arguments unless API clearly states so.

Common interview prompts

- Explain "pass-by-assignment" and give an example where a function mutates its argument.
- Why are tuples hashable but lists are not? What are implications for dict keys?
- Demonstrate the default mutable argument bug and how you fix it.
- How would you design thread-safe access to a shared cache implemented as a dict?
- When would you choose deep copy vs shallow copy? Give an example.

Further reading and exercises

- Implement a function that returns an immutable snapshot of a nested structure (convert to tuples/frozensets).
- Explore dataclasses with frozen=True and write a sample value object.
- Benchmark list copy vs view vs generator for large datasets.

Notes

- This guide focuses on behavioral and practical aspects to help reasoning in interviews and in real code. For production-critical code, measure and profile choices before optimizing.
