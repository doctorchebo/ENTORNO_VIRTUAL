from django.db.models.signals import post_save, m2m_changed, pre_save, pre_delete, post_delete
from django.dispatch import receiver     
from django.contrib.auth.models import User
from .models import *
from import_export.signals import post_import, post_export

#USUARIO
@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, nombre='New User')

#CAJA PREDETERMINADA
@receiver(post_save, sender=User)
def post_save_create_parametros(sender, instance, created, **kwargs):
    if created:
        Parametro.objects.create(usuario=instance)

#CORRESPONDENCIA
# @receiver(post_save, sender=Correspondencia)
# def post_save_crear_correspondencia(sender, instance, created, **kwargs):
#     if created:
#         instance.estado == 'Enviado'
#         instance.save()

@receiver(m2m_changed, sender=Correspondencia.desembolso.through)
def m2m_changed_desembolsos_estado(sender, instance, action, **kwargs):
    if action =='post_add' or action =='pre_add' :
        for item in instance.desembolso.all():
            item.estado = 'Enviado'
            item.save()
    elif  action=='post_remove' or action =='pre_remove':
        for item in instance.desembolso.all():
            item.estado = 'Pendiente'
            item.save()

@receiver(m2m_changed, sender=Correspondencia.documento_suelto.through)
def m2m_changed_documento_suelto_estado(sender, instance, action, **kwargs):
    if action =='post_add' or action =='pre_add' :
        for item in instance.documento_suelto.all():
            item.estado = 'Enviado'
            item.save()
    elif  action=='post_remove' or action =='pre_remove':
        for item in instance.documento_suelto.all():
            item.estado = 'Pendiente'
            item.save()
            
@receiver(pre_save, sender=Correspondencia)
def pre_save_recibir_correspondencia(sender, instance, **kwargs):
    if instance.conformidad == True:
        for item in instance.desembolso.all():
            item.estado = 'Recibido'
            item.save()
        for item in instance.documento_suelto.all():
            item.estado = 'Recibido'
            item.save()
        instance.estado = 'Recibido'
    elif (instance.conformidad == False and instance.estado==None):
        for item in instance.desembolso.all():
            item.estado = 'Enviado'
            item.save()
        for item in instance.documento_suelto.all():
            item.estado = 'Enviado'
            item.save()
        instance.estado = 'Enviado'
        
@receiver(pre_delete, sender=Correspondencia)
def pre_delete_borrar_correspondencia(sender,instance,**kwargs):
    for item in instance.desembolso.all():
        item.estado = 'Pendiente'
        item.save()
    for item in instance.documento_suelto.all():
        item.estado = 'Pendiente'
        item.save()

# DESEMBOLSOS
@receiver(pre_save, sender=Desembolsos)
def pre_save_crear_desembolso(sender, instance, **kwargs):
    if instance.estado == None:
        instance.estado = "Pendiente"

#DISTRIBUCIÓN
@receiver(post_save, sender=Distribucion)
def post_save_distribucion(sender,instance,created,**kwargs):
    desembolso = instance.desembolso
    if created:
        desembolso.estado='Distribuido'
        desembolso.save()  
        empate = Empate.objects.create(distribucion_id=instance.id)
        empate.estado = 'Distribuido'
        empate.save()
       
@receiver(pre_delete, sender=Distribucion)
def pre_delete_delete_distribucion(sender,instance,**kwargs):
        desembolso = instance.desembolso
        desembolso.estado='Recibido'
        desembolso.save()

#EMPATE
@receiver(pre_save, sender=Empate)
def pre_save_editar_empate(sender,instance,**kwargs):
    desembolso = instance.distribucion.desembolso
    if instance.empatado == True:
        instance.estado = 'Empatado'
        desembolso.estado = 'Empatado'
    else:
        instance.estado = 'Pendiente'
        desembolso.estado = 'Distribuido'
    desembolso.save()
      

@receiver(post_delete, sender=Empate)
def post_delete_delete_empate(sender,instance,**kwargs):
        empate = instance.distribucion.desembolso
        empate.estado='Distribuido'
        empate.save()

#APERTURAS
@receiver(post_save, sender=Apertura)
def post_save_apertura(sender,instance,created,**kwargs):
    if created:
        instance.estado='Pendiente'
        instance.save()
#POLIZAS
@receiver(post_save, sender=Poliza)
def post_save_poliza(sender,instance,created,**kwargs):
    if created:
        instance.estado='Pendiente'
        instance.save()
#DOCUMENTOS SUELTOS
@receiver(post_save, sender=DocumentosSueltos)
def pre_save_crear_documento_suelto(sender, instance, **kwargs):
    if instance.estado == None:
        instance.estado = "Pendiente"

#CONTRATOS
@receiver(pre_save, sender=Contratos)
def pre_save_enviar_contrato(sender,instance,**kwargs):
        instance.estado='Enviado'

@receiver(pre_save, sender=Contratos)
def pre_save_recibir_contrato(sender,instance,**kwargs):
    if instance.conformidad == True:
        instance.estado='Recibido'

#PRESTAMOS
@receiver(post_save, sender=Prestamo)
def post_save_solicitar_prestamo(sender,instance,created,**kwargs):
    if created:
        instance.estado='Solicitado'
        instance.save()

# @receiver(pre_delete, sender=Prestamo)
# def pre_delete_eliminar_prestamo(sender,instance,**kwargs):
#         for item in instance.sobre.all():
#             item.estado = 'Archivado'
#             item.save()
               
@receiver(post_save, sender=Prestamo)
def post_save_cambiar_estado_sobres(sender, instance, **kwargs):
    if instance.estado == 'Prestado':
        for sobre in instance.sobre.all():
            sobre.estado = 'Prestado'
            sobre.save()
    elif instance.estado == 'Devuelto':
        for sobre in instance.sobre.all():
            sobre.estado = 'Archivado'
            sobre.save()
          
# TAREAS
@receiver(post_save, sender=Tarea)
def post_save_solicitar_prestamo(sender,instance,created,**kwargs):
    if created:
        instance.estado='Asignado'
        instance.save()
 

# @receiver(post_export, dispatch_uid='')
# def post_export(model, **kwargs):
#     # model is the actual model instance which after export
#     pass