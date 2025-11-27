import django_filters
from .models import Caja
from django import forms


class CajaFilter(django_filters.FilterSet):
    tipo_movimiento = django_filters.ChoiceFilter(
        choices=Caja._meta.get_field("tipo_movimiento").choices,
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Tipo de Movimiento",
    )

    fecha_inicio = django_filters.DateFilter(
        field_name="created",
        lookup_expr="date__gte",
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        label="Fecha desde",
    )
    fecha_fin = django_filters.DateFilter(
        field_name="created",
        lookup_expr="date__lte",
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        label="Fecha hasta",
    )

    class Meta:
        model = Caja
        fields = ["tipo_movimiento", "fecha_inicio", "fecha_fin"]
