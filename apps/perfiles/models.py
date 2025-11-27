from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.conf import settings
import uuid
from phonenumber_field.modelfields import PhoneNumberField


class CargoUsuario(models.TextChoices):
    Gerente = "GERENTE", "Gerente"
    Administrador = "ADMINISTRADOR", "Administrador"
    Ingeniero = "INGENIERO", "Ingeniero"
    Tecnico = "TECNICO", "Técnico"
    Agente = "AGENTE", "Agente"
    Marketing = "MARKETING", "Marketing"


class EstadoCivilUsuario(models.TextChoices):
    Casado = "CASADO", "Casado"
    Soltero = "SOLTERO", "Soltero"
    Union_Libre = "UNION_LIBRE", "Unión Libre"


class NivelEducativoUsuario(models.TextChoices):
    Primaria = "PRIMARIA", "Primaria"
    Basica_Secundaria = "BASICA_SECUNDARIA", "Básica Secundaria"
    Bachiller_academico = "BACHILLER_ACADEMICO", "Bachiller Académico"
    Tecnico = "TECNICO", "Técnico"
    Ingeniero = "INGENIERO", "Ingeniero"


class GeneroUsuario(models.TextChoices):
    Hombre = "HOMBRE", "Hombre"
    Mujer = "MUJER", "Mujer"
    Inclusivo = "INCLUSIVO", "Inclusivo"


class PerfilUsuario(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        editable=False,
        verbose_name="Identificador",
    )

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="perfil_usuario",
        verbose_name="Usuario",
    )

    nombres = models.CharField(max_length=100, verbose_name="Nombres")
    apellidos = models.CharField(max_length=100, verbose_name="Apellidos")
    direccion = models.TextField(verbose_name="Dirección", blank=True, null=True)
    telefono = PhoneNumberField(verbose_name="Teléfono", blank=True, null=True)
    whatsapp = PhoneNumberField(verbose_name="WhatsApp", blank=True, null=True)
    fecha_nacimiento = models.DateField(
        verbose_name="Fecha de nacimiento", blank=True, null=True
    )

    foto_perfil = models.ImageField(
        upload_to="perfiles/fotos_perfil/",
        verbose_name="Foto de perfil",
        blank=True,
        null=True,
    )
    foto_cedula_adelante = models.ImageField(
        upload_to="perfiles/cedula_adelante/",
        verbose_name="Foto cédula adelante",
        blank=True,
        null=True,
    )
    foto_cedula_atras = models.ImageField(
        upload_to="perfiles/cedula_atras/",
        verbose_name="Foto cédula atrás",
        blank=True,
        null=True,
    )
    foto_casa = models.ImageField(
        upload_to="perfiles/fotos_casa/",
        verbose_name="Foto casa",
        blank=True,
        null=True,
    )
    foto_curso_altura = models.ImageField(
        upload_to="perfiles/fotos_curso_altura/",
        verbose_name="Foto curso de altura",
        blank=True,
        null=True,
    )
    foto_diploma_grado = models.ImageField(
        upload_to="perfiles/fotos_diploma_grado/",
        verbose_name="Foto diploma grado",
        blank=True,
        null=True,
    )

    cargo = models.CharField(
        max_length=50,
        choices=CargoUsuario.choices,
        verbose_name="Cargo",
        blank=True,
        null=True,
    )
    nivel_educativo = models.CharField(
        max_length=50,
        choices=NivelEducativoUsuario.choices,
        verbose_name="Nivel educativo",
        blank=True,
        null=True,
    )
    curso_altura = models.BooleanField(
        verbose_name="Curso de altura aprobado", default=False
    )

    hijos = models.BooleanField(verbose_name="Tiene hijos", default=False)
    estado_civil = models.CharField(
        max_length=50,
        choices=EstadoCivilUsuario.choices,
        verbose_name="Estado civil",
        blank=True,
        null=True,
    )
    conyugue = models.BooleanField(verbose_name="Tiene cónyuge", default=False)
    nombre_conyugue = models.CharField(
        max_length=100, verbose_name="Nombre cónyuge", blank=True, null=True
    )
    telefono_conyugue = PhoneNumberField(
        verbose_name="Teléfono conyugue", blank=True, null=True
    )

    fecha_ingreso_empresa = models.DateField(
        verbose_name="Fecha de ingreso a la empresa", blank=True, null=True
    )
    fecha_retiro_empresa = models.DateField(
        verbose_name="Fecha de retiro de la empresa", blank=True, null=True
    )

    genero = models.CharField(
        max_length=20,
        choices=GeneroUsuario.choices,
        verbose_name="Género",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

    class Meta:
        db_table = "PERFILES"
        verbose_name = "Perfil"
        verbose_name_plural = "Perfiles"


class TipoVehiculo(models.TextChoices):
    Moto = "MOTO", "Moto"
    Carro = "CARRO", "Carro"
    Camioneta = "CAMIONETA", "Camioneta"
    Camion = "CAMION", "Camion"


class VehiculoUsuario(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        editable=False,
        verbose_name="Identificador",
    )

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="vehiculos_usuario",
        verbose_name="Usuario",
    )

    foto_vehiculo = models.ImageField(
        upload_to="vehiculos/foto_vehiculo/",
        verbose_name="Foto vehículo",
        blank=True,
        null=True,
    )
    foto_soat = models.ImageField(
        upload_to="vehiculos/foto_soat/",
        verbose_name="Foto SOAT",
        blank=True,
        null=True,
    )
    foto_tecnomecanico = models.ImageField(
        upload_to="vehiculos/foto_tecnomecanico/",
        verbose_name="Foto Tecnomecánico",
        blank=True,
        null=True,
    )
    foto_tarjeta_propiedad = models.ImageField(
        upload_to="vehiculos/foto_tarjeta_propiedad/",
        verbose_name="Foto tarjeta de propiedad",
        blank=True,
        null=True,
    )
    foto_pase_conducir = models.ImageField(
        upload_to="vehiculos/foto_pase_conducir/",
        verbose_name="Foto pase de conducir",
        blank=True,
        null=True,
    )

    marca = models.CharField(max_length=50, verbose_name="Marca", blank=True, null=True)
    placas_vehiculo = models.CharField(
        max_length=50, verbose_name="Placas", blank=True, null=True
    )

    soat = models.DateField(
        verbose_name="Fecha de vencimiento del SOAT", null=True, blank=True
    )

    tecnomecanico = models.DateField(
        verbose_name="Fecha de vencimiento del Tecnomecánico", null=True, blank=True
    )

    tarjeta_propiedad = models.DateField(
        verbose_name="Fecha de vencimiento de la Tarjeta de Propiedad",
        null=True,
        blank=True,
    )

    pase_conducir = models.DateField(
        verbose_name="Fecha de vencimiento del Pase de Conducir", null=True, blank=True
    )

    tipo_vehiculo = models.CharField(
        max_length=50,
        choices=TipoVehiculo,
        verbose_name="tipo de vehiculo",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.marca} - {self.placas_vehiculo}"

    class Meta:
        db_table = "VEHICULO"
        verbose_name = "Vehículo"
        verbose_name_plural = "Vehículos"
