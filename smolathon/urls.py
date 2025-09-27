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
from django.http import JsonResponse
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from apps.content.views import TablesInfoView
from apps.trafficlights.views import TrafficLightViewSet
from apps.fines.views import FineViewSet
from apps.evacuations.views import EvacuationViewSet
from apps.analytics.views import MetricViewSet
from apps.projects.views import ProjectViewSet
from apps.notifications.views import NotificationViewSet
from apps.accidents.views import AccidentViewSet
from apps.analytics.views import StatsViewSet


# домашняя страница
def home(request):
    return JsonResponse({"message": "Welcome to TestTask-Backend!"})


# основной router для всего API
router = routers.DefaultRouter()
router.register(r'traffic-lights', TrafficLightViewSet, basename='trafficlight')
router.register(r'fines', FineViewSet, basename='fine')
router.register(r'evacuations', EvacuationViewSet, basename='evacuation')
router.register(r'metrics', MetricViewSet, basename='metric')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'accidents', AccidentViewSet, basename='accident')

# подключение всех URL
urlpatterns = [
    path('', home),  # корень сайта
    path('admin/', admin.site.urls),
    path('tables/', TablesInfoView.as_view(), name='tables-info'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/analytics/stats', StatsViewSet.as_view(), name='stats'),
    path('api/content/', include('apps.content.urls')),
    path('api/users/', include('apps.users.urls')),
    # path('api/analytics/', include('apps.analytics.urls')),
    path('api/', include(router.urls)),  # все зарегистрированные ViewSet’ы
]