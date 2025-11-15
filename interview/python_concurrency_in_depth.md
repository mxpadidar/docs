# Python Concurrency — Threads, Processes, Asyncio (In-Depth)

Purpose: Complete, standalone reference for Python concurrency: models, libraries, primitives, patterns, examples, and practical guidance on when/why to use each approach.

Contents

- Concurrency vs Parallelism
- Global Interpreter Lock (GIL) and implications
- Concurrency options in Python: threading, multiprocessing, asyncio, concurrent.futures
- Threads: API, primitives, common patterns, pitfalls
- Processes: API, IPC, pickling, spawn/fork semantics
- Asyncio: event loop, coroutines, tasks, cancellation, synchronization primitives
- Choosing between models (I/O-bound vs CPU-bound, latency vs throughput)
- Combining models, executors, and best practices
- Debugging, testing, monitoring, performance tips
- Interview prompts and quick recipes

Concurrency vs Parallelism

- Concurrency: structuring program to make progress on multiple tasks logically at once (interleaved execution).
- Parallelism: executing multiple tasks literally at the same time on multiple CPU cores.
- In Python, concurrency can be achieved with threads, processes, or async I/O; parallelism for CPU-bound tasks requires multiple processes or native extensions.

Global Interpreter Lock (GIL)

- CPython has a GIL: a process-wide mutex that prevents multiple native threads from executing Python bytecode simultaneously.
- Implication: threads do not yield CPU-parallelism for CPU-bound Python code; they still help with I/O-bound tasks.
- GIL does not prevent parallelism in C extensions that release the GIL (e.g., NumPy heavy computations) or when using multiprocessing.

Overview of concurrency options

- threading: in-process OS threads; good for I/O-bound workloads and simpler shared-memory interactions.
- multiprocessing: separate processes; bypass GIL, suitable for CPU-bound tasks; heavier IPC.
- asyncio: single-threaded cooperative concurrency using coroutines and an event loop; great for scalable I/O and many concurrent connections.
- concurrent.futures: high-level API offering ThreadPoolExecutor and ProcessPoolExecutor for simple parallelism.

Threads (threading module)

- Use cases: I/O-bound tasks (network calls, disk I/O), background tasks.
- Key APIs: threading.Thread, Lock, RLock, Event, Condition, Semaphore.
- Example:
  - Create thread: t = threading.Thread(target=worker, args=(...)); t.start(); t.join()
- Synchronization:
  - Lock: mutual exclusion for critical sections.
  - RLock: reentrant lock for recursive locking.
  - Condition: wait/notify patterns.
  - Semaphore: limit concurrency (e.g., connection pool).
- Pitfalls:
  - Race conditions: simultaneous access to shared mutable state.
  - Deadlocks: circular waiting on locks.
  - Resource contention: threads share the same memory and GIL causes context switching overhead.
- Atomicity:
  - Some operations are atomic in CPython (e.g., appending to list is thread-safe at C level), but relying on such behavior is brittle; always protect shared mutable state via locks.
- Example snippet:

```python
# filepath: /home/mxpadidar/Documents/docs/interview/python_concurrency_in_depth.md
import threading

counter = 0
lock = threading.Lock()

def worker():
    global counter
    for _ in range(1000):
        with lock:
            counter += 1

threads = [threading.Thread(target=worker) for _ in range(10)]
for t in threads:
    t.start()
for t in threads:
    t.join()
print(counter)  # expected 10000
```

Multiprocessing (multiprocessing module)

- Use cases: CPU-bound tasks, bypassing GIL, isolation per process.
- Models: Process, Pool, shared memory, Manager proxies.
- IPC options: pipes, queues, shared memory (multiprocessing.shared_memory), Manager-based proxies (multiprocessing.Manager).
- Spawn vs fork:
  - spawn (default on Windows, available on Unix): child imports and runs initializers; safer with threads; avoids forking state.
  - fork (default on Unix historically): faster startup but can be problematic with threads or external state (e.g., DB connections).
- Pickling:
  - Function arguments and return values must be picklable for most IPC patterns; closures/lambdas may not be picklable across platforms.
- Example:

