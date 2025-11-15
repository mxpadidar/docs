# Microservices & Service-Oriented Architecture — Complete Guide

Purpose: Read this file end-to-end to understand microservice design, trade-offs, communication, data consistency patterns, resilience, deployment and operational practices you can discuss in interviews.

Table of contents

- Overview & when to choose microservices
- SOA vs microservices
- Service boundaries & decomposition
- Communication patterns (sync vs async)
- Data management, transactions & consistency
- Common distributed patterns (sagas, CQRS, event sourcing)
- Resilience & reliability patterns
- API design & versioning, contract testing
- Deployment, orchestration & service discovery
- Observability & monitoring for microservices
- Security & multi-tenant considerations
- Testing & CI/CD strategies
- Interview prompts

## Overview & when to choose microservices

- Microservices: small, independently deployable services owned by a single team, communicating over network APIs.
- Choose when you need autonomous teams, independent scaling, polyglot stacks, or deploy-freedom. Avoid premature microservices for small projects—operational complexity grows quickly.
- Benefits: independent deploys, fault isolation, scaling per-service, technology freedom. Costs: distributed systems complexity, operational burden, data consistency issues.

## SOA vs microservices

- SOA (Service-Oriented Architecture): broader enterprise focus, often with an enterprise service bus; services can be larger and more integrated.
- Microservices: emphasize small, bounded-context services, decentralized governance, lighter-weight comms (HTTP/gRPC/events).
- Key difference: granularity and operational decentralization.

## Service boundaries & decomposition

- Decompose by business capability (bounded context) not technical layers.
- Guiding questions: who owns the data? who owns the lifecycle of an object? what changes together?
- Anti-patterns: splitting by technical layers (UI/API/DB) or by table -> leads to chatty comms and coupling.

Example decomposition (e-commerce): catalog, pricing, inventory, checkout, payments, user-profile, recommendations.

## Communication patterns (sync vs async)

- Synchronous: HTTP/REST or gRPC. Simple, low latency, but causes tight coupling and cascading failures.
  - Use for request-response flows where immediate result required.
  - Example: gRPC for internal RPC with protobuf schemas.
- Asynchronous: message brokers (Kafka, RabbitMQ, Pulsar). Decouples producers/consumers and enables resilience and replayability.
  - Use for events, notifications, background processing, and high-throughput feeds.
- Hybrid: use sync for queries/commands needing immediate response; async for eventual consistency and fan-out.

Practical tip: prefer idempotent operations, include correlation IDs in headers, and keep messages small and schema-versioned.

## Data management, transactions & consistency

- Database-per-service: each service owns its data store to avoid coupling; replicate or duplicate data where reads require it.
- Challenges: distributed transactions. Avoid two-phase commit in most microservices; prefer eventual consistency patterns.
- Patterns:
  - Sagas (choreography or orchestration): series of local transactions with compensating actions on failure.
  - Event sourcing + materialized views: append-only events are source of truth; views are built asynchronously.
  - CQRS: separate models for commands (writes) and queries (reads) to optimize each side.
- Idempotency: ensure operations can be retried safely using idempotency keys or deduplication stores.

Example saga (order placement):

1. Create order (ORDER service) -> emit OrderCreated
2. Reserve inventory (INVENTORY service) -> emit InventoryReserved
3. Charge payment (PAYMENTS service) -> emit PaymentSucceeded
   If payment fails -> emit PaymentFailed -> compensate by releasing inventory and marking order cancelled.

## Common distributed patterns

- Circuit Breaker: prevent cascading failures; open circuit on repeated errors, allow limited retries.
- Bulkhead: isolate resources per-service to prevent resource exhaustion (thread pools, connection pools).
- Retries with exponential backoff + jitter.
- Backpressure: handle overload gracefully; brokers and queues help buffer.
- Dead-letter queues for poison messages.

## Resilience & reliability

- Design for partial failure: services may be down or slow; degrade gracefully.
- Timeouts: set sane client and server timeouts.
- Use health checks (liveness/readiness) for orchestrators to manage traffic.
- Implement retries only where operations are idempotent, and include retry budgets.

