import csv
import json
from warnings import filters
from auditlog.models import LogEntry
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Min
from django.core.paginator import Paginator
from django.db.models import Q, Max, Prefetch
from django.db import transaction
from django.db.transaction import atomic
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django_filters.rest_framework import DjangoFilterBackend
from django.core.mail import EmailMessage, BadHeaderError
from django.views.decorators.cache import cache_page
from itertools import chain
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.mixins import * 
from tablib import Dataset 
from .tasks import enviar_emails_task, esperar
import pandas as pd
from datetime import datetime, timedelta

from .decorators import allowed_users, unauthenticated_user
from .filters import *
from .forms import *
from .models import *
from .pagination import *
from .serializers import *
from .admin import *

import custodia

#FUNCIONES DE ACCESOS
def is_solicitante(user):
    return user.groups.filter(name__in=['CUSTODIA','JEFE OPERATIVO','EJECUTIVO']).exists()
def is_politicas(user):
    return user.groups.filter(name__in=['POLITICAS']).exists()
def is_liquidaciones(user):
    return user.groups.filter(name__in=['LIQUIDACIONES']).exists()
def is_comercial(user):
    return user.groups.filter(name__in=['EJECUTIVO', 'JEFE OPERATIVO']).exists()
def is_admin(user):
    return user.groups.filter(name='admin').exists()
def is_custodia(user):
    return user.groups.filter(name='CUSTODIA').exists()
def is_jefe_custodia(user):
    return user.groups.filter(name='JEFE_CUSTODIA').exists()
def is_custodio(user):
    return user.groups.filter(name='ARCHIVO').exists()
def is_legal(user):
    return user.groups.filter(name='LEGAL').exists()

class PerfilesViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = PerfilesSerializer

class EmpateViewSet(ModelViewSet):
    queryset = Empate.objects.all()
    filter_backends= [DjangoFilterBackend, SearchFilter]
    filterset_class = EmpateFilter
    search_fields = ['distribucion__desembolso__cliente','distribucion__desembolso__sucursal','distribucion__desembolso__agencia']
    serializer_class = EmpateSerializer

    def get_serializer_context(self):
        return {'request':self.request}
class DesembolsosViewSet(ModelViewSet):
    queryset = Desembolsos.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = DesembolsoFilter
    search_fields = ['cliente','sucursal','agencia']
    ordering_fields = ['fecha_desembolso']
    serializer_class = DesembolsosSerializer
    pagination_class = DefaultPagination

class ObservacionesViewSet(ModelViewSet):
    queryset = Observaciones.objects.all()
    serializer_class = ObservacionesSerializer

    def get_serializer_context(self):
        return {'empate_id':self.kwargs['empate_pk']}



#MODULOS
@login_required()
def empate_index(request):
    return render(request, "empate_index.html")
@login_required
def levantamiento_index(request):
    return render(request, "levantamiento_index.html")
@login_required
def servicios_index(request):
    return render(request, "servicios_index.html")
@login_required
def correspondencia_index(request):
    return render(request, "correspondencia_index.html")

    
#DESEMBOLSOS
@login_required()
# @transaction.atomic
def desembolso_list(request):
    if request.method =='GET':
        desembolso_list=Desembolsos.objects.all().order_by('-fecha_creacion')
        # p = Paginator(desembolso_list, 10)
        # page = request.GET.get('page')
        # desembolsos = p.get_page(page)
        filter = DesembolsoFilter(request.GET, queryset=desembolso_list)
        # desembolso_list=filter.qs
        desembolso_list = filter.qs
        return render(request,"desembolso_list.html",{'desembolso_list':desembolso_list, 'filter':filter})
    elif request.method=='POST':
        desembolso_resource = DesembolsosResource()  
        dataset = Dataset()  
        #print(dataset)  
        nuevos_desembosos = request.FILES['xlsxfile']  
        # print(nuevos_desembosos)  
        dataset.load(nuevos_desembosos)  
        # print(imported_data)  
        # result = desembolso_resource.import_data(dataset, dry_run=True) # Test the data import  
        # # print(result.has_errors())  
        # if not result.has_errors():  
        with transaction.atomic():
            try:
                desembolso_resource.import_data(dataset, dry_run=False) # Actually import now    
                messages.success(request, 'Se importó correctamente')
            except:
                messages.error(request, 'Ocurrió un error, favor intentar de nuevo')
    return redirect('/custodia/desembolso_list')    


@login_required()
def desembolso_formulario(request,desembolso_id=0):
    if request.method =='GET':
        if desembolso_id==0:
            form = DesembolsoCrearForm()
        else:
            desembolso = Desembolsos.objects.get(pk=desembolso_id)
            form = DesembolsoEditarForm(instance=desembolso)
        return render(request,"desembolso_form.html",{'form':form, 'desembolso_id':desembolso_id})
    else:
        if desembolso_id == 0:
            form = DesembolsoCrearForm(request.POST)
        else:
            desembolso = Desembolsos.objects.get(pk=desembolso_id)
            form = DesembolsoEditarForm(request.POST, instance = desembolso)
        if form.is_valid():
            messages.success(request, 'Se registró con éxito')
            obj = form.save(commit=False)
            if desembolso_id == 0:
                obj.usuario_creacion_id = request.user.id
            else:
                obj.usuario_modificacion_id = request.user.id
            obj.save()
        return redirect('/custodia/desembolso_list')

# DESESTIMADAS
def desestimada_formulario(request, id=0):
    if request.method =="GET":
        if id == 0:
            form = DesestimadaCrearForm()
        else:
            desestimada = Desembolsos.objects.get(pk=id)
            form = DesestimadaCrearForm(instance=desestimada)    
    else:
        if id == 0:
            form = DesestimadaCrearForm(request.POST)    
        else:
            desestimada =Desembolsos.objects.get(pk=id)
            form = DesestimadaCrearForm(request.POST, instance=desestimada)
        if form.is_valid():
            messages.success(request, 'Se registró la desestimada con éxito')
            obj = form.save(commit=False)
            if id == 0:
                obj.usuario_creacion_id = request.user.id
            else:
                obj.usuario_modificacion_id = request.user.id
            obj.save()
        else:
           messages.error(request, 'Ocurrió un error. Por favor intenta de nuevo') 
    return render(request, "desestimada_formulario.html", {'form':form})

@allowed_users(allowed_roles=['admin'])
@login_required()
def desembolso_delete(request,desembolso_id):
    try:
        desembolso = Desembolsos.objects.get(pk=desembolso_id)
        desembolso.delete()
        messages.success(request, 'El desembolso se eliminó con éxito')
    except:
        messages.error(request, 'Ocurrió un problema. Por favor vuelve a intentar')
    return redirect ('/custodia/desembolso_list')

#EMPATE
@login_required
def empate_form(request, id=0, id_2=0):
    if request.method =='GET':
        caja = Parametro.objects.get(usuario_id=request.user.id)
        caja_form = ParametroForm(instance=caja)
        empate = Empate.objects.get(pk=id)
        desembolso = Desembolsos.objects.get(pk=id_2)
        empate_form = EmpateForm(instance=empate)
        desembolso_form = DesembolsoEditarForm(instance=desembolso)
        return render(request,"empate_form.html",{'form':empate_form, 'desembolso_form':desembolso_form, 'caja_form':caja_form})
    elif request.method =='POST':
        desembolso = Desembolsos.objects.get(pk=id_2)
        empate = Empate.objects.get(pk=id)
        form = EmpateForm(request.POST, instance = empate)
        desembolso_form = DesembolsoEditarForm(request.POST, instance = desembolso)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.usuario_empate_id = request.user.id
        obj.save()
    if desembolso_form.is_valid():
        messages.success(request, 'Se empató con éxito')
        obj = desembolso_form.save(commit=False)
        obj.save(update_fields=["fecha_desembolso","producto","tipo","codigo_cliente","cliente","operacion","monto","desembolso_parcial","ejecutivo","onbase","sucursal","agencia","tipo_banca","tipo_trabajo","instancia_aprobacion"])
    else:
        messages.error(request, 'Ocurrió un error. Intenta de nuevo')
    return redirect('/custodia/empate_list')
 
@login_required   
def tiempo_empate(request, id=0):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        empate = Empate.objects.get(pk=id)
        tiempo = request.POST.get('tiempo')
        empate.tiempo_empate = int(tiempo)/1000
        empate.save()
        return JsonResponse({'msg':'éxito'})
        
@login_required
def empate_list(request):
    if is_jefe_custodia(request.user) or is_admin(request.user):
        empate_list = Empate.objects.all().select_related('distribucion__desembolso').order_by('-fecha_modificacion')
    else:
        empate_list = Empate.objects.filter(distribucion__analista_asignado__id=request.user.id).select_related('distribucion__desembolso').order_by('-fecha_modificacion')
    filter =EmpateFilter(request.GET, queryset=empate_list)
    empate_list = filter.qs
    return render (request,"empate_list.html", {'empate_list':empate_list, 'filter':filter})

@allowed_users(allowed_roles=['admin'])
@login_required
def empate_delete(request,id):
    empate = Empate.objects.get(pk=id)
    try:
        empate.delete()
        messages.success(request, 'Se eliminó el empate con éxito')
    except:
        messages.error(request, 'No se puede borrar porque hay observaciones dependientes de este empate')
    return redirect('/custodia/empate_list')

#LEVANTAMIENTOS
@allowed_users(allowed_roles=['LEVANTAMIENTOS','admin'])
@login_required
def formulario_levantamiento(request, levantamiento_id=0):
    if request.method =='GET':
        if levantamiento_id==0:
            form = LevantamientosCrearForm()
        else:
            levantamiento = Levantamientos.objects.get(pk=levantamiento_id)
            form = LevantamientosEditarForm(instance=levantamiento)
        return render(request,"levantamiento_form.html",{'form':form, 'levantamiento_id':levantamiento_id})
    else:
        if levantamiento_id == 0:
            form = LevantamientosCrearForm(request.POST)
        else:
            levantamiento = Levantamientos.objects.get(pk=levantamiento_id)
            form = LevantamientosEditarForm(request.POST, instance = levantamiento)
        if form.is_valid():
            messages.success(request, 'Se registró el levantamiento con éxito')
            obj = form.save(commit=False)
            if levantamiento_id == 0:
                obj.usuario_creacion_id = request.user.id
            else:
                obj.usuario_modificacion_id = request.user.id
            obj.save()
        return redirect('/custodia/levantamiento_list')

