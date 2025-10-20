from django.urls import path, include
from rest_framework.routers import DefaultRouter
from catalog.views import ProductViewSet, MockProductListView

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path("", include(router.urls)),
    path("mock-products/", MockProductListView.as_view(), name="mock-products"),
]