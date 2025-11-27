# url de la api

## Método HTTP	URL	Acción

- GET	    /notificaciones/	    Lista todas las notificaciones
- POST	    /notificaciones/	    Crear una nueva notificación
- GET	    /notificaciones/{pk}/	Ver detalle de una notificación
- PUT	    /notificaciones/{pk}/	Actualizar una notificación
- PATCH	    /notificaciones/{pk}/	Actualizar parcialmente
- DELETE	/notificaciones/{pk}/	Eliminar una notificación



# registro en urls del proyecto 
- path('api/', include('notificaciones.urls_api')),


# url de la vista frontend

- path('notificaciones/historial/', NotificacionesListView.as_view(), name='notificaciones_historial'),

==============================================================================================================

- instalar DRF y Django filters