# apps/core/urls.py

from django.urls import path

from .views_frontend import (
    CambiarPasswordView,
    CrearUsuarioView,
    DesactivarCuentaView,
    EditarUsuarioView,
    EliminarUsuarioView,
    ListaUsuariosView,
    ModificarCorreoView,
    RestablecerPasswordView,
    SolicitarRecuperacionView,
    UsuarioCreateView,
    UsuarioLoginView,
    UsuarioLogoutView,
    VerificarCodigoView,
)

urlpatterns = [
    # Registro de usuario
    path("registro/", UsuarioCreateView.as_view(), name="registro_usuario"),
    # Login y Logout
    path("login/", UsuarioLoginView.as_view(), name="login_usuario"),
    path("logout/", UsuarioLogoutView.as_view(), name="logout_usuario"),
    # Cambio de contraseña con sesión iniciada
    path("cambiar-password/", CambiarPasswordView.as_view(), name="cambiar_password"),
    # Recuperación de contraseña - Solicitar código
    path(
        "recuperacion/solicitar/",
        SolicitarRecuperacionView.as_view(),
        name="solicitar_recuperacion",
    ),
    # Recuperación de contraseña - Verificar código
    path(
        "recuperacion/verificar-codigo/",
        VerificarCodigoView.as_view(),
        name="verificar_codigo",
    ),
    # Recuperación de contraseña - Restablecer contraseña
    path(
        "recuperacion/restablecer/",
        RestablecerPasswordView.as_view(),
        name="restablecer_contrasena",
    ),
    # Modificar correo
    path("editar-correo/", ModificarCorreoView.as_view(), name="editar_correo"),
    # Desactivar cuenta
    path(
        "desactivar-cuenta/", DesactivarCuentaView.as_view(), name="desactivar_cuenta"
    ),
    # Ruta para ver la lista de usuarios (solo administradores)
    path("usuarios/", ListaUsuariosView.as_view(), name="lista_usuarios"),
    # Ruta para crear un nuevo usuario (solo administradores)
    path("crear-usuario/", CrearUsuarioView.as_view(), name="crear_usuario"),
    # Ruta para editar un usuario existente (solo administradores)
    path(
        "editar-usuario/<uuid:pk>/", EditarUsuarioView.as_view(), name="editar_usuario"
    ),
    # Ruta para eliminar un usuario (solo administradores)
    path(
        "eliminar-usuario/<uuid:pk>/",
        EliminarUsuarioView.as_view(),
        name="eliminar_usuario",
    ),
]
