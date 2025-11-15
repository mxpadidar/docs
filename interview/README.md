# Interview Notes — Backend / Django & Systems

This folder contains self-contained study notes for backend interviews. Each file is written so you can read it end-to-end without extra search.

Files:

- **python_django.md** — Complete Django concepts: request/response cycle, ORM internals, query optimization, select_related/prefetch_related, CBV vs FBV, settings/middleware/signals/apps, forms & DRF serializers, auth/authorization patterns, clean/testable code practices, async in Django 4+.
- **relational_databases.md** — Indexes, transactions & isolation levels, joins/subqueries/window functions, query optimization with EXPLAIN, migrations and schema design, normalization vs pragmatic denormalization.
- **software_design.md** — SOLID principles, dependency injection in Python, common architectures, reasoning about boundaries and data flow, error handling, retries and idempotency.
- **data_structures_algorithms.md** — Time/space complexity, hash maps, heaps, trees, graphs, queues, common algorithms and trade-offs for backend systems.
- **architecture_cross_boundary.md** — Caching layers and invalidation strategies, REST design principles, event-driven architecture & async pipelines, scaling patterns (replicas, sharding, rate limiting).
- **git_workflows.md** — Rebasing vs merging, conflicts, best practices and sample commands.
- **search_data_tech.md** — When to use Elasticsearch, full-text vs relational search, Cassandra basics, and high-volume log/event pipeline design.
- **monitoring_tools.md** — Observability: metrics, logs, traces; Prometheus, Grafana, Alertmanager, Sentry, ELK/Opensearch, Datadog; SLIs/SLOs/alerting best practices.
- **microservices.md** — Microservices and Service-Oriented Architecture: service decomposition, communication patterns (sync/async), data consistency, sagas & transactions, deployment, service discovery, service mesh, observability, testing, and CI/CD strategies.
- **hash_tables.md** — Hash tables: concepts, collision resolution strategies (chaining, open addressing), hash functions, load factor & resizing, deletion/tombstones, Python dict internals, concurrency considerations, examples and interview prompts.
- **python_data_structures_in_depth.md** — Deep dive: mutable vs immutable types, Python's parameter-passing semantics (pass-by-assignment), shallow vs deep copy, hashing and immutability, default mutable argument pitfalls, concurrency implications, immutability patterns (frozen dataclass, tuples, frozenset), and practical examples.
- **python_dicts.md** — Comprehensive guide to Python dicts: what can be keys, hashability rules, dict methods and views, iteration order, dict comprehensions, merging/update semantics, shallow vs deep copy (with examples), performance characteristics, implementation notes, mapping protocol, common pitfalls and best practices.
- **python_concurrency_in_depth.md** — In-depth: threading, multiprocessing, asyncio (coroutines & event loop), GIL and parallelism vs concurrency, synchronization primitives, common pitfalls (deadlocks, race conditions), patterns, examples, and guidance when to choose each approach.
- **django_drf_querying.md** — DRF & Django querying: pagination (page-number, limit-offset, cursor, keyset), filtering (SearchFilter, OrderingFilter, django-filter), queryset patterns (select_related/prefetch, annotate/aggregate, Q/F expressions), performance tips, API design, testing examples and recipes.
- **django/** — Folder with focused Django & DRF recipes and runnable examples:
  - paginations.md — PageNumber, LimitOffset, Cursor, and keyset pagination with DRF examples.
  - filtering.md — django-filter, DRF Search/Ordering filters, and custom filter backends.
  - query_and_queryset.md — QuerySet internals, select_related/prefetch_related, annotate, F/Q, values(), raw() and EXPLAIN examples.
  - views_comparison.md — APIView vs Generic views vs ViewSets (ModelViewSet) with sample code and routing.

How to use:

- Read files top-to-bottom. Each file contains short examples, pitfalls, and interview prompts.
- Use the "Interview prompts" sections to rehearse answers or create flashcards.

Contact: These notes are intended as study material. Update files to add your own examples and questions.
