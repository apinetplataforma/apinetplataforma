from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from .views import BaseView, DashboardView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", BaseView.as_view(), name="base"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("usuario/", include("apps.usuario.urls_frontend")),
    path("notificaciones/", include("apps.notificaciones.urls_frontend")),
    path("inventario/", include("apps.inventario.urls_frontend")),
    path("perfiles/", include("apps.perfiles.urls_frontend")),
    path("caja/", include("apps.caja.urls_frontend")),
    # api notificaciones
    path("api/", include("apps.notificaciones.urls_api")),
]


if settings.DEBUG:
    # Sirve archivos estáticos y de medios en desarrollo
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0]
    )
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)