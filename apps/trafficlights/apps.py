from django.apps import AppConfig

class TrafficlightsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.trafficlights'   # <- очень важно, именно путь к пакету приложения