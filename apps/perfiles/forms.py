from django import forms
from .models import PerfilUsuario, VehiculoUsuario


# ============================================================
# PERFIL USUARIO FORM
# ============================================================
class PerfilUsuarioForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Ajustar formato yyyy-mm-dd para los inputs tipo date
        date_fields = [
            "fecha_nacimiento",
            "fecha_ingreso_empresa",
            "fecha_retiro_empresa",
        ]
        for field in date_fields:
            value = self.initial.get(field) or (
                self.instance and getattr(self.instance, field)
            )
            if value:
                self.initial[field] = value.strftime("%Y-%m-%d")

    class Meta:
        model = PerfilUsuario
        fields = [
            "usuario",
            "nombres",
            "apellidos",
            "direccion",
            "telefono",
            "whatsapp",
            "fecha_nacimiento",
            "foto_perfil",
            "foto_cedula_adelante",
            "foto_cedula_atras",
            "foto_casa",
            "foto_curso_altura",
            "foto_diploma_grado",
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
            "genero",
        ]

        widgets = {
            "usuario": forms.Select(attrs={"class": "form-select"}),
            "nombres": forms.TextInput(attrs={"class": "form-control"}),
            "apellidos": forms.TextInput(attrs={"class": "form-control"}),
            "direccion": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "telefono": forms.TextInput(attrs={"class": "form-control"}),
            "whatsapp": forms.TextInput(attrs={"class": "form-control"}),
            "fecha_nacimiento": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "fecha_ingreso_empresa": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "fecha_retiro_empresa": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "foto_perfil": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "foto_cedula_adelante": forms.ClearableFileInput(
                attrs={"class": "form-control"}
            ),
            "foto_cedula_atras": forms.ClearableFileInput(
                attrs={"class": "form-control"}
            ),
            "foto_casa": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "foto_curso_altura": forms.ClearableFileInput(
                attrs={"class": "form-control"}
            ),
            "foto_diploma_grado": forms.ClearableFileInput(
                attrs={"class": "form-control"}
            ),
            "cargo": forms.Select(attrs={"class": "form-select"}),
            "nivel_educativo": forms.Select(attrs={"class": "form-select"}),
            "curso_altura": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "hijos": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "estado_civil": forms.Select(attrs={"class": "form-select"}),
            "conyugue": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "nombre_conyugue": forms.TextInput(attrs={"class": "form-control"}),
            "telefono_conyugue": forms.TextInput(attrs={"class": "form-control"}),
            "genero": forms.Select(attrs={"class": "form-select"}),
        }


# ============================================================
# VEHICULO USUARIO FORM
# ============================================================
class VehiculoUsuarioForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["usuario"].widget.attrs.update({"class": "form-select"})
        self.fields["tipo_vehiculo"].widget.attrs.update({"class": "form-select"})

        # LISTA REAL DE TODOS LOS CAMPOS DE FECHA
        date_fields = ["soat", "tecnomecanico", "tarjeta_propiedad", "pase_conducir"]

        # AJUSTE CORRECTO PARA MOSTRAR LAS FECHAS GUARDADAS
        for field in date_fields:
            value = getattr(self.instance, field, None)
            if value:
                self.initial[field] = value.strftime("%Y-%m-%d")

    class Meta:
        model = VehiculoUsuario
        fields = [
            "usuario",
            "tipo_vehiculo",
            "foto_vehiculo",
            "foto_soat",
            "foto_tecnomecanico",
            "foto_tarjeta_propiedad",
            "foto_pase_conducir",
            "marca",
            "placas_vehiculo",
            # FECHAS
            "soat",
            "tecnomecanico",
            "tarjeta_propiedad",
            "pase_conducir",
        ]

        widgets = {
            "foto_vehiculo": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "foto_soat": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "foto_tecnomecanico": forms.ClearableFileInput(
                attrs={"class": "form-control"}
            ),
            "foto_tarjeta_propiedad": forms.ClearableFileInput(
                attrs={"class": "form-control"}
            ),
            "foto_pase_conducir": forms.ClearableFileInput(
                attrs={"class": "form-control"}
            ),
            "marca": forms.TextInput(attrs={"class": "form-control"}),
            "placas_vehiculo": forms.TextInput(attrs={"class": "form-control"}),
            # ✔ Inputs tipo fecha correctamente configurados
            "soat": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "tecnomecanico": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "tarjeta_propiedad": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "pase_conducir": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
        }
