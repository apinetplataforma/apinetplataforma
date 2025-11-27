from django.urls import path
from .views_frontend import (
    CajaListView,
    CajaCreateView,
    CajaUpdateView,
    CajaDeleteView,
    CajaDetailView,
    SaldoResetView,
    ExportarCajaExcelView,
)

urlpatterns = [
    # LISTA DE MOVIMIENTOS
    path("", CajaListView.as_view(), name="caja_list"),
    # CREAR MOVIMIENTO
    path("nuevo/", CajaCreateView.as_view(), name="caja_create"),
    # DETALLE DE MOVIMIENTO
    path("<uuid:pk>/detalle/", CajaDetailView.as_view(), name="caja_detail"),
    # ACTUALIZAR MOVIMIENTO
    path("<uuid:pk>/editar/", CajaUpdateView.as_view(), name="caja_update"),
    # ELIMINAR MOVIMIENTO
    path("<uuid:pk>/eliminar/", CajaDeleteView.as_view(), name="caja_delete"),
    path(
        "caja/saldo/<uuid:user_id>/reset/", SaldoResetView.as_view(), name="saldo_reset"
    ),
    path("exportar-caja/", ExportarCajaExcelView.as_view(), name="exportar_caja"),
]
