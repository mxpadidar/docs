# Filtering & Search in Django + DRF — Practical Guide

Install:

```bash
pip install django-filter
# add "django_filters" to INSTALLED_APPS
```

Basic DRF filter setup (global)

```python
# settings.py
REST_FRAMEWORK = {
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter"
    ]
}
```

1. django-filter FilterSet (declarative)

```python
# filters.py
import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    price_min = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    price_max = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    category = django_filters.CharFilter(field_name="category__slug", lookup_expr="iexact")

    class Meta:

        model = Product

        fields = ["is_active", "category", "price_min", "price_max"]
```

Usage:

```python
# views.py
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter

    search_fields = ["name", "description"]
    ordering_fields = ["price", "created_at"]
```

2. DRF SearchFilter & OrderingFilter

- SearchFilter: /api/products/?search=shirt -> performs ILIKE/contains on configured fields; not full-text by default.
- OrderingFilter: /api/products/?ordering=-price

3. Full-text search (Postgres)

```python
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank


qs = Product.objects.annotate(
    rank=SearchRank(SearchVector('name', 'description'), SearchQuery('t-shirt'))
).filter(rank__gte=0.1).order_by('-rank')
```

For production-scale search use Elasticsearch/OpenSearch with change-data-capture sync.

4. Custom FilterBackend example

```python
from rest_framework.filters import BaseFilterBackend


class OwnerFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        owner = request.query_params.get("owner")
        if owner:
            return queryset.filter(owner__username=owner)
        return queryset

```

Performance considerations

- Avoid unindexed LIKE on large text columns; use full-text indexes or external search.
- Use indexed fields for filters and ordering.
- Limit allowed ordering fields to avoid expensive queries.
- Validate and sanitize filter input to avoid expensive patterns or injections.

Security & validation

- Apply input validation in FilterSet to prevent heavy queries (e.g., very large IN lists).
- Use rate limiting on complex filter endpoints.

Interview prompts

- How to implement case-insensitive filtering on a related field?
- When to use django-filter vs building a custom filter backend?
