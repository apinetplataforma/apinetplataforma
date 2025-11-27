from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Usuario
from django.core.mail import send_mail


@receiver(post_save, sender=Usuario)
def enviar_bienvenida(sender, instance, created, **kwargs):
    if created:
        subject = "Bienvenido a nuestra plataforma"
        message = f"Hola {instance.email}, gracias por registrarte."
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [instance.email]

        send_mail(subject, message, from_email, recipient_list)