@login_required
def levantamiento_list(request):
    levantamiento_list = Levantamientos.objects.all().order_by('-fecha_creacion')
    filter = LevantamientoFilter(request.GET, queryset=levantamiento_list)
    levantamiento_list=filter.qs
    return render(request,"levantamiento_list.html", {'levantamiento_list':levantamiento_list, 'filter':filter})

@allowed_users(allowed_roles=['admin'])
@login_required
def levantamiento_delete(request,levantamiento_id):
    try:
        levantamiento = Levantamientos.objects.get(pk=levantamiento_id)
        levantamiento.delete()
        messages.success(request, 'Se eliminó el levantamiento con éxito')
    except:
        messages.error(request, 'Ocurrió un problema. Por favor vuelve a intentar')
    return redirect('/custodia/levantamiento_list')

#APERTURAS
@login_required
def apertura_list(request):
    if request.method == 'GET':  
        apertura_list = Apertura.objects.all().order_by('-fecha_creacion')
        filter = AperturaFilter(request.GET, queryset=apertura_list)
        apertura_list = filter.qs
        return render(request,"apertura_list.html",{'apertura_list':apertura_list,'filter':filter })    
    #template = loader.get_template('export/importar.html')  
    elif request.method == 'POST':  
        apertura_resource = AperturaResource()  
        dataset = Dataset()  
        #print(dataset)  
        nuevas_aperturas = request.FILES['xlsxfile']  
        # print(nuevas_aperturas)  
        imported_data = dataset.load(nuevas_aperturas.read())  
        print(imported_data)  
        result = apertura_resource.import_data(dataset, dry_run=True) # Test the data import  
        print(result.has_errors())  
        if not result.has_errors():  
            apertura_resource.import_data(dataset, dry_run=False) # Actually import now    
            messages.success(request, 'Se importó correctamente')
    return redirect('/custodia/apertura_list')
    

@allowed_users(allowed_roles=['admin'])
@login_required
def apertura_delete(request,apertura_id):
    apertura = Apertura.objects.get(pk=apertura_id)
    apertura.delete()
    messages.success(request, 'Apertura eliminada exitosamente')
    return redirect('/custodia/apertura_list')

@allowed_users(allowed_roles=['SERVICIOS', 'admin'])
@login_required
def apertura_formulario(request, apertura_id=0):
    request.session['login_from'] = request.META.get('HTTP_REFERER', '/')
    if request.method =='GET':
        caja = Parametro.objects.get(usuario_id=request.user.id)
        caja_form = ParametroForm(instance=caja)
        if apertura_id==0:
            apertura_form = AperturaCrearForm()
        else:
            apertura = Apertura.objects.get(pk=apertura_id)
            apertura_form = AperturaEditarForm(instance=apertura)
        return render(request,"apertura_formulario.html",{'form':apertura_form, 'apertura_id':apertura_id,'caja_form':caja_form})
    else:
        if apertura_id ==0:
            form = AperturaCrearForm(request.POST)
        else:
            apertura = Apertura.objects.get(pk=apertura_id)
            form = AperturaEditarForm(request.POST, instance = apertura)
        if form.is_valid():
            messages.success(request, 'Apertura registrada exitosamente')
            obj = form.save(commit=False)
            if apertura_id ==0:
                obj.usuario_creacion_id = request.user.id
            else:   
                obj.usuario_modificacion_id = request.user.id
            obj.save()
            return redirect('/custodia/apertura_list')
        else:
            # messages.error(request, 'Ocurrió un problema. Por favor vuelve a intentar')
            return HttpResponseRedirect(request.path_info)
#POLIZAS
@login_required
def poliza_list(request):
    if request.method == 'GET':  
        poliza_list = Poliza.objects.all().order_by('-fecha_creacion')
        filter = PolizaFilter(request.GET, queryset=poliza_list)
        poliza_list = filter.qs
        return render(request,"poliza_list.html",{'poliza_list':poliza_list,'filter':filter })    
    #template = loader.get_template('export/importar.html')  
    elif request.method == 'POST':  
        poliza_resource = PolizaResource()  
        dataset = Dataset()  
        #print(dataset)  
        nuevas_polizas = request.FILES['xlsxfile']  
        # print(nuevas_aperturas)  
        imported_data = dataset.load(nuevas_polizas.read())  
        print(imported_data)  
        result = poliza_resource.import_data(dataset, dry_run=True) # Test the data import  
        print(result.has_errors())  
        if not result.has_errors():  
            poliza_resource.import_data(dataset, dry_run=False) # Actually import now    
            messages.success(request, 'Se importó correctamente')
    return redirect('/custodia/poliza_list')    
    
@allowed_users(allowed_roles=['admin'])
@login_required
def poliza_delete(request,poliza_id):
    poliza = Poliza.objects.get(pk=poliza_id)
    poliza.delete()
    messages.success(request, 'Se eliminó la póliza con éxito')
    return redirect('/custodia/poliza_list')

# @allowed_users(allowed_roles=['POLIZAS','admin'])
@login_required
def poliza_formulario(request, poliza_id=0):
    if request.method =='GET':
        caja = Parametro.objects.get(usuario_id=request.user.id)
        caja_form = ParametroForm(instance=caja)
        if poliza_id==0:
            form = PolizaCrearForm()
        else:
            poliza = Poliza.objects.get(pk=poliza_id)
            form = PolizaEditarForm(instance=poliza)
        return render(request,"poliza_formulario.html",{'form':form,'poliza_id':poliza_id,'caja_form':caja_form})
    else:
        if poliza_id ==0:
            form = PolizaCrearForm(request.POST)
        else:
            poliza = Poliza.objects.get(pk=poliza_id)
            form = PolizaEditarForm(request.POST, instance = poliza)
        if form.is_valid():
            messages.success(request, 'Se registró la póliza con éxito')
            obj = form.save(commit=False)
            if poliza_id == 0:
                obj.usuario_creacion_id = request.user.id 
            else:   
                obj.usuario_modificacion_id = request.user.id
            obj.save()
        else:
            messages.error(request, 'Ocurrió un error. Por favor intenta de nuevo')
        return redirect('/custodia/poliza_list')

#CORRESPONDENCIA
@login_required
def correspondencia_list(request):
    correspondencia_list = Correspondencia.objects.all().order_by('-fecha_envio')
    filter = CorrespondenciaFilter(request.GET, queryset=correspondencia_list)
    correspondencia_list=filter.qs
    return render(request,"correspondencia_list.html",{'correspondencia_list':correspondencia_list,'filter':filter})
@login_required
def correspondencia_list_recibido(request):
    correspondencia_list = Correspondencia.objects.all().order_by('-fecha_envio')
    filter = CorrespondenciaFilter(request.GET, queryset=correspondencia_list)
    correspondencia_list=filter.qs
    return render(request,"correspondencia_list_recibido.html",{'correspondencia_list':correspondencia_list,'filter':filter})

@allowed_users(allowed_roles=['admin'])
@login_required
def correspondencia_delete(request,id):
    try:
        correspondencia = Correspondencia.objects.get(pk=id)
        correspondencia.delete()
        messages.success(request, 'Se eliminó exitosamente')
    except:
        messages.error(request, 'Ocurrió un error. Por favor intenta de nuevo')
    return redirect('/custodia/correspondencia_list')

@allowed_users(allowed_roles=['JEFE_OPERATIVO','admin'])
@login_required
def correspondencia_formulario_enviar(request, id=0):
    if request.method =='GET':
        if id==0:
            correspondencia_form = CorrespondenciaEnviarForm()
        else:
            correspondencia = Correspondencia.objects.get(pk=id)
            correspondencia_form = CorrespondenciaModificarForm(instance=correspondencia)
        return render(request,"correspondencia_formulario_enviar.html",{'form':correspondencia_form})
    else:
        if id ==0:
            form = CorrespondenciaEnviarForm(request.POST)
        else:
            correspondencia = Correspondencia.objects.get(pk=id)
            form = CorrespondenciaModificarForm(request.POST, instance = correspondencia)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.usuario_registro_id = request.user.id
            if id == 0:
                obj.estado = "Enviado"
            obj.save()
            form.save_m2m()
            messages.success(request, 'Se registró exitosamente')
        else:
            messages.error(request, 'Ocurrió un error. Por favor intenta de nuevo')
        return redirect('/custodia/correspondencia_list')

# @allowed_users(allowed_roles=['DISTRIBUCION','SERVICIOS', 'admin'])
@login_required
def correspondencia_formulario_recibir(request, id=0):
    if request.method =='GET':
        if id==0:
            correspondencia_form = CorrespondenciaRecibirForm()
        else:
            correspondencia = Correspondencia.objects.get(pk=id)
            correspondencia_form = CorrespondenciaRecibirForm(instance=correspondencia)
        return render(request,"correspondencia_formulario_recibir.html",{'form':correspondencia_form})
    else:
        if id ==0:
            form = CorrespondenciaRecibirForm(request.POST)
        else:
            correspondencia = Correspondencia.objects.get(pk=id)
            form = CorrespondenciaRecibirForm(request.POST, instance = correspondencia)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.usuario_registro_id = request.user.id
            obj.save()
            form.save_m2m()
            messages.success(request, 'Se registró exitosamente')
        else:
            messages.error(request, 'Ocurrió un error. Por favor intenta de nuevo')
        return redirect('/custodia/correspondencia_list_recibido')

# @allowed_users(allowed_roles=['DISTRIBUCION','SERVICIOS', 'admin'])
@login_required
def correspondencia_formulario_modificar(request, id=0):
    if request.method =='GET':
        if id==0:
            correspondencia_form = CorrespondenciaModificarForm()
        else:
            correspondencia = Correspondencia.objects.get(pk=id)
            correspondencia_form = CorrespondenciaModificarForm(instance=correspondencia)
        return render(request,"correspondencia_formulario_enviar.html",{'form':correspondencia_form})
    else:
        if id ==0:
            form = CorrespondenciaModificarForm(request.POST)
        else:
            correspondencia = Correspondencia.objects.get(pk=id)
            form = CorrespondenciaModificarForm(request.POST, instance = correspondencia)
        if form.is_valid():
            messages.success(request, 'Se registró exitosamente')
            obj = form.save(commit=False)
            obj.usuario_registro_id = request.user.id
            obj.save()
            form.save_m2m()
        else:
            messages.error(request, 'Ocurrió un error. Por favor intenta de nuevo')
        return redirect('/custodia/correspondencia_list')

#PRESTAMOS
@login_required
def prestamo_index(request):
    return render(request, "prestamo_index.html")

