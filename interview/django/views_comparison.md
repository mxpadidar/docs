# APIView vs Generic Views vs ViewSet (DRF) — Examples & When to Use

Overview

- APIView: low-level class-based view; gives full control over request/response logic (explicit methods get/post/put/delete).
- GenericAPIView + Mixins or Concrete generic views (ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView): provide common REST patterns with less boilerplate.
- ViewSet / ModelViewSet: group related actions (list/retrieve/create/update/destroy) in one class and use routers for URL routing.

1. APIView example

```python
# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class ProductListAPI(APIView):
    def get(self, request):
        qs = Product.objects.all()
        serializer = ProductSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
```

Use when custom behavior per method required.

2. Generic views (less boilerplate)

```python
from rest_framework import generics

class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
```

Generics handle get/post automatically.

3. ViewSet / ModelViewSet + Router (recommended for CRUD)

```python
from rest_framework import viewsets
from rest_framework.routers import DefaultRouter

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    pagination_class = StandardResultsSetPagination

# urls.py
router = DefaultRouter()
router.register(r"products", ProductViewSet, basename="product")
urlpatterns = router.urls
```

Advantages:

- Centralized CRUD actions, easy router-based URL generation.
- Easily extend with @action decorators for custom endpoints:

```python
from rest_framework.decorators import action

class ProductViewSet(viewsets.ModelViewSet):
    ...
    @action(detail=True, methods=['post'])
    def mark_featured(self, request, pk=None):
        p = self.get_object()
        p.featured = True
        p.save()
        return Response({"status": "ok"})
```

When to pick which

- APIView: custom complex endpoints, streaming responses, non-CRUD flows.
- Generic views: when you want standard behaviors with little code.
- ViewSet: when building resourceful APIs with RESTful routes and many CRUD endpoints—works well with routers and automatic URL mapping.

Testing patterns

- Use APIClient for view-level tests, assert pagination metadata, filters, and permission behavior.
- For ViewSets, test both action methods and custom actions.

Interview prompts

- Explain how routers map ViewSet actions to URLs.
- Where would you put business logic: view or service layer?
- Show how to add a custom non-CRUD action to a ModelViewSet.

Notes

- Keep views thin: push business logic to services or model managers.
- Use serializers for validation and representation; keep complex query logic in queryset methods or managers.
