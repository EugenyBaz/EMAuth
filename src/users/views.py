from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import logout

from catalog.permissions import IsAdmin
from users.models import User
from users.serializers import GroupSerializer, RegisterSerializer, UserSerializer
from users.utils import generate_custom_jwt


class RegistrationView(CreateAPIView):
    """Проводим регистрацию пользователя"""

    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer) -> None :
        """Сохраняем пользователя с кастомным хешем пароля"""
        user = serializer.save(is_active=True)
        user.set_custom_password(serializer.validated_data["password"])
        user.save()


class UserViewSet(ModelViewSet):
    """Создание пользователя, редактирование, удаление, просмотр"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["post"])
    def soft_delete(self, request, pk=None) -> Response:
        """ 'Мягкое' удаление """
        user = self.get_object()
        user.is_active = False
        user.save()

        response = Response({})
        response.status_code = status.HTTP_204_NO_CONTENT
        return response


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request) -> Response:
        """Выход из аккаунта"""

        logout(request)  # очищает сессию
        response = Response({"message": "Вы вышли из аккаунта"}, status=200)
        response.delete_cookie('jwt')  # если токен в куки
        return response


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request)  -> Response :
        """Проверка email и пароля, генерация JWT"""
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.check_custom_password(password):
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        token = generate_custom_jwt(user)
        return Response(token, status=status.HTTP_200_OK)


class GroupViewSet(ModelViewSet):
    """Управление ролями и пользователями - для администратора"""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAdmin]

    @action(detail=True, methods=["post"])
    def add_user(self, request, pk=None)-> Response:
        """ Добавление пользователя в группу"""
        group = self.get_object()
        user_id = request.data.get("user_id")
        user = User.objects.get(id=user_id)
        group.user_set.add(user)
        return Response({"detail": f"Пользователь {user.email} добавлен в {group.name}"})