@login_required
def prestamo_list(request):
    prestamo_list = Prestamo.objects.filter(usuario_solicitante__id=request.user.id).order_by('-fecha_creacion')
    filter = PrestamoFilter(request.GET, queryset=prestamo_list)
    prestamo_list=filter.qs
    return render(request,"prestamo_list.html",{'prestamo_list':prestamo_list, 'filter':filter})
@allowed_users(allowed_roles=['ARCHIVO','admin'])
@login_required
def prestamo_list_archivo(request):
    prestamo_list = Prestamo.objects.all().order_by('-fecha_creacion')
    filter = PrestamoFilter(request.GET, queryset=prestamo_list)
    prestamo_list=filter.qs
    return render(request,"prestamo_list_archivo.html",{'prestamo_list':prestamo_list, 'filter':filter})

@allowed_users(allowed_roles=['admin'])
@login_required
def prestamo_delete(request,prestamo_id):
    try:
        prestamo = Prestamo.objects.get(pk=prestamo_id)
        prestamo.delete()
        messages.success(request, 'Se eliminó el préstamo con éxito')
    except:
        messages.error(request, 'Ocurrió un problema. Por favor vuelve a intentar')
    return redirect('/custodia/prestamo_list')

@allowed_users(allowed_roles=['admin'])
@login_required
def prestamo_delete_archivo(request,prestamo_id):
    try:
        prestamo = Prestamo.objects.get(pk=prestamo_id)
        prestamo.delete()
        messages.success(request, 'Se eliminó el préstamo con éxito')
    except:
        messages.error(request, 'Ocurrió un problema. Por favor vuelve a intentar')
    return redirect('/custodia/prestamo_list_archivo')

@login_required
def prestamo_formulario(request, prestamo_id=0):
    if request.method =='GET':
        if prestamo_id==0:
            form = PrestamoCrearForm()
        else:
            prestamo = Prestamo.objects.get(pk=prestamo_id)
            form = PrestamoEditarForm(instance=prestamo)
        return render(request,"prestamo_formulario.html",{'form':form, 'prestamo_id':prestamo_id})
    else:
        if prestamo_id ==0:
            form = PrestamoCrearForm(request.POST)
        else:
            prestamo = Prestamo.objects.get(pk=prestamo_id)
            form = PrestamoEditarForm(request.POST, instance = prestamo)
        if form.is_valid():
            messages.success(request, 'Se registró el préstamo exitosamente')
            obj = form.save(commit=False)
            obj.usuario_solicitante_id = request.user.id
            obj.save()
            form.save_m2m()
        else: 
            messages.error(request, 'Ocurrió un error. Por favor intenta de nuevo') 
        return redirect('/custodia/prestamo_list')

@login_required
def prestamo_formulario_archivo(request, prestamo_id=0):
    if request.method =='GET':
        prestamo = Prestamo.objects.get(pk=prestamo_id)
        form = PrestamoArchivoForm(instance=prestamo)
        return render(request,"prestamo_formulario.html",{'form':form, 'prestamo_id':prestamo_id})
    else:
        prestamo = Prestamo.objects.get(pk=prestamo_id)
        form = PrestamoArchivoForm(request.POST, instance = prestamo)
        if form.is_valid():
            messages.success(request, 'Se cambió el estado del préstamo exitosamente')
            obj = form.save(commit=False)
            obj.usuario_custodio_id = request.user.id
            obj.save()
        else: 
            messages.error(request, 'Ocurrió un error. Por favor intenta de nuevo') 
        return redirect('/custodia/prestamo_list_archivo')

#SOBRES
@login_required
def sobre_list(request):
    if request.method=='GET':
        sobre_list = Sobre.objects.all().order_by('-fecha_creacion')
        filter = SobreFilter(request.GET, queryset=sobre_list)
        sobre_list=filter.qs
        return render(request,"sobre_list.html",{'sobre_list':sobre_list,'filter':filter})
    elif request.method=='POST':
        sobre_resource = SobreResource()  
        dataset = Dataset() 
        nuevos_sobres = request.FILES['xlsxfile']  
        imported_data = dataset.load(nuevos_sobres.read())  
        result = sobre_resource.import_data(dataset, dry_run=True) # Test the data import   
        if not result.has_errors():  
            sobre_resource.import_data(dataset, dry_run=False) # Actually import now    
            messages.success(request, 'Se importó correctamente')
            return redirect('/custodia/sobre_list')

@allowed_users(allowed_roles=['admin'])
@login_required
def sobre_delete(request,id):
    try:
        sobre = Sobre.objects.get(pk=id)
        sobre.delete()
        messages.success(request, 'Se eliminó el sobre exitosamente')
    except:
        messages.error(request, 'Ocurrió un problema. Por favor volver a intentar')
    return redirect('/custodia/sobre_list')

# @allowed_users(allowed_roles=['LEVANTAMIENTOS', 'admin'])
@login_required
def sobre_formulario(request, id=0):
    if request.method =='GET':
        if id==0:
            sobre_form = SobreCrearForm()
        else:
            sobre = Sobre.objects.get(pk=id)
            sobre_form = SobreEditarForm(instance=sobre)
        return render(request,"sobre_formulario.html",{'form':sobre_form})
    else:
        if id ==0:
            form = SobreCrearForm(request.POST)
        else:
            sobre = Sobre.objects.get(pk=id)
            form = SobreEditarForm(request.POST, instance = sobre)
        if form.is_valid():
            messages.success(request, 'Se registró el sobre exitosamente')
            obj = form.save(commit=False)
            if id == 0:
                obj.usuario_creacion_id = request.user.id  
            else:  
                obj.usuario_modificacion_id = request.user.id
            obj.save()
            form.save_m2m()
        else:
            messages.error(request,'Ocurrió un error. Por favor intenta de nuevo')
        return redirect('/custodia/sobre_list')

#TAREAS
@login_required
def tarea_list(request):
    añade_tarea = is_jefe_custodia(request.user) or is_admin(request.user)
    if  is_admin(request.user) or is_jefe_custodia(request.user):
        tarea_list = Tarea.objects.all().order_by('-fecha_creacion')
    else:
        tarea_list = Tarea.objects.filter(analista_asignado_id = request.user.id).order_by('-fecha_creacion')
    filter = TareaFilter(request.GET, queryset=tarea_list)
    tarea_list=filter.qs
    return render(request,"tarea_list.html",{'tarea_list':tarea_list,'filter':filter, 'añade_tarea':añade_tarea})

@allowed_users(allowed_roles=['admin'])
@login_required
def tarea_delete(request,tarea_id):
    try:
        tarea = Tarea.objects.get(pk=tarea_id)
        tarea.delete()
        messages.success(request, 'Se eliminó la tarea exitosamente')
    except:
        messages.error(request, 'Ocurrió un problema. Por favor volver a intentar')
    return redirect('/custodia/tarea_list')

# @allowed_users(allowed_roles=['JEFE_CUSTODIA', 'admin'])
@login_required
def tarea_formulario(request, tarea_id=0):
    if request.method =='GET':
        if tarea_id==0:
            tarea_form = TareaCrearForm()
        else:
            tarea = Tarea.objects.get(pk=tarea_id)
            tarea_form = TareaEditarForm(instance=tarea)
        return render(request,"tarea_form.html",{'form':tarea_form, 'tarea_id':tarea_id})
    else:
        if tarea_id ==0:
            form = TareaCrearForm(request.POST)
        else:
            tarea = Tarea.objects.get(pk=tarea_id)
            form = TareaEditarForm(request.POST, instance = tarea)
        if form.is_valid():
            messages.success(request, 'Se creó la tarea exitosamente')
            obj = form.save(commit=False)
            if tarea_id == 0:
                obj.usuario_creacion_id = request.user.id
            else:
                obj.usuario_modificacion_id = request.user.id
            obj.save()
            form.save_m2m()
        else:
            messages.error(request,'Ocurrió un error. Por favor intenta de nuevo')
        return redirect('/custodia/tarea_list')

#CONSULTAS
@login_required
def consultas_index(request):
    return render(request, "consultas_index.html")
#CAJAS ARDISA APERTURAS
@login_required
def cajas(request):
    if request.method=='GET':
        form = BuscarCajaForm()
        listado=''
        filter=''  
    else:
        form = BuscarCajaForm(request.POST)
        if form.is_valid():
            tipo = request.POST['tipo']
            caja = request.POST['caja']
            modelo = getattr(custodia.models, tipo)
            listado = modelo.objects.filter(numero_caja__icontains=caja).order_by('fecha_modificacion')
            filter = CajaFilter(request.GET, queryset=listado)
            listado = filter.qs
    return render(request,"cajas.html",{'listado':listado,'form':form, 'filter':filter})
@login_required        
def cajas_list(request, base, caja):
    form = BuscarCajaForm(request.GET)
    if form.is_valid():
        model = getattr(custodia.models, base)
        listado = model.objects.filter(numero_caja__icontains=caja)
        filter = CajaFilter(request.GET, queryset=listado)
        listado = filter.qs
        return render(request,"cajas.html",{'listado':listado, 'filter':filter})
   
@login_required
def listado_ardisa(request,id):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=listado_ardisa.csv'
    
    #Create CSV writer
    writer = csv.writer(response)
    
    #Designate the model
    caja = Empate.objects.filter(numero_caja=id).order_by('fecha_empate')

    #Add column headings
    writer.writerow(['FISA','Cliente','Onbase','Operacion','Caja'])
    
    #Loop thu and output
    for i in caja:
        writer.writerow([
            i.codigo_cliente,
            i.cliente,
            i.onbase,
            i.operacion,
            i.numero_caja])
    return response
#OBSERVACIONES
@allowed_users(allowed_roles=['EMPATE','POLITICAS','EJECUTIVO', 'FEJE_OPERATIVO', 'admin'])
@login_required
def formulario_observaciones(request, id, desembolso_id):
    if request.method =='GET':  
        form = ObservacionesCrearForm()
        return render(request,"observaciones_form_crear.html",{'form':form})
    else:
        form = ObservacionesCrearForm(request.POST)
        if form.is_valid():
            destino = form.cleaned_data['destino']
            
            # ENVIAR EMAIL
            email = Parametro.objects.get(usuario_id=request.user.id)
            
            desembolso = Desembolsos.objects.get(pk=desembolso_id)
            ejecutivo = desembolso.ejecutivo
            onbase = desembolso.onbase
            cliente = desembolso.cliente

            if destino == "Comercial":
                destinatario = ejecutivo
                recipient = "marcelo.munoz.coaquira@gmail.com"
            elif destino == "Políticas":
                destinatario = destino
                recipient = email.email_politicas
            elif destino == "Liquidaciones":
                destinatario = destino
                recipient = email.email_liquidaciones

            glosa = request.POST.get('glosa')

            subject = f'Observación OB {onbase} - cliente {cliente}:'
            message = f'Estimado(a) {destinatario}: {chr(10)} Se encontraron las siguientes observaciones en el onbase {onbase}: {chr(10)} {glosa} {chr(10)} Favor regularizar a la brevedad posible y notificar la corrección mediante el sistema de custodia'
            enviado_por = request.user.email
                
            try:
                message = EmailMessage(subject,message,enviado_por,[recipient], [email.email_jefe_custodia])
                # message.attach_file()
                message.send()
            except BadHeaderError: 
                print("error")
    if form.is_valid():
        obs = form.save(commit=False)
        obs.empate_id=id
        obs.glosa = glosa.upper()
        if is_custodia(request.user):
            obs.usuario_observacion_id=request.user.id
        else:
            obs.usuario_revision_id=request.user.id
        obs.save()
    messages.success(request, f'Se añadió la observación con éxito y se envió email a {destinatario}')
    return redirect(request.path)


