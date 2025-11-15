# DRF Pagination — Examples & Recipes

Why: pagination limits result size, reduces memory and latency, and protects DB from expensive OFFSET scans.

Settings (global)

```python
# settings.py
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
}
```

1. PageNumberPagination (simple)

```python
# paginations.py
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100
```

Usage:

```python
# views.py
from rest_framework.viewsets import ReadOnlyModelViewSet
from .paginations import StandardResultsSetPagination

class ProductViewSet(ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = StandardResultsSetPagination
```

2. LimitOffsetPagination

```python
# settings or view: set pagination_class = LimitOffsetPagination
# client: /api/products/?limit=50&offset=100
```

3. CursorPagination (recommended for stable paging)

```python
from rest_framework.pagination import CursorPagination

class CursorSetPagination(CursorPagination):
    page_size = 25
    ordering = '-created_at'  # must be deterministic; include unique tie-breaker
```

Notes:

- Cursor avoids deep OFFSET cost but requires deterministic ordering (e.g., created_at + id pair).
- Cursor tokens are opaque and should be treated as such by clients.

4. Keyset pagination (manual, fastest for huge tables)
   Pattern:

```python
# client sends last_seen_id or last_seen_created_at
page_size = 50
qs = Product.objects.filter(
    Q(created_at__lt=last_seen_created_at) |
    Q(created_at=last_seen_created_at, id__lt=last_seen_id)
).order_by('-created_at', '-id')[:page_size]
```

Wrap this logic into a paginator that encodes/decodes cursors (timestamp + id).

Best practices

- Use keyset/cursor for large datasets or infinite-scroll feeds.
- Add an index on ordering columns (created_at, id).
- Avoid returning total_count for very large tables; compute asynchronously or omit for performance.

Interview prompts

- When would you choose cursor over offset pagination?
- How to implement a stable cursor using created_at and id?
