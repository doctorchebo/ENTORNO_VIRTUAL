from auditlog.models import LogEntry
from django_filters.rest_framework import FilterSet
import django_filters
from .models import *
from django import forms
from .widgets import DateTimePickerInput, DatePickerInput

class EmpateFilter(django_filters.FilterSet):
    distribucion__desembolso__onbase = django_filters.NumberFilter(label='', lookup_expr='icontains', widget=forms.NumberInput(attrs=
        {
        'placeholder': 'Onbase', 
        'class': 'form-control',
        'size': 10,}))
    distribucion__desembolso__operacion = django_filters.NumberFilter(label='', lookup_expr='icontains', widget=forms.NumberInput(attrs=
        {
        'placeholder': 'Operación', 
        'class': 'form-control',
        'size': 10,}))
    distribucion__desembolso__cliente = django_filters.CharFilter(label='',lookup_expr='icontains', widget=forms.TextInput(attrs=
        {
        'placeholder': 'Cliente', 
        'class': 'form-control',
        'size': 10,}))
    caja = django_filters.NumberFilter(label='', lookup_expr='icontains', widget=forms.NumberInput(attrs=
        {
        'placeholder': 'Caja', 
        'class': 'form-control',
        'size': 10,}))
    
    fecha_modificacion = django_filters.DateFilter(label='', lookup_expr='icontains', widget=DatePickerInput(attrs=
        {
        'placeholder': 'Fecha modificación', 
        'class': 'form-control',
        'size': 10,}))
    
    estado = django_filters.CharFilter(label='',lookup_expr='icontains', widget=forms.TextInput(attrs=
        {
        'placeholder': 'Estado', 
        'class': 'form-control',
        'size': 10,}))
    # numero_caja = django_filters.NumberFilter(label='Caja',lookup_expr='icontains')
    class Meta:
        model = Empate
        fields = ['distribucion__desembolso__onbase','distribucion__desembolso__operacion','distribucion__desembolso__cliente','estado']
class ContratosEmpateFilter(django_filters.FilterSet):
    num_testimonio = django_filters.CharFilter(label='', lookup_expr='icontains', widget=forms.TextInput(attrs=
        {
        'placeholder': 'Num. Testimonio', 
        'class': 'form-control',
        'size': 10,}))
    ubicacion = django_filters.CharFilter(label='', lookup_expr='icontains', widget=forms.TextInput(attrs=
        {
        'placeholder': 'Ubicación', 
        'class': 'form-control',
        'size': 10,}))
    estado = django_filters.CharFilter(label='',lookup_expr='icontains', widget=forms.TextInput(attrs=
        {
        'placeholder': 'Estado', 
        'class': 'form-control',
        'size': 10,}))
    class Meta:
        model = Contratos
        fields = ['num_testimonio','ubicacion','estado',]

class ContratosLevantamientoFilter(django_filters.FilterSet):
    desembolso__codigo_cliente= django_filters.NumberFilter(label='', lookup_expr='icontains', widget=forms.NumberInput(attrs=
        {
        'placeholder': 'Cód. Cliente', 
        'class': 'form-control',
        'size': 10,}))
    desembolso__cliente = django_filters.CharFilter(label='', lookup_expr='icontains', widget=forms.TextInput(attrs=
        {
        'placeholder': 'Cliente', 
        'class': 'form-control',
        'size': 10,}))
    num_testimonio = django_filters.CharFilter(label='', lookup_expr='icontains', widget=forms.TextInput(attrs=
        {
        'placeholder': 'Nº Testimonio', 
        'class': 'form-control',
        'size': 10,}))
    ubicacion = django_filters.CharFilter(label='', lookup_expr='icontains', widget=forms.TextInput(attrs=
        {
        'placeholder': 'Ubicación', 
        'class': 'form-control',
        'size': 10,}))
    estado = django_filters.CharFilter(label='',lookup_expr='icontains', widget=forms.TextInput(attrs=
        {
        'placeholder': 'Estado', 
        'class': 'form-control',
        'size': 10,}))
    class Meta:
        model = Contratos
        fields = ['desembolso__codigo_cliente','desembolso__cliente','num_testimonio','ubicacion','estado']

