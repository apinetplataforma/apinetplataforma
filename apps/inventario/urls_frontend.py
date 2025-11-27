from django.urls import path

from .views_frontend import (
    CategoriaCreateView,
    CategoriaDeleteView,
    CategoriaListView,
    CategoriaUpdateView,
    ProductoCreateView,
    ProductoDeleteView,
    ProductoListView,
    ProductoUpdateView,
    ProveedorCreateView,
    ProveedorDeleteView,
    ProveedorListView,
    ProveedorUpdateView,
    StockListView,
    MoverProductoBodegaView,
    MiStockListView,
    RestarProductoView,
    StockUsuariosAdministradorView,
    ExportarStockExcelView,
    HistorialRestasAdministradorView,
    EliminarRestaView,
    EliminarRestaTecnicoView,
)

urlpatterns = [
    # ============================
    # PROVEEDORES
    # ============================
    path("proveedores/", ProveedorListView.as_view(), name="proveedor_list"),
    path("proveedores/nuevo/", ProveedorCreateView.as_view(), name="proveedor_create"),
    path(
        "proveedores/<uuid:pk>/editar/",
        ProveedorUpdateView.as_view(),
        name="proveedor_update",
    ),
    path(
        "proveedores/<uuid:pk>/eliminar/",
        ProveedorDeleteView.as_view(),
        name="proveedor_delete",
    ),
    # ============================
    # CATEGORÍAS
    # ============================
    path("categorias/", CategoriaListView.as_view(), name="categoria_list"),
    path("categorias/crear/", CategoriaCreateView.as_view(), name="categoria_create"),
    path(
        "categorias/<uuid:pk>/editar/",
        CategoriaUpdateView.as_view(),
        name="categoria_update",
    ),
    path(
        "categorias/<uuid:pk>/eliminar/",
        CategoriaDeleteView.as_view(),
        name="categoria_delete",
    ),
    # ============================
    # PRODUCTOS
    # ============================
    path("productos/", ProductoListView.as_view(), name="producto_list"),
    path("productos/crear/", ProductoCreateView.as_view(), name="producto_create"),
    path(
        "productos/<uuid:pk>/editar/",
        ProductoUpdateView.as_view(),
        name="producto_update",
    ),
    path(
        "productos/<uuid:pk>/eliminar/",
        ProductoDeleteView.as_view(),
        name="producto_delete",
    ),
    # ============================
    # STOCK
    # ============================
    path("stock/", StockListView.as_view(), name="stock_list"),
    path(
        "stock/agregar/",
        MoverProductoBodegaView.as_view(),
        name="agregar_producto_bodega",
    ),
    path("mi-stock/", MiStockListView.as_view(), name="mi_stock"),
    path("restar-producto/", RestarProductoView.as_view(), name="restar_producto"),
    path(
        "admin/stock-usuarios/",
        StockUsuariosAdministradorView.as_view(),
        name="stock_usuarios_admin",
    ),
    path(
        "exportar-stock/", ExportarStockExcelView.as_view(), name="exportar_stock"
    ),  # boton exportar a excel movimientos
    # ============================
    # ADMIN – HISTORIAL RESTAS
    # ============================
    path(
        "admin/restas/",
        HistorialRestasAdministradorView.as_view(),
        name="historial_restas_admin",
    ),
    path(
        "admin/restas/<uuid:pk>/eliminar/",
        EliminarRestaView.as_view(),
        name="eliminar_resta",
    ),
    path(
        "admin/restas/<uuid:pk>/eliminar-resta/",
        EliminarRestaTecnicoView.as_view(),
        name="eliminar_resta_tecnico",
    ),
]