@allowed_users(allowed_roles=['EMPATE','POLITICAS','EJECUTIVO', 'FEJE_OPERATIVO', 'admin'])
@login_required
def observaciones_update(request, id):
    if request.method =='GET':   
        observacion = Observaciones.objects.get(pk=id)
        form = ObservacionesEditarForm(instance=observacion)
        
        return render(request,"observaciones_form_revisar.html",{'form':form})
    else:
        observacion = Observaciones.objects.get(pk=id)
        form = ObservacionesEditarForm(request.POST, instance = observacion)
    if form.is_valid():
        obs = form.save(commit=False)
        if is_custodia(request.user):
            obs.usuario_observacion_id=request.user.id
        else:
            obs.usuario_revision_id=request.user.id
        obs.save()
        messages.success(request, 'Se añadió con éxito')
        return redirect('/custodia/observacion_list')

@login_required
def observacion_list(request):
    if is_custodia(request.user):
        observacion_list = Observaciones.objects.filter(usuario_observacion_id=request.user.id).order_by('-fecha_observación')
    elif is_politicas(request.user):
        observacion_list = Observaciones.objects.filter(destino = "Políticas").order_by('-fecha_observación')
    elif is_liquidaciones(request.user):
        observacion_list = Observaciones.objects.filter(destino = "Liquidaciones").order_by('-fecha_observación')
    elif is_comercial(request.user):
        observacion_list = Observaciones.objects.filter(destino = "Comercial").order_by('-fecha_observación')
    else:
        observacion_list = Observaciones.objects.all().order_by('-fecha_observación')
    filter = ObservacionFilter(request.GET, queryset=observacion_list)
    observacion_list=filter.qs
    return render(request,"observacion_list.html", {'observacion_list':observacion_list, 'filter':filter})   

@allowed_users(allowed_roles=['admin'])
@login_required
def observaciones_delete(request,observacion_id):
    observacion = Observaciones.objects.get(pk=observacion_id)
    observacion.delete()
    messages.success(request, 'Se eliminó la observación con éxito')
    return redirect('/custodia/observacion_list')

@login_required
def cargar_sub_categoria(request):
    categoria_id = request.GET.get('categoria')
    sub_categorias = SubCategoriaObservacion.objects.filter(categoria_id=categoria_id).order_by('nombre')
    return render(request, "sub_categoria_opciones.html",{'sub_categorias':sub_categorias})

@login_required
def cargar_item_observacion(request):
    sub_categoria_id = request.GET.get('sub_categoria')
    items_observacion = ItemObservacion.objects.filter(sub_categoria_id=sub_categoria_id).order_by('nombre')
    return render(request, "item_observacion_opciones.html",{'items_observacion':items_observacion})
# def borrar_items_observacion(request):
#     return render(request, "borrar_items_observacion.html")

@login_required
def volver_a_empate(request):
    request.session['login_from'] = request.META.get('HTTP_REFERER', '/')
    return HttpResponseRedirect(request.path_info)
#DISTRIBUCION

# @allowed_users(allowed_roles=['EMPATE','admin'])
@login_required        
def distribucion_list(request):
    if request.method == 'GET':
        distribucion_list = Distribucion.objects.all().order_by('-fecha_creacion')
        filter = DistribucionFilter(request.GET, queryset=distribucion_list)
        distribucion_list = filter.qs
        return render(request,"distribucion_list.html",{'distribucion_list':distribucion_list, 'filter':filter})
    elif request.method == 'POST':
        distribucion_resource = DistribucionResource()  
        dataset = Dataset()  
        #print(dataset)  
        nuevas_distribuciones = request.FILES['xlsxfile']  
        # print(nuevas_aperturas)  
        imported_data = dataset.load(nuevas_distribuciones.read()) 
        print(imported_data)  
        result = distribucion_resource.import_data(dataset, dry_run=True) # Test the data import  
        print(result.has_errors())  
        if not result.has_errors():  
            distribucion_resource.import_data(dataset, dry_run=False) # Actually import now    
            messages.success(request, 'Se importó correctamente')
    return redirect('/custodia/distribucion_list')    

@allowed_users(allowed_roles=['EMPATE','admin'])
@login_required
def distribucion_formulario(request,distribucion_id=0):
    if request.method =='GET':
        if distribucion_id==0:
            empatadores = Tarea.objects.filter(nombre="Empate", estado="Asignado")
            form = DistribucionCrearForm()  
        else:
            empatadores = Tarea.objects.filter(nombre="Empate", estado="Asignado")
            distribucion = Distribucion.objects.get(pk=distribucion_id)
            form = DistribucionEditarForm(instance=distribucion)
        return render(request,"distribucion_formulario.html",{'form':form,'distribucion_id':distribucion_id, 'empatadores':empatadores})
    else:
        if distribucion_id ==0:
            form = DistribucionCrearForm(request.POST)
        else:
            distribucion = Distribucion.objects.get(pk=distribucion_id)
            form = DistribucionEditarForm(request.POST, instance = distribucion)
        if form.is_valid():
            nombre = form.cleaned_data['analista_asignado']
            tipo = form.cleaned_data['tipo']
            analista = Tarea.objects.get(analista_asignado__nombre=nombre, estado="Asignado")
            
            tipo_operacion = TipoOperacion.objects.get(nombre=tipo)

            id = analista.analista_asignado_id
            tiempo_total = analista.tiempo
            print(nombre, " ",  tipo_operacion, id, tiempo_total)

            analista.tiempo -= tipo_operacion.tiempo
            analista.save()

            obj = form.save(commit=False)
            if distribucion_id==0:
                obj.usuario_creacion_id = request.user.id
            else:
                obj.usuario_modificacion_id = request.user.id
            messages.success(request, f'Se distribuyó con éxito a {nombre}')
            obj.save()
        return redirect(request.path)    

def asignar_analista_automatico(request):
    tipo = request.GET.get('tipo')
    print('el tipo es ', tipo)
    empatadores = Tarea.objects.filter(nombre="Empate", estado = "Asignado")
    # tipo_operacion = TipoOperacion.objects.get(pk=tipo)
    # print(empatadores, tipo)
   
    empatador_con_mas_tiempo = Tarea.objects.filter(nombre="Empate", estado = "Asignado").order_by('-tiempo').first()
    print('el que tiene mas tiempo es ', empatador_con_mas_tiempo.analista_asignado)
    
    nombre = empatador_con_mas_tiempo.analista_asignado
    print('el nombre es ' , nombre)
    print(type(nombre))

    usuario = Profile.objects.get(nombre=empatador_con_mas_tiempo.analista_asignado)
    id = int(usuario.pk)

    print('su codigo de usuario es ', id)
    return JsonResponse({'id':id})
    
@allowed_users(allowed_roles=['admin'])
@login_required
def distribucion_delete(request, distribucion_id):
    
    distribucion = Distribucion.objects.get(pk=distribucion_id)
    analista = distribucion.analista_asignado
    tipo = distribucion.tipo

    tarea = Tarea.objects.get(analista_asignado=analista, estado="Asignado", nombre="Empate")
    tipo_operacion = TipoOperacion.objects.get(nombre=tipo)
    
    tarea.tiempo += tipo_operacion.tiempo
    tarea.save()
    print(analista, tipo, tarea.tiempo, tipo_operacion.tiempo)

    distribucion.delete()
    messages.success(request, 'Se eliminó la distribución con éxito')
           
        # messages.error(request, 'No se puede borrar porque hay empates y observaciones dependientes de esta distribución')
    return redirect('/custodia/distribucion_list')

#CONTRATOS
@allowed_users(allowed_roles=['EMPATE','admin'])
@login_required
def formulario_contratos_empate(request, desembolso_id=0, contrato_id=0):
    next_url = request.GET.get('next')
    if request.method =='GET':
        if contrato_id ==0:
            # Crear contrato (no hay instancia de contrato)
            form = ContratosEmpateForm(initial={'desembolso':desembolso_id})
        else:
            # Editar Contrato (hay instancia de contrato)
            contrato = Contratos.objects.get(pk=contrato_id)
            desembolso_id = contrato.desembolso_id
            form = ContratosEmpateEditarForm(instance = contrato)
        return render(request,"contrato_form_empate.html",{'form':form,'desembolso_id':desembolso_id, 'contrato_id':contrato_id} )
    else:
        if contrato_id==0:
            form = ContratosEmpateForm(request.POST)
        else:
            contrato = Contratos.objects.get(pk=contrato_id)
            form = ContratosEmpateEditarForm(request.POST, instance = contrato)
        if form.is_valid():
            messages.success(request, 'El contrato se registró con éxito')
            obj= form.save(commit=False)
            if contrato_id == 0:
                obj.usuario_creacion_id=request.user.id
            else:
                obj.usuario_modificacion_empate_id=request.user.id
            obj.save()
        return redirect(next_url)
        # else:
        #     messages.error(request, 'Ocurrió un error, intenta de nuevo')
        # return redirect(f'/custodia/contratos_list_empate/{desembolso_id}') 
        

