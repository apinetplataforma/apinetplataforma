from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Notificaciones
from .serializers import NotificacionSerializer


class NotificacionViewSet(viewsets.ModelViewSet):
    serializer_class = NotificacionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notificaciones.objects.filter(usuario=self.request.user).order_by(
            "-created"
        )

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

    @action(detail=True, methods=["post"])
    def marcar_leida(self, request, pk=None):
        notificacion = self.get_object()
        notificacion.marcar_leida()
        return Response({"status": "ok", "mensaje": "Notificación marcada como leída"})

    @action(detail=False, methods=["post"])
    def marcar_todas_leidas(self, request):
        Notificaciones.objects.marcar_todas_como_leidas(request.user)
        return Response(
            {"status": "ok", "mensaje": "Todas las notificaciones marcadas como leídas"}
        )
