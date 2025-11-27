import uuid

from django.conf import settings

from django.db import models
from django_extensions.db.models import TimeStampedModel
from phonenumber_field.modelfields import PhoneNumberField
from apps.notificaciones.models import Notificaciones, EstadoNotificacion


# ===========================================================================================
# MODELO PROVEEDOR
# ===========================================================================================
class Proveedor(TimeStampedModel):
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
        related_name="proveedor",
        verbose_name="Usuario",
    )
    nombre = models.CharField(max_length=100, verbose_name="nombre proveedor")
    telefono = PhoneNumberField(verbose_name="Teléfono", blank=True, null=True)
    whatsapp = PhoneNumberField(verbose_name="WhatsApp", blank=True, null=True)
    direccion = models.TextField(verbose_name="Dirección", blank=True, null=True)
    url = models.URLField(verbose_name="URL", blank=True, null=True)
    email = models.EmailField(verbose_name="Correo electrónico", blank=True, null=True)

    class Meta:
        db_table = "PROVEEDORES"
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"

    def __str__(self):
        return self.nombre


# ===========================================================================================
# MODELO CATEGORIA
# ===========================================================================================
class Categoria(TimeStampedModel):
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
        related_name="categoria_usuario",
        verbose_name="Usuario",
    )
    nombre = models.CharField(max_length=100, verbose_name="nombre de categoria")
    descripcion = models.TextField(verbose_name="descripcion")

    class Meta:
        db_table = "CATEGORIA"
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.nombre


# ===========================================================================================
# MODELO PRODUCTO CON SUS MEDIDAS
# ===========================================================================================
class MedidaProducto(models.TextChoices):
    ROLLOS = "ROLLOS", "Rollos"
    UNIDADES = "UNIDADES", "Unidades"
    PAQUETES = "PAQUETES", "Paquetes"
    METROS = "METROS", "Metros"


class Producto(TimeStampedModel):
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
        related_name="producto_usuario",
        verbose_name="Usuario",
    )
    proveedor = models.ForeignKey(
        "Proveedor",
        on_delete=models.CASCADE,
        related_name="producto_proveedor",
        verbose_name="proveedor",
    )
    categoria = models.ForeignKey(
        "Categoria",
        on_delete=models.CASCADE,
        related_name="producto_categoria",
        verbose_name="categoria",
    )
    nombre = models.CharField(max_length=100, verbose_name="nombre de producto")
    descripcion = models.TextField(verbose_name="descripcion")

    precio_compra = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="precio_compra",
    )
    precio_venta = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="precio_venta",
    )

    imagen = models.ImageField(
        upload_to="productos/",
        blank=True,
        null=True,
        verbose_name="imagen del producto",
    )

    medida = models.CharField(
        max_length=20,
        choices=MedidaProducto.choices,
        default=MedidaProducto.UNIDADES,
        verbose_name="Medida del producto",
    )

    class Meta:
        db_table = "PRODUCTO"
        managed = True
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return self.nombre


# ===========================================================================================
# MODELO STOCK
# ===========================================================================================


class StockMovimiento(models.TextChoices):
    Entrada = "ENTRADA", "Entrada"
    Salida = "SALIDA", "Salida"
    Transferencia = "TRANSFERENCIA", "Transferencia"


class StockMotivo(models.TextChoices):
    Surtir = "SURTIR", "Surtir"
    Desecho = "DESECHO", "Desecho"
    Ticket = "TICKET", "Ticket"
    Transferencia = "TRANSFERENCIA", "Transferencia"


