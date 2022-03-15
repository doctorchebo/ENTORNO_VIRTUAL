from . import views
from django.urls import path, include
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('empate-rf',views.EmpateViewSet)
router.register('desembolsos-rf',views.DesembolsosViewSet)
router.register('perfiles-rf',views.PerfilesViewSet)

custodia_router = routers.NestedDefaultRouter(router,'empate-rf',lookup='empate')
custodia_router.register('observaciones',views.ObservacionesViewSet, basename='observaciones-empate')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(custodia_router.urls)),

    #MODULOS
    path('empate_index/', views.empate_index, name='empate_index'),
    path('levantamiento_index/', views.levantamiento_index, name='levantamiento_index'),
    path('servicios_index/', views.servicios_index, name='servicios_index'),
    path('correspondencia_index/', views.correspondencia_index, name='correspondencia_index'),
    path('consultas_index/', views.consultas_index, name='consultas_index'),
    path('reportes_index/', views.reportes_index, name='reportes_index'),

    #DESEMBOLSOS
    path('desembolso_formulario/', views.desembolso_formulario, name='desembolso_insert'),
    path('desestimada_formulario/', views.desembolso_formulario, name='desestimada_insert'),
    path('desembolso_update/<int:desembolso_id>/',views.desembolso_formulario, name='desembolso_update'),
    path('desembolso_delete/<int:desembolso_id>', views.desembolso_delete, name='desembolso_delete'),
    path('desembolso_list/', views.desembolso_list, name='desembolso_list'),

    #EMPATE
    path('empate_update/<int:id>/<int:id_2>/',views.empate_form, name='empate_update'),
    path('empate_list/', views.empate_list, name='empate_list'),
    path('delete_empate/<int:id>', views.empate_delete, name='empate_delete'),
    #CONTRATOS
    path('contrato_update_empate/<int:contrato_id>/',views.formulario_contratos_empate, name='contrato_update_empate'),
    path('formulario_contratos_empate/<int:desembolso_id>/<int:contrato_id>/', views.formulario_contratos_empate, name='contrato_insert_empate'),
    path('contrato_delete_empate/<int:contrato_id>/', views.contrato_delete_empate, name='contrato_delete_empate'),
    path('contratos_list_empate/<int:desembolso_id>/', views.contratos_list_empate, name='contratos_list_empate'),
    
    
    path('contrato_update_levantamiento/<int:contrato_id>/',views.formulario_contratos_levantamiento, name='contrato_update_levantamiento'),
    path('formulario_contratos_levantamiento/', views.formulario_contratos_levantamiento, name='contrato_insert_levantamiento'),
    path('contrato_delete_levantamiento/<int:contrato_id>/', views.contrato_delete_levantamiento, name='contrato_delete_levantamiento'),
    path('contratos_list_levantamiento/', views.contratos_list_levantamiento, name='contratos_list_levantamiento'),
    
    #GARANTIAS
    path('garantias_list_empate/<int:desembolso_id>', views.garantias_list_empate, name='garantias_list_empate'),
    
    path('inmueble_update_empate/<int:inmueble_id>/',views.inmueble_formulario_empate, name='inmueble_update_empate'),
    path('formulario_inmueble_empate/<int:desembolso_id>/<int:inmueble_id>/',views.inmueble_formulario_empate, name='inmueble_insert_empate'),
    path('inmueble_delete_empate/<int:inmueble_id>/', views.inmueble_delete_empate, name='inmueble_delete_empate'),
    
    path('vehiculo_update_empate/<int:vehiculo_id>/',views.vehiculo_formulario_empate, name='vehiculo_update_empate'),
    path('formulario_vehiculo_empate/<int:desembolso_id>/<int:vehiculo_id>/',views.vehiculo_formulario_empate, name='vehiculo_insert_empate'),
    path('vehiculo_delete_empate/<int:vehiculo_id>/', views.vehiculo_delete_empate, name='vehiculo_delete_empate'),
    

    path('garantias_list_levantamiento/', views.garantias_list_levantamiento, name='garantias_list_levantamiento'),

    path('inmueble_update/<int:inmueble_id>/',views.inmueble_formulario_levantamiento, name='inmueble_update_levantamiento'),
    path('formulario_inmueble_levantamiento/',views.inmueble_formulario_levantamiento, name='inmueble_insert_levantamiento'),
    path('inmueble_delete_levantamiento/<int:inmueble_id>/', views.inmueble_delete_levantamiento, name='inmueble_delete_levantamiento'),
    
    path('vehiculo_update_levantamiento/<int:vehiculo_id>/',views.vehiculo_formulario_levantamiento, name='vehiculo_update_levantamiento'),
    path('formulario_vehiculo_levantamiento/',views.vehiculo_formulario_levantamiento, name='vehiculo_insert_levantamiento'),
    path('vehiculo_delete_levantamiento/<int:vehiculo_id>/', views.vehiculo_delete_levantamiento, name='vehiculo_delete_levantamiento'),


    #DOCUMENTOS SUELTOS
    path('formulario_documento_suelto/', views.formulario_documento_suelto, name='documento_suelto_insert'),
    path('documento_suelto_update/<int:documento_suelto_id>/',views.formulario_documento_suelto, name='documento_suelto_update'),
    path('documento_suelto_delete/<int:documento_suelto_id>', views.documento_suelto_delete, name='documento_suelto_delete'),
    path('documentos_sueltos_list/', views.documentos_sueltos_list, name='documentos_sueltos_list'),
    
    #CAJAS
    path('cajas/',views.cajas, name='cajas'),
    path('cajas_list/<int:base>/<int:caja>',views.cajas_list, name='cajas_list'),
    path('listado_ardisa/<int:id>/',views.listado_ardisa, name='listado_ardisa'),
    #DISTRIBUCION
    path('distribucion_list/', views.distribucion_list, name='distribucion_list'),
    path('desestimada/', views.desestimada_formulario, name='desestimada_insert'),
    path('distribucion_update/<int:distribucion_id>/', views.distribucion_formulario, name='distribucion_update'),
    path('distribucion_delete/<int:distribucion_id>/', views.distribucion_delete, name='distribucion_delete'),
    path('distribucion/', views.distribucion_formulario, name='distribucion_insert'),
    #OBSERVACIONES
    path('formulario_observaciones/<int:id>/<int:desembolso_id>',views.formulario_observaciones, name='observaciones_insert'),
    path('delete_observaciones/<int:id>/',views.formulario_observaciones, name='observaciones_delete'),
    path('observacion_list/',views.observacion_list, name='observacion_list'),
    path('observaciones_update/<int:id>/',views.observaciones_update, name='observaciones_update'),
    path('observaciones_delete/<int:observacion_id>/',views.observaciones_delete, name='observaciones_delete'),
    path('volver_a_empate/',views.volver_a_empate, name='volver_a_empate'),
    # path('observacion_email/<int:id>/', views.observacion_email, name='observacion_email'),
    # path('borrar_items_observacion/',views.borrar_items_observacion, name='borrar_items_observacion'),
    
    
    #LEVANTAMIENTOS
    path('levantamiento/',views.formulario_levantamiento, name='levantamiento_insert'),
    path('levantamiento_update/<int:levantamiento_id>/',views.formulario_levantamiento, name='levantamiento_update'),
    path('levantamiento_delete/<int:levantamiento_id>', views.levantamiento_delete, name='levantamiento_delete'),
    path('levantamiento_list/', views.levantamiento_list, name='levantamiento_list'),

    #PRESTAMOS
    path('prestamo_index/',views.prestamo_index, name='prestamo_index'),
    path('prestamo/',views.prestamo_formulario, name='prestamo_insert'),
    path('prestamo_update/<int:prestamo_id>/',views.prestamo_formulario, name='prestamo_update'),
    path('prestamo_update_archivo/<int:prestamo_id>/',views.prestamo_formulario_archivo, name='prestamo_update_archivo'),
    path('prestamo_delete/<int:prestamo_id>/',views.prestamo_delete, name='prestamo_delete'),
    path('prestamo_delete_archivo/<int:prestamo_id>/',views.prestamo_delete_archivo, name='prestamo_delete_archivo'),
    path('prestamo_list/', views.prestamo_list, name='prestamo_list'),
    path('prestamo_list_archivo/',views.prestamo_list_archivo, name='prestamo_list_archivo'),

    #SOBRES
    path('sobre/',views.sobre_formulario, name='sobre_insert'),
    path('sobre_update/<int:id>/',views.sobre_formulario, name='sobre_update'),
    path('sobre_delete/<int:id>/',views.sobre_delete, name='sobre_delete'),
    path('sobre_list/', views.sobre_list, name='sobre_list'),

    #APERTURAS
    path('apertura/',views.apertura_formulario, name='apertura_insert'),
    path('apertura_update/<int:apertura_id>/',views.apertura_formulario, name='apertura_update'),
    path('apertura_delete/<int:apertura_id>/',views.apertura_delete, name='apertura_delete'),
    path('apertura_list/', views.apertura_list, name='apertura_list'),

    #POLIZAS
    path('poliza/',views.poliza_formulario, name='poliza_insert'),
    path('poliza_update/<int:poliza_id>/',views.poliza_formulario, name='poliza_update'),
    path('poliza_delete/<int:poliza_id>/',views.poliza_delete, name='poliza_delete'),
    path('poliza_list/', views.poliza_list, name='poliza_list'),

    #CORRESPONDENCIA
    path('correspondencia/',views.correspondencia_formulario_enviar, name='correspondencia_enviar'),
    path('correspondencia_enviar/<int:id>/',views.correspondencia_formulario_modificar, name='correspondencia_modificar'),
    path('correspondencia_recibir/<int:id>/',views.correspondencia_formulario_recibir, name='correspondencia_recibir'),
    path('correspondencia_delete/<int:id>/',views.correspondencia_delete, name='correspondencia_delete'),
    path('correspondencia_list/', views.correspondencia_list, name='correspondencia_list'),
    path('correspondencia_list_recibido/', views.correspondencia_list_recibido, name='correspondencia_list_recibido'),

    #CONFIGURACIONES
    path('configuraciones_index/', views.configuraciones_index, name='configuraciones_index'),
    path('configuraciones/',views.configuraciones_formulario, name='configuraciones_formulario'),

    path('tiempos_operaciones/',views.tiempos_operaciones, name='tiempos_operaciones'),
    path('tiempos_operaciones_update/',views.tiempos_operaciones_formulario, name='tiempos_operaciones_insert'),
    path('tiempos_operaciones_update/<int:id>/',views.tiempos_operaciones_formulario, name='tiempos_operaciones_update'),
    path('tiempos_operaciones_delete/<int:id>/',views.tiempos_operaciones_delete, name='tiempos_operaciones_delete'),

    #TAREAS
    path('tarea/',views.tarea_formulario, name='tarea_insert'),
    path('tarea_update/<int:tarea_id>/',views.tarea_formulario, name='tarea_update'),
    path('tarea_delete/<int:tarea_id>/',views.tarea_delete, name='tarea_delete'),
    path('tarea_list/', views.tarea_list, name='tarea_list'),

    #REPORTES
    path('reporte_empate/',views.reporte_empate, name='reporte_empate'),
    path('reporte_contratos/',views.reporte_contratos, name='reporte_contratos'),
    path('reporte_aperturas/',views.reporte_aperturas, name='reporte_aperturas'),
    path('reporte_polizas/',views.reporte_polizas, name='reporte_polizas'),
    path('reporte_documentos_sueltos/',views.reporte_documentos_sueltos, name='reporte_documentos_sueltos'),
    path('reporte_levantamientos/',views.reporte_levantamientos, name='reporte_levantamientos'),

    #AJAX
    path('tiempo_empate/<int:id>',views.tiempo_empate, name='tiempo_empate'),
    path('asignar_analista_automatico/',views.asignar_analista_automatico, name='asignar_analista_automatico'),
    path('cargar_sub_categoria/',views.cargar_sub_categoria, name='cargar_sub_categoria'),
    path('cargar_item_observacion/',views.cargar_item_observacion, name='cargar_item_observacion'),
    path('cantidad_contrato/',views.cantidad_contrato, name='cantidad_contrato'),


    # HISTORIAL
    path('historial/',views.historial, name='historial'),
    path('detalle_historial/<int:id>/',views.detalle_historial, name='detalle_historial'),

    # HOJA RESUMEN
    path('hoja_resumen/',views.hoja_resumen, name='hoja_resumen'),

    #PRUEBA
    path('prueba/',views.enviar_emails, name='enviar_emails'),
]