@allowed_users(allowed_roles=['LEVANTAMIENTOS','LEGAL','admin'])
@login_required
def formulario_contratos_levantamiento(request, contrato_id=0):
    if request.method =='GET':
        es_legal = is_legal(request.user)
        if contrato_id ==0:
            form = ContratosCrearForm()
        else:
            contrato = Contratos.objects.get(pk=contrato_id)
            estado = contrato.estado

            if is_legal(request.user):
                if estado == "Enviado":
                    form = ContratosEditarForm(instance = contrato)
                else:
                    form = ContratosEditarEmpateForm(instance = contrato)  
            else:
                form = ContratosEditarEmpateForm(instance = contrato)
        return render(request,"contrato_form_levantamiento.html",{'form':form,'contrato_id':contrato_id, 'es_legal':es_legal} )
    else:
        if contrato_id==0:
            form = ContratosCrearForm(request.POST)
        else:
            contrato = Contratos.objects.get(pk=contrato_id)
            estado = contrato.estado

            if is_legal(request.user):
                if estado == "Enviado":
                    form = ContratosEditarForm(request.POST, instance = contrato)
                else:
                    form = ContratosEditarEmpateForm(request.POST, instance = contrato)  
            else:
                form = ContratosEditarEmpateForm(request.POST, instance = contrato)

        if form.is_valid():
            messages.success(request, 'El contrato se registró con éxito')
            obj= form.save(commit=False)
            if contrato_id ==0:
                obj.usuario_creacion_id=request.user.id
            elif is_custodia(request.user):
                obj.usuario_modificacion_empate_id=request.user.id
            elif is_admin(request.user):
                obj.usuario_modificacion_empate_id=request.user.id
            elif is_legal(request.user):
                obj.usuario_modificacion_legal_id=request.user.id
            obj.save()
        else:
            messages.error(request, 'Ocurrió un error, intenta de nuevo')
        return redirect('/custodia/contratos_list_levantamiento') 
        
@login_required
def contratos_list_empate(request, desembolso_id):
    try:
        detalles_desembolso = Desembolsos.objects.get(id=desembolso_id)
        form = DesembolsoCrearForm(instance=detalles_desembolso)
    except:
        detalles_desembolso = 0
        form = 0
    contratos_list=Contratos.objects.filter(desembolso_id=desembolso_id).order_by('-fecha_creacion')
    filter = ContratosEmpateFilter(request.GET, queryset=contratos_list)
    contratos_list=filter.qs
    return render(request,"contratos_list_empate.html",{'contratos_list':contratos_list,'form':form,'filter':filter})

@login_required
def contratos_list_levantamiento(request):
    contratos_list=Contratos.objects.all().order_by('-fecha_creacion')
    filter = ContratosLevantamientoFilter(request.GET, queryset=contratos_list)
    contratos_list=filter.qs
    return render(request,"contratos_list_levantamiento.html",{'contratos_list':contratos_list,'filter':filter})

@allowed_users(allowed_roles=['admin'])
@login_required
def contrato_delete_empate(request, contrato_id):
    next_url = request.GET.get('next')
    try:
        contrato = Contratos.objects.get(pk=contrato_id)
        contrato.delete()
        messages.success(request, 'Se eliminó el contrato con éxito')
    except:
        messages.error(request, 'Ocurrió un problema. Por favor volver a intentar')
    return redirect(next_url)

@allowed_users(allowed_roles=['admin','LEGAL'])
@login_required
def contrato_delete_levantamiento(request, contrato_id):
    contrato = Contratos.objects.get(pk=contrato_id)
    estado = contrato.estado

    if is_admin(request.user): 
        try:
            contrato.delete()
            messages.success(request, 'Se eliminó el contrato con éxito')
        except:
            messages.error(request, 'Ocurrió un problema. Por favor volver a intentar')
    elif is_legal(request.user):
        if estado == "Enviado":
            try:
                contrato.delete()
                messages.success(request, 'Se eliminó el contrato con éxito')
            except:
                messages.error(request, 'Ocurrió un problema. Por favor volver a intentar')  
    return redirect('/custodia/contratos_list_levantamiento')

def cantidad_contrato(request):
    cantidad = request.GET.get('cantidad')
    opciones = FormatoContrato.objects.filter(cantidad=cantidad)
    return render(request, "cargar_opciones_contratos.html", {'opciones':opciones})

#GARANTIAS
@allowed_users(allowed_roles=['EMPATE','admin'])
@login_required
def inmueble_formulario_empate(request, desembolso_id=0, inmueble_id=0):
    next_url = request.GET.get('next')
    if request.method =='GET':
        if inmueble_id ==0:
            # Crear inmueble (no hay instancia de inmueble)
            form = InmuebleEmpateForm(initial={'desembolso':desembolso_id})
        else:
            # Editar inmueble (hay instancia de inmueble)
            inmueble = Inmueble.objects.get(pk=inmueble_id)
            inmueble_id = inmueble.desembolso_id
            form = InmuebleEditarEmpateForm(instance = inmueble)
        return render(request,"inmueble_form_empate.html",{'form':form,'desembolso_id':desembolso_id, 'inmueble_id':inmueble_id} )
    else:
        if inmueble_id==0:
            form = InmuebleEmpateForm(request.POST)
        else:
            inmueble = Inmueble.objects.get(pk=inmueble_id)
            form = InmuebleEditarEmpateForm(request.POST, instance = inmueble)
        if form.is_valid():
            messages.success(request, 'El inmueble se registró con éxito')
            obj= form.save(commit=False)
            if inmueble_id==0:
                obj.usuario_creacion_id=request.user.id
            else:
                obj.usuario_modificacion_id=request.user.id
            obj.save()
        else:
            messages.error(request, 'Ocurrió un error, intenta de nuevo')
        # return redirect(f'/custodia/contratos_list_empate/{desembolso_id}') 
        return redirect(next_url)

@allowed_users(allowed_roles=['LEVANTAMIENTOS','admin'])
@login_required
def inmueble_formulario_levantamiento(request, inmueble_id=0):
    if request.method =='GET':
        if inmueble_id ==0:
            # Crear inmueble (no hay instancia de inmueble)
            form = InmuebleEmpateForm()
        else:
            # Editar inmueble (hay instancia de inmueble)
            inmueble = Inmueble.objects.get(pk=inmueble_id)
            inmueble_id = inmueble.desembolso_id
            form = InmuebleEditarEmpateForm(instance = inmueble)
        return render(request,"inmueble_form_empate.html",{'form':form,'inmueble_id':inmueble_id} )
    else:
        if inmueble_id==0:
            form = InmuebleEmpateForm(request.POST)
        else:
            inmueble = Inmueble.objects.get(pk=inmueble_id)
            form = InmuebleEditarEmpateForm(request.POST, instance = inmueble)
        if form.is_valid():
            messages.success(request, 'El inmueble se registró con éxito')
            obj= form.save(commit=False)
            if inmueble_id==0:
                obj.usuario_creacion_id=request.user.id
            else:
                obj.usuario_modificacion_id=request.user.id
            obj.save()
        else:
            messages.error(request, 'Ocurrió un error, intenta de nuevo')
        return redirect('/custodia/garantias_list_levantamiento/') 

@allowed_users(allowed_roles=['EMPATE','admin'])
@login_required
def vehiculo_formulario_empate(request, desembolso_id=0, vehiculo_id=0):
    next_url = request.GET.get('next')
    if request.method =='GET':
        if vehiculo_id ==0:
            # Crear vehiculo (no hay instancia de vehiculo)
            form = VehiculoEmpateForm(initial={'desembolso':desembolso_id})
        else:
            # Editar vehículo (hay instancia de vehículo)
            vehiculo = Vehiculo.objects.get(pk=vehiculo_id)
            vehiculo_id = vehiculo.desembolso_id
            form = VehiculoEditarEmpateForm(instance = vehiculo)
        return render(request,"vehiculo_form_empate.html",{'form':form,'desembolso_id':desembolso_id, 'vehiculo_id':vehiculo_id} )
    else:
        if vehiculo_id==0:
            form = VehiculoEmpateForm(request.POST)
        else:
            vehiculo = Vehiculo.objects.get(pk=vehiculo_id)
            form = VehiculoEditarEmpateForm(request.POST, instance = vehiculo)
        if form.is_valid():
            messages.success(request, 'El vehículo se registró con éxito')
            obj= form.save(commit=False)
            if vehiculo_id==0:
                obj.usuario_creacion_id=request.user.id
            else:
                obj.usuario_modificacion_id=request.user.id
            obj.save()
            obj.save()
        else:
            messages.error(request, 'Ocurrió un error, intenta de nuevo') 
        return redirect(next_url)

@allowed_users(allowed_roles=['LEVANTAMIENTOS','admin'])
@login_required
def vehiculo_formulario_levantamiento(request, vehiculo_id=0):
    if request.method =='GET':
        if vehiculo_id ==0:
            # Crear vehiculo (no hay instancia de vehiculo)
            form = VehiculoEmpateForm()
        else:
            # Editar vehículo (hay instancia de vehículo)
            vehiculo = Vehiculo.objects.get(pk=vehiculo_id)
            vehiculo_id = vehiculo.desembolso_id
            form = VehiculoEditarEmpateForm(instance = vehiculo)
        return render(request,"vehiculo_form_empate.html",{'form':form, 'vehiculo_id':vehiculo_id} )
    else:
        if vehiculo_id==0:
            form = VehiculoEmpateForm(request.POST)
        else:
            vehiculo = Vehiculo.objects.get(pk=vehiculo_id)
            form = VehiculoEditarEmpateForm(request.POST, instance = vehiculo)
        if form.is_valid():
            messages.success(request, 'El vehículo se registró con éxito')
            obj= form.save(commit=False)
            if vehiculo_id==0:
                obj.usuario_creacion_id=request.user.id
            else:
                obj.usuario_modificacion_id=request.user.id
            obj.save()
            obj.save()
        else:
            messages.error(request, 'Ocurrió un error, intenta de nuevo') 
        return redirect('/custodia/garantias_list_levantamiento/') 

@login_required
def garantias_list_empate(request, desembolso_id):
    try:
        detalles_desembolso = Desembolsos.objects.get(id=desembolso_id)
        form = DesembolsoCrearForm(instance=detalles_desembolso)
    except:
        detalles_desembolso = 0
        form = 0

    inmuebles_list= Inmueble.objects.filter(desembolso_id=desembolso_id)
    inmueble_filter = InmuebleFilter(request.GET, queryset=inmuebles_list)
    inmuebles_list = inmueble_filter.qs 

    vehiculos_list= Vehiculo.objects.filter(desembolso_id=desembolso_id)
    vehiculo_filter = VehiculoFilter(request.GET, queryset=vehiculos_list)
    vehiculos_list=vehiculo_filter.qs

    context = {'inmuebles_list':inmuebles_list,
                'vehiculos_list':vehiculos_list,
                'inmueble_filter':inmueble_filter,
                'vehiculo_filter':vehiculo_filter,
                'form':form
                }
    return render(request,"garantias_list_empate.html", context)


