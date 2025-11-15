# Django & DRF — Pagination, Filtering, Querying, and Best Practices

Purpose: Complete, self-contained reference for implementing and reasoning about pagination, filtering, searching and querying with Django & Django REST Framework (DRF). Includes configuration examples, performance tips, and interview-style prompts.

Contents

- Settings & quick setup
- Pagination (page-number, limit-offset, cursor, keyset)
- Filtering & search (DRF filters, django-filter, custom filters)
- Querying techniques (select_related, prefetch_related, annotate, aggregate, Q/F)
- Performance considerations and optimizations
- API design and client guidance
- Testing, metrics, and common pitfalls
- Interview prompts

Settings & quick setup

- Minimal REST_FRAMEWORK config:
  REST_FRAMEWORK = {
  "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
  "PAGE_SIZE": 20,
  "DEFAULT_FILTER_BACKENDS": [
  "django_filters.rest_framework.DjangoFilterBackend",
  "rest_framework.filters.SearchFilter",
  "rest_framework.filters.OrderingFilter",
  ],
  }
- Install django-filter for richer filtering: pip install django-filter and add 'django_filters' to INSTALLED_APPS.

Pagination: types, trade-offs, examples

- PageNumberPagination

  - Simple: /items/?page=3
  - Pros: easy to use; cons: offset performance (DB does COUNT and OFFSET), unstable with concurrent writes.
  - Example:
    class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100

- LimitOffsetPagination

  - /items/?limit=50&offset=100
  - Pros: flexible; cons: offset cost for deep pages.
  - Example: use when clients need explicit offsets or partial scroll.

- CursorPagination (DRF)

  - Stable, encoded cursor referencing ordering position: /items/?cursor=abc123
  - Pros: avoids OFFSET, stable with inserts/deletes if ordering deterministic; cons: requires unique ordering fields and opaque cursor.
  - Example:
    class CursorSetPagination(CursorPagination):
    page_size = 20
    ordering = "-created_at" # must be deterministic

- Keyset pagination (manual)

  - Use WHERE/ORDER BY + LIMIT pattern (e.g., created_at < last_seen_created_at), often faster than OFFSET for large tables.
  - Implement via cursor token that contains last-seen key(s). Preferred for very large datasets.
  - Example QuerySet pattern:
    qs = Model.objects.filter(created_at\_\_lt=cursor_ts).order_by['-created_at'](:page_size)

- Choosing:
  - Small datasets or admin UIs: page-number OK.
  - Public APIs with deep pagination: cursor or keyset recommended.
  - Very large tables: keyset or cursor to avoid OFFSET.

Filtering & search

- DRF built-in filters:
  - SearchFilter: query param 'search' with simple OR across fields; uses PostgreSQL ILIKE or DB text ops.
  - OrderingFilter: order_by fields, specified via 'ordering' param.
- django-filter (recommended)

  - Define FilterSet for declarative, typed filtering (exact, range, date, boolean, related fields).
  - Example:
    import django_filters
    class ProductFilter(django_filters.FilterSet):
    price_min = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    price_max = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    category = django_filters.CharFilter(field_name="category\_\_slug")
    class Meta:
    model = Product
    fields = ["is_active", "category", "price_min", "price_max"]
  - In ViewSet: filterset_class = ProductFilter

- Advanced filtering patterns:
  - Filtering by related fields: use **traversal (author**username).
  - Filtering with Q objects for OR logic or complex predicates.
  - Field-level performance: avoid unindexed LIKE on big text columns; use full-text search if needed.

Search / full-text

- For simple needs use SearchFilter or PostgreSQL's full-text search (SearchVector, SearchQuery).
- For relevance and advanced queries, index to Elasticsearch/OpenSearch and keep DB as source of truth.

Querying techniques and ORM features

- select_related: follow FK/OneToOne via JOIN; reduces query count for single-related objects.
- prefetch_related: separate query + in-Python join for M2M or reverse FK; good to avoid cartesian explosion.
- annotate / aggregate: use .annotate(Count('comments')), .aggregate(Sum('amount')) to compute server-side.
- F expressions: perform DB-side arithmetic (F('value') + 1).
- Q objects: build dynamic OR/AND conditions; combine with & and |.
- values/values_list: return dict/tuple rows without model instantiation for performance.
- defer/only: limit loaded columns to reduce transfer and model instantiation cost.

Performance considerations

- N+1 queries: detect via django-debug-toolbar or logging connection.queries. Use select_related/prefetch_related to fix.
- COUNT(\*) cost: expensive on large tables with joins; avoid unnecessary .count() on every page; consider approximate counts (Postgres stats) or omit total_count for deep pagination.
- Indexes: create indexes used for WHERE and ORDER BY columns. Cursor/keyset pagination benefits from index on ordering column(s).
- Avoid heavy annotations on large result sets unless necessary; consider precomputed aggregates or materialized views.
- Bulk operations: use bulk_create/bulk_update for batch writes to reduce DB roundtrips.
- Transactions: wrap multi-step writes in atomic transactions to maintain integrity.
- Caching: cache responses or computed pages (Redis) when data is mostly read-only.

API design and client tips

- Return pagination metadata (count, next, previous, results) or link headers for RESTful clients.
- For infinite scroll, prefer cursor/keyset pagination.
- Expose page_size limits and enforce max_page_size to avoid client abuse.
- Document filter parameters and allowed ordering fields; validate server-side.

Examples: ViewSet with filters & pagination

- Minimal ViewSet:
  from rest_framework import viewsets
  from django_filters.rest_framework import DjangoFilterBackend
  from rest_framework.filters import SearchFilter, OrderingFilter

  class ProductViewSet(viewsets.ModelViewSet):
  queryset = Product.objects.all().select_related('category')
  serializer_class = ProductSerializer
  pagination_class = CursorSetPagination # or StandardResultsSetPagination
  filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
  filterset_class = ProductFilter
  search_fields = ['name', 'description']
  ordering_fields = ['price', 'created_at']
  ordering = ['-created_at']

Testing & monitoring

- Tests:
  - Use APIClient to request pages and assert pagination metadata.
  - Test filter combinations and ordering stability.
  - Test cursor boundaries and edge cases (deleted items).
- Metrics:
  - Monitor query counts per endpoint, p99 latency, DB slow queries, pagination-related heavy queries.
  - Alert on abnormal counts or slow aggregations.

Common pitfalls & mitigations

- Deep OFFSET pages are slow — migrate to cursor/keyset.
- Using ORDER BY on unindexed columns — add index or avoid.
- Counting with joins -> expensive; consider deferring count or using approximate counts.
- Inconsistent ordering with pagination -> ensure deterministic ordering using unique tie-breaker (id).
- Serializing large objects list -> stream results or limit page_size.

Interview prompts

- Compare page-number, limit-offset, cursor and keyset pagination; when choose each?
- How do you fix an N+1 problem in DRF list endpoints?
- Design a cursor pagination approach for a feed that must remain stable under new inserts.
- How to implement filtering by nested related fields and ensure performance?

Further reading & tools

- DRF docs: Pagination, Filters
- django-filter docs and examples
- django-debug-toolbar and silk for query inspection
- Postgres keyset pagination patterns and explain analyze for tuning

Notes

- Always profile with realistic data. Start with simple, correct design; optimize with indexes, adjusted pagination, caching and precomputation when necessary.
