from rest_framework import viewsets, permissions
from .models import TrafficLight
from .serializers import TrafficLightSerializer

class TrafficLightViewSet(viewsets.ModelViewSet):
    queryset = TrafficLight.objects.all()
    serializer_class = TrafficLightSerializer

    # гости видят только публичные
    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_anonymous:
            return qs.filter(is_public=True)
        return qs

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]