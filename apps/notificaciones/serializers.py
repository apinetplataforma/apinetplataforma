from rest_framework import serializers

from .models import Notificaciones


class NotificacionSerializer(serializers.ModelSerializer):
    estado_display = serializers.CharField(source="get_estado_display", read_only=True)

    class Meta:
        model = Notificaciones
        fields = [
            "id",
            "titulo",
            "mensaje",
            "estado",
            "estado_display",
            "leida",
            "created",
            "modified",
        ]
        read_only_fields = ["id", "created", "modified", "estado_display"]
