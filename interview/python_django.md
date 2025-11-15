# Python & Django — Complete Interview Guide

Purpose: Read this file to understand core Django internals, design patterns, performance considerations, and practical examples you can discuss in interviews.

Table of contents

- Django request/response cycle
- ORM internals & query optimization
- select_related vs prefetch_related (with examples)
- Class-based vs function-based views
- Settings, middleware, signals, apps structure
- Forms & DRF serializers
- Authentication & authorization patterns
- Clean, maintainable, testable Django code
- Async capabilities in Django 4+ (what's supported, what's not)
- Interview prompts

## Django request/response cycle

- Entrance: WSGI (sync) or ASGI (async) server accepts connection -> server calls Django application.
- Django wraps incoming data into HttpRequest/ASGI scope -> middleware chain (process_request/process_view for sync; async middleware for ASGI) -> URL resolver matches view -> view executes -> view returns HttpResponse (or StreamingHttpResponse, JsonResponse, HttpResponseNotFound, etc.) -> middleware process_response runs -> final response to server -> client.
- Middleware ordering matters: top-to-bottom on request, reverse on response.
- Typical performance pitfalls: heavy synchronous DB or I/O in middleware or views, long-running templates rendering, large response bodies without streaming.

Example flow (sync):

- WSGI server -> process_request (mw1) -> process_request (mw2) -> url resolver -> view -> process_response (mw2) -> process_response (mw1) -> WSGI server.

## Django ORM internals & query optimization

- QuerySets are lazy: building is cheap; evaluation happens on iteration, bool check, serialization, slicing that hits DB, or calling .list(), .count(), .exists().
- QuerySet pipeline: Python expression -> Query object -> SQL compiler -> DB cursor -> row factory -> model instances.
- Use .only()/.defer() to limit columns; .values()/values_list() to get raw dicts/tuples and avoid model instantiation if you don't need methods.
- Avoid forcing evaluation inside loops (N+1 problem).

Performance tools:

- django-debug-toolbar, logging with connection.queries, EXPLAIN on raw SQL for heavy queries.

## select_related vs prefetch_related

- select_related: performs SQL JOINs and populates related objects in the same query. Best for foreign keys and one-to-one relations. Example:
  - MyModel.objects.select_related('author').get(pk=1) -> 1 query with JOIN.
- prefetch_related: issues separate queries and does in-Python joining. Best for many-to-many and reverse FK. Example:
  - books = Book.objects.filter(published=True).prefetch_related('tags') -> 2 queries, tags attached to each book.
- Performance rule: for single-valued relations use select_related; for set-valued relations use prefetch_related. For deep nested relations combine both strategically.
- Pitfall: over-joining can produce huge result sets due to cartesian product; prefetch_related avoids that.

## Class-based views vs function-based views

- Function-based views (FBV): explicit, easy to read for simple endpoints.
- Class-based views (CBV): provide structure, reusability via mixins and generic views (ListView, DetailView, CreateView). Useful to avoid repeating boilerplate.
- DRF (Django REST Framework): APIView, GenericAPIView, ViewSets + Routers for REST endpoints. ViewSets reduce routing boilerplate.
- When to use: FBV for simple endpoints; CBV for repeated patterns or where you want reusable behaviors. Be explicit in CBVs: override dispatch / get / post and test the flow.

## Settings, middleware, signals, apps structure

- Settings: keep secrets out of source (env vars, Django-environ), split settings (base.py, dev.py, prod.py), use django-configurations or pydantic-based config patterns if you prefer typed config.
- Middleware: write small, focused middleware. Prefer add-on middlewares that are idempotent. Avoid direct DB writes in middleware on high-traffic apps.
- Signals: use for decoupled side-effects (e.g., post_save cleanup). Avoid business-critical flows in signals; they are harder to trace and test. Consider explicit service calls instead.
- Apps: organize by domain (accounts/, billing/, catalog/) rather than technical layers when domain-driven. Use AppConfig.ready() carefully (avoid heavy work there).

## Forms & DRF serializers

- Django Forms: validation, clean\_ methods, widget rendering for HTML.
- DRF Serializers: .validate(), field-level validators, nested serializers, SerializerMethodField for computed fields.
- Performance note: avoid deep nested serializers for list endpoints; prefer hyperlinked or summary serializers for lists and detail serializers for single-resource endpoints.
- Example DRF pattern: use ListSerializer with many=True and a lightweight serializer for lists.

## Authentication & authorization patterns

- Authentication: session-based (browser), token-based (Bearer tokens, JWT), OAuth2/OIDC for third-party auth. Consider refresh tokens and short-lived access tokens for security.
- Authorization: coarse-grained (role-based access control — RBAC) and fine-grained (object-level permissions).
- DRF provides permission classes (IsAuthenticated, IsAdminUser), and you can implement custom BasePermission classes.
- Best practice: enforce auth at the boundary (views/API) and re-check invariants in the service layer for critical business logic.

## Clean, maintainable, testable Django code

- Keep views thin; push business logic into services/domain modules.
- Use repository pattern sparingly — prefer explicit QuerySet methods and manager methods when data access abstraction helps testing.
- Dependency injection: pass services/repositories as parameters to functions or constructors for easier mocking.
- Testing: unit test services, integration test views with Django test client or APIClient (DRF). Use pytest + pytest-django + factory_boy for fixtures.
- CI: run linters (flake8/ruff), type checks (mypy/pyright), and tests.

## Async capabilities in Django 4+

- Supported: async views (async def view(request)), async middleware, async handlers in ASGI deployments. Django's request lifecycle supports async callables.
- Caveats: many ORM operations remain synchronous; as of Django 4.x more operations are async-friendly but some database backends and third-party libs are sync-only — calling sync DB ops in async code blocks requires sync_to_async or running in threadpool.
- Use case: async views make sense when awaiting external I/O (HTTP, websocket, background services). For CPU-bound tasks use background workers.
- Example: async view with httpx (async HTTP client), or integrating Channels for websockets.
- Not supported/warning: Blocking the event loop with sync DB calls or long-running CPU tasks will degrade performance.

## Interview prompts

- Explain the lifecycle of a Django request through middleware and routing.
- Demonstrate fixing an N+1 problem and explain why your approach improves performance.
- When would you prefer prefetch_related over select_related and why?
- How do you structure settings for multiple environments and secrets?
- What are the trade-offs when adding async views to a Django codebase?

Appendix: quick snippets, debug commands

- Show SQL for a queryset: print(str(qs.query)) or qs.query.get_compiler(connection=connection).as_sql()
- DB profiling: pip install django-debug-toolbar
- Running a management command to run migrations and show SQL: python manage.py sqlmigrate app_label 0001
