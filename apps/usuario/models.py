import random
import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from .managers import UsuarioManager


class Usuario(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        editable=False,
        verbose_name="identificador",
    )

    email = models.EmailField(
        max_length=50, unique=True, editable=True, verbose_name="correo electrónico"
    )
    fecha_creacion = models.DateTimeField(
        auto_now_add=True, verbose_name="fecha de creación"
    )
    fecha_modificacion = models.DateTimeField(
        auto_now=True, verbose_name="fecha de modificación"
    )

    is_active = models.BooleanField(default=True, verbose_name="usuario activo")
    is_staff = models.BooleanField(default=False, verbose_name="administrador")
    is_superuser = models.BooleanField(default=False, verbose_name="superusuario")

    objects = UsuarioManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "USUARIO"
        verbose_name = "USUARIO"
        verbose_name_plural = "USUARIOS"
        ordering = ["-fecha_creacion"]
        indexes = [models.Index(fields=["email"], name="email_idx")]

    def __str__(self):
        return self.email

    # Métodos para activar o desactivar usuario
    def activar_usuario(self):
        if not self.is_active:
            self.is_active = True
            self.save(update_fields=["is_active"])

    def desactivar_usuario(self):
        if self.is_active:
            self.is_active = False
            self.save(update_fields=["is_active"])


class CodigoRecuperacion(models.Model):
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="ver_codigo_recuperacion",
        verbose_name="Usuario",
    )
    codigo = models.CharField(max_length=6)
    fecha_creacion = models.DateTimeField(
        auto_now_add=True, verbose_name="fecha de creación"
    )
    usado = models.BooleanField(default=False)

    class Meta:
        db_table = "CODIGO_RECUPERACION"
        verbose_name = "Código de recuperación"
        verbose_name_plural = "Códigos de recuperación"
        ordering = ["-fecha_creacion"]

    def generar_codigo(self):
        # Generar código aleatorio
        self.codigo = f"{random.randint(100000, 999999):06d}"
        self.usado = False
        self.save(update_fields=["codigo", "usado"])

    def __str__(self):
        return f"{self.usuario.email} - {self.codigo}"
