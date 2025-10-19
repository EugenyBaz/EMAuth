from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Product
from catalog.serializers import ProductSerializer
from catalog.permissions import IsOwnerOrModer, NOTModer, NOTModerOrIsOwner, IsAdmin

class ProductViewSet(ModelViewSet):
    """ Создаем представление по продуктам CRUD"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):

        if self.request.user.is_superuser:
            return [IsAdmin()]

        if self.action == "create":
            permission_classes = [IsAuthenticated, NOTModer]
        elif self.action in ["update", "partial_update", "retrieve"]:
            permission_classes = [IsAuthenticated, IsOwnerOrModer]
        elif self.action == "destroy":
            permission_classes = [IsAuthenticated, NOTModerOrIsOwner]
        else:
            permission_classes = [IsAuthenticated]
        return [perm() for perm in permission_classes]

    def list(self, request, *args, **kwargs):
        print("AUTH HEADER:", request.META.get("HTTP_AUTHORIZATION"))
        return super().list(request, *args, **kwargs)