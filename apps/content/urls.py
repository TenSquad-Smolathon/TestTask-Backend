from rest_framework.routers import DefaultRouter
from .views import ServiceViewSet, TeamMemberViewSet, VacancyViewSet, ContactViewSet, NewsViewSet, ArticlesViewSet, DocumentsViewSet
from rest_framework.routers import DefaultRouter
from .views import ServiceRequestViewSet


router = DefaultRouter()
router.register(r'service-requests', ServiceRequestViewSet, basename='service-request')
router.register(r'services', ServiceViewSet)
router.register(r'team', TeamMemberViewSet)
router.register(r'vacancies', VacancyViewSet)
router.register(r'contacts', ContactViewSet)
router.register(r'news', NewsViewSet)
router.register(r'articles', ArticlesViewSet)
router.register(r'documents', DocumentsViewSet)

urlpatterns = router.urls