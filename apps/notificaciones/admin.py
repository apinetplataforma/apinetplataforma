from django.contrib import admin
from django.utils.html import format_html

from .models import EstadoNotificacion, Notificaciones


@admin.register(Notificaciones)
class NotificacionesAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "usuario",
        "titulo",
        "estado_coloreado",
        "leida",
        "created",
    )

    list_filter = (
        "estado",
        "leida",
        "created",
        "usuario",
    )

    search_fields = (
        "titulo",
        "mensaje",
        "usuario__username",
        "usuario__email",
    )

    list_display_links = ("titulo",)

    ordering = ("-created",)

    actions = ["marcar_como_leidas", "marcar_como_no_leidas"]

    # ===============================
    # ACCIONES PERSONALIZADAS
    # ===============================

    def marcar_como_leidas(self, request, queryset):
        queryset.update(leida=True)
        self.message_user(request, "Notificaciones marcadas como leídas.")

    marcar_como_leidas.short_description = "Marcar seleccionadas como leídas"

    def marcar_como_no_leidas(self, request, queryset):
        queryset.update(leida=False)
        self.message_user(request, "Notificaciones marcadas como no leídas.")

    marcar_como_no_leidas.short_description = "Marcar seleccionadas como NO leídas"

    # ===============================
    # MOSTRAR ETIQUETA DE COLOR POR ESTADO
    # ===============================
    def estado_coloreado(self, obj):
        colores = {
            EstadoNotificacion.INFORMACION: "blue",
            EstadoNotificacion.ADVERTENCIA: "orange",
            EstadoNotificacion.EXITO: "green",
            EstadoNotificacion.FALLO: "red",
            EstadoNotificacion.ERROR: "darkred",
        }

        color = colores.get(obj.estado, "black")
        return format_html(
            '<span style="color:{}; font-weight:bold;">{}</span>',
            color,
            obj.get_estado_display(),
        )

    estado_coloreado.short_description = "Estado"
