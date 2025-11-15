# Architecture & Cross-Boundary Thinking — Practical Guide

Purpose: Understand cross-system concerns: caching, API design, async events, and scaling patterns.

## Caching layers & cache invalidation

- Layers: client (browser cache), CDN, edge caches, application cache (Redis/Memcached), DB cache (materialized views).
- Strategies:
  - Cache-aside: application checks cache, on miss fetches DB and populates cache.
  - Write-through: write goes to cache and persistent store synchronously.
  - Write-back: write goes to cache and asynchronously persisted (riskier).
- Invalidations: TTLs, explicit delete on writes, versioned keys. Prefer short TTLs for highly dynamic data and versioning for complex invalidation.
- Pitfalls: stale data, cache stampede — mitigate with locking, request coalescing, or probabilistic early expiration.

## REST design principles

- Resources are nouns; actions via HTTP verbs (GET/POST/PUT/PATCH/DELETE).
- Use proper status codes, content negotiation, and pagination.
- Versioning: URL (v1) or header-based; plan for backward compatibility.
- Idempotency: PUT should be idempotent; POST not necessarily.
- HATEOAS optional — focus on clear, discoverable endpoints and docs (OpenAPI).

## Event-driven architecture & async pipelines

- Producers emit events to a broker (Kafka, RabbitMQ). Consumers subscribe and process events.
- Patterns: pub/sub for broadcast, queue for task processing, event sourcing for audit/history.
- Design events small and versioned; avoid coupling consumers to producer schemas.
- Idempotency in consumers: dedupe using event IDs, store processed offset/state.

## Scaling patterns

- Vertical vs horizontal scaling: prefer horizontal where possible.
- Read replicas: offload read-heavy workloads; handle eventual consistency and replication lag.
- Sharding: split by partition key (user_id, tenant_id). Design to avoid hot partitions.
- Rate limiting: token bucket or leaky bucket. Implement at gateway or service boundary.
- Circuit breakers and bulkheads to isolate failures and prevent cascading failures.

## Interview prompts

- Design a cache strategy for product catalog with frequent reads and occasional writes.
- Explain how you'd add a new consumer to an event streaming pipeline without affecting producers.

Commands & tools:

- Use load tests (locust, k6) to validate scaling choices.
- Use tracing (OpenTelemetry) to identify cross-service latency.
