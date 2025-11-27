from django import forms
from .models import Caja, MovimientoCaja, MotivoMovimientoCaja


class CajaForm(forms.ModelForm):

    class Meta:
        model = Caja
        fields = [
            "tipo_movimiento",
            "motivo_movimiento",
            "cantidad_movida",
            "info_adicional",
        ]

        widgets = {
            "tipo_movimiento": forms.Select(attrs={"class": "form-select"}),
            "motivo_movimiento": forms.Select(attrs={"class": "form-select"}),
            "cantidad_movida": forms.NumberInput(
                attrs={"class": "form-control", "min": "0", "step": "0.01"}
            ),
            "info_adicional": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()

        tipo = cleaned_data.get("tipo_movimiento")
        cantidad = cleaned_data.get("cantidad_movida")

        if cantidad is not None and cantidad <= 0:
            self.add_error("cantidad_movida", "La cantidad debe ser mayor a 0.")

        if tipo not in dict(MovimientoCaja.choices):
            self.add_error("tipo_movimiento", "Tipo de movimiento inválido.")

        return cleaned_data