class DistribucionFilter(django_filters.FilterSet):
    desembolso__onbase = django_filters.NumberFilter(label='', lookup_expr='icontains', widget=forms.NumberInput(attrs=
        {
        'placeholder': 'Onbase', 
        'class': 'form-control',
        'size': 10,}))
    desembolso__operacion = django_filters.NumberFilter(label='', lookup_expr='icontains', widget=forms.NumberInput(attrs=
        {
        'placeholder': 'Operación', 
        'class': 'form-control',
        'size': 10,}))
    desembolso__cliente = django_filters.CharFilter(label='',lookup_expr='icontains', widget=forms.TextInput(attrs=
        {
        'placeholder': 'Cliente', 
        'class': 'form-control',
        'size': 10,}))
    tipo__nombre = django_filters.CharFilter(label='',lookup_expr='icontains', widget=forms.TextInput(attrs=
        {
        'placeholder': 'Tipo', 
        'class': 'form-control',
        'size': 30,}))
    analista_asignado__nombre = django_filters.CharFilter(label='',lookup_expr='icontains', widget=forms.TextInput(attrs=
        {
        'placeholder': 'Analista asignado', 
        'class': 'form-control',
        'size': 10,}))
    class Meta:
        model = Distribucion
        fields = ['desembolso__onbase','desembolso__operacion','desembolso__cliente','tipo__nombre','analista_asignado__nombre']

class AperturaFilter(django_filters.FilterSet):
    codigo_cliente = django_filters.NumberFilter(label='', lookup_expr='icontains', widget=forms.NumberInput(attrs=
        {
        'placeholder': 'Cód. Cliente', 
        'class': 'form-control',
        'size': 10,}))
    cliente = django_filters.CharFilter(label='', lookup_expr='icontains', widget=forms.TextInput(attrs=
        {
        'placeholder': 'Cliente', 
        'class': 'form-control',
        'size': 10,}))
    cuenta = django_filters.NumberFilter(label='', lookup_expr='icontains', widget=forms.NumberInput(attrs=
        {
        'placeholder': 'Cuenta', 
        'class': 'form-control',
        'size': 10,}))
    estado = django_filters.CharFilter(label='', lookup_expr='icontains', widget=forms.TextInput(attrs=
        {
        'placeholder': 'Estado', 
        'class': 'form-control',
        'size': 10,}))
    caja = django_filters.NumberFilter(label='',lookup_expr='icontains', widget=forms.NumberInput(attrs=
        {
        'placeholder': 'Caja', 
        'class': 'form-control',
        'size': 10,}))
    class Meta:
        model = Apertura
        fields = ['codigo_cliente','cliente','cuenta','estado','caja']

class DocumentoSueltoFilter(django_filters.FilterSet):
    codigo_cliente = django_filters.NumberFilter(label='', lookup_expr='icontains', widget=forms.NumberInput(attrs=
        {
        'placeholder': 'Cód. Cliente', 
        'class': 'form-control',
        'size': 10,}))
    agencia = django_filters.CharFilter(label='', lookup_expr='icontains', widget=forms.TextInput(attrs=
        {
        'placeholder': 'Agencia', 
        'class': 'form-control',
        'size': 20,}))
    cliente = django_filters.CharFilter(label='', lookup_expr='icontains', widget=forms.TextInput(attrs=
        {
        'placeholder': 'Cliente', 
        'class': 'form-control',
        'size': 20,}))
    operacion = django_filters.NumberFilter(label='', lookup_expr='icontains', widget=forms.NumberInput(attrs=
        {
        'placeholder': 'Operación', 
        'class': 'form-control',
        'size': 10,}))
    estado = django_filters.CharFilter(label='', lookup_expr='icontains', widget=forms.TextInput(attrs=
        {
        'placeholder': 'Estado', 
        'class': 'form-control',
        'size': 25,}))
    caja = django_filters.NumberFilter(label='',lookup_expr='icontains', widget=forms.NumberInput(attrs=
        {
        'placeholder': 'Caja', 
        'class': 'form-control',
        'size': 5,}))
    class Meta:
        model = DocumentosSueltos
        fields = ['codigo_cliente','agencia','cliente','operacion','estado','caja']

