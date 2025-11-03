from django.urls import include, path
from rest_framework.routers import DefaultRouter

from catalog.views import MockProductListView, ProductViewSet

router = DefaultRouter()
router.register(r"products", ProductViewSet, basename="product")

urlpatterns = [
    path("", include(router.urls)),
    path("mock-products/", MockProductListView.as_view(), name="mock-products"),
]
