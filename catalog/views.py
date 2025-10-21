from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from catalog.permissions import IsAdmin, IsOwnerOrModer, NOTModer, NOTModerOrIsOwner
from catalog.serializers import ProductSerializer

from .models import Product


class ProductViewSet(ModelViewSet):
    """Создаем представление по продуктам CRUD"""

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


# Имитация базы данных с продуктами
MOCK_PRODUCTS = [
    {"id": 1, "name": "Телевизор Toshiba", "owner_id": 3, "price": 100000},
    {"id": 2, "name": "Телевизор TCL", "owner_id": 4, "price": 79900},
    {"id": 3, "name": "Телефон Samsung", "owner_id": 3, "price": 130000},
]


class MockProductListView(APIView):
    """
    Mock-View для демонстрации работы системы прав:
    - 401, если пользователь не залогинен
    - 403, если нет доступа к объекту
    - Иначе возвращает список "доступных" продуктов
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Пользователь не залогинен
        if not request.user or not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED
            )

        user_id = request.user.id
        user_groups = [g.name for g in request.user.groups.all()]

        list_products = []

        for product in MOCK_PRODUCTS:
            # Модератор видит все продукты
            if "moders" in user_groups or "admins" in user_groups:
                list_products.append(product)
            # Владелец видит свои продукты
            elif product["owner_id"] == user_id:
                list_products.append(product)

        return Response(list_products)
