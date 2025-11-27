from django import forms
from django.contrib.auth import get_user_model
from phonenumber_field.formfields import PhoneNumberField

from .models import (
    Categoria,
    Producto,
    Proveedor,
    Stock,
    StockMovimiento,
    StockMotivo,
    StockActual,
)

from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


class ProveedorForm(forms.ModelForm):
    telefono = PhoneNumberField(
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Teléfono"}
        ),
    )
    whatsapp = PhoneNumberField(
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "WhatsApp"}
        ),
    )

    class Meta:
        model = Proveedor
        fields = ["nombre", "telefono", "whatsapp", "direccion", "url", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            "nombre": "Nombre del proveedor",
            "direccion": "Dirección",
            "url": "URL del sitio web",
            "email": "Correo electrónico",
        }

        for name, field in self.fields.items():
            if name not in ["telefono", "whatsapp"]:
                field.widget.attrs.update(
                    {"class": "form-control", "placeholder": placeholders.get(name, "")}
                )
            field.label = ""


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ["nombre", "descripcion"]

        widgets = {
            "nombre": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Nombre de la categoría"}
            ),
            "descripcion": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Descripción de la categoría",
                    "rows": 4,
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Ocultar labels como a ti te gusta
        for field in self.fields.values():
            field.label = ""


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            "nombre",
            "descripcion",
            "proveedor",
            "categoria",
            "precio_compra",
            "precio_venta",
            "medida",
            "imagen",
        ]

        widgets = {
            "nombre": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nombre del producto",
                }
            ),
            "descripcion": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Descripción del producto",
                    "rows": 4,
                }
            ),
            "proveedor": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
            "categoria": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
            "precio_compra": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Precio de compra",
                }
            ),
            "precio_venta": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Precio de venta",
                }
            ),
            "medida": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
            "imagen": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Ocultar labels (como tú trabajas)
        for field in self.fields.values():
            field.label = ""

        # Placeholder dinámico para selects (opcional)
        self.fields["proveedor"].empty_label = "Seleccione un proveedor"
        self.fields["categoria"].empty_label = "Seleccione una categoría"


class StockMoverProductoBodegaForm(forms.ModelForm):

    movimiento = forms.ChoiceField(
        choices=StockMovimiento.choices,
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
        label="Tipo de movimiento",
    )

    usuario_origen = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        label="Usuario Origen",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    usuario_destino = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        label="Usuario Destino",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    motivo_personalizado = forms.CharField(
        required=False,
        label="Motivo personal",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Escribe el motivo personalizado",
                "rows": 3,
            }
        ),
    )

    class Meta:
        model = Stock
        fields = [
            "usuario_origen",
            "producto",
            "usuario_destino",
            "cantidad_movida",
            "movimiento",
            "motivo",
            "motivo_personalizado",  # ← YA INCLUIDO
            "codigo_ticket",
        ]
        labels = {
            "usuario_origen": "",
            "producto": "",
            "usuario_destino": "",
            "cantidad_movida": "",
            "motivo": "",
            "motivo_personalizado": "",
            "codigo_ticket": "Código Ticket",
        }
        widgets = {
            "usuario_origen": forms.Select(attrs={"class": "form-select"}),
            "producto": forms.Select(attrs={"class": "form-select"}),
            "usuario_destino": forms.Select(attrs={"class": "form-select"}),
            "cantidad_movida": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Cantidad a mover"}
            ),
            "motivo": forms.Select(attrs={"class": "form-select"}),
            "codigo_ticket": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Código del ticket"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["usuario_origen"].empty_label = "Selecciona usuario origen"
        self.fields["producto"].empty_label = "Selecciona un producto"
        self.fields["usuario_destino"].empty_label = "Selecciona usuario destino"
        self.fields["motivo"].empty_label = "Selecciona un motivo"

    def clean(self):
        cleaned_data = super().clean()

        cantidad = cleaned_data.get("cantidad_movida")
        producto = cleaned_data.get("producto")
        movimiento = cleaned_data.get("movimiento")
        motivo = cleaned_data.get("motivo")
        motivo_personalizado = cleaned_data.get("motivo_personalizado")
        usuario_origen = cleaned_data.get("usuario_origen")
        usuario_destino = cleaned_data.get("usuario_destino")

        # Cantidad
        if cantidad is None or cantidad <= 0:
            self.add_error("cantidad_movida", "La cantidad debe ser mayor que cero.")

        # Producto obligatorio
        if not producto:
            self.add_error("producto", "Debes seleccionar un producto.")

        # Movimiento válido
        if movimiento not in dict(StockMovimiento.choices):
            self.add_error("movimiento", "Tipo de movimiento inválido.")

        # Validación según tipo de movimiento
        if movimiento == StockMovimiento.Transferencia:
            if not usuario_origen:
                self.add_error("usuario_origen", "Debes seleccionar un usuario origen.")
            if not usuario_destino:
                self.add_error(
                    "usuario_destino", "Debes seleccionar un usuario destino."
                )
            if usuario_origen == usuario_destino and usuario_origen is not None:
                self.add_error(
                    "usuario_destino", "Usuario destino debe ser diferente al origen."
                )

        elif movimiento == StockMovimiento.Entrada:
            if not usuario_destino:
                self.add_error(
                    "usuario_destino", "Debes seleccionar un usuario destino."
                )

        elif movimiento == StockMovimiento.Salida:
            if not usuario_origen:
                self.add_error("usuario_origen", "Debes seleccionar un usuario origen.")

        # Motivo obligatorio
        if not motivo:
            self.add_error("motivo", "Debes seleccionar un motivo.")

        # Validación de motivo personalizado
        if motivo == StockMotivo.Transferencia and motivo_personalizado:
            self.add_error(
                "motivo_personalizado",
                "En una transferencia no se usa motivo personalizado.",
            )

        return cleaned_data


# ===============================================================================================
# RESTAR PRODUCTO FORM
# ===============================================================================================


class RestarProductoForm(forms.Form):
    producto = forms.ModelChoiceField(
        queryset=StockActual.objects.none(), label="Producto"
    )
    cantidad = forms.IntegerField(min_value=1, label="Cantidad a restar")
    motivo = forms.CharField(
        required=False,
        label="Motivo (opcional)",
        widget=forms.Textarea(attrs={"rows": 3}),
    )

    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop("usuario")
        super().__init__(*args, **kwargs)
        self.fields["producto"].queryset = StockActual.objects.filter(usuario=usuario)
