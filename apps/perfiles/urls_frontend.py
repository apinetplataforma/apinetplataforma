from django.urls import path
from .views_frontend import (
    PerfilUsuarioListView,
    PerfilUsuarioDetailView,
    PerfilUsuarioCreateView,
    PerfilUsuarioUpdateView,
    PerfilUsuarioDeleteView,
    VehiculoUsuarioListView,
    VehiculoUsuarioDetailView,
    VehiculoUsuarioCreateView,
    VehiculoUsuarioUpdateView,
    VehiculoUsuarioDeleteView,
    MiPerfilView,
    MisVehiculosListView,
)

urlpatterns = [
    # Perfiles
    path("perfiles/", PerfilUsuarioListView.as_view(), name="perfilusuario_list"),
    path(
        "perfiles/<uuid:pk>/",
        PerfilUsuarioDetailView.as_view(),
        name="perfilusuario_detail",
    ),
    path(
        "perfiles/crear/",
        PerfilUsuarioCreateView.as_view(),
        name="perfilusuario_create",
    ),
    path(
        "perfiles/<uuid:pk>/editar/",
        PerfilUsuarioUpdateView.as_view(),
        name="perfilusuario_update",
    ),
    path(
        "perfiles/<uuid:pk>/eliminar/",
        PerfilUsuarioDeleteView.as_view(),
        name="perfilusuario_delete",
    ),
    path("mi-perfil/", MiPerfilView.as_view(), name="mi_perfil"),
    # Vehículos
    path("vehiculos/", VehiculoUsuarioListView.as_view(), name="vehiculousuario_list"),
    path(
        "vehiculos/<uuid:pk>/",
        VehiculoUsuarioDetailView.as_view(),
        name="vehiculousuario_detail",
    ),
    path(
        "vehiculos/crear/",
        VehiculoUsuarioCreateView.as_view(),
        name="vehiculousuario_create",
    ),
    path(
        "vehiculos/<uuid:pk>/editar/",
        VehiculoUsuarioUpdateView.as_view(),
        name="vehiculousuario_update",
    ),
    path(
        "vehiculos/<uuid:pk>/eliminar/",
        VehiculoUsuarioDeleteView.as_view(),
        name="vehiculousuario_delete",
    ),
    path("mis-vehiculos/", MisVehiculosListView.as_view(), name="mis_vehiculos"),
]
