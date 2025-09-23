from rest_framework import viewsets
from .models import Fine
from .serializers import FineSerializer

class FineViewSet(viewsets.ModelViewSet):
    queryset = Fine.objects.all()
    serializer_class = FineSerializer