@login_required
def garantias_list_levantamiento(request):

    inmuebles_list= Inmueble.objects.all()
    inmueble_filter = InmuebleFilter(request.GET, queryset=inmuebles_list)
    inmuebles_list = inmueble_filter.qs 

    vehiculos_list= Vehiculo.objects.all()
    vehiculo_filter = VehiculoFilter(request.GET, queryset=vehiculos_list)
    vehiculos_list=vehiculo_filter.qs

    context = {'inmuebles_list':inmuebles_list,
                'vehiculos_list':vehiculos_list,
                'inmueble_filter':inmueble_filter,
                'vehiculo_filter':vehiculo_filter,
                }
    return render(request,"garantias_list_levantamiento.html", context)

@allowed_users(allowed_roles=['admin'])
@login_required
def inmueble_delete_empate(request,inmueble_id):
    next_url = request.GET.get('next')
    inmueble = Inmueble.objects.get(pk=inmueble_id)
    inmueble.delete()
    messages.success(request, 'Se eliminó la garantía con éxito')
    return redirect(next_url)
    # return redirect(f'/custodia/garantias_list_empate/{desembolso_id}')

@allowed_users(allowed_roles=['admin'])
@login_required
def vehiculo_delete_empate(request,vehiculo_id):
    next_url = request.GET.get('next')
    vehiculo = Vehiculo.objects.get(pk=vehiculo_id)
    vehiculo.delete()
    messages.success(request, 'Se eliminó la garantía con éxito')
    return redirect(next_url)
    # return redirect(f'/custodia/garantias_list_empate/{desembolso_id}')

@allowed_users(allowed_roles=['admin'])
@login_required
def inmueble_delete_levantamiento(request,inmueble_id):
    inmueble = Inmueble.objects.get(pk=inmueble_id)
    inmueble.delete()
    messages.success(request,'Se eliminó la garantía con éxito')
    return redirect('/custodia/garantias_list_levantamiento')

@allowed_users(allowed_roles=['admin'])
@login_required
def vehiculo_delete_levantamiento(request, vehiculo_id):
    vehiculo = Vehiculo.objects.get(pk=vehiculo_id)
    vehiculo.delete()
    messages.success(request,'Se eliminó la garantía con éxito')
    return redirect('/custodia/garantias_list_levantamiento')

#DOCUMENTOS SUELTOS
@login_required
def documentos_sueltos_list(request):
    if request.method == 'GET':  
        documentos_sueltos_list = DocumentosSueltos.objects.all().order_by('-fecha_creacion')
        filter = DocumentoSueltoFilter(request.GET, queryset=documentos_sueltos_list)
        documentos_sueltos_list = filter.qs
        return render(request,"documentos_sueltos_list.html",{'documentos_sueltos_list':documentos_sueltos_list,'filter':filter })    
    #template = loader.get_template('export/importar.html')  
    elif request.method == 'POST':  
        documentos_sueltos_resource = DocumentosSueltosResource()  
        dataset = Dataset()  
        #print(dataset)  
        nuevos_documentos_sueltos = request.FILES['xlsxfile']  
        # print(nuevas_aperturas)  
        imported_data = dataset.load(nuevos_documentos_sueltos.read()) 
        print(imported_data)  
        result = documentos_sueltos_resource.import_data(dataset, dry_run=True) # Test the data import  
        print(result.has_errors())  
        if not result.has_errors():  
            documentos_sueltos_resource.import_data(dataset, dry_run=False) # Actually import now    
            messages.success(request, 'Se importó correctamente')
    return redirect('/custodia/documentos_sueltos_list')    

@allowed_users(allowed_roles=['SERVICIOS','admin'])
@login_required
def formulario_documento_suelto(request, documento_suelto_id=0):
    if request.method =='GET':
        caja = Parametro.objects.get(usuario_id=request.user.id)
        caja_form = ParametroForm(instance=caja)
        if documento_suelto_id==0:
            form = DocumentosSueltosCrearForm()
        else:
            documentos_sueltos = DocumentosSueltos.objects.get(pk=documento_suelto_id)
            form = DocumentosSueltosEditarForm(instance=documentos_sueltos)
        return render(request,"documentos_sueltos_form.html",{'form':form,'documento_suelto_id':documento_suelto_id,'caja_form':caja_form})
    else:
        if documento_suelto_id ==0:
            form = DocumentosSueltosCrearForm(request.POST)
        else:
            documentos_sueltos = DocumentosSueltos.objects.get(pk=documento_suelto_id)
            form = DocumentosSueltosEditarForm(request.POST, instance = documentos_sueltos)
        if form.is_valid():
            obj = form.save(commit=False)
            if documento_suelto_id == 0:
                obj.usuario_creacion_id = request.user.id
            else:
                obj.usuario_modificacion_id = request.user.id
            messages.success(request, 'Se registró el documento suelto con éxito')
            form.save() 
        return redirect('/custodia/documentos_sueltos_list')

@allowed_users(allowed_roles=['admin'])
@login_required
def documento_suelto_delete(request, documento_suelto_id):
    try:
        documento_suelto = DocumentosSueltos.objects.get(pk=documento_suelto_id)
        documento_suelto.delete()
        messages.success(request, 'Se eliminó con éxito')
    except:
        messages.error(request, 'Ocurrió un problema. Por favor vuelve a intentar')
    return redirect('/custodia/documentos_sueltos_list')

#CONFIGURACIONES
@login_required
def configuraciones_index(request):
    return render(request, "configuraciones_index.html")
@login_required
def configuraciones_formulario(request):
    if request.method=='GET':
        try: 
            configuraciones = Parametro.objects.get(usuario_id=request.user.id)
            form = ParametroForm(instance=configuraciones)
        except:
            form = ParametroForm()
    else:
        try:
            configuraciones = Parametro.objects.get(usuario_id=request.user.id)
            form = ParametroForm(request.POST, instance=configuraciones)
        except:
            form = ParametroForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.usuario_id = request.user.id
            obj.save()
            messages.success(request, 'Las configuraciones se guardaron con éxito.')
        else:
            messages.error(request, 'Hubo un error. Intenta de nuevo.')
    return render(request, "configurar_parametros.html", {'form':form})


@login_required
def tiempos_operaciones(request):
    tipos = TipoOperacion.objects.all()
    return render(request, "tiempos_operaciones.html", {'tipos':tipos})

def tiempos_operaciones_formulario(request, id=0):
    if request.method=='GET':
        if id==0:
            form = TipoOperacionForm()
        else:
            tipo = TipoOperacion.objects.get(pk=id)
            form = TipoOperacionForm(instance=tipo)
        return render(request, "tiempos_operaciones_formulario.html", {'form':form, 'tipo_id':id})
    else:
        if id==0:
            form = TipoOperacionForm(request.POST)
        else:
            tipo = TipoOperacion.objects.get(pk=id)
            form = TipoOperacionForm(request.POST, instance=tipo)
        if form.is_valid():
            obj= form.save(commit=False) 
            obj.save()
            messages.success(request, 'Se registró el tipo de operación con éxito') 
        else:
            messages.error(request, 'Ocurrió un problema, por favor vuelve a intentar') 
    return redirect('/custodia/tiempos_operaciones/')
    
def tiempos_operaciones_delete(request, id):
    tipo = TipoOperacion.objects.get(pk=id)
    tipo.delete()
    return redirect('/custodia/tiempos_operaciones/')

