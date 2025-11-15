# Software Design — Principles & Patterns

Purpose: Practical reasoning about design choices, maintainability, testability, and system resilience.

## SOLID principles

- Single Responsibility: each module/class should have one responsibility; smaller units are easier to test.
- Open/Closed: extend systems via composition or polymorphism rather than modifying existing code.
- Liskov Substitution: derived classes must be usable via base interfaces; watch for tightened preconditions.
- Interface Segregation: prefer small, focused interfaces rather than one large interface.
- Dependency Inversion: depend on abstractions (interfaces/protocols) rather than concrete classes.

Example: service interfaces in Python using Protocols or abstract base classes to allow mocking in tests.

## Dependency injection patterns in Python

- Constructor injection: pass dependencies in **init**.
- Function injection: pass collaborators as arguments to functions (easy for single-use functions).
- Factory/provider pattern: centralize wiring for complex object graphs.
- Lightweight DI containers can help, but avoid over-engineering; explicit wiring is often clearer.

## Common architectural patterns

- Layered: presentation -> service -> repository -> DB. Good for clear separation; may create anemic domain model.
- Hexagonal (Ports & Adapters): core domain independent of I/O; useful for testability and swapping adapters.
- Module-by-domain (service modules): keep domain logic together; each module owns its models, services, tasks, and APIs.

## How to reason about system boundaries & data flow

- Define authoritative data source per domain.
- Draw sequence diagrams for critical paths to find latency and failure points.
- At boundaries, validate input strictly and return precise errors. Use contracts (OpenAPI) for service-to-service communication.

## Error handling, retries, idempotency

- Fail fast: validate inputs early.
- Retries: use exponential backoff + full jitter; cap attempts and backoff window.
- Idempotency: for non-idempotent operations require idempotency keys (e.g., payment operations).
- Compensating transactions: for eventual consistency, design compensators to undo partial effects.

## Interview prompts

- Sketch an architecture for a payment processing flow that ensures payments are not double-charged, includes retries, and supports refunds.
- Explain how you'd extract a service from a monolith and deploy it safely.

Best practices:

- Keep code modular, small public surfaces, and rely on tests and automated checks to maintain design quality.
