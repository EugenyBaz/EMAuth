from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework import status
from users.models import User
from users.serializers import UserSerializer, RegisterSerializer


class RegistrationView(CreateAPIView):
    """ Проводим регистрацию пользователя """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    # permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserViewSet(ModelViewSet):
    """ Создание пользователя, редактирование, удаление, просмотр"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def soft_delete(self, request, pk=None):
        user = self.get_object()
        user.is_active = False
        user.save()

        response = Response({})
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

class LogoutView(APIView):
    def post(self, request):
        return Response({"message": "Вы вышли из аккаунта"}, status=status.HTTP_200_OK)
