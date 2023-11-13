from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet
from django.conf import settings

router = DefaultRouter()
router.register('project', ProjectViewSet)


urlpatterns = [
    path('', include(router.urls))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += router.urls
