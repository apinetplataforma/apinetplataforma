from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404

from .models import PerfilUsuario, VehiculoUsuario
from .forms import PerfilUsuarioForm, VehiculoUsuarioForm
from apps.notificaciones.models import Notificaciones, EstadoNotificacion

# ============================================================
# PERFIL USUARIO - CRUD
# ============================================================


class PerfilUsuarioListView(LoginRequiredMixin, ListView):
    model = PerfilUsuario
    template_name = "perfiles/perfilusuario_list.html"
    context_object_name = "perfiles"
    paginate_by = 10

    def get_queryset(self):
        return PerfilUsuario.objects.all().order_by("-created")


class PerfilUsuarioDetailView(LoginRequiredMixin, DetailView):
    model = PerfilUsuario
    template_name = "perfiles/perfilusuario_detail.html"
    context_object_name = "perfil"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        perfil = self.get_object()

        context["fotos_perfil"] = [
            (perfil.foto_perfil, "Foto de Perfil"),
            (perfil.foto_cedula_adelante, "Foto Cédula Adelante"),
            (perfil.foto_cedula_atras, "Foto Cédula Atrás"),
            (perfil.foto_casa, "Foto Casa"),
            (perfil.foto_curso_altura, "Foto Curso Altura"),
            (perfil.foto_diploma_grado, "Foto Diploma Grado"),
        ]

        return context


class PerfilUsuarioCreateView(LoginRequiredMixin, CreateView):
    model = PerfilUsuario
    form_class = PerfilUsuarioForm
    template_name = "perfiles/perfilusuario_create.html"
    success_url = reverse_lazy("perfilusuario_list")

    def form_valid(self, form):
        response = super().form_valid(form)

        Notificaciones.objects.create(
            usuario=self.object.usuario,
            estado=EstadoNotificacion.EXITO,
            titulo="Perfil creado",
            mensaje=f"Un administrador creó tu perfil.",
        )

        return response


class PerfilUsuarioUpdateView(LoginRequiredMixin, UpdateView):
    model = PerfilUsuario
    form_class = PerfilUsuarioForm
    template_name = "perfiles/perfilusuario_update.html"
    success_url = reverse_lazy("perfilusuario_list")

    def form_valid(self, form):
        response = super().form_valid(form)

        Notificaciones.objects.create(
            usuario=self.object.usuario,
            estado=EstadoNotificacion.ADVERTENCIA,
            titulo="Perfil creado",
            mensaje=f"Un administrador modificó tu perfil.",
        )

        return response


class PerfilUsuarioDeleteView(LoginRequiredMixin, DeleteView):
    model = PerfilUsuario
    template_name = "perfiles/perfilusuario_confirm_delete.html"
    success_url = reverse_lazy("perfilusuario_list")

    def form_valid(self, form):
        response = super().form_valid(form)

        Notificaciones.objects.create(
            usuario=self.object.usuario,
            estado=EstadoNotificacion.ADVERTENCIA,
            titulo="Perfil creado",
            mensaje=f"Un administrador Eliminó tu perfil.",
        )

        return response


# ============================================================
# MI PERFIL (Ver/crear automáticamente)
# ============================================================


class MiPerfilView(LoginRequiredMixin, DetailView):
    model = PerfilUsuario
    template_name = "perfiles/mi_perfil.html"
    context_object_name = "perfil"

    def get_object(self):
        perfil, creado = PerfilUsuario.objects.get_or_create(usuario=self.request.user)
        return perfil

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        perfil = self.get_object()

        context["fotos_perfil"] = [
            (perfil.foto_perfil, "Foto de Perfil"),
            (perfil.foto_cedula_adelante, "Foto Cédula Adelante"),
            (perfil.foto_cedula_atras, "Foto Cédula Atrás"),
            (perfil.foto_casa, "Foto Casa"),
            (perfil.foto_curso_altura, "Foto Curso Altura"),
            (perfil.foto_diploma_grado, "Foto Diploma Grado"),
        ]

        return context


# ============================================================
# VEHÍCULOS - CRUD
# ============================================================


class VehiculoUsuarioListView(LoginRequiredMixin, ListView):
    model = VehiculoUsuario
    template_name = "perfiles/vehiculos/vehiculousuario_list.html"
    context_object_name = "vehiculos"
    paginate_by = 10

    def get_queryset(self):
        return VehiculoUsuario.objects.all().order_by("-created")


class VehiculoUsuarioDetailView(LoginRequiredMixin, DetailView):
    model = VehiculoUsuario
    template_name = "perfiles/vehiculos/vehiculousuario_detail.html"
    context_object_name = "vehiculo"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vehiculo = self.get_object()

        context["fotos_vehiculo"] = [
            (vehiculo.foto_vehiculo, "Foto del Vehículo"),
            (vehiculo.foto_soat, "Foto SOAT"),
            (vehiculo.foto_tecnomecanico, "Foto Tecnomecánico"),
            (vehiculo.foto_tarjeta_propiedad, "Foto Tarjeta Propiedad"),
            (vehiculo.foto_pase_conducir, "Foto Pase de Conducir"),
        ]

        return context


class VehiculoUsuarioCreateView(LoginRequiredMixin, CreateView):
    model = VehiculoUsuario
    form_class = VehiculoUsuarioForm
    template_name = "perfiles/vehiculos/vehiculousuario_create.html"
    success_url = reverse_lazy("vehiculousuario_list")

    def form_valid(self, form):
        response = super().form_valid(form)

        Notificaciones.objects.create(
            usuario=self.object.usuario,
            estado=EstadoNotificacion.EXITO,
            titulo="Perfil creado",
            mensaje=f"Un administrador cargo tu vehículo en sistema",
        )

        return response


class VehiculoUsuarioUpdateView(LoginRequiredMixin, UpdateView):
    model = VehiculoUsuario
    form_class = VehiculoUsuarioForm
    template_name = "perfiles/vehiculos/vehiculousuario_update.html"
    success_url = reverse_lazy("vehiculousuario_list")

    def form_valid(self, form):
        response = super().form_valid(form)

        Notificaciones.objects.create(
            usuario=self.object.usuario,
            estado=EstadoNotificacion.ADVERTENCIA,
            titulo="Perfil creado",
            mensaje=f"Un administrador modificó datos de tu vehículo en sistema",
        )

        return response


class VehiculoUsuarioDeleteView(LoginRequiredMixin, DeleteView):
    model = VehiculoUsuario
    template_name = "perfiles/vehiculos/vehiculousuario_confirm_delete.html"
    success_url = reverse_lazy("vehiculousuario_list")

    def form_valid(self, form):
        response = super().form_valid(form)

        Notificaciones.objects.create(
            usuario=self.object.usuario,
            estado=EstadoNotificacion.ADVERTENCIA,
            titulo="Perfil creado",
            mensaje=f"Un administrador eliminó tu vehículo del sistema",
        )

        return response


# ============================================================
# MIS VEHÍCULOS (Solo del usuario autenticado)
# ============================================================


class MisVehiculosListView(LoginRequiredMixin, ListView):
    model = VehiculoUsuario
    template_name = "perfiles/vehiculos/mis_vehiculos.html"
    context_object_name = "vehiculos"
    paginate_by = 10

    def get_queryset(self):
        return VehiculoUsuario.objects.filter(usuario=self.request.user)
