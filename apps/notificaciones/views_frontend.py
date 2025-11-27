from django.contrib.auth.mixins import LoginRequiredMixin
from django_filters.views import FilterView

from .filters import NotificacionFilter
from .models import Notificaciones


class NotificacionesListView(LoginRequiredMixin, FilterView):
    model = Notificaciones
    template_name = "notificaciones/historial.html"
    context_object_name = "notificaciones"
    filterset_class = NotificacionFilter
    paginate_by = 10

    def get_queryset(self):
        # Solo las notificaciones del usuario logueado
        qs = Notificaciones.objects.filter(usuario=self.request.user).order_by(
            "-created"
        )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario = self.request.user
        all_notifs = Notificaciones.objects.filter(usuario=usuario)
        context["total_notificaciones"] = all_notifs.count()
        context["notificaciones_leidas"] = all_notifs.filter(leida=True).count()
        context["notificaciones_no_leidas"] = all_notifs.filter(leida=False).count()
        return context
