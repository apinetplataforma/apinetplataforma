import uuid

from django.conf import settings
from django.db import models
from django_extensions.db.models import TimeStampedModel


class EstadoNotificacion(models.TextChoices):
    INFORMACION = "INFORMACION", "Información"
    ADVERTENCIA = "ADVERTENCIA", "Advertencia"
    EXITO = "EXITO", "Éxito"
    FALLO = "FALLO", "Fallo"
    ERROR = "ERROR", "Error"


class NotificacionesManager(models.Manager):
    def no_leidas(self, usuario):
        return self.filter(usuario=usuario, leida=False)

    def marcar_todas_como_leidas(self, usuario):
        return self.filter(usuario=usuario, leida=False).update(leida=True)


class Notificaciones(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        editable=False,
        verbose_name="identificador",
    )

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notificaciones",
        verbose_name="Usuario",
    )

    estado = models.CharField(
        max_length=20,
        choices=EstadoNotificacion.choices,
        default=EstadoNotificacion.INFORMACION,
    )

    titulo = models.CharField(max_length=50, verbose_name="titulo")
    mensaje = models.TextField(verbose_name="mensaje")

    leida = models.BooleanField(default=False, verbose_name="leida")

    objects = NotificacionesManager()

    class Meta:
        db_table = "NOTIFICACIONES"
        verbose_name = "Notificacion"
        verbose_name_plural = "Notificaciones"
        ordering = ["-created"]

    def __str__(self):
        return self.titulo

    def marcar_leida(self, save=True):
        """Marca solo esta notificación como leída."""
        if not self.leida:
            self.leida = True
            if save:
                self.save(update_fields=["leida"])
