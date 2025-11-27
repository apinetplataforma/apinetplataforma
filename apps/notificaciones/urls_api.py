from rest_framework.routers import DefaultRouter

from .views_api import NotificacionViewSet

router = DefaultRouter()
router.register(r"notificaciones", NotificacionViewSet, basename="notificacion")

urlpatterns = router.urls
