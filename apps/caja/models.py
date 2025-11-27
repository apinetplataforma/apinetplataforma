from django.db import models
from django_extensions.db.models import TimeStampedModel
import uuid
from django.conf import settings
from decimal import Decimal


# =============================================================================
# ELECCIÓN DE TIPO DE MOVIMIENTO
# =============================================================================


class MovimientoCaja(models.TextChoices):
    INGRESO = "INGRESO", "Ingreso"
    SALIDA = "SALIDA", "Salida"


# =============================================================================
# MOTIVOS DEL MOVIMIENTO
# =============================================================================


class MotivoMovimientoCaja(models.TextChoices):
    ENTREGA_CUENTAS = "ENTREGA_CUENTAS", "Entrega Cuentas"
    ABONO_A_BASE = "ABONO_A_BASE", "Abono a Base"
    RECAUDO_OFICINA = "RECAUDO_OFICINA", "Recaudo Oficina"
    RECAUDO_PUNTO_FISICO = "RECAUDO_PUNTO_FISICO", "Recaudo Punto Físico"
    GASOLINA = "GASOLINA", "Gasolina"
    ACEITE = "ACEITE", "Aceite"
    HERRAMIENTAS_COMPLEMENTARIAS = (
        "HERRAMIENTAS_COMPLEMENTARIAS",
        "Herramientas Complementarias",
    )
    REPARACION_VEHICULO = "REPARACION_VEHICULO", "Reparación Vehículo"
    CAFETERIA = "CAFETERIA", "Cafetería"
    ELEMENTOS_ASEO = "ELEMENTOS_ASEO", "Elementos Aseo"
    PRESTAMOS = "PRESTAMOS", "Préstamos"
    VENTA_EQUIPO = "VENTA_EQUIPO", "Venta Equipo"


# =============================================================================
# SALDO ACTUAL DE LA CAJA
# =============================================================================


class SaldoCaja(TimeStampedModel):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="saldo_caja",
        verbose_name="Usuario",
    )

    saldo = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        verbose_name="Saldo Actual",
    )

    class Meta:
        db_table = "SALDO_CAJA"
        verbose_name = "Saldo Caja"
        verbose_name_plural = "Saldos de Caja"

    def __str__(self):
        return f"{self.usuario} - Saldo: {self.saldo}"


# =============================================================================
# MOVIMIENTOS DE CAJA
# =============================================================================


class Caja(TimeStampedModel):
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
        related_name="movimientos_caja",
        verbose_name="Usuario",
    )

    tipo_movimiento = models.CharField(
        max_length=10,
        choices=MovimientoCaja.choices,
        verbose_name="Tipo de movimiento",
    )

    cantidad_movida = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        verbose_name="Cantidad Movida",
    )

    motivo_movimiento = models.CharField(
        max_length=50,
        choices=MotivoMovimientoCaja.choices,
        verbose_name="Motivo de movimiento",
    )

    info_adicional = models.TextField(
        verbose_name="Información adicional", blank=True, null=True
    )

    class Meta:
        db_table = "CAJA"
        verbose_name = "Movimiento de Caja"
        verbose_name_plural = "Movimientos de Caja"

    def __str__(self):
        return f"{self.usuario} - {self.tipo_movimiento} - {self.cantidad_movida}"

    # =========================================================================
    # APLICAR SALDO
    # =========================================================================

    def aplicar_a_saldo(self):
        saldo, created = SaldoCaja.objects.get_or_create(
            usuario=self.usuario, defaults={"saldo": Decimal("0.00")}
        )

        if self.tipo_movimiento == MovimientoCaja.INGRESO:
            saldo.saldo += self.cantidad_movida

        elif self.tipo_movimiento == MovimientoCaja.SALIDA:
            if saldo.saldo < self.cantidad_movida:
                raise ValueError("Saldo insuficiente en caja.")
            saldo.saldo -= self.cantidad_movida

        saldo.save()

    # =========================================================================
    # REVERTIR SALDO (AL ELIMINAR)
    # =========================================================================

    def revertir_saldo(self):
        saldo = SaldoCaja.objects.get(usuario=self.usuario)

        if self.tipo_movimiento == MovimientoCaja.INGRESO:
            # Si era un ingreso → se resta
            saldo.saldo -= self.cantidad_movida

        elif self.tipo_movimiento == MovimientoCaja.SALIDA:
            # Si era una salida → se suma
            saldo.saldo += self.cantidad_movida

        saldo.save()

    # =========================================================================
    # GUARDAR
    # =========================================================================

    def save(self, *args, **kwargs):
        es_nuevo = self.pk is None

        super().save(*args, **kwargs)

        if es_nuevo:
            self.aplicar_a_saldo()

    # =========================================================================
    # BORRAR
    # =========================================================================

    def delete(self, *args, **kwargs):
        self.revertir_saldo()
        super().delete(*args, **kwargs)
