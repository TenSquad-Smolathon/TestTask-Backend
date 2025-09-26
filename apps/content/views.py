from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import Service, TeamMember, Vacancy, Contact
from .serializers import (
    ServiceSerializer,
    TeamMemberSerializer,
    VacancySerializer,
    ContactSerializer
)
from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class TeamMemberViewSet(viewsets.ModelViewSet):
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer

class VacancyViewSet(viewsets.ModelViewSet):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
    permission_classes = [AllowAny]

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class TablesInfoView(APIView):
    def get(self, request):
        data = {}
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cursor.fetchall()]
            for table in tables:
                cursor.execute(f"PRAGMA table_info({table})")
                columns = [col[1] for col in cursor.fetchall()]
                data[table] = columns
        return Response(data)