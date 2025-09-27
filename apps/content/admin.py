from django.contrib import admin
from .models import Service, TeamMember, Vacancy, Contact, New, Article, ServiceRequest

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('service', 'status', 'created_at')
admin.site.register(Service)
admin.site.register(TeamMember)
admin.site.register(Vacancy)
admin.site.register(Contact)
admin.site.register(New)
admin.site.register(Article)