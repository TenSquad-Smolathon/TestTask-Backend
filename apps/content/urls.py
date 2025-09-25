from rest_framework.routers import DefaultRouter
from .views import ServiceViewSet, TeamMemberViewSet, VacancyViewSet, ContactViewSet

router = DefaultRouter()
router.register(r'services', ServiceViewSet)
router.register(r'team', TeamMemberViewSet)
router.register(r'vacancies', VacancyViewSet)
router.register(r'contacts', ContactViewSet)

urlpatterns = router.urls