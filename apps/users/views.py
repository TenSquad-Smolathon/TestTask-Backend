from rest_framework import viewsets, permissions
from django.contrib.auth import get_user_model
from .serializers import UserSerializer

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint для просмотра и регистрации пользователей.
    POST /api/users/  -> создать пользователя (регистрация)
    GET /api/users/   -> список пользователей (для админов)
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # Только администратор может видеть список, но любой может зарегистрироваться
    def get_permissions(self):
        if self.action == 'create':  # регистрация
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]