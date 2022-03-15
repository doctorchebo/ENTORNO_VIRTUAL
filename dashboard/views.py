from django.shortcuts import render
from . import plotly_app
from custodia.models import *
from django.db.models import Count 
from .forms import *
from django.contrib.auth.models import Group

# DASHBOARD
def dashboard(request):
    if request.method == 'GET':
        form = DashboardForm()

        context = {
            'form':form,
        }
    else:
        form = DashboardForm(request.POST)

        if form.is_valid():
            estado = form.cleaned_data.get("estado", None)
            fecha_inicial = form.cleaned_data.get("fecha_inicial", None)
            fecha_final = form.cleaned_data.get("fecha_final", None)

            desembolsos_estado = Desembolsos.objects.filter(fecha_desembolso__gte=fecha_inicial,fecha_desembolso__lte=fecha_final, estado=estado).aggregate(estado_count=(Count('estado')))
            aperturas_estado = Apertura.objects.filter(fecha_creacion__gte=fecha_inicial,fecha_creacion__lte=fecha_final, estado=estado).aggregate(estado_count=(Count('estado')))
            polizas_estado = Poliza.objects.filter(fecha_creacion__gte=fecha_inicial,fecha_creacion__lte=fecha_final, estado=estado).aggregate(estado_count=(Count('estado')))
            documentos_sueltos_estado = DocumentosSueltos.objects.filter(fecha_creacion__gte=fecha_inicial,fecha_creacion__lte=fecha_final, estado=estado).aggregate(estado_count=(Count('estado')))
            levantamientos = Levantamientos.objects.count()
            
            empates_estado = Empate.objects.filter(fecha_modificacion__gte=fecha_inicial,fecha_modificacion__lte=fecha_final, estado=estado).aggregate(estado_count=(Count('estado')))

            correspondencia_estado = Correspondencia.objects.filter(fecha_envio__gte=fecha_inicial,fecha_envio__lte=fecha_final, estado=estado).aggregate(estado_count=(Count('estado')))
            
            context = {
                'form':form,
                'desembolsos_estado': desembolsos_estado,
                'empates_estado': empates_estado,
                'aperturas_estado':aperturas_estado,
                'polizas_estado':polizas_estado,
                'documentos_sueltos_estado':documentos_sueltos_estado,
                'levantamientos':levantamientos,
                # 'sobres':sobres,
                'correspondencia_estado':correspondencia_estado,
            }
    return render(request, "dashboard.html", context)


