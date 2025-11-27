# apps/app_usuario/usuario/forms.py

from django import forms
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, View

from .models import Usuario


# ------------------------------------------------------------
# CREACION DE USUARIOS
# ------------------------------------------------------------
class UsuarioForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Contraseña",
                "autocomplete": "new-password",
                "class": "form-control",
            }
        ),
        required=True,
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirmar contraseña",
                "autocomplete": "new-password",
                "class": "form-control",
            }
        ),
        required=True,
        label="",
    )

    class Meta:
        model = Usuario
        fields = ["email", "password", "password_confirm"]
        widgets = {
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "Correo electrónico",
                    "class": "form-control",
                    "autocomplete": "email",
                }
            ),
        }
        labels = {"email": ""}

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error("password_confirm", "Las contraseñas no coinciden.")
        return cleaned_data

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.set_password(self.cleaned_data["password"])
        if commit:
            usuario.save()
        return usuario


class UsuarioEditForm(forms.ModelForm):
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Contraseña",
                "autocomplete": "new-password",
            }
        ),
        required=False,
        help_text="Dejar en blanco para mantener la contraseña actual.",
    )

    class Meta:
        model = Usuario
        fields = ["email", "password", "is_active", "is_staff"]
        widgets = {
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "Correo electrónico",
                    "class": "form-control",
                    "autocomplete": "email",
                }
            ),
        }
        labels = {"email": "Correo Electrónico", "password": "Contraseña"}

        help_texts = {
            "is_active": "Estado Activo.",
            "is_staff": "Administrador.",
        }

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if not password:
            # Retorna la contraseña actual si no se cambia
            return self.instance.password
        return password

    def save(self, commit=True):
        usuario = super().save(commit=False)
        password = self.cleaned_data.get("password")
        if password and not usuario.check_password(password):
            usuario.set_password(password)
        if commit:
            usuario.save()
        return usuario


# ------------------------------------------------------------
# LOGIN DE USUARIOS
# ------------------------------------------------------------
class CustomLoginForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Correo electrónico",
                "autocomplete": "email",
                "autofocus": True,
            }
        ),
        label="",
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Contraseña",
                "autocomplete": "current-password",
            }
        ),
        label="",
    )

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)


# ------------------------------------------------------------
# CAMBIO DE CONTRASEÑA SESION INICIADA
# ------------------------------------------------------------
class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Contraseña actual",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Contraseña actual"}
        ),
    )
    new_password1 = forms.CharField(
        label="Nueva contraseña",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Nueva contraseña"}
        ),
    )
    new_password2 = forms.CharField(
        label="Confirmar nueva contraseña",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirmar nueva contraseña"}
        ),
    )


# ------------------------------------------------------------
# RESTABLECIMIENTO DE CONTRASEÑA
# ------------------------------------------------------------
class SolicitarRecuperacionForm(forms.Form):
    email = forms.EmailField(
        label="",
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Correo electrónico",
                "class": "form-control",
                "autocomplete": "email",
            }
        ),
    )


class VerificarCodigoForm(forms.Form):
    codigo = forms.CharField(
        label="",
        max_length=6,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Código de verificación",
                "class": "form-control",
                "autocomplete": "off",
            }
        ),
    )


class RestablecerPasswordForm(forms.Form):
    nueva_contrasena = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Nueva contraseña"}
        ),
    )
    confirmar_contrasena = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirmar contraseña"}
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("nueva_contrasena")
        p2 = cleaned_data.get("confirmar_contrasena")
        if p1 != p2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned_data


# ------------------------------------------------------------
# FORMULARIO PARA MODIFICAR EL CORREO
# ------------------------------------------------------------
class ModificarCorreoForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ["email"]
        widgets = {
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "Nuevo correo electrónico",
                    "class": "form-control",
                    "autocomplete": "email",
                }
            ),
        }
        labels = {"email": ""}

    def save(self, commit=True):
        usuario = super().save(commit=False)
        if commit:
            usuario.save()
        return usuario


# ------------------------------------------------------------
# FORMULARIO PARA DESACTIVAR CUENTA
# ------------------------------------------------------------
class ConfirmarDesactivacionForm(forms.Form):
    confirmacion = forms.BooleanField(
        label="Confirmo que quiero desactivar mi cuenta. Solo el administrador podrá activarla de nuevo.",
        required=True,
    )


# ------------------------------------------------------------
# FORMULARIO PARA ELIMINAR CUENTA
# ------------------------------------------------------------
class ConfirmarEliminacionForm(forms.Form):
    confirmacion = forms.BooleanField(
        label="Confirmo que quiero eliminar este usuario permanentemente.",
        required=True,
    )
