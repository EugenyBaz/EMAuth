from django.http import HttpResponse
from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from users.views import RegistrationView, UserViewSet, LogoutView, GroupViewSet


def home(request):
    return HttpResponse("<h1>Добро пожаловать!</h1>")

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)

urlpatterns = [
    path("", home, name='home'),
    path("", include(router.urls)),
    path("register/", RegistrationView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]