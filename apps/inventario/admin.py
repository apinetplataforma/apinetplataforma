from django.contrib import admin

from .models import Categoria, Producto, Proveedor, Stock, StockActual


# ============================================================
# PROVEEDOR
# ============================================================
@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ("nombre", "usuario", "telefono", "email")
    search_fields = ("nombre", "usuario__username", "email")
    list_filter = ("usuario",)


# ============================================================
# CATEGORIA
# ============================================================
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "usuario", "created")
    search_fields = ("nombre", "usuario__username")
    list_filter = ("usuario",)
    ordering = ("-created",)


# ============================================================
# PRODUCTO
# ============================================================
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "usuario",
        "proveedor",
        "categoria",
        "precio_compra",
        "precio_venta",
        "medida",
    )
    search_fields = (
        "nombre",
        "usuario__username",
        "proveedor__nombre",
        "categoria__nombre",
    )
    list_filter = ("usuario", "proveedor", "categoria", "medida")


# ============================================================
# STOCK
# ============================================================
@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = (
        "producto",
        "usuario",
        "usuario_origen",
        "usuario_destino",
        "cantidad_movida",
        "movimiento",
        "motivo",
        "created",
    )
    list_filter = ("movimiento", "motivo", "producto")
    search_fields = (
        "producto__nombre",
        "usuario__username",
        "usuario_origen__username",
        "usuario_destino__username",
    )

    # ❌ QUITAMOS readonly_fields porque contenía 'stock_producto' (que NO existe)
    readonly_fields = ("created", "modified")

    # ❌ También quitamos 'stock_producto' de fieldsets
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "producto",
                    "usuario",
                    "usuario_origen",
                    "usuario_destino",
                    "cantidad_movida",
                    "movimiento",
                    "motivo",
                    "check_motivo_personalizado",
                    "motivo_personalizado",
                    "codigo_ticket",
                )
            },
        ),
        (
            "Fechas",
            {
                "fields": ("created", "modified"),
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        if not obj.usuario_id:
            obj.usuario = request.user
        super().save_model(request, obj, form, change)


# ============================================================
# STOCK ACTUAL
# ============================================================
@admin.register(StockActual)
class StockActualAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "producto", "cantidad")
    list_filter = ("usuario", "producto")
    search_fields = ("usuario__email", "producto__nombre")
