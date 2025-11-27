from django.urls import path

from .views_frontend import NotificacionesListView

urlpatterns = [
    path(
        "historial/", NotificacionesListView.as_view(), name="notificaciones_historial"
    ),
]