#REPORTES
@login_required
def reportes_index(request):
    if request.method == 'GET':
        form = ReporteForm()
    else:
        form = ReporteForm(request.POST)
        if form.is_valid():
            reporte = form.cleaned_data['reporte']
            caja = form.cleaned_data['caja']
            # modelo = getattr(custodia.models, reporte)
            if reporte == "Empate":
                if caja != None:
                    data = Empate.objects.filter(usuario_empate=request.user.id, empatado=True, caja=caja).values('distribucion__desembolso__codigo_cliente','distribucion__desembolso__operacion', 'distribucion__desembolso__onbase', 'distribucion__desembolso__cliente','fecha_modificacion', 'caja' )
                else:
                    data = Empate.objects.filter(usuario_empate=request.user.id, empatado=True).values('distribucion__desembolso__codigo_cliente','distribucion__desembolso__operacion', 'distribucion__desembolso__onbase', 'distribucion__desembolso__cliente','fecha_modificacion', 'caja' )
                df = pd.DataFrame(data)
                try:
                    df['fecha_modificacion'] = df['fecha_modificacion'].dt.tz_localize(None)
                except:
                    messages.error(request, "No tiene operaciones para descargar")
                    return redirect('/custodia/reportes_index/')
                df = df.rename(columns={'distribucion__desembolso__codigo_cliente':'FISA','distribucion__desembolso__operacion': 'Operación','distribucion__desembolso__onbase':'Onbase', 'distribucion__desembolso__cliente': 'Cliente','fecha_modificacion':'Fecha Empate', 'caja':'Caja'})
            elif reporte == "Contratos":
                if caja != None:
                    data = Contratos.objects.filter(usuario_modificacion_empate=request.user.id, estado="Recibido", ubicacion=caja).values('desembolso__codigo_cliente','desembolso__operacion', 'desembolso__onbase', 'desembolso__cliente','fecha_modificacion','ubicacion')
                else:
                    data = Contratos.objects.filter(usuario_modificacion_empate=request.user.id, estado="Recibido").values('desembolso__codigo_cliente','desembolso__operacion', 'desembolso__onbase', 'desembolso__cliente','fecha_modificacion','ubicacion')
                df = pd.DataFrame(data)
                try:
                    df['fecha_modificacion'] = df['fecha_modificacion'].dt.tz_localize(None)
                except:
                    messages.error(request, "no tiene operaciones para descargar")
                    return redirect('/custodia/reportes_index/')
                df = df.rename(columns={'desembolso__codigo_cliente': 'FISA','desembolso__operacion': 'Operación', 'desembolso__onbase': 'Onbase', 'desembolso_cliente': 'Cliente','fecha_modificacion': 'Fecha Recepción' ,'ubicacion': 'Ubicación' }) 
            elif reporte == "Aperturas":
                if caja != None:
                    data = Apertura.objects.filter(usuario_modificacion=request.user.id, estado="Recibido", caja=caja).values('codigo_cliente','cuenta', 'fecha_modificacion', 'usuario_modificacion__nombre','caja','bloque')
                else:
                    data = Apertura.objects.filter(usuario_modificacion=request.user.id, estado="Recibido").values('codigo_cliente','cuenta', 'fecha_modificacion', 'usuario_modificacion__nombre','caja','bloque')
                df = pd.DataFrame(data)
                try:
                    df['fecha_modificacion'] = df['fecha_modificacion'].dt.tz_localize(None)
                except:
                    messages.error(request, "no tiene operaciones para descargar")
                    return redirect('/custodia/reportes_index/')
                df['Analista_bloque'] = df['usuario_modificacion__nombre'] + '_' + df['bloque'].map(str)
                del df['usuario_modificacion__nombre']
                del df['bloque']
                df = df.rename(columns={'codigo_cliente':'FISA','cuenta':'Cuenta','fecha_modificacion':'Fecha Recepción','Analista_bloque':'Bloque','caja':'Caja'})
            elif reporte == "Pólizas": 
                if caja != None:
                    df = pd.DataFrame(list(Poliza.objects.filter(usuario_modificacion=request.user.id, estado="Recibido", caja=caja).values('codigo_cliente','cliente','poliza','caja','fecha_modificacion','bloque','usuario_modificacion__nombre')))
                else:
                    df = pd.DataFrame(list(Poliza.objects.filter(usuario_modificacion=request.user.id, estado="Recibido").values('codigo_cliente','cliente','poliza','caja','fecha_modificacion','bloque','usuario_modificacion__nombre')))    
                try:
                    df['fecha_modificacion'] = df['fecha_modificacion'].dt.tz_localize(None)
                except:
                    messages.error(request, "no tiene operaciones para descargar")
                    return redirect('/custodia/reportes_index/')
                df['Analista_bloque'] = df['usuario_modificacion__nombre'] + '_' + df['bloque'].map(str)
                del df['bloque']
                del df['usuario_modificacion__nombre']
                df.rename(columns = {'codigo_cliente':'FISA','cliente':'Cliente','poliza':'Póliza','caja':'Caja','fecha_modificacion':'Fecha Recepción','Analista_bloque':'Bloque'})
            elif reporte == "Documentos Sueltos":
                if caja != None:
                    df = pd.DataFrame(list(DocumentosSueltos.objects.filter(usuario_modificacion=request.user.id, estado="Recibido", caja=caja).values('codigo_cliente','cliente','operacion','caja','fecha_modificacion','bloque','usuario_modificacion__nombre')))
                else:
                    df = pd.DataFrame(list(DocumentosSueltos.objects.filter(usuario_modificacion=request.user.id, estado="Recibido").values('codigo_cliente','cliente','operacion','caja','fecha_modificacion','bloque','usuario_modificacion__nombre')))
                try:
                    df['fecha_modificacion'] = df['fecha_modificacion'].dt.tz_localize(None)
                except:
                    messages.error(request, "no tiene operaciones para descargar")
                    return redirect('/custodia/reportes_index/')
                df['Analista_bloque'] = df['usuario_modificacion__nombre'] + '_' + df['bloque'].map(str)
                del df['bloque']
                del df['usuario_modificacion__nombre']
                df.rename(columns = {'codigo_cliente':'FISA','cliente':'Cliente','operacion':'Operación','caja':'Caja','fecha_modificacion':'Fecha Recepción','Analista_bloque':'Bloque'})
            elif reporte == "Levantamientos":
                if caja != None:
                    df = pd.DataFrame(list(Levantamientos.objects.filter(estado="Listo Para Entrega",caja=caja).values('sucursal', 'codigo_cliente','cliente','descripcion','fecha_modificacion')))
                else:
                    df = pd.DataFrame(list(Levantamientos.objects.filter(estado="Listo Para Entrega").values('sucursal', 'codigo_cliente','cliente','descripcion','fecha_modificacion')))
                try:
                    df['fecha_modificacion'] = df['fecha_modificacion'].dt.tz_localize(None)
                except:
                    messages.error(request, "no tiene operaciones para descargar")
                    return redirect('/custodia/reportes_index/')
                df.rename(columns = {'sucursal':'Sucursal', 'codigo_cliente':'FISA','cliente':'Cliente','fecha_modificacion':'Fecha Modificación'})
            
            elif reporte == "Desembolsos":
                df = pd.DataFrame(list(Desembolsos.objects.select_related('profile').prefetch_related(Prefetch('distribucion')).all().values('fecha_desembolso','producto','tipo','cliente','operacion','monto','desembolso_parcial','ejecutivo','onbase','sucursal','agencia','tipo_banca','tipo_trabajo','instancia_aprobacion','estado','usuario_creacion__nombre','usuario_modificacion__nombre','fecha_creacion','fecha_modificacion','distribucion__tipo__nombre','distribucion__analista_asignado__nombre','distribucion__usuario_creacion__nombre','distribucion__usuario_modificacion__nombre','distribucion__fecha_creacion','distribucion__fecha_modificacion','distribucion__empate__fecha_modificacion', 'distribucion__empate__caja', 'distribucion__empate__tiempo_empate', 'distribucion__empate__usuario_empate__nombre' )))
                df['fecha_creacion'] = df['fecha_creacion'].dt.tz_localize(None)
                df['fecha_modificacion'] = df['fecha_modificacion'].dt.tz_localize(None)
                df['distribucion__fecha_creacion'] = df['distribucion__fecha_creacion'].dt.tz_localize(None)
                df['distribucion__fecha_modificacion'] = df['distribucion__fecha_modificacion'].dt.tz_localize(None)
                df['distribucion__empate__fecha_modificacion'] = df['distribucion__empate__fecha_modificacion'].dt.tz_localize(None)
                
                df.rename(columns = {'fecha_desembolso':'Fecha Desembolso',
                                    'producto':'Producto',
                                    'tipo':'Tipo',
                                    'cliente':'Cliente',
                                    'operacion':'Operacion',
                                    'monto':'Monto',
                                    'desembolso_parcial':'Desembolso Parcial',
                                    'ejecutivo':'Ejecutivo',
                                    'onbase':'Onbase',
                                    'sucursal':'Sucursal',
                                    'agencia':'Agencia',
                                    'tipo_banca':'Tipo Banca',
                                    'tipo_trabajo':'Tipo Trabajo',
                                    'instancia_aprobacion':'Instancia Aprobacion',
                                    'estado':'Estado',
                                    'usuario_creacion__nombre':'Usuario Creacion Desembolso',
                                    'usuario_modificacion__nombre':'Usuario Modificacion Desembolso',
                                    'fecha_creacion':'Fecha Creacion Desembolso',
                                    'fecha_modificacion':'Fecha Modificacion Desembolso',
                                    'distribucion__tipo__nombre':'Distribucion Tipo',
                                    'distribucion__analista_asignado__nombre':'Distribucion Analista Asignado',
                                    'distribucion__usuario_creacion__nombre':'Distribucion Usuario Creacion',
                                    'distribucion__usuario_modificacion__nombre':'Distribucion Usuario Modificacion',
                                    'distribucion__fecha_creacion':'Distribucion Fecha Creacion',
                                    'distribucion__fecha_modificacion':'Distribucion Fecha Modificacion',
                                    'distribucion__empate__fecha_modificacion':'Empate Fecha Modificacion',	
                                    'distribucion__empate__caja':'Empate Caja',	
                                    'distribucion__empate__tiempo_empate':'Empate Tiempo Empate',	
                                    'distribucion__empate__usuario_empate__nombre':'Empate Usuario Empate'

                }, inplace=True)
                print(df)
                
            usuario = request.user
            out_path = f"C:/Users/USUARIO/Desktop/reporte_{reporte}_{usuario}_{datetime.date.today()}.xlsx"
            writer = pd.ExcelWriter(out_path, engine='xlsxwriter')
            df.to_excel(writer, sheet_name = 'Hoja1', index = False)         
            try:
                writer.save()
                messages.success(request, 'Se generó el reporte con éxito')
            except:
                messages.error(request, 'Ocurrió un problema. Por favor vuelve a intentar')
    return render(request, "reportes_index.html", {'form':form})

