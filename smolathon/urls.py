"""
URL configuration for smolathon project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.trafficlights.views import TrafficLightViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.http import JsonResponse
from rest_framework import routers
from apps.fines.views import FineViewSet
from apps.evacuations.views import EvacuationViewSet
from apps.analytics.views import MetricViewSet
from apps.projects.views import ProjectViewSet
from apps.accidents.views import AccidentViewSet
from apps.notifications.views import NotificationViewSet

router = DefaultRouter()
router.register(r'traffic-lights', TrafficLightViewSet, basename='trafficlight')
router.register(r'fines', FineViewSet, basename='fine')
router.register(r'evacuations', EvacuationViewSet, basename='evacuation')
router.register(r'metrics', MetricViewSet, basename='metric')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'accidents', AccidentViewSet, basename='accident')
# Если нужно, сюда же можно добавить services, team, vacancies, contacts

def home(request):
    return JsonResponse({"message": "Welcome to TestTask-Backend!"})

router = DefaultRouter()
router.register(r'traffic-lights', TrafficLightViewSet, basename='trafficlight')

urlpatterns = [
    path('', home),  # корень сайта
    path('admin/', admin.site.urls),

    # JWT токены
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Подключаем свои внутренние url’ы, если они есть
    path('api/content/', include('apps.content.urls')),  # если сделал отдельный urls.py
    path('api/users/', include('apps.users.urls')),      # если сделал отдельный urls.py

    # Всё, что зарегистрировано в роутере DRF
    path('api/', include(router.urls)),
    # path('api/content/', include('apps.content.urls')),
    # path('api/users/', include('apps.users.urls')),
    # path('api/traffic-lights/', include('apps.trafficlights.urls')),
    # path('api/', include('apps.accidents.urls')),
]
