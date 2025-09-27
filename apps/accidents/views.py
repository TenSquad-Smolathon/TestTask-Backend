from rest_framework import viewsets
from .models import Accident
from .serializers import AccidentSerializer

class AccidentViewSet(viewsets.ModelViewSet):
    """
    CRUD для аварий.
    Можно POST'ом прислать lat/long/description, чтобы создать точку на карте.
    """
    queryset = Accident.objects.all().order_by('-reported_at')
    serializer_class = AccidentSerializer