class PolizaFilter(django_filters.FilterSet):
    codigo_cliente = django_filters.NumberFilter(label='', lookup_expr='icontains', widget=forms.NumberInput(attrs=
        {
        'placeholder': 'Cód. Cliente', 
        'class': 'form-control',
        'size': 10,}))
    cliente = django_filters.CharFilter(label='', lookup_expr='icontains', widget=forms.TextInput(attrs=
        {
        'placeholder': 'Cliente', 
        'class': 'form-control',
        'size': 10,}))
    poliza = django_filters.NumberFilter(label='', lookup_expr='icontains', widget=forms.NumberInput(attrs=
        {
        'placeholder': 'Póliza', 
        'class': 'form-control',
        'size': 10,}))
    estado = django_filters.CharFilter(label='', lookup_expr='icontains', widget=forms.TextInput(attrs=
        {
        'placeholder': 'Estado', 
        'class': 'form-control',
        'size': 10,}))    
    caja = django_filters.NumberFilter(label='',lookup_expr='icontains', widget=forms.NumberInput(attrs=
        {
        'placeholder': 'Caja', 
        'class': 'form-control',
        'size': 10,}))
    class Meta:
        model = Poliza
        fields = ['codigo_cliente','cliente','poliza','estado', 'caja']

class CajaFilter(django_filters.FilterSet):
    codigo_cliente = django_filters.NumberFilter(label='Cód. Cliente', lookup_expr='icontains')
    cliente = django_filters.CharFilter(label='Cliente', lookup_expr='icontains')
    caja = django_filters.NumberFilter(label='Caja',lookup_expr='icontains')
    class Meta:
        model = Poliza
        fields = ['codigo_cliente','cliente','caja']

class ObservacionFilter(django_filters.FilterSet):
    empate__distribucion__desembolso__onbase = django_filters.NumberFilter(label='', lookup_expr='icontains', widget=forms.NumberInput(attrs=
        {
        'placeholder': 'Onbase', 
        'class': 'form-control',
        'size': 10,}))
    destino = django_filters.CharFilter(label='', lookup_expr='icontains', widget=forms.TextInput(attrs=
        {
        'placeholder': 'Destino', 
        'class': 'form-control',
        'size': 10,}))    
    categoria__nombre = django_filters.CharFilter(label='', lookup_expr='icontains', widget=forms.TextInput(attrs=
        {
        'placeholder': 'Categoría', 
        'class': 'form-control',
        'size': 10,}))
    sub_categoria__nombre = django_filters.CharFilter(label='', lookup_expr='icontains', widget=forms.TextInput(attrs=
        {
        'placeholder': 'Sub Categoría', 
        'class': 'form-control',
        'size': 10,}))
    observacion__nombre = django_filters.CharFilter(label='', lookup_expr='icontains', widget=forms.TextInput(attrs=
        {
        'placeholder': 'Obseración', 
        'class': 'form-control',
        'size': 10,}))
    estado = django_filters.CharFilter(label='',lookup_expr='icontains', widget=forms.TextInput(attrs=
        {
        'placeholder': 'Estado', 
        'class': 'form-control',
        'size': 10,}))
    class Meta:
        model = Observaciones
        fields = ['empate__distribucion__desembolso__onbase', 'destino','categoria__nombre','sub_categoria__nombre','observacion__nombre','estado']

class CorrespondenciaFilter(django_filters.FilterSet):
    codigo_barras = django_filters.NumberFilter(label='', lookup_expr='icontains', widget=forms.NumberInput(attrs=
        {
        'placeholder': 'Cod. Barras', 
        'class': 'form-control',
        'size': 10,}))
    fecha_envio = django_filters.DateFilter(label='', lookup_expr='icontains', widget=DatePickerInput(attrs=
        {
        'placeholder': 'Fecha Envío', 
        'class': 'form-control',
        'size': 10,}))
    contenido = django_filters.CharFilter(label='', lookup_expr='icontains', widget=forms.TextInput(attrs=
        {
        'placeholder': 'Contenido', 
        'class': 'form-control',
        'size': 10,}))
    estado = django_filters.CharFilter(label='',lookup_expr='icontains', widget=forms.TextInput(attrs=
        {
        'placeholder': 'Estado', 
        'class': 'form-control',
        'size': 10,}))
    class Meta:
        model = Observaciones
        fields = ['codigo_barras','fecha_envio','contenido','estado']

