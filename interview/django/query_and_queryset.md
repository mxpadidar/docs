# Django QuerySet & Querying — Deep Dive

QuerySet basics

- QuerySets are lazy: construction is cheap; evaluation happens on iteration, slicing that hits DB, bool check, list(), repr(), etc.
- Common triggers of evaluation: list(qs), for x in qs, qs.count(), qs.exists(), qs[0], str(qs.query)

Inspecting SQL

```python
qs = Product.objects.filter(active=True, price__gte=10)
print(qs.query)        # shows SQL
from django.db import connection
print(connection.queries)  # in DEBUG mode; use DEBUG toolbar in dev
```

Avoid N+1 queries

- Problem: iterating objects and calling related fields triggers separate queries.
- Fix:
  - select_related for FK/OneToOne (single-valued relationships)
    ```python
    qs = Order.objects.select_related("customer__profile").filter(status="paid")
    ```
  - prefetch_related for M2M or reverse FK (collection-valued)
    ```python
    qs = Book.objects.prefetch_related("tags", "authors")
    ```

Using annotate, aggregate, F, and Q

- annotate:

```python
from django.db.models import Count
qs = Post.objects.annotate(comment_count=Count("comments")).filter(comment_count__gt=3)
```

- aggregate:

```python
from django.db.models import Avg
avg_price = Product.objects.filter(active=True).aggregate(Avg("price"))["price__avg"]
```

- F expressions (DB-side arithmetic)

```python
from django.db.models import F
Product.objects.update(stock=F("stock") - 1)
```

- Q objects (complex OR/AND)

```python
from django.db.models import Q
qs = User.objects.filter(Q(first_name__icontains="alex") | Q(email__icontains="@example"))
```

values / values_list / only / defer

- values() / values_list(): return dicts/tuples, no model instantiation — faster for simple projections.
- only()/defer(): selectively load columns to reduce transfer cost (use when models wide or big JSON/Text fields).

```python
qs = Product.objects.only("id", "name")
```

Raw SQL & EXPLAIN

- raw():

```python
for row in Model.objects.raw("SELECT id, name FROM app_model WHERE ..."):
    print(row.name)
```

- EXPLAIN:

```python
from django.db import connection
with connection.cursor() as c:
    c.execute("EXPLAIN ANALYZE " + str(qs.query))
    print("\n".join(r[0] for r in c.fetchall()))
```

Bulk operations

- bulk_create, bulk_update for many rows (fewer DB roundtrips). Beware of signals not firing for bulk_create.

```python
Model.objects.bulk_create([Model(...), ...], batch_size=500)
```

Transactions

- Use transaction.atomic() for multi-step writes to preserve integrity.

```python
from django.db import transaction
with transaction.atomic():
    order = Order.objects.create(...)
    # multiple writes here
```

Performance checklist

- Use select_related/prefetch_related to eliminate N+1.
- Add proper indexes for filters and ordering.
- Avoid annotating giant qs; precompute when possible.
- Limit result sets and use keyset/cursor pagination for deep pages.

Interview prompts

- Why are QuerySets lazy? How would you detect premature evaluation?
- Show how select_related vs prefetch_related optimize different relation types.
