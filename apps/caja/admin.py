from django.contrib import admin
from .models import Caja, SaldoCaja, MovimientoCaja, MotivoMovimientoCaja


# =============================================================================
# ADMIN DE SALDO DE CAJA
# =============================================================================


@admin.register(SaldoCaja)
class SaldoCajaAdmin(admin.ModelAdmin):
    list_display = ("usuario", "saldo", "created", "modified")
    search_fields = ("usuario__username", "usuario__first_name", "usuario__last_name")
    readonly_fields = ("usuario", "saldo", "created", "modified")

    fieldsets = (
        ("Información del usuario", {"fields": ("usuario",)}),
        ("Saldo de Caja", {"fields": ("saldo",)}),
        ("Tiempos", {"fields": ("created", "modified")}),
    )

    def has_add_permission(self, request):
        # El saldo se crea automáticamente al hacer un movimiento
        return False

    def has_delete_permission(self, request, obj=None):
        # No permitir eliminar saldos
        return False


# =============================================================================
# ADMIN DE MOVIMIENTOS DE CAJA
# =============================================================================


@admin.register(Caja)
class CajaAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "usuario",
        "tipo_movimiento",
        "cantidad_movida",
        "motivo_movimiento",
        "created",
    )

    list_filter = (
        "tipo_movimiento",
        "motivo_movimiento",
        "usuario",
        "created",
    )

    search_fields = (
        "usuario__username",
        "usuario__first_name",
        "usuario__last_name",
        "motivo_movimiento",
    )

    readonly_fields = ("created", "modified")

    fieldsets = (
        (
            "Información del Movimiento",
            {
                "fields": (
                    "usuario",
                    "tipo_movimiento",
                    "cantidad_movida",
                    "motivo_movimiento",
                    "info_adicional",
                )
            },
        ),
        ("Tiempos", {"fields": ("created", "modified")}),
    )

    def has_change_permission(self, request, obj=None):
        """
        🚫 IMPORTANTE:
        Para mantener la integridad contable, NO se debe permitir editar movimientos.
        SOLO crear y eliminar.
        """
        return False  # Desactivar edición