class Stock(TimeStampedModel):
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
        related_name="stock_usuario",
        verbose_name="Usuario",
        editable=False,
    )

    producto = models.ForeignKey(
        "Producto",
        on_delete=models.CASCADE,
        related_name="stock_producto",
        verbose_name="producto",
    )

    usuario_origen = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="stock_usuario_origen",
        verbose_name="Usuario Origen",
        blank=True,
        null=True,
    )
    usuario_destino = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="stock_usuario_destino",
        verbose_name="Usuario Destino",
        blank=True,
        null=True,
    )

    cantidad_movida = models.PositiveIntegerField(verbose_name="Cantidad_movida")
    movimiento = models.CharField(
        max_length=50, choices=StockMovimiento, verbose_name="movimiento"
    )
    motivo = models.CharField(
        max_length=50, choices=StockMotivo, verbose_name="motivo", blank=True, null=True
    )

    motivo_personalizado = models.TextField(
        verbose_name="motivo personalizado", blank=True, null=True
    )
    codigo_ticket = models.CharField(
        max_length=100, verbose_name="codigo ticket", blank=True, null=True
    )

    class Meta:
        db_table = "STOCK"
        verbose_name = "Stock"
        verbose_name_plural = "Stocks"

    def __str__(self):
        return f"{self.producto.nombre} - Cantidad: {self.cantidad_movida}"

    # ================================================================
    # LÓGICA COMPLETA DE MOVIMIENTO + ACTUALIZACIÓN StockActual
    # ================================================================
    def save(self, *args, **kwargs):

        from .models import StockActual  # evitar import circular

        # ------------------------------------------------------------
        # Función para obtener o crear el stock actual
        # ------------------------------------------------------------
        def obtener_stock_actual(usuario, producto):
            stock, creado = StockActual.objects.get_or_create(
                usuario=usuario, producto=producto, defaults={"cantidad": 0}
            )
            return stock

        # ============================================================
        #   MOVIMIENTO: ENTRADA
        # ============================================================
        if self.movimiento == StockMovimiento.Entrada:

            if not self.usuario_destino:
                self.usuario_destino = self.usuario

            stock_destino = obtener_stock_actual(self.usuario_destino, self.producto)

            stock_destino.cantidad += self.cantidad_movida
            stock_destino.save()

        # ============================================================
        #   MOVIMIENTO: SALIDA
        # ============================================================
        elif self.movimiento == StockMovimiento.Salida:

            if not self.usuario_origen:
                self.usuario_origen = self.usuario

            stock_origen = obtener_stock_actual(self.usuario_origen, self.producto)

            if stock_origen.cantidad < self.cantidad_movida:
                raise ValueError("No hay suficiente stock para realizar la salida.")

            stock_origen.cantidad -= self.cantidad_movida
            stock_origen.save()

        # ============================================================
        #   MOVIMIENTO: TRANSFERENCIA
        # ============================================================
        elif self.movimiento == StockMovimiento.Transferencia:

            if not self.usuario_origen or not self.usuario_destino:
                raise ValueError(
                    "La transferencia requiere usuario origen y usuario destino."
                )

            stock_origen = obtener_stock_actual(self.usuario_origen, self.producto)
            stock_destino = obtener_stock_actual(self.usuario_destino, self.producto)

            if stock_origen.cantidad < self.cantidad_movida:
                raise ValueError("No hay suficiente stock en el usuario origen.")

            stock_origen.cantidad -= self.cantidad_movida
            stock_destino.cantidad += self.cantidad_movida

            stock_origen.save()
            stock_destino.save()

            # Notificaciones para origen y destino
            Notificaciones.objects.create(
                usuario=self.usuario_origen,
                estado=EstadoNotificacion.EXITO,
                titulo="Transferencia de stock realizada",
                mensaje=(
                    f"Transferiste {self.cantidad_movida} unidades del producto "
                    f"{self.producto.nombre} al usuario {self.usuario_destino.email}."
                ),
            )

            Notificaciones.objects.create(
                usuario=self.usuario_destino,
                estado=EstadoNotificacion.EXITO,
                titulo="Has recibido stock",
                mensaje=(
                    f"Has recibido {self.cantidad_movida} unidades del producto "
                    f"{self.producto.nombre} desde {self.usuario_origen.email}."
                ),
            )

        # Registrar el movimiento
        super().save(*args, **kwargs)

        @property
        def stock_actual(self):
            from .models import StockActual

            try:
                return StockActual.objects.get(
                    usuario=self.usuario, producto=self.producto
                )
            except StockActual.DoesNotExist:
                return None


class StockActual(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, unique=True, editable=False
    )

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="stock_actual_usuario",
    )

    producto = models.ForeignKey(
        "Producto", on_delete=models.CASCADE, related_name="stock_actual_producto"
    )

    cantidad = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "STOCK_ACTUAL"
        verbose_name = "Stock Actual"
        verbose_name_plural = "Stock Actual"
        unique_together = ("usuario", "producto")

    def __str__(self):
        return f"{self.usuario.email} - {self.producto.nombre}: {self.cantidad}"
