import django_filters
from django import forms
from .models import Stock, Producto, StockActual
from apps.usuario.models import Usuario


class StockFilter(django_filters.FilterSet):

    # -----------------------------
    # NUEVOS FILTROS
    # -----------------------------
    usuario_origen = django_filters.ModelChoiceFilter(
        queryset=Usuario.objects.all(),
        label="",
        empty_label="Usuario Origen",
        field_name="usuario_origen",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    usuario_destino = django_filters.ModelChoiceFilter(
        queryset=Usuario.objects.all(),
        label="",
        empty_label="Usuario Destino",
        field_name="usuario_destino",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    # -----------------------------
    # FILTROS EXISTENTES
    # -----------------------------
    usuario = django_filters.ModelChoiceFilter(
        queryset=Usuario.objects.all(),
        label="",
        empty_label="Usuario (quien realiza la acción)",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    producto = django_filters.ModelChoiceFilter(
        queryset=Producto.objects.all(),
        label="",
        empty_label="Producto",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    fecha_inicio = django_filters.DateFilter(
        field_name="created",
        lookup_expr="gte",
        label="Desde",
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
    )

    fecha_fin = django_filters.DateFilter(
        field_name="created",
        lookup_expr="lte",
        label="Hasta",
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
    )

    class Meta:
        model = Stock
        fields = [
            "usuario",
            "producto",
            "usuario_origen",
            "usuario_destino",
        ]
        labels = {
            "usuario": "",
            "producto": "",
            "usuario_origen": "",
            "usuario_destino": "",
            "fecha_inicio": "",
            "fecha_fin": "",
        }


class StockActualAdminFilter(django_filters.FilterSet):

    usuario = django_filters.ModelChoiceFilter(
        queryset=Usuario.objects.all(),
        label="",
        empty_label="Usuario",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    producto = django_filters.ModelChoiceFilter(
        queryset=Producto.objects.all(),
        label="",
        empty_label="Producto",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = StockActual
        fields = ["usuario", "producto"]
        labels = {
            "usuario": "",
            "producto": "",
        }
