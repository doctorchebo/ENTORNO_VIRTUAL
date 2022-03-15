from django.core import management
from django.core.mail import EmailMessage, BadHeaderError
from celery import shared_task
from django.db.models import Min
from datetime import datetime, timedelta
from .models import *
from time import sleep
from celery.schedules import crontab

@shared_task
def esperar(duration):
    sleep(duration)
    return None

@shared_task()
def enviar_emails_task():
    dias = datetime.now()-timedelta(days=0)
    print(dias)
    observaciones = Observaciones.objects.select_related('empate__distribucion__desembolso').filter(fecha_observación__lte=dias, estado="Observado")
    print(list(observaciones))

    for observacion in observaciones:
        destino = observacion.destino
        glosa = observacion.glosa
        onbase = observacion.empate.distribucion.desembolso.onbase
        ejecutivo = observacion.empate.distribucion.desembolso.ejecutivo
        cliente = observacion.empate.distribucion.desembolso.cliente

        if destino == "Comercial":
            destinatario = ejecutivo
            recipient = "marcelo.munoz.coaquira@gmail.com"
        elif destino == "Políticas":
            destinatario = destino
            recipient = "politicas.bmsc@gmail.com"
        elif destino == "Liquidaciones":
            destinatario = destino
            recipient = "liquidaciones.bmsc@gmail.com"

        subject = f'Recortario Observación OB {onbase} - cliente {cliente}:'
        message = f'Estimado(a) {destinatario}: {chr(10)} La siguiente observación del onbase {onbase} sigue pendiente: {chr(10)} {glosa} {chr(10)} Favor regularizar a la brevedad posible y notificar la corrección mediante el sistema de custodia'
        enviado_por = "marcelo.munoz.coaquira@gmail.com"
        
        message = EmailMessage(subject,message,enviado_por,[recipient])
        # message.attach_file()
        message.send()
    return None

@shared_task()
def copiar_base_datos():
    management.call_command('dbbackup')
    
