from django.contrib import admin
from .models import Service, TeamMember, Vacancy, Contact

admin.site.register(Service)
admin.site.register(TeamMember)
admin.site.register(Vacancy)
admin.site.register(Contact)