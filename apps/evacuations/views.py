from rest_framework import viewsets
from .models import Evacuation
from .serializers import EvacuationSerializer

class EvacuationViewSet(viewsets.ModelViewSet):
    queryset = Evacuation.objects.all()
    serializer_class = EvacuationSerializer