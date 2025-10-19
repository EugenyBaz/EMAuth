from django.http import HttpResponse
from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from catalog.views import ProductViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path("", include(router.urls)),
]