```python
# filepath: /home/mxpadidar/Documents/docs/interview/python_concurrency_in_depth.md
from multiprocessing import Pool

def heavy(x):
    return x * x

if __name__ == "__main__":
    with Pool(4) as p:
        print(p.map(heavy, range(10)))
```

- Pitfalls:
  - Overhead of process creation and IPC; not ideal for many tiny tasks without batching.
  - Shared mutable state is harder; use explicit managers or shared memory.
  - Debugging processes can be more complex.

Asyncio (async/await, event loop)

- Model: cooperative multitasking—coroutines yield control with await; a single-threaded event loop schedules tasks.
- Use cases: high-concurrency I/O-bound workloads (thousands of open sockets), low-latency servers, network clients.
- Key concepts:
  - coroutine: async def f(): ...
  - task: asyncio.create_task(coro) schedules coroutine execution.
  - event loop: runs tasks, handles I/O readiness.
  - futures: low-level primitives representing eventual result.
- Primitives & synchronization: asyncio.Lock, Event, Condition, Queue—cooperative versions of threading primitives.
- Cancellation & timeouts: asyncio.TimeoutError, task.cancel(), shield, wait_for.
- Integrating blocking code:
  - run blocking I/O in executor: loop.run_in_executor(None, blocking_fn)
  - use ThreadPoolExecutor or ProcessPoolExecutor for CPU-bound work.
- Example server snippet (async HTTP client example):

```python
# filepath: /home/mxpadidar/Documents/docs/interview/python_concurrency_in_depth.md
import asyncio
import aiohttp

async def fetch(session, url):
    async with session.get(url) as resp:
        return await resp.text()

async def main(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(fetch(session, u)) for u in urls]
        results = await asyncio.gather(*tasks)
        return results

# run: asyncio.run(main([...]))
```

- Pitfalls:
  - Blocking the event loop (sync I/O or CPU work) stalls all tasks—must offload blocking calls.
  - Third-party libraries must be async-compatible; else use executors.
  - Debugging stack traces across awaits can be unfamiliar; use asyncio debug mode.

concurrent.futures (high-level)

- ThreadPoolExecutor: easy offloading of I/O-bound tasks to threads.
- ProcessPoolExecutor: easy parallelization for CPU-bound tasks; similar pickling constraints as multiprocessing.
- Example:

```python
# filepath: /home/mxpadidar/Documents/docs/interview/python_concurrency_in_depth.md
from concurrent.futures import ThreadPoolExecutor, as_completed

with ThreadPoolExecutor(max_workers=10) as ex:
    futures = [ex.submit(request, url) for url in urls]
    for fut in as_completed(futures):
        process(fut.result())
```

Choosing between models (rules of thumb)

- I/O-bound, high concurrency, many sockets -> asyncio or threads with async libraries. Asyncio typically scales better with lower memory and fewer threads.
- CPU-bound tasks -> multiprocessing / ProcessPoolExecutor or native C extensions that release GIL.
- Simpler concurrency and compatibility with blocking libraries -> threads (threading) or ThreadPoolExecutor.
- Mixed workloads -> asyncio for I/O plus run_in_executor for CPU work, or a hybrid architecture (separate worker processes).
- Low-latency, predictable isolation -> processes (isolation, separate memory).

Combining models

- Use concurrent.futures executors inside asyncio via loop.run_in_executor or asyncio.to_thread (Python 3.9+).
- Spawn worker processes that consume tasks from a queue (e.g., multiprocessing.Queue or external broker like Redis/Kafka) for decoupling.
- Avoid complex mixes of threads + fork: fork after process is single-threaded to avoid duplicating locks.

Synchronization patterns & pitfalls

- Avoid holding locks across blocking operations or network calls to prevent deadlocks and poor throughput.
- Prefer fine-grained locks or lock-free designs where feasible.
- Use immutable messages and message-passing to reduce shared-state complexity.
- Deadlocks: avoid circular lock acquisition; establish lock ordering or use try-lock with timeouts and retries.
- Race conditions: protect shared state, use atomic primitives where possible, and prefer message passing.

### Race conditions & deadlocks

Race condition

- Definition: a bug that occurs when multiple threads/processes access and modify shared state concurrently and the program outcome depends on the interleaving of operations.
- Simple example (lost update):

```python
# filepath: /home/mxpadidar/Documents/docs/interview/python_concurrency_in_depth.md
counter = 0

def inc():
    global counter
    for _ in range(1000):
        # read-modify-write not atomic -> race
        counter += 1
```

- Why it fails: counter += 1 compiles to separate read/modify/write bytecode; two threads can read same value then both write back, losing one increment.
- Prevention:
  - Use locks (threading.Lock) to protect critical sections.
  - Use atomic counters from libraries or rely on C extensions that release GIL.
  - Prefer message-passing (queues) to avoid shared mutable state.
  - Keep critical sections minimal.

Deadlock

- Definition: a situation where two or more threads/processes wait indefinitely for resources held by each other, forming a cycle; no progress is possible.
- Classic example:

```python
# filepath: /home/mxpadidar/Documents/docs/interview/python_concurrency_in_depth.md
import threading
a = threading.Lock()
b = threading.Lock()

def t1():
    with a:
        with b:
            pass

def t2():
    with b:
        with a:
            pass
```

If t1 acquires `a` while t2 acquires `b`, both block on the other lock → deadlock.

- Prevention strategies:
  - Lock ordering: establish a global order for acquiring multiple locks and always acquire locks in that order.
  - Try-lock with timeout: attempt to acquire locks with timeout and back off/retry if not all acquired.
  - Avoid nested locks where possible; hold locks for the shortest duration.
  - Use higher-level concurrency constructs (queues, actor model) to eliminate shared locks.
  - Use deadlock detection / watchdogs in complex systems; prefer design that makes cycles impossible.
- Practical tips:
  - Document lock ownership and intended ordering.
  - Avoid doing I/O or blocking work while holding locks.
  - Prefer immutable data and message passing for complex interactions.

Performance tips

- Measure: use timeit, perf, or realistic load tests.
- For many short tasks, thread/process spawn overhead matters—use pools or batch work.
- Asyncio reduces per-connection memory compared to threads when handling many simultaneous connections.
- For CPU-heavy numerical work, use libraries that release GIL (NumPy), or distribute work across processes.

Debugging & testing concurrency

- Reproduce concurrency issues with stress tests, larger worker counts, and tools such as pytest-xdist.
- Use logging with thread/process/task identifiers and correlation ids.
- For asyncio, enable debug: asyncio.get_event_loop().set_debug(True) and use tracemalloc for memory issues.
- Use race detection tools and static analysis where available, but most concurrency bugs require dynamic testing.

Security & resource considerations

- Limit number of threads/processes to avoid resource exhaustion.
- Manage file descriptors and connection pools; set timeouts.
- Be mindful of safe handling of secrets and close resources properly in child processes.

Operational patterns

- Prefer external task queues (Celery, RQ, Dramatiq) for long-running background tasks; they manage worker processes and retries.
- Use circuit breakers, bulkheads, and backpressure when services call external dependencies.
- Monitor thread/process counts, queue lengths, CPU usage, and event loop latencies.

Practical recipes

- I/O server with asyncio + uvloop (optional) for best throughput.
- CPU pool: ProcessPoolExecutor with chunked map for heavy calculations.
- Combining: HTTP server in asyncio, offload blocking DB calls to thread pool or use async DB drivers.

Interview prompts

- Explain GIL and how it affects threads in Python.
- Design an architecture for a web scraper that needs to fetch 10k pages quickly—what concurrency model do you choose and why?
- Show how you’d safely share a counter across threads vs processes.
- Explain how to integrate a blocking library into an asyncio application.
- Describe common causes of deadlocks and how you’d debug one.

Further reading

- Python docs: threading, multiprocessing, asyncio, concurrent.futures.
- "Python Concurrency with asyncio" articles and PEPs (PEP 3156, etc.).
- Libraries: aiohttp, trio (alternative async model), uvloop (high performance event loop).
- Practice: implement small projects using each model; measure and compare.

Notes

- This document aims to be a complete practical reference for interviews and real-world engineering decisions. Always benchmark with realistic workloads and prefer simpler models that meet requirements.