@login_required
def reporte_empate(request):
    data = Empate.objects.filter(usuario_empate=request.user.id, empatado=True).values('distribucion__desembolso__codigo_cliente','distribucion__desembolso__operacion', 'distribucion__desembolso__onbase', 'distribucion__desembolso__cliente','fecha_modificacion', 'caja' )
    df = pd.DataFrame(data)
    df['fecha_modificacion'] = df['fecha_modificacion'].dt.tz_localize(None)
    df = df.rename(columns={'distribucion__desembolso__codigo_cliente':'FISA','distribucion__desembolso__operacion': 'Operación','distribucion__desembolso__onbase':'Onbase', 'distribucion__desembolso__cliente': 'Cliente','fecha_modificacion':'Fecha Empate', 'caja':'Caja'})
    usuario = request.user
    out_path = f"C:/Users/USUARIO/Desktop/reporte_empates_{usuario}.xlsx"
    writer = pd.ExcelWriter(out_path , engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1', index = False)
    try:
        writer.save()
        messages.success(request, 'Se generó el reporte con éxito')
    except:
        messages.error(request, 'Ocurrió un problema. Por favor vuelve a intentar')
    return redirect('/custodia/reportes_index/')
@login_required
def reporte_contratos(request):
    data = Contratos.objects.filter(usuario_modificacion_empate=request.user.id, estado="Recibido").values('desembolso__codigo_cliente','desembolso__operacion', 'desembolso__onbase', 'desembolso__cliente','fecha_modificacion','ubicacion')
    df = pd.DataFrame(data)
    df['fecha_modificacion'] = df['fecha_modificacion'].dt.tz_localize(None)
    df = df.rename(columns={'desembolso__codigo_cliente': 'FISA','desembolso__operacion': 'Operación', 'desembolso__onbase': 'Onbase', 'desembolso_cliente': 'Cliente','fecha_modificacion': 'Fecha Recepción' ,'ubicacion': 'Ubicación' })
    usuario = request.user
    out_path = f"C:/Users/USUARIO/Desktop/reporte_contratos_{usuario}.xlsx"
    writer = pd.ExcelWriter(out_path , engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1', index = False)
    try:
        writer.save()
        messages.success(request, 'Se generó el reporte con éxito')
    except:
        messages.error(request, 'Ocurrió un problema. Por favor vuelve a intentar')
    return redirect('/custodia/reportes_index/')
@login_required
def reporte_aperturas(request):
    data = Apertura.objects.filter(usuario_modificacion_id=request.user.id, estado="Recibido").values('codigo_cliente','cuenta', 'fecha_modificacion', 'usuario_modificacion__nombre','caja','bloque')
    df = pd.DataFrame(data)
    # df['fecha_modificacion'] = df['fecha_modificacion'].dt.tz_localize(None)
    df['Analista_bloque'] = df['usuario_modificacion__nombre'] + '_' + df['bloque'].map(str)
    del df['usuario_modificacion__nombre']
    del df['bloque']
    df = df.rename(columns={'codigo_cliente':'FISA','cuenta':'Cuenta','fecha_modificacion':'Fecha Recepción','Analista_bloque':'Bloque','caja':'Caja'})
    usuario = request.user
    out_path = f"C:/Users/USUARIO/Desktop/reporte_aperturas_{usuario}.xlsx"
    writer = pd.ExcelWriter(out_path, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1', index = False)
    try:
        writer.save()
        messages.success(request, 'Se generó el reporte con éxito')
    except:
        messages.error(request, 'Ocurrió un problema. Por favor vuelve a intentar')
    return redirect('/custodia/reportes_index/')
@login_required
def reporte_polizas(request):
    df = pd.DataFrame(list(Poliza.objects.filter(usuario_modificacion=request.user.id, estado="Recibido").values('codigo_cliente','cliente','poliza','caja','fecha_modificacion','bloque','usuario_modificacion__nombre')))
    df['fecha_modificacion'] = df['fecha_modificacion'].dt.tz_localize(None)
    df['Analista_bloque'] = df['usuario_modificacion__nombre'] + '_' + df['bloque'].map(str)
    del df['bloque']
    del df['usuario_modificacion__nombre']
    df.rename(columns = {'codigo_cliente':'FISA','cliente':'Cliente','poliza':'Póliza','caja':'Caja','fecha_modificacion':'Fecha Recepción','Analista_bloque':'Bloque'})
    usuario = request.user
    out_path = f"C:/Users/USUARIO/Desktop/reporte_polizas_{usuario}.xlsx"
    writer = pd.ExcelWriter(out_path, engine='xlsxwriter')
    df.to_excel(writer, sheet_name = 'Sheet1', index = False)
    try:
        writer.save()
        messages.success(request, 'Se generó el reporte con éxito')
    except:
        messages.error(request, 'Ocurrió un problema. Por favor vuelve a intentar')
    return redirect ('/custodia/reportes_index/')
@login_required
def reporte_documentos_sueltos(request):
    df = pd.DataFrame(list(DocumentosSueltos.objects.filter(usuario_modificacion=request.user.id, estado="Recibido").values('codigo_cliente','cliente','operacion','caja','fecha_modificacion','bloque','usuario_modificacion__nombre')))
    df['fecha_modificacion'] = df['fecha_modificacion'].dt.tz_localize(None)
    df['Analista_bloque'] = df['usuario_modificacion__nombre'] + '_' + df['bloque'].map(str)
    del df['bloque']
    del df['usuario_modificacion__nombre']
    df.rename(columns = {'codigo_cliente':'FISA','cliente':'Cliente','operacion':'Operación','caja':'Caja','fecha_modificacion':'Fecha Recepción','Analista_bloque':'Bloque'})
    usuario = request.user
    out_path = f"C:/Users/USUARIO/Desktop/reporte_docs_sueltos_{usuario}.xlsx"
    writer = pd.ExcelWriter(out_path, engine='xlsxwriter')
    df.to_excel(writer, sheet_name = 'Sheet1', index = False)
    try:
        writer.save()
        messages.success(request, 'Se generó el reporte con éxito')
    except:
        messages.error(request, 'Ocurrió un problema. Por favor vuelve a intentar')
    return redirect ('/custodia/reportes_index/')
@login_required
def reporte_levantamientos(request):
    df = pd.DataFrame(list(Levantamientos.objects.filter(estado="Listo Para Entrega").values('sucursal', 'codigo_cliente','cliente','descripcion','fecha_modificacion')))
    df['fecha_modificacion'] = df['fecha_modificacion'].dt.tz_localize(None)
    df.rename(columns = {'sucursal':'Sucursal', 'codigo_cliente':'FISA','cliente':'Cliente','fecha_modificacion':'Fecha Modificación'})
    usuario = request.user
    out_path = f"C:/Users/USUARIO/Desktop/reporte_levantamientos_{usuario}.xlsx"
    writer = pd.ExcelWriter(out_path, engine='xlsxwriter')
    df.to_excel(writer, sheet_name = 'Sheet1', index = False)
    try:
        writer.save()
        messages.success(request, 'Se generó el reporte con éxito')
    except:
        messages.error(request, 'Ocurrió un problema. Por favor vuelve a intentar')
    return redirect ('/custodia/reportes_index/')

def historial(request):
    modelo = LogEntry.objects.select_related('content_type', 'actor').only('content_type', 'actor', 'action', 'timestamp')
    filter = HistorialFilter(request.GET, queryset=modelo)
    modelo = filter.qs
    return render(request, "historial.html", {'modelo':modelo, 'filter':filter})


def detalle_historial(request, id=0):
    if request.method == 'GET':
        log = LogEntry.objects.only('changes').get(id=id)
    return render(request, "detalle_historial.html", {'log':log})

# HOJA RESUMEN
def hoja_resumen(request):
    if request.method=='GET':
        form = HojaResumenForm() 
        return render(request, "hoja_resumen.html", {'form':form})   
    else:
        form = HojaResumenForm() 
        codigo_cliente = request.POST.get('codigo_cliente')
        onbase = request.POST.get('onbase')
        operacion = request.POST.get('operacion')
        cliente = request.POST.get('cliente')

        
        if codigo_cliente != "":
            desembolsos = Desembolsos.objects.filter(codigo_cliente=codigo_cliente)
            distribuciones = Distribucion.objects.filter(desembolso__codigo_cliente=codigo_cliente)
            empates = Empate.objects.filter(distribucion__desembolso__codigo_cliente=codigo_cliente).annotate(observaciones_count=(Count('observaciones')))
            observaciones = Observaciones.objects.filter(empate__distribucion__desembolso__codigo_cliente=codigo_cliente)
            contratos = Contratos.objects.filter(desembolso__codigo_cliente=codigo_cliente)
            vehiculos = Vehiculo.objects.filter(desembolso__codigo_cliente=codigo_cliente)
            inmuebles = Inmueble.objects.filter(desembolso__codigo_cliente=codigo_cliente)
            aperturas = Apertura.objects.filter(codigo_cliente=codigo_cliente)
            polizas = Poliza.objects.filter(codigo_cliente=codigo_cliente)
            documentos_sueltos = DocumentosSueltos.objects.filter(codigo_cliente=codigo_cliente)
            levantamientos = Levantamientos.objects.filter(Q(codigo_cliente=codigo_cliente)|Q(desembolso__codigo_cliente=codigo_cliente))
        elif onbase != "":
            desembolsos = Desembolsos.objects.filter(onbase=onbase)
            distribuciones = Distribucion.objects.filter(desembolso__onbase=onbase)
            empates = Empate.objects.filter(distribucion__desembolso__onbase=onbase).annotate(observaciones_count=(Count('observaciones')))
            observaciones = Observaciones.objects.filter(empate__distribucion__desembolso__onbase=onbase)
            contratos = Contratos.objects.filter(desembolso__onbase=onbase)
            vehiculos = Vehiculo.objects.filter(desembolso__onbase=onbase)
            inmuebles = Inmueble.objects.filter(desembolso__onbase=onbase)
            aperturas = Apertura.objects.filter(codigo_cliente=onbase)
            polizas = Poliza.objects.filter(codigo_cliente=onbase)
            documentos_sueltos = DocumentosSueltos.objects.filter(codigo_cliente=onbase)
            levantamientos = Levantamientos.objects.filter(Q(onbase=codigo_cliente)|Q(desembolso__onbase=onbase))
        elif operacion != "":
            desembolsos = Desembolsos.objects.filter(operacion=operacion)
            distribuciones = Distribucion.objects.filter(desembolso__operacion=operacion)
            empates = Empate.objects.filter(distribucion__desembolso__operacion=operacion).annotate(observaciones_count=(Count('observaciones')))
            observaciones = Observaciones.objects.filter(empate__distribucion__desembolso__operacion=operacion)
            contratos = Contratos.objects.filter(desembolso__operacion=operacion)
            vehiculos = Vehiculo.objects.filter(desembolso__operacion=operacion)
            inmuebles = Inmueble.objects.filter(desembolso__operacion=operacion)
            aperturas = Apertura.objects.filter(codigo_cliente=operacion)
            polizas = Poliza.objects.filter(codigo_cliente=operacion)
            documentos_sueltos = DocumentosSueltos.objects.filter(codigo_cliente=operacion)
            levantamientos = Levantamientos.objects.filter(Q(operacion=operacion)|Q(desembolso__operacion=operacion))
        
        elif cliente != "":
            desembolsos = Desembolsos.objects.filter(cliente__icontains=cliente)
            distribuciones = Distribucion.objects.filter(desembolso__cliente__icontains=cliente)
            empates = Empate.objects.filter(distribucion__desembolso__cliente__icontains=cliente).annotate(observaciones_count=(Count('observaciones')))
            observaciones = Observaciones.objects.filter(empate__distribucion__desembolso__cliente__icontains=cliente)
            contratos = Contratos.objects.filter(desembolso__cliente__icontains=cliente)
            vehiculos = Vehiculo.objects.filter(desembolso__cliente__icontains=cliente)
            inmuebles = Inmueble.objects.filter(desembolso__cliente__icontains=cliente)
            aperturas = Apertura.objects.filter(cliente__icontains=cliente)
            polizas = Poliza.objects.filter(cliente__icontains=cliente)
            documentos_sueltos = DocumentosSueltos.objects.filter(cliente__icontains=cliente)
            levantamientos = Levantamientos.objects.filter(Q(cliente__icontains=cliente)|Q(desembolso__cliente__icontains=cliente))

        # filter = DesembolsoFilter(request.GET, queryset=clientes)
        # clientes = filter.qs

        # results = chain(desembolsos, contratos, vehiculos, inmuebles, aperturas, polizas, documentos_sueltos)
        # print(list(results))
        context = {
            'form':form,
            'desembolsos':desembolsos,
            'distribuciones':distribuciones,
            'empates':empates,
            'observaciones':observaciones,
            'contratos':contratos,
            'vehiculos':vehiculos,
            'inmuebles':inmuebles,
            'aperturas':aperturas,
            'polizas':polizas,
            'levantamientos':levantamientos,
            'documentos_sueltos':documentos_sueltos,
        }

        return render(request, "hoja_resumen.html", context)

# EMAILS RECORDATORIO
def enviar_emails(request):
    enviar_emails_task.delay()
    return HttpResponse("Se enviaron emails")

    




    