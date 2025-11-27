from django.contrib import admin
from .models import PerfilUsuario, VehiculoUsuario


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = (
        "nombres",
        "apellidos",
        "usuario",
        "cargo",
        "nivel_educativo",
        "estado_civil",
        "fecha_nacimiento",
    )
    list_filter = ("cargo", "nivel_educativo", "estado_civil", "genero")
    search_fields = ("nombres", "apellidos", "usuario__email")
    readonly_fields = ("id", "created", "modified")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "usuario",
                    "nombres",
                    "apellidos",
                    "direccion",
                    "telefono",
                    "whatsapp",
                    "fecha_nacimiento",
                    "genero",
                )
            },
        ),
        (
            "Imágenes",
            {
                "fields": (
                    "foto_perfil",
                    "foto_cedula_adelante",
                    "foto_cedula_atras",
                    "foto_casa",
                    "foto_curso_altura",
                    "foto_diploma_grado",
                )
            },
        ),
        (
            "Información laboral",
            {
                "fields": (
                    "cargo",
                    "nivel_educativo",
                    "curso_altura",
                    "hijos",
                    "estado_civil",
                    "conyugue",
                    "nombre_conyugue",
                    "telefono_conyugue",
                    "fecha_ingreso_empresa",
                    "fecha_retiro_empresa",
                )
            },
        ),
        (
            "Metadatos",
            {
                "fields": ("id", "created", "modified"),
            },
        ),
    )


@admin.register(VehiculoUsuario)
class VehiculoUsuarioAdmin(admin.ModelAdmin):
    list_display = (
        "usuario",
        "marca",
        "placas_vehiculo",
        "soat",
        "tecnomecanico",
        "tarjeta_propiedad",
    )
    list_filter = ("soat", "tecnomecanico", "tarjeta_propiedad")
    search_fields = ("usuario__email", "marca", "placas_vehiculo")
    readonly_fields = ("id",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "usuario",
                    "marca",
                    "placas_vehiculo",
                )
            },
        ),
        (
            "Documentación",
            {
                "fields": (
                    "foto_vehiculo",
                    "foto_soat",
                    "foto_tecnomecanico",
                    "foto_tarjeta_propiedad",
                    "soat",
                    "tecnomecanico",
                    "tarjeta_propiedad",
                )
            },
        ),
        (
            "Metadatos",
            {
                "fields": ("id",),
            },
        ),
    )