## API design & versioning, contract testing

- API design: use consistent resource naming, clear semantics for PUT vs PATCH vs POST, use hypermedia if helpful, and publish OpenAPI/Protobuf specs.
- Versioning options: URI (v1), header, or content negotiation. Aim for backward compatibility where possible.
- Contract testing: use consumer-driven contract testing (Pact) to ensure changes don’t break clients.
- Schema evolution: design messages and APIs to be additive—avoid removing fields unexpectedly.

## Deployment, orchestration & service discovery

- Packaging: containerize services (Docker). Keep images minimal and reproducible.
- Orchestration: Kubernetes for scheduling, scaling, deployment strategies (rolling, blue/green, canary).
- Service discovery: DNS-based (Kubernetes), or dedicated (Consul). For internal comms prefer platform-native discovery.
- Service mesh (Istio/Linkerd): observability, mTLS, traffic shaping, retries and circuit breaking at platform level—useful but adds complexity.

Example deploy patterns:

- Canary: route small percentage of traffic to new version and monitor.
- Blue/Green: switch traffic suddenly from old to new after validation.

## Observability & monitoring for microservices

- Correlation IDs: propagate request id across services; tie logs/metrics/traces together.
- Tracing: OpenTelemetry + Jaeger/Zipkin for distributed traces to find latency hotspots.
- Metrics: Prometheus metrics per service (HTTP latencies, error counts, queue lengths).
- Logs: structured JSON logs aggregated to ELK/Opensearch or commercial providers; include context (service, correlation id, trace id).
- SLOs/SLIs: set per-service objectives, monitor error budgets and escalate.

## Security & multi-tenant considerations

- AuthN/AuthZ: central identity provider (OAuth2/OIDC) for users; mTLS or JWT for service-to-service auth.
- Principle of least privilege for service credentials.
- Network segmentation, API gateways for ingress control, WAFs for public endpoints.
- Secrets management: use vaults (HashiCorp Vault, Kubernetes Secrets with encryption).

## Testing & CI/CD

- Unit tests for logic, component tests for modules, integration tests for service boundaries (test doubles for external services).
- Contract tests to validate provider/consumer expectations.
- End-to-end tests in a staging environment that simulates production.
- CI/CD: build -> test -> deploy with automated gating. Promote artifacts across environments (artifact registry).
- Feature flags for safe rollout and dark launches.

## Operational concerns & data migrations

- Schema migrations: prefer backward-compatible steps (add columns first, deploy consumers, backfill, then remove old fields).
- Data migration strategies: online backfills, live migrations, strangler pattern to migrate functionality piecewise.
- Scaling: replicate stateless services easily; stateful services require careful partitioning and scaling (sharding).

## Quick examples & snippets

- Simple Dockerfile
  - FROM python:3.11-slim
  - WORKDIR /app
  - COPY requirements.txt .
  - RUN pip install -r requirements.txt
  - COPY . .
  - CMD ["gunicorn", "app:app", "-b", "0.0.0.0:8000"]
- Basic event flow with Kafka:
  - producer: publish OrderCreated event to orders topic
  - consumer: inventory service consumes orders topic and reserves stock

## Interview prompts

- Design a microservice architecture for an e-commerce checkout flow: list services, data ownership, async flows, failure modes, and deployment strategy.
- Explain how you would implement a saga for order processing and how you'd handle partial failures and compensations.
- Describe trade-offs between sharing a DB across services vs database-per-service.
- How would you roll out a breaking API change with minimal client disruption?

Further reading/action items

- Practice whiteboarding service decomposition and sequence diagrams.
- Implement a simple two-service example with async messaging (producer -> Kafka -> consumer) and add tracing + metrics.

Operational checklist for production-readiness

- Health checks (liveness/readiness)
- Structured logging with correlation IDs
- Tracing and metrics instrumentation
- Alerting on error rate, latency, queue growth and resource exhaustion
- CI/CD with automated tests and safe deployment strategies
