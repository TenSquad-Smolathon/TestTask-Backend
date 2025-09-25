from rest_framework import routers
from django.urls import path, include
from .views import ServiceViewSet, TeamMemberViewSet

# Создаём роутер
router = routers.DefaultRouter()

# Регистрируем ViewSet'ы с уникальными basename
router.register(r'services', ServiceViewSet, basename='service')        # URL: /services/
router.register(r'team-members', TeamMemberViewSet, basename='teammember')  # URL: /team-members/

# Если будут ещё ViewSet'ы, регистрируйте их аналогично:
# router.register(r/путь/, ViewSetКласс, basename='уникальное_имя')

# Подключаем роутер к URLconf
urlpatterns = [
    path('', include(router.urls)),
]