from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import CodigoRecuperacion, Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = ("email", "is_active", "is_staff", "is_superuser", "fecha_creacion")
    list_filter = ("is_active", "is_staff", "is_superuser")
    search_fields = ("email",)
    ordering = ("-fecha_creacion",)
    readonly_fields = ("fecha_creacion", "fecha_modificacion")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Permisos"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Fechas importantes"), {"fields": ("fecha_creacion", "fecha_modificacion")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )


@admin.register(CodigoRecuperacion)
class CodigoRecuperacionAdmin(admin.ModelAdmin):
    list_display = ("usuario", "codigo", "fecha_creacion", "usado")
    list_filter = ("usado", "fecha_creacion")
    search_fields = ("usuario__email", "codigo")
    readonly_fields = ("fecha_creacion",)