class PrestamoFilter(django_filters.FilterSet):
    sobre__codigo = django_filters.NumberFilter(label='', lookup_expr='icontains', widget=forms.TextInput(attrs=
        {
        'placeholder': 'Cod. Cliente', 
        'class': 'form-control',
        'size': 10,}))
    sobre__nombre = django_filters.CharFilter(label='', lookup_expr='icontains', widget=forms.TextInput(attrs=
        {
        'placeholder': 'Nombre', 
        'class': 'form-control',
        'size': 10,}))
    estado = django_filters.CharFilter(label='',lookup_expr='icontains', widget=forms.TextInput(attrs=
        {
        'placeholder': 'Estado', 
        'class': 'form-control',
        'size': 10,}))
    class Meta:
        model = Prestamo
        fields = ['sobre__codigo','sobre__nombre','estado']

class SobreFilter(django_filters.FilterSet):
    codigo = django_filters.NumberFilter(label='', lookup_expr='icontains', widget=forms.TextInput(attrs=
        {
        'placeholder': 'Código', 
        'class': 'form-control',
        'size': 10,}))
    nombre = django_filters.CharFilter(label='', lookup_expr='icontains', widget=forms.TextInput(attrs=
        {
        'placeholder': 'Nombre', 
        'class': 'form-control',
        'size': 10,}))
    estado = django_filters.CharFilter(label='',lookup_expr='icontains', widget=forms.TextInput(attrs=
        {
        'placeholder': 'Estado', 
        'class': 'form-control',
        'size': 10,}))
    ubicacion = django_filters.CharFilter(label='',lookup_expr='icontains', widget=forms.TextInput(attrs=
        {
        'placeholder': 'Ubicación', 
        'class': 'form-control',
        'size': 10,}))
    class Meta:
        model = Sobre
        fields = ['codigo','nombre','estado','ubicacion']

class InmuebleFilter(django_filters.FilterSet):
    escritura_publica = django_filters.CharFilter(label='', lookup_expr='icontains', widget=forms.TextInput(attrs=
        {
        'placeholder': 'Escritura Pública', 
        'class': 'form-control',
        'size': 10,}))
    folio = django_filters.NumberFilter(label='', lookup_expr='icontains', widget=forms.NumberInput(attrs=
        {
        'placeholder': 'Folio', 
        'class': 'form-control',
        'size': 10,}))
    class Meta:
        model = Inmueble
        fields = ['escritura_publica','folio']

class VehiculoFilter(django_filters.FilterSet):
    crpva = django_filters.NumberFilter(label='', lookup_expr='icontains', widget=forms.NumberInput(attrs=
        {
        'placeholder': 'CRPVA', 
        'class': 'form-control',
        'size': 10,}))
    placa = django_filters.CharFilter(label='', lookup_expr='icontains', widget=forms.TextInput(attrs=
        {
        'placeholder': 'Placa', 
        'class': 'form-control',
        'size': 10,}))
    class Meta:
        model = Inmueble
        fields = ['crpva','placa']

class LevantamientoFilter(django_filters.FilterSet):
    codigo_cliente = django_filters.NumberFilter(label='', lookup_expr='icontains', widget=forms.NumberInput(attrs=
        {
        'placeholder': 'Cód. Cliente', 
        'class': 'form-control',
        'size': 10,}))
    operacion = django_filters.NumberFilter(label='', lookup_expr='icontains', widget=forms.NumberInput(attrs=
        {
        'placeholder': 'Operación', 
        'class': 'form-control',
        'size': 10,}))
    cliente = django_filters.CharFilter(label='', lookup_expr='icontains', widget=forms.TextInput(attrs=
        {
        'placeholder': 'Cliente', 
        'class': 'form-control',
        'size': 10,}))
    onbase = django_filters.NumberFilter(label='', lookup_expr='icontains', widget=forms.NumberInput(attrs=
        {
        'placeholder': 'Onbase', 
        'class': 'form-control',
        'size': 10,}))
    estado = django_filters.CharFilter(label='', lookup_expr='icontains', widget=forms.TextInput(attrs=
        {
        'placeholder': 'Estado', 
        'class': 'form-control',
        'size': 10,}))
    class Meta:
        model = Inmueble
        fields = ['codigo_cliente','operacion','cliente','onbase','estado']

class TareaFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(label='', lookup_expr='icontains', widget=forms.TextInput(attrs=
        {
        'placeholder': 'Tarea', 
        'class': 'form-control',
        'size': 10,}))
    tiempo = django_filters.NumberFilter(label='', lookup_expr='icontains', widget=forms.NumberInput(attrs=
        {
        'placeholder': 'Tiempo', 
        'class': 'form-control',
        'size': 10,}))
    analista_asignado__nombre = django_filters.CharFilter(label='', lookup_expr='icontains', widget=forms.TextInput(attrs=
        {
        'placeholder': 'Analista Asignado', 
        'class': 'form-control',
        'size': 10,}))
    estado = django_filters.CharFilter(label='', lookup_expr='icontains', widget=forms.TextInput(attrs=
        {
        'placeholder': 'Estado', 
        'class': 'form-control',
        'size': 10,}))
    class Meta:
        model = Tarea
        fields = ['nombre','tiempo','analista_asignado__nombre','estado']

class DesembolsoFilter(django_filters.FilterSet):
    codigo_cliente = django_filters.NumberFilter(label='', lookup_expr='icontains', widget=forms.NumberInput(attrs=
        {
        'placeholder': 'Cod. Cliente', 
        'class': 'form-control',
        'size': 10,}))
    onbase = django_filters.NumberFilter(label='', lookup_expr='icontains', widget=forms.NumberInput(attrs=
        {
        'placeholder': 'Onbase', 
        'class': 'form-control',
        'size': 10,}))
    operacion = django_filters.NumberFilter(label='', lookup_expr='icontains', widget=forms.NumberInput(attrs=
        {
        'placeholder': 'Operación', 
        'class': 'form-control',
        'size': 10,}))
    cliente = django_filters.CharFilter(label='', lookup_expr='icontains', widget=forms.TextInput(attrs=
        {
        'placeholder': 'Cliente', 
        'class': 'form-control',
        'size': 10,}))
    fecha_desembolso = django_filters.DateFilter(label='', lookup_expr='iexact', widget=DatePickerInput(attrs=
        {
        'placeholder': 'Fecha Desembolso', 
        'class': 'form-control',
        'size': 10,}))
    estado = django_filters.CharFilter(label='', lookup_expr='icontains', widget=forms.TextInput(attrs=
        {
        'placeholder': 'Estado', 
        'class': 'form-control',
        'size': 10,}))    
    class Meta:
        model = Desembolsos
        fields = ['codigo_cliente','onbase','operacion','cliente','fecha_desembolso']

class HistorialFilter(django_filters.FilterSet):
    
    content_type__model = django_filters.CharFilter(label='', lookup_expr='icontains', widget=forms.TextInput(attrs=
        {
        'placeholder': 'Modelo', 
        'class': 'form-control',
        'size': 10,}))
    action = django_filters.CharFilter(method= 'accion', label='', lookup_expr='icontains', widget=forms.TextInput(attrs=
        {
        'placeholder': 'Acción', 
        'class': 'form-control',
        'size': 10,}))
    actor__username = django_filters.CharFilter(label='', lookup_expr='icontains', widget=forms.TextInput(attrs=
        {
        'placeholder': 'Usuario', 
        'class': 'form-control',
        'size': 10,}))
    timestamp = django_filters.DateFilter(label='', lookup_expr='icontains', widget=DatePickerInput(attrs=
        {
        'placeholder': 'Fecha', 
        'class': 'form-control',
        'size': 10,}))
    
    
    def accion(self, queryset, name, value):

        value = value.upper()
        # create a dictionary string -> integer
        value_map = dict((v, k) for k, v in LogEntry.Action.choices)
        # get the integer value for the input string
        try:
            value = value_map[(value)]
        except:
            value = 0
        return queryset.filter(action=value)


    class Meta:
        model = LogEntry
        fields = ['content_type__model','action', 'actor__username', 'timestamp']
        
        
