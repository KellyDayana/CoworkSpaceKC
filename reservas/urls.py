from django.urls import path
from . import views

urlpatterns = [
    # Inicio y Dashboard
    path('', views.inicio, name='inicio'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Autenticación
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registro_view, name='registro'),
    
    # CRUD Empresas Clientes
    path('empresas/', views.empresa_lista, name='empresa_lista'),
    path('empresas/nuevo/', views.nueva_empresa, name='nueva_empresa'),
    path('empresas/guardar/', views.guardar_empresa, name='guardar_empresa'),
    path('empresas/editar/<int:id>/', views.editar_empresa, name='editar_empresa'),
    path('empresas/procesarEdicion/', views.procesar_edicion_empresa, name='procesar_edicion_empresa'),
    path('empresas/eliminar/<int:id>/', views.eliminar_empresa, name='eliminar_empresa'),
    
    # CRUD Miembros (asociados a una Empresa)
    path('empresas/<int:empresa_id>/miembros/', views.miembro_lista, name='miembro_lista'),
    path('empresas/<int:empresa_id>/miembros/nuevo/', views.nuevo_miembro, name='nuevo_miembro'),
    path('empresas/<int:empresa_id>/miembros/guardar/', views.guardar_miembro, name='guardar_miembro'),
    path('miembros/editar/<int:id>/', views.editar_miembro, name='editar_miembro'),
    path('miembros/procesarEdicion/', views.procesar_edicion_miembro, name='procesar_edicion_miembro'),
    path('miembros/eliminar/<int:id>/', views.eliminar_miembro, name='eliminar_miembro'),
    
    # CRUD Salas de Reunión
    path('salas/', views.sala_lista, name='sala_lista'),
    path('salas/nuevo/', views.nueva_sala, name='nueva_sala'),
    path('salas/guardar/', views.guardar_sala, name='guardar_sala'),
    path('salas/editar/<int:id>/', views.editar_sala, name='editar_sala'),
    path('salas/procesarEdicion/', views.procesar_edicion_sala, name='procesar_edicion_sala'),
    path('salas/eliminar/<int:id>/', views.eliminar_sala, name='eliminar_sala'),
    
    # CRUD Escritorios Dedicados
    path('escritorios/', views.escritorio_lista, name='escritorio_lista'),
    path('escritorios/mapa/', views.escritorio_mapa, name='escritorio_mapa'),
    path('escritorios/nuevo/', views.nuevo_escritorio, name='nuevo_escritorio'),
    path('escritorios/guardar/', views.guardar_escritorio, name='guardar_escritorio'),
    path('escritorios/editar/<int:id>/', views.editar_escritorio, name='editar_escritorio'),
    path('escritorios/procesarEdicion/', views.procesar_edicion_escritorio, name='procesar_edicion_escritorio'),
    path('escritorios/eliminar/<int:id>/', views.eliminar_escritorio, name='eliminar_escritorio'),
    path('escritorios/actualizar_posicion/', views.actualizar_posicion_escritorio, name='actualizar_posicion_escritorio'),
    
    # CRUD Reservas de Salas
    path('reservas/', views.reserva_lista, name='reserva_lista'),
    path('reservas/calendario/', views.reserva_calendario, name='reserva_calendario'),
    path('reservas/nuevo/', views.nueva_reserva, name='nueva_reserva'),
    path('reservas/guardar/', views.guardar_reserva, name='guardar_reserva'),
    path('reservas/editar/<int:id>/', views.editar_reserva, name='editar_reserva'),
    path('reservas/procesarEdicion/', views.procesar_edicion_reserva, name='procesar_edicion_reserva'),
    path('reservas/eliminar/<int:id>/', views.eliminar_reserva, name='eliminar_reserva'),
    path('reservas/api/', views.reservas_api, name='reservas_api'),  # Para FullCalendar
    
    # CRUD Eventos
    path('eventos/', views.evento_lista, name='evento_lista'),
    path('eventos/nuevo/', views.nuevo_evento, name='nuevo_evento'),
    path('eventos/guardar/', views.guardar_evento, name='guardar_evento'),
    path('eventos/editar/<int:id>/', views.editar_evento, name='editar_evento'),
    path('eventos/procesarEdicion/', views.procesar_edicion_evento, name='procesar_edicion_evento'),
    path('eventos/eliminar/<int:id>/', views.eliminar_evento, name='eliminar_evento'),
    
    # CRUD Facturas
    path('facturas/', views.factura_lista, name='factura_lista'),
    path('facturas/nuevo/', views.nueva_factura, name='nueva_factura'),
    path('facturas/guardar/', views.guardar_factura, name='guardar_factura'),
    path('facturas/editar/<int:id>/', views.editar_factura, name='editar_factura'),
    path('facturas/procesarEdicion/', views.procesar_edicion_factura, name='procesar_edicion_factura'),
    path('facturas/eliminar/<int:id>/', views.eliminar_factura, name='eliminar_factura'),
    path('facturas/generar_pdf/<int:id>/', views.generar_pdf_factura, name='generar_pdf_factura'),
    path('facturas/calcular-subtotal/<int:empresa_id>/', views.calcular_subtotal_automatico, name='calcular_subtotal_automatico'),
    
    # Reportes
    path('reportes/', views.reportes, name='reportes'),
    path('reportes/ocupacion/', views.reporte_ocupacion, name='reporte_ocupacion'),
    path('reportes/facturacion/', views.reporte_facturacion, name='reporte_facturacion'),
]
