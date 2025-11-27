from datetime import timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.views.generic.edit import FormView

from apps.notificaciones.models import EstadoNotificacion, Notificaciones
from apps.usuario.forms import (
    ConfirmarDesactivacionForm,
    ConfirmarEliminacionForm,
    CustomLoginForm,
    CustomPasswordChangeForm,
    RestablecerPasswordForm,
    SolicitarRecuperacionForm,
    UsuarioEditForm,
    UsuarioForm,
    VerificarCodigoForm,
)
from apps.usuario.models import Usuario

from .models import CodigoRecuperacion
from django.core.mail import send_mail


# ------------------------------------------------------------
# CREACION DE USUARIOS
# ------------------------------------------------------------
class UsuarioCreateView(CreateView):
    form_class = UsuarioForm
    template_name = "usuario/ingreso/crear_usuario.html"
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form):
        usuario = form.save()

        Notificaciones.objects.create(
            usuario=usuario,
            estado=EstadoNotificacion.EXITO,
            titulo="Cuenta creada",
            mensaje="Tu cuenta fue creada exitosamente.",
        )

        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


# ------------------------------------------------------------
# LOGIN DE USUARIOS
# ------------------------------------------------------------
class UsuarioLoginView(LoginView):
    template_name = "usuario/ingreso/login.html"
    form_class = CustomLoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("dashboard")

    def form_invalid(self, form):
        return super().form_invalid(form)


# ------------------------------------------------------------
# LOGOUT DE USUARIOS
# ------------------------------------------------------------
class UsuarioLogoutView(LogoutView):
    next_page = reverse_lazy("base")

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


# ------------------------------------------------------------
# CAMBIO DE CONTRASEÑA CON SESION INICIADA
# ------------------------------------------------------------
class CambiarPasswordView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = "usuario/insesion/cambiar_password.html"
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form):
        usuario = self.request.user

        Notificaciones.objects.create(
            usuario=usuario,
            estado=EstadoNotificacion.EXITO,
            titulo="Contraseña cambiada",
            mensaje="Has cambiado tu contraseña exitosamente.",
        )

        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class SolicitarRecuperacionView(FormView):
    template_name = "usuario/recuperacion/solicitar_recuperacion.html"
    form_class = SolicitarRecuperacionForm
    success_url = reverse_lazy("verificar_codigo")

    def form_valid(self, form):
        email = form.cleaned_data["email"]

        try:
            usuario = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            messages.error(self.request, "No existe una cuenta asociada a ese correo.")
            return redirect("solicitar_recuperacion")

        codigo_obj, _ = CodigoRecuperacion.objects.get_or_create(usuario=usuario)
        codigo_obj.generar_codigo()

        # envio de correo
        subject = "Código de recuperación de contraseña"
        message = (
            f"Hola {usuario.email},\n\n"
            f"Tu código de recuperación es: {codigo_obj.codigo}\n\n"
            "Si no solicitaste este cambio, ignora este mensaje."
        )
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [usuario.email]

        try:
            send_mail(subject, message, from_email, recipient_list)

            messages.success(
                self.request, "Se ha enviado un código de verificación a tu correo."
            )
            print(f"correo enviado con exito a {usuario.email}")
        except Exception as e:
            print(f"Error enviando correo: {e}")

        self.request.session["usuario_recuperacion"] = usuario.email
        return super().form_valid(form)


class VerificarCodigoView(FormView):
    template_name = "usuario/recuperacion/verificar_codigo.html"
    form_class = VerificarCodigoForm
    success_url = reverse_lazy("restablecer_contrasena")

    def dispatch(self, request, *args, **kwargs):
        if "usuario_recuperacion" not in request.session:
            messages.error(
                request, "Primero solicita el restablecimiento de contraseña."
            )
            return redirect("solicitar_recuperacion")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        email = self.request.session.get("usuario_recuperacion")
        usuario = get_object_or_404(Usuario, email=email)
        codigo_ingresado = form.cleaned_data["codigo"].strip()

        try:
            codigo_obj = CodigoRecuperacion.objects.filter(
                usuario=usuario, usado=False
            ).latest("fecha_creacion")
        except CodigoRecuperacion.DoesNotExist:
            form.add_error(None, "Código no válido o ya usado.")
            return self.form_invalid(form)

        if codigo_obj.codigo == codigo_ingresado:
            codigo_obj.usado = True
            codigo_obj.save(update_fields=["usado"])
            self.request.session["codigo_verificado"] = True
            messages.success(self.request, "Código verificado correctamente.")
            return super().form_valid(form)
        else:
            form.add_error("codigo", "El código ingresado es incorrecto.")
            return self.form_invalid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class RestablecerPasswordView(FormView):
    template_name = "usuario/recuperacion/restablecer_contrasena.html"
    form_class = RestablecerPasswordForm
    success_url = reverse_lazy("login_usuario")

    def dispatch(self, request, *args, **kwargs):
        if "usuario_recuperacion" not in request.session or not request.session.get(
            "codigo_verificado"
        ):
            messages.error(request, "Debes verificar tu código antes de continuar.")
            return redirect("solicitar_recuperacion")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        email = self.request.session.get("usuario_recuperacion")
        usuario = get_object_or_404(Usuario, email=email)
        nueva_contrasena = form.cleaned_data["nueva_contrasena"]
        usuario.set_password(nueva_contrasena)
        usuario.save()

        self.request.session.pop("usuario_recuperacion", None)
        self.request.session.pop("codigo_verificado", None)

        messages.success(self.request, "Has restablecido tu contraseña exitosamente.")
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


# ------------------------------------------------------------
# MODIFICAR CORREO DEL USUARIO
# ------------------------------------------------------------
class ModificarCorreoView(FormView):
    template_name = "usuario/insesion/editar_correo.html"
    form_class = UsuarioEditForm
    success_url = reverse_lazy("perfil_usuario")

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        usuario = form.save(commit=False)
        usuario.save()

        Notificaciones.objects.create(
            usuario=usuario,
            estado=EstadoNotificacion.EXITO,
            titulo="Correo actualizado",
            mensaje="Has actualizado tu correo exitosamente.",
        )

        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


# ------------------------------------------------------------
# DESACTIVAR CUENTA DEL USUARIO
# ------------------------------------------------------------
class DesactivarCuentaView(FormView):
    template_name = "usuario/insesion/desactivar_cuenta.html"
    form_class = ConfirmarDesactivacionForm
    success_url = reverse_lazy("base")

    def form_valid(self, form):
        usuario = self.request.user
        usuario.is_active = False
        usuario.save()

        Notificaciones.objects.create(
            usuario=usuario,
            estado=EstadoNotificacion.ADVERTENCIA,
            titulo="Cuenta desactivada",
            mensaje="Tu cuenta ha sido desactivada. Solo el administrador podrá activarla nuevamente.",
        )

        return redirect(self.success_url)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Debes confirmar la desactivación de tu cuenta para continuar.",
        )
        return super().form_invalid(form)


# ========================================================================================================
# ADMINISTRADOR
# ========================================================================================================


# ========================================================================================================
# lista usuarios
# ========================================================================================================
class ListaUsuariosView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Usuario
    template_name = "usuario/admin/lista.html"
    context_object_name = "usuarios"

    def test_func(self):
        can_access = self.request.user.is_staff
        return can_access

    def handle_no_permission(self):
        return redirect("dashboard")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_usuarios"] = Usuario.objects.count()
        context["total_administradores"] = Usuario.objects.filter(is_staff=True).count()
        context["total_superusuarios"] = Usuario.objects.filter(
            is_superuser=True
        ).count()
        context["total_activos"] = Usuario.objects.filter(is_active=True).count()
        return context


# ========================================================================================================
# crea usuarios
# ========================================================================================================
class CrearUsuarioView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = UsuarioForm
    template_name = "usuario/admin/crear_usuario.html"
    success_url = reverse_lazy("lista_usuarios")

    def test_func(self):
        can_access = self.request.user.is_staff
        return can_access

    def handle_no_permission(self):
        return redirect("dashboard")

    def form_valid(self, form):
        usuario = form.save()

        Notificaciones.objects.create(
            usuario=usuario,
            estado=EstadoNotificacion.EXITO,
            titulo="Cuenta creada",
            mensaje="Tu cuenta fue creada exitosamente por un administrador.",
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


# ========================================================================================================
# edita usuarios
# ========================================================================================================
class EditarUsuarioView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Usuario
    form_class = UsuarioEditForm
    template_name = "usuario/admin/editar_usuario.html"
    success_url = reverse_lazy("lista_usuarios")

    def test_func(self):
        can_access = self.request.user.is_staff
        return can_access

    def handle_no_permission(self):
        return redirect("dashboard")

    def form_valid(self, form):
        usuario = form.save()

        Notificaciones.objects.create(
            usuario=usuario,
            estado=EstadoNotificacion.EXITO,
            titulo="Usuario actualizado",
            mensaje="Tu perfil ha sido actualizado exitosamente por un administrador.",
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


# ========================================================================================================
# eliminar usuarios
# ========================================================================================================
class EliminarUsuarioView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Usuario
    template_name = "usuario/admin/eliminar_usuario.html"
    success_url = reverse_lazy("lista_usuarios")

    def test_func(self):
        can_access = self.request.user.is_staff
        return can_access

    def handle_no_permission(self):
        return redirect("dashboard")

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ConfirmarEliminacionForm()
        return self.render_to_response({"form": form, "usuario": self.object})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ConfirmarEliminacionForm(request.POST)
        if form.is_valid() and form.cleaned_data["confirmacion"]:
            self.object.delete()

            Notificaciones.objects.create(
                usuario=request.user,
                estado=EstadoNotificacion.EXITO,
                titulo="Usuario eliminado",
                mensaje=f"Has eliminado al usuario {self.object.email} correctamente.",
            )

            return redirect(self.success_url)
        messages.error(request, "Debes confirmar la eliminación del usuario.")
        return self.render_to_response({"form": form, "usuario": self.object})
