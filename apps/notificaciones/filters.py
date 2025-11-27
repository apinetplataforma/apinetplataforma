import django_filters
from django.db import models
from django.forms import widgets

from .models import EstadoNotificacion, Notificaciones


class NotificacionFilter(django_filters.FilterSet):

    estado = django_filters.ChoiceFilter(
        choices=EstadoNotificacion.choices,
        empty_label="Seleccione estado",
        widget=widgets.Select(
            attrs={
                "class": "form-select form-select",
                "aria-label": "Estado",
            }
        ),
        label="",
    )

    buscar = django_filters.CharFilter(
        method="filtrar_busqueda",
        widget=widgets.TextInput(
            attrs={
                "class": "form-control form-control",
                "placeholder": "Buscar título o mensaje",
                "aria-label": "Buscar",
            }
        ),
        label="",
    )

    class Meta:
        model = Notificaciones
        fields = ["estado"]

    def filtrar_busqueda(self, queryset, name, value):
        return queryset.filter(
            models.Q(titulo__icontains=value) | models.Q(mensaje__icontains=value)
        )
