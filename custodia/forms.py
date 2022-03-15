# from bootstrap_datepicker_plus.widgets import DatePickerInput
from .widgets import DatePickerInput, DateTimePickerInput
from crispy_forms.helper import FormHelper
from django import forms
from django.forms import SelectMultiple, fields
from .models import *
from django.db.models import Q


class DocumentosSueltosCrearForm(forms.ModelForm):
    class Meta:
        model = DocumentosSueltos
        fields = '__all__'
        labels = {
            'sobre':'Sobre',
            'sucursal':'Sucursal',
            'agencia':'Agencia',
            'descripcion':'Descripcion',
            'codigo_cliente':'Codigo Cliente',
            'cliente':'Cliente',
            'operacion':'Operacion',
            'oficina':'Oficina',
            'observacion_agencia':'Observacion Agencia',
            'observacion_custodia':'Observacion Custodia',
            'digitalizado':'Digitalizado',
            'usuario_creacion':'Usuario Creacion',
            'usuario_modificacion':'Usuario Modificacion',
            'fecha_creacion':'Fecha Creacion',
            'fecha_modificacion':'Fecha Modificacion',
            'bloque':'Bloque',
            'caja':'Caja',
            'estado': 'Estado'
        }

class DocumentosSueltosEditarForm(forms.ModelForm):
    usuario_creacion = forms.ModelChoiceField(queryset=Profile.objects.all(),disabled=True)
    class Meta:
        model = DocumentosSueltos
        fields = '__all__'  
        labels = {
            'sobre':'Sobre',
            'sucursal':'Sucursal',
            'agencia':'Agencia',
            'descripcion':'Descripcion',
            'codigo_cliente':'Codigo Cliente',
            'cliente':'Cliente',
            'operacion':'Operacion',
            'oficina':'Oficina',
            'observacion_agencia':'Observacion Agencia',
            'observacion_custodia':'Observacion Custodia',
            'digitalizado':'Digitalizado',
            'usuario_creacion':'Usuario Creacion',
            'usuario_modificacion':'Usuario Modificacion',
            'fecha_creacion':'Fecha Creacion',
            'fecha_modificacion':'Fecha Modificacion',
            'bloque':'Bloque',
            'caja':'Caja',
            'estado': 'Estado'
        }   

class DesembolsoCrearForm(forms.ModelForm):
    class Meta:
        model =Desembolsos
        fields = '__all__'
        labels = {
            'fecha_desembolso':'Fecha Desembolso',
            'producto':'Producto',
            'tipo':'Tipo',
            'codigo_cliente':'Código Cliente',
            'cliente':'Cliente',
            'operacion':'Operación',
            'monto':'Monto',
            'desembolso_parcial':'Desembolso Parcial',
            'ejecutivo':'Ejecutivo',
            'onbase':'Onbase',
            'sucursal':'Sucursal',
            'agencia':'Agencia',
            'tipo_banca':'Tipo Banca',
            'tipo_trabajo':'Tipo Trabajo',
            'instancia_aprobacion':'Instancia Aprobación',
            'estado':'Estado',
        }
        widgets = {
            'fecha_desembolso': DatePickerInput(format ='%d/%m/%Y')
        }
       

class DesembolsoEditarForm(forms.ModelForm):
    usuario_creacion = forms.ModelChoiceField(queryset=Profile.objects.all(), disabled=True)
    class Meta:
        model =Desembolsos
        fields = '__all__'
        labels = {
            'fecha_desembolso':'Fecha Desembolso',
            'producto':'Producto',
            'tipo':'Tipo',
            'codigo_cliente':'Código Cliente',
            'cliente':'Cliente',
            'operacion':'Operación',
            'monto':'Monto',
            'desembolso_parcial':'Desembolso Parcial',
            'ejecutivo':'Ejecutivo',
            'onbase':'Onbase',
            'sucursal':'Sucursal',
            'agencia':'Agencia',
            'tipo_banca':'Tipo Banca',
            'tipo_trabajo':'Tipo Trabajo',
            'instancia_aprobacion':'Instancia Aprobación',
            'estado':'Estado',
        }
        widgets = {
            'fecha_desembolso': DatePickerInput()
        }

class DesestimadaCrearForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DesestimadaCrearForm, self).__init__(*args, **kwargs)
        self.fields['estado'].initial = 'Desestimada'
        self.fields['estado'].disabled = True
    codigo_cliente = forms.IntegerField(required=True, widget= forms.widgets.NumberInput())
    onbase = forms.IntegerField(required=True, widget= forms.widgets.NumberInput())
    operacion = forms.IntegerField(required=True, widget= forms.widgets.NumberInput())
    monto = forms.DecimalField(required=True, widget= forms.widgets.NumberInput())
    cliente = forms.CharField(required=True, widget= forms.widgets.TextInput())
    tipo = forms.CharField(required=True, widget= forms.widgets.TextInput())
    sucursal = forms.CharField(required=True, widget= forms.widgets.TextInput())
    monto = forms.CharField(required=True, widget= forms.widgets.TextInput())
    
    class Meta:
        model = Desembolsos
        fields = '__all__'
        labels = {
            'fecha_desembolso':'Fecha Desembolso',
            'producto':'Producto',
            'tipo':'Tipo',
            'codigo_cliente':'Código Cliente',
            'cliente':'Cliente',
            'operacion':'Operación',
            'monto':'Monto',
            'desembolso_parcial':'Desembolso Parcial',
            'ejecutivo':'Ejecutivo',
            'onbase':'Onbase',
            'sucursal':'Sucursal',
            'agencia':'Agencia',
            'tipo_banca':'Tipo Banca',
            'tipo_trabajo':'Tipo Trabajo',
            'instancia_aprobacion':'Instancia Aprobación',
            'estado':'Estado',
        }
        widgets = {
            'fecha_desembolso': DatePickerInput(format ='%d/%m/%Y')
        }        

class EmpateForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     user_id = kwargs.pop('user_id', None)
    #     super(EmpateForm,self).__init__(*args,**kwargs)
    #     self.fields['distribucion'].queryset=Distribucion.objects.filter(analista_asignado=user_id)
    class Meta:
    #     distribucion = forms.ModelChoiceField(queryset=Distribucion.objects.all(),widget=forms.Select(attrs={
    #     'class' : 'select2'
    # }), required=False) 
        model = Empate
        fields = '__all__'
        exclude = ['distribucion','tiempo_empate']
        labels = {
            'estado':'Estado',
            'tipo_operacion':'Tipo Operacion',
            'onbase_referencia':'Onbase Paralelo',
            'propuesta':'Propuesta',
            'flujo':'Flujo',
            'respaldos_ingresos':'Respaldos Ingresos',
            'autorizacion_investigacion':'Aut. Investigacion',
            'cic_cod_con_ext':'CIC Con Ext',
            'cic_cod_sin_ext':'CIC Sin Ext',
            'cic_hist_con_ext':'CIC Hist Con Ext',
            'cic_hist_sin_ext':'CIC Hist Sin Ext',
            'cic_nombre':'CIC Nombre',
            'bi_codigo':'BI Código',
            'bi_nombre':'BI Nombre',
            'hoja_riesgos':'Hoja Riesgos',
            'lista_confidencial':'Lista Confidencial',
            'atencion_preferente':'Atencion Preferente',
            'retenciones_judiciales':'Ret. Judiciales',
            'cliente_pleno_oportuno_pago':'CPOP',
            'segip':'Segip',
            'carnet_identidad':'Carnet Identidad',
            'cic_cod_con_ext_desembolso':'CIC Con Ext',
            'cic_cod_sin_ext_desembolso':'CIC Sin Ext',
            'cic_nombre_desembolso':'CIC Nombre',
            'bi_codigo_desembolso':'BI Código',
            'bi_nombre_desembolso':'BI Nombre',
            'plan_pagos':'Plan Pagos',
            'nota_credito':'Nota Crédito',
            'formulario_solicitud':'Formulario Solicitud',
            'verif_domiciliaria':'Verif Domiciliaria',
            'verif_laboral':'Verif Laboral',
            'ddjj_bienes':'DDJJ Bienes',
            'copia_boleta_garantia':'Copia Boleta Garantia',
            'solicitud_seguro_desgravamen':'Solicitud Seguro Desgravamen',
            'solicitud_seguro_cesantia':'Solicitud Seguro Cesantía',
            'solicitud_seguro_dima':'Solicitud Seguro Dima',
            'notas':'Notas',
            'numero_caja':'Numero Caja',
            'usuario_empate':'Usuario Empate',
        } 

class DistribucionCrearForm(forms.ModelForm):
    desembolso = forms.ModelChoiceField(queryset=Desembolsos.objects.filter(Q(estado='Recibido')|Q(estado='Desestimada')),widget=forms.Select(attrs={
        'class' : 'select2'
    }), required=True) 
    analista_asignado = forms.ModelChoiceField(queryset=Profile.objects.filter(tarea__nombre="Empate", tarea__estado="Asignado"),widget=forms.Select(attrs={
        
    })) 
    class Meta:
        model = Distribucion
        fields = '__all__'
        # exclude = ['analista_distribucion']
        labels = {
            'desembolso':'Desembolso',
            'analista_asignado':'Analista Asignado', 
            'tipo':'Tipo de Operación', 
            }
class DistribucionEditarForm(forms.ModelForm):
    usuario_creacion = forms.ModelChoiceField(queryset=Profile.objects.all(), disabled=True)
    analista_asignado = forms.ModelChoiceField(queryset=Profile.objects.all(),widget=forms.Select(attrs={
        'class' : 'select2'
    }), required=True) 
    class Meta:
        model = Distribucion
        fields = '__all__'
        labels = {
            'desembolso':'Desembolso',
            'fecha_recepcion':'Fecha de Recepción',
            'analista_asignado':'Analista Asignado',
            'tipo':'Tipo de Operación', 
            }

class ContratosCrearForm(forms.ModelForm):
    desembolso = forms.ModelChoiceField(queryset=Desembolsos.objects.all(),widget=forms.Select(attrs={
        'class' : 'select2'
    }), required=False)
    class Meta:
        model = Contratos
        fields = '__all__'
        # exclude = []
        labels = {
            'ubicacion':'Ubicación',
            'adenda':'Adenda',
            'minuta':'Minuta',
            'cantidad_minuta':'',
            'estado_minuta':'',
            'testimonio':'Testimonio',
            'num_testimonio':'',
            'reg_testimonio':'',
            'cantidad_testimonio':'',
            'estado_testimonio':'',
            'contrato_privado':'Contrato Privado',
            'cantidad_contrato':'',
            'estado_contrato':'',
            'rec_firmas':'Rec Firmas',
            'num_rec_firmas':'',
            'reg_rec_firmas':'',
            'cantidad_rec_firmas':'',
            'estado_rec_firmas':'',
            'cert_tdr':'Cert Tdr',
            'cantidad_cert_tdr':'',
            'estado_cert_tdr':'',
            'cert_desgravamen':'Cert Desgravamen',
            'cantidad_cert_desgravamen':'',
            'estado_cert_desgravamen':'',
            'seguro_cesantia':'Seguro Cesantia',
            'cantidad_seguro_cesantia':'',
            'estado_seguro_cesantia':'',
            'seguro_dima':'Seguro Dima',
            'cantidad_seguro_dima':'',
            'estado_seguro_dima':'',
            'anexos_seguros':'Anexos Seguros',
            'cert_gravamen':'Cert Gravamen',
            'cantidad_cert_gravamen':'',
            'estado_cert_gravamen':'',
            'glosa_cert_gravamen':'',
            'reg_cert_gravamen':'',
            'cert_fundempresa':'Cert Fundempresa',
            'cantidad_cert_fundempresa':'',
            'estado_cert_fundempresa':'',
            'glosa_cert_fundempresa':'',
            'reg_cert_fundempresa':'',
            'folio':'Folio',
            'cantidad_folio':'',
            'estado_folio':'',
            'glosa_folio':'',
            'reg_folio':'',
            'inf_rapido':'Inf Rapido',
            'cantidad_inf_rapido':'',
            'estado_inf_rapido':'',
            'glosa_inf_rapido':'',
            'reg_inf_rapido':'',
            'fecha_envio':'Fecha Envio',
            'fecha_recepcion':'Fecha Recepcion',
            'ubicacion': 'Ubicacion',
            'notas':'Notas',
            'usuario_legal':'Usuario Legal',
            'usuario_empate':'Usuario Empate',
        }

class ContratosEditarForm(forms.ModelForm):
    desembolso = forms.ModelChoiceField(queryset=Desembolsos.objects.all(),widget=forms.Select(attrs={
        'class' : 'select2'
    }), required=False)
    usuario_creacion = forms.ModelChoiceField(queryset=Desembolsos.objects.all(),widget=forms.Select(), required=False, disabled=True)
    class Meta:
        model = Contratos
        fields = '__all__'
        exclude = ['usuario_creacion']
        labels = {
            'ubicacion':'Ubicación',
            'adenda':'Adenda',
            'minuta':'Minuta',
            'cantidad_minuta':'',
            'estado_minuta':'',
            'testimonio':'Testimonio',
            'num_testimonio':'',
            'reg_testimonio':'',
            'cantidad_testimonio':'',
            'estado_testimonio':'',
            'contrato_privado':'Contrato Privado',
            'cantidad_contrato':'',
            'estado_contrato':'',
            'rec_firmas':'Rec Firmas',
            'num_rec_firmas':'',
            'reg_rec_firmas':'',
            'cantidad_rec_firmas':'',
            'estado_rec_firmas':'',
            'cert_tdr':'Cert Tdr',
            'cantidad_cert_tdr':'',
            'estado_cert_tdr':'',
            'cert_desgravamen':'Cert Desgravamen',
            'cantidad_cert_desgravamen':'',
            'estado_cert_desgravamen':'',
            'seguro_cesantia':'Seguro Cesantia',
            'cantidad_seguro_cesantia':'',
            'estado_seguro_cesantia':'',
            'seguro_dima':'Seguro Dima',
            'cantidad_seguro_dima':'',
            'estado_seguro_dima':'',
            'anexos_seguros':'Anexos Seguros',
            'cert_gravamen':'Cert Gravamen',
            'cantidad_cert_gravamen':'',
            'estado_cert_gravamen':'',
            'glosa_cert_gravamen':'',
            'reg_cert_gravamen':'',
            'cert_fundempresa':'Cert Fundempresa',
            'cantidad_cert_fundempresa':'',
            'estado_cert_fundempresa':'',
            'glosa_cert_fundempresa':'',
            'reg_cert_fundempresa':'',
            'folio':'Folio',
            'cantidad_folio':'',
            'estado_folio':'',
            'glosa_folio':'',
            'reg_folio':'',
            'inf_rapido':'Inf Rapido',
            'cantidad_inf_rapido':'',
            'estado_inf_rapido':'',
            'glosa_inf_rapido':'',
            'reg_inf_rapido':'',
            'fecha_envio':'Fecha Envio',
            'fecha_recepcion':'Fecha Recepcion',
            'ubicacion': 'Ubicacion',
            'notas':'Notas',
            'usuario_legal':'Usuario Legal',
            'usuario_empate':'Usuario Empate',
        }
class ContratosEditarEmpateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ContratosEditarEmpateForm, self).__init__(*args, **kwargs)
        self.fields['adenda'].disabled = True

        self.fields['minuta'].disabled = True
        self.fields['cantidad_minuta'].disabled = True
        self.fields['estado_minuta'].disabled = True

        self.fields['testimonio'].disabled = True
        self.fields['cantidad_testimonio'].disabled = True
        self.fields['estado_testimonio'].disabled = True
        self.fields['num_testimonio'].disabled = True

        self.fields['contrato_privado'].disabled = True
        self.fields['cantidad_contrato'].disabled = True
        self.fields['estado_contrato'].disabled = True

        self.fields['rec_firmas'].disabled = True
        self.fields['cantidad_rec_firmas'].disabled = True
        self.fields['estado_rec_firmas'].disabled = True
        self.fields['num_rec_firmas'].disabled = True
        
        self.fields['cert_tdr'].disabled = True
        self.fields['cantidad_cert_tdr'].disabled = True
        self.fields['estado_cert_tdr'].disabled = True
        
        self.fields['cert_desgravamen'].disabled = True
        self.fields['cantidad_cert_desgravamen'].disabled = True
        self.fields['estado_cert_tdr'].disabled = True

        self.fields['seguro_cesantia'].disabled = True
        self.fields['cantidad_seguro_cesantia'].disabled = True
        self.fields['estado_seguro_cesantia'].disabled = True

        self.fields['seguro_dima'].disabled = True
        self.fields['cantidad_seguro_dima'].disabled = True
        self.fields['estado_seguro_dima'].disabled = True

        self.fields['anexos_seguros'].disabled = True

        self.fields['cert_gravamen'].disabled = True
        self.fields['cantidad_cert_gravamen'].disabled = True
        self.fields['estado_cert_gravamen'].disabled = True
        self.fields['glosa_cert_gravamen'].disabled = True

        self.fields['cert_fundempresa'].disabled = True
        self.fields['cantidad_cert_fundempresa'].disabled = True
        self.fields['estado_cert_fundempresa'].disabled = True
        self.fields['glosa_cert_fundempresa'].disabled = True

        self.fields['folio'].disabled = True
        self.fields['cantidad_folio'].disabled = True
        self.fields['estado_folio'].disabled = True
        self.fields['glosa_folio'].disabled = True

        self.fields['inf_rapido'].disabled = True
        self.fields['cantidad_inf_rapido'].disabled = True
        self.fields['estado_inf_rapido'].disabled = True
        self.fields['glosa_inf_rapido'].disabled = True

        self.fields['notas'].disabled = True

    desembolso = forms.ModelChoiceField(queryset=Desembolsos.objects.all(),widget=forms.Select(attrs={
        'class' : 'select2'
    }), required=False, disabled=True)
    usuario_modificacion_legal = forms.ModelChoiceField(queryset=Profile.objects.all(),widget=forms.Select(), required=False, disabled=True)
    class Meta:
        model = Contratos
        fields = '__all__'
        exclude = ['usuario_creacion']
        labels = {
            'ubicacion':'Ubicación',
            'adenda':'Adenda',
            'minuta':'Minuta',
            'cantidad_minuta':'',
            'estado_minuta':'',
            'testimonio':'Testimonio',
            'num_testimonio':'',
            'reg_testimonio':'',
            'cantidad_testimonio':'',
            'estado_testimonio':'',
            'contrato_privado':'Contrato Privado',
            'cantidad_contrato':'',
            'estado_contrato':'',
            'rec_firmas':'Rec Firmas',
            'num_rec_firmas':'',
            'reg_rec_firmas':'',
            'cantidad_rec_firmas':'',
            'estado_rec_firmas':'',
            'cert_tdr':'Cert Tdr',
            'cantidad_cert_tdr':'',
            'estado_cert_tdr':'',
            'cert_desgravamen':'Cert Desgravamen',
            'cantidad_cert_desgravamen':'',
            'estado_cert_desgravamen':'',
            'seguro_cesantia':'Seguro Cesantia',
            'cantidad_seguro_cesantia':'',
            'estado_seguro_cesantia':'',
            'seguro_dima':'Seguro Dima',
            'cantidad_seguro_dima':'',
            'estado_seguro_dima':'',
            'anexos_seguros':'Anexos Seguros',
            'cert_gravamen':'Cert Gravamen',
            'cantidad_cert_gravamen':'',
            'estado_cert_gravamen':'',
            'glosa_cert_gravamen':'',
            'reg_cert_gravamen':'',
            'cert_fundempresa':'Cert Fundempresa',
            'cantidad_cert_fundempresa':'',
            'estado_cert_fundempresa':'',
            'glosa_cert_fundempresa':'',
            'reg_cert_fundempresa':'',
            'folio':'Folio',
            'cantidad_folio':'',
            'estado_folio':'',
            'glosa_folio':'',
            'reg_folio':'',
            'inf_rapido':'Inf Rapido',
            'cantidad_inf_rapido':'',
            'estado_inf_rapido':'',
            'glosa_inf_rapido':'',
            'reg_inf_rapido':'',
            'fecha_envio':'Fecha Envio',
            'fecha_recepcion':'Fecha Recepcion',
            'ubicacion': 'Ubicacion',
            'notas':'Notas',
            'usuario_legal':'Usuario Legal',
            'usuario_empate':'Usuario Empate',
        }

class ContratosEmpateForm(forms.ModelForm):
    desembolso = forms.ModelChoiceField(queryset=Desembolsos.objects.all(),widget=forms.Select(attrs={
        'class' : 'select2'
    }), required=False)
    # usuario_legal = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    class Meta:
        model = Contratos
        fields = '__all__'
        # exclude = ['usuario_empate']
        labels = {
            'ubicacion':'Ubicación',
            'adenda':'Adenda',
            'minuta':'Minuta',
            'cantidad_minuta':'',
            'estado_minuta':'',
            'testimonio':'Testimonio',
            'num_testimonio':'',
            'reg_testimonio':'',
            'cantidad_testimonio':'',
            'estado_testimonio':'',
            'contrato_privado':'Contrato Privado',
            'cantidad_contrato':'',
            'estado_contrato':'',
            'rec_firmas':'Rec Firmas',
            'num_rec_firmas':'',
            'reg_rec_firmas':'',
            'cantidad_rec_firmas':'',
            'estado_rec_firmas':'',
            'cert_tdr':'Cert Tdr',
            'cantidad_cert_tdr':'',
            'estado_cert_tdr':'',
            'cert_desgravamen':'Cert Desgravamen',
            'cantidad_cert_desgravamen':'',
            'estado_cert_desgravamen':'',
            'seguro_cesantia':'Seguro Cesantia',
            'cantidad_seguro_cesantia':'',
            'estado_seguro_cesantia':'',
            'seguro_dima':'Seguro Dima',
            'cantidad_seguro_dima':'',
            'estado_seguro_dima':'',
            'anexos_seguros':'Anexos Seguros',
            'cert_gravamen':'Cert Gravamen',
            'cantidad_cert_gravamen':'',
            'estado_cert_gravamen':'',
            'glosa_cert_gravamen':'',
            'reg_cert_gravamen':'',
            'cert_fundempresa':'Cert Fundempresa',
            'cantidad_cert_fundempresa':'',
            'estado_cert_fundempresa':'',
            'glosa_cert_fundempresa':'',
            'reg_cert_fundempresa':'',
            'folio':'Folio',
            'cantidad_folio':'',
            'estado_folio':'',
            'glosa_folio':'',
            'reg_folio':'',
            'inf_rapido':'Inf Rapido',
            'cantidad_inf_rapido':'',
            'estado_inf_rapido':'',
            'glosa_inf_rapido':'',
            'reg_inf_rapido':'',
            'fecha_envio':'Fecha Envio',
            'fecha_recepcion':'Fecha Recepcion',
            'ubicacion': 'Ubicacion',
            'notas':'Notas',
            'usuario_legal':'Usuario Legal',
            'usuario_empate':'Usuario Empate',
        }
class ContratosEmpateEditarForm(forms.ModelForm):
    desembolso = forms.ModelChoiceField(queryset=Desembolsos.objects.all(),widget=forms.Select(attrs={
        'class' : 'select2'
    }), required=False)
    usuario_legal = forms.ModelChoiceField(queryset=Profile.objects.all(),required=False, disabled=True)
    class Meta:
        model = Contratos
        fields = '__all__'
        exclude = ['usuario_creacion']
        labels = {
            'ubicacion':'Ubicación',
            'adenda':'Adenda',
            'minuta':'Minuta',
            'cantidad_minuta':'',
            'estado_minuta':'',
            'testimonio':'Testimonio',
            'num_testimonio':'',
            'reg_testimonio':'',
            'cantidad_testimonio':'',
            'estado_testimonio':'',
            'contrato_privado':'Contrato Privado',
            'cantidad_contrato':'',
            'estado_contrato':'',
            'rec_firmas':'Rec Firmas',
            'num_rec_firmas':'',
            'reg_rec_firmas':'',
            'cantidad_rec_firmas':'',
            'estado_rec_firmas':'',
            'cert_tdr':'Cert Tdr',
            'cantidad_cert_tdr':'',
            'estado_cert_tdr':'',
            'cert_desgravamen':'Cert Desgravamen',
            'cantidad_cert_desgravamen':'',
            'estado_cert_desgravamen':'',
            'seguro_cesantia':'Seguro Cesantia',
            'cantidad_seguro_cesantia':'',
            'estado_seguro_cesantia':'',
            'seguro_dima':'Seguro Dima',
            'cantidad_seguro_dima':'',
            'estado_seguro_dima':'',
            'anexos_seguros':'Anexos Seguros',
            'cert_gravamen':'Cert Gravamen',
            'cantidad_cert_gravamen':'',
            'estado_cert_gravamen':'',
            'glosa_cert_gravamen':'',
            'reg_cert_gravamen':'',
            'cert_fundempresa':'Cert Fundempresa',
            'cantidad_cert_fundempresa':'',
            'estado_cert_fundempresa':'',
            'glosa_cert_fundempresa':'',
            'reg_cert_fundempresa':'',
            'folio':'Folio',
            'cantidad_folio':'',
            'estado_folio':'',
            'glosa_folio':'',
            'reg_folio':'',
            'inf_rapido':'Inf Rapido',
            'cantidad_inf_rapido':'',
            'estado_inf_rapido':'',
            'glosa_inf_rapido':'',
            'reg_inf_rapido':'',
            'fecha_envio':'Fecha Envio',
            'fecha_recepcion':'Fecha Recepcion',
            'ubicacion': 'Ubicacion',
            'notas':'Notas',
            'usuario_legal':'Usuario Legal',
            'usuario_empate':'Usuario Empate',
        }

class DocumentosSueltosAgenciaForm(forms.ModelForm):
    class Meta:
        model = DocumentosSueltos
        fields = '__all__'
        exclude =['usuario_envio','usuario_recepcion','fecha_recepcion','observacion_custodia' ]

class DocumentosSueltosCustodiaForm(forms.ModelForm):
    class Meta:
        model = DocumentosSueltos
        fields = '__all__'
        exclude =['usuario_envio','usuario_recepcion','fecha_envio','observacion_agencia' ]

class ObservacionesCrearForm(forms.ModelForm):
    class Meta:
        model = Observaciones
        fields = '__all__'
        exclude = ['usuario_revision','fecha_modificacion']
        labels = {
            'empate':'Empate',
            'destino':'Destino',
            'categoria':'Categoria',
            'sub_categoria':'Sub Categoria',
            'observacion':'Observacion',
            'glosa':'Glosa',
            'estado':'Estado',
            'fecha_observación':'Fecha Observación',
            'comentarios_custodia':'Comentarios Custodia',
            'comentarios_area_observada':'Comentarios Area Observada',
            'usuario_observacion':'Usuario Observacion',
        }
    def __init__(self, *args,**kwargs):
        super().__init__(*args,**kwargs)

        # self.fields['sub_categoria'].queryset = CategoriaObservacion.objects.none()
        # self.fields['observacion'].queryset = ItemObservacion.objects.none()
        if 'categoria' in self.data:
            try:
                categoria_id=int(self.data.get('categoria'))
                self.fields['sub_categoria'].queryset=SubCategoriaObservacion.objects.filter(categoria_id=categoria_id).order_by('nombre')
            except (ValueError, TypeError):
                pass
        elif 'sub_categoria' in self.data:
            try:
                sub_categoria_id=int(self.data.get('sub_categoria'))
                self.fields['observacion'].queryset=ItemObservacion.objects.filter(sub_categoria_id=sub_categoria_id).order_by('nombre')
            except (ValueError, TypeError):
                pass
        # elif self.instance.pk:
        #     self.fields['sub_categoria'].queryset=self.instance.categoria.sub_categoria_set.all().order_by('nombre')
        #     self.fields['observacion'].queryset=self.instance.sub_categoria.observacion_set.all().order_by('nombre')

class ObservacionesEditarForm(forms.ModelForm):
    empate = forms.ModelChoiceField(queryset=Empate.objects.all(), disabled=True)
    destino = forms.CharField(disabled=True)
    categoria = forms.ModelChoiceField(queryset=CategoriaObservacion.objects.all(), disabled=True)
    sub_categoria = forms.ModelChoiceField(queryset=SubCategoriaObservacion.objects.all(), disabled=True)
    observacion = forms.ModelChoiceField(queryset=ItemObservacion.objects.all(), disabled=True)
    class Meta:
        model = Observaciones
        fields = '__all__'
        exclude = ['usuario_revision','fecha_modificacion']
        labels = {
            'empate':'Empate',
            'destino':'Destino',
            'categoria':'Categoria',
            'sub_categoria':'Sub Categoria',
            'observacion':'Observacion',
            'glosa':'Glosa',
            'estado':'Estado',
            'comentarios_custodia':'Comentarios Custodia',
            'comentarios_area_observada':'Comentarios Area Observada',
            'usuario_observacion':'Usuario Observacion',
        }
class LevantamientosCrearForm(forms.ModelForm):
    desembolso = forms.ModelChoiceField(queryset=Desembolsos.objects.all(),widget=forms.Select(attrs={
        'class' : 'select2'
    }), required=False)
    solicitante = forms.ModelChoiceField(queryset=Profile.objects.all(),widget=forms.Select(attrs={
        'class' : 'select2'
    }), required=False)
    enviado_a = forms.ModelChoiceField(queryset=Profile.objects.all(),widget=forms.Select(attrs={
        'class' : 'select2'
    }), required=False)
    class Meta:
        model = Levantamientos
        fields = '__all__'
        labels = {
            'tipo':'Tipo de garantía',
            'fecha_ingreso':'Fecha de Ingreso', 
            'sucursal':'Sucursal', 
            'referencia_legal':'Ref. Legal', 
            'operacion':'Operación', 
            'nombre':'Nombre', 
            'fisa':'Fisa', 
            'descripcion':'Descripción',  
            'fecha_entrega':'Fecha de entrega', 
            'fecha_devolucion':'Fecha de devolución', 
            'estado':'Estado', 
            'observaciones':'Observaciones', 
            'caja':'Caja', 
            'carpeta':'Carpeta'
            }
        widgets = {
            'fecha_ingreso' : DatePickerInput(),
            'fecha_entrega' : DatePickerInput(),
            'fecha_devolucion' : DatePickerInput(),
        }

class LevantamientosEditarForm(forms.ModelForm):
    enviado_a = forms.ModelChoiceField(queryset=Profile.objects.all(),widget=forms.Select(attrs={
        'class' : 'select2'
    }), required=False)
    class Meta:
        model = Levantamientos
        fields = '__all__'
        exclude = ['usuario_creacion']
        labels = {
            'tipo':'Tipo de garantía',
            'fecha_ingreso':'Fecha de Ingreso', 
            'sucursal':'Sucursal', 
            'referencia_legal':'Ref. Legal', 
            'operacion':'Operación', 
            'nombre':'Nombre', 
            'fisa':'Fisa', 
            'descripcion':'Descripción',  
            'fecha_entrega':'Fecha de entrega', 
            'fecha_devolucion':'Fecha de devolución', 
            'estado':'Estado', 
            'observaciones':'Observaciones', 
            'caja':'Caja', 
            'carpeta':'Carpeta'
            }
        widgets = {
            'fecha_ingreso' : DatePickerInput(),
            'fecha_entrega' : DatePickerInput(),
            'fecha_devolucion' : DatePickerInput(),
        }
class InmuebleEmpateForm(forms.ModelForm):
    desembolso = forms.ModelChoiceField(queryset=Desembolsos.objects.all(),widget=forms.Select(attrs={
        'class' : 'select2'}))
    class Meta:
        model = Inmueble
        fields = '__all__'
        # exclude = ['usuario_creacion','usuario_modificacion']
        labels = {
            'desembolso':'Desembolso',
            'escritura_publica':'Escritura Publica',
            'folio':'Folio',
            'catastro':'Catastro',
            'plano':'Plano',
            'plano_cebolla':'Plano Cebolla',
            'plano_construccion':'Plano Construccion',
            'informe_rapido':'Informe Rapido',
            'otros':'Otros',
            'observaciones':'Observaciones',
            'checklist':'Checklist',
            'call_center':'Call Center',
        }
class InmuebleEditarEmpateForm(forms.ModelForm):
    desembolso = forms.ModelChoiceField(queryset=Desembolsos.objects.all(),widget=forms.Select(attrs={
        'class' : 'select2'}), disabled=True)
    usuario_creacion = forms.ModelChoiceField(queryset=Profile.objects.all(),widget=forms.Select(attrs={
        'class' : 'select2'
    }),required=False, disabled=True)
    class Meta:
        model = Inmueble
        fields = '__all__'
        exclude = ['usuario_creacion']
        labels = {
            'desembolso':'Desembolso',
            'escritura_publica':'Escritura Publica',
            'folio':'Folio',
            'catastro':'Catastro',
            'plano':'Plano',
            'plano_cebolla':'Plano Cebolla',
            'plano_construccion':'Plano Construccion',
            'informe_rapido':'Informe Rapido',
            'otros':'Otros',
            'observaciones':'Observaciones',
            'checklist':'Checklist',
            'call_center':'Call Center',
        }

class VehiculoEmpateForm(forms.ModelForm):
    desembolso = forms.ModelChoiceField(queryset=Desembolsos.objects.all(),widget=forms.Select(attrs={
        'class' : 'select2'}))
    class Meta:
        model = Vehiculo
        fields = '__all__'
        # exclude = ['usuario_creacion','usuario_modificacion']
        labels = {
            'desembolso':'Desembolso',
            'crpva':'Crpva',
            'talon':'Talón',
            'placa':'Placa',
            'resolucion_inscripcion':'Resol. Inscripción',
            'formulario_registro_vehicular':'Registro Vehicular',
            'poliza_importacion':'Póliza. Importación',
            'declarcion_mercancias':'Declaración Mercancías',
            'dim':'Dim',
            'anexo_subrogacion':'Anexo Subrogación',
            'resolucion_transferencia':'Resolución Transferencia',
            'informe_tecnico':'Informe Técnico',
            'impuestos':'Impuestos',
        }

class VehiculoEditarEmpateForm(forms.ModelForm):
    desembolso = forms.ModelChoiceField(queryset=Desembolsos.objects.all(),widget=forms.Select(attrs={
        'class' : 'select2'}))
    usuario_creacion = forms.ModelChoiceField(queryset=Profile.objects.all(),widget=forms.Select(attrs={
        'class' : 'select2'
    }),required=False, disabled=True)
    class Meta:
        model = Vehiculo
        fields = '__all__'
        exclude = ['usuario_creacion']
        labels = {
            'desembolso':'Desembolso',
            'crpva':'Crpva',
            'talon':'Talón',
            'placa':'Placa',
            'resolucion_inscripcion':'Resol. Inscripción',
            'formulario_registro_vehicular':'Registro Vehicular',
            'poliza_importacion':'Póliza. Importación',
            'declarcion_mercancias':'Declaración Mercancías',
            'dim':'Dim',
            'anexo_subrogacion':'Anexo Subrogación',
            'resolucion_transferencia':'Resolución Transferencia',
            'informe_tecnico':'Informe Técnico',
            'impuestos':'Impuestos',
        }

class PrestamoCrearForm(forms.ModelForm):
    sobre = forms.ModelMultipleChoiceField(queryset=Sobre.objects.filter(estado='Archivado'),widget=forms.SelectMultiple(attrs={
        'class' : 'select2'
    }), required=True)
    class Meta:
        model = Prestamo
        fields = '__all__'
        labels = {
            'sobre':'Sobre', 
            'estado':'Estado',
            'notas':'Notas',
        }
class PrestamoEditarForm(forms.ModelForm):
    sobre = forms.ModelMultipleChoiceField(queryset=Sobre.objects.all(),widget=forms.SelectMultiple(attrs={
        'class' : 'select2'
    }), required=True)
    estado = forms.CharField(disabled=True)
    class Meta:
        model = Prestamo
        exclude =['usuario_solicitante']
        fields = '__all__'  
        labels = {
            'sobre':'Sobre', 
            'estado':'Estado',
            'notas':'Notas',
        }

class PrestamoArchivoForm(forms.ModelForm):
    sobre = forms.ModelMultipleChoiceField(queryset=Sobre.objects.all(),widget=forms.SelectMultiple(attrs={
        'class' : 'select2'
    }), required=True, disabled=True)
    class Meta:
        model = Prestamo
        fields = '__all__'  
        exclude = ['usuario_solicitante']
        labels = {
            'sobre':'Sobre', 
            'estado':'Estado',
            'notas':'Notas',
        }

class SobreCrearForm(forms.ModelForm):
    desembolso = forms.ModelMultipleChoiceField(queryset=Desembolsos.objects.all(),widget=forms.SelectMultiple(attrs={
        'class' : 'select2'
    }), required=False)
    class Meta:
        model = Sobre
        fields = '__all__'
        labels = {
            'codigo':'Código Sobre',
            'nombre':'Nombre Cliente',
            'desembolso':'Desembolso',
            'estado':'Estado',
            'ubicacion':'Ubicacion',
            'observaciones':'Observaciones',
            'ultima_modificacion':'Ultima modificación',
            'usuario_modifiacion':'Usuario modifiación',    
        }

class SobreEditarForm(forms.ModelForm):
    desembolso = forms.ModelMultipleChoiceField(queryset=Desembolsos.objects.all(),widget=forms.SelectMultiple(attrs={
        'class' : 'select2'
    }), required=False)
    class Meta:
        model = Sobre
        fields = '__all__'
        exclude = ['usuario_creacion']
        labels = {
            'codigo':'Código Sobre',
            'nombre':'Nombre Cliente',
            'desembolso':'Desembolso',
            'estado':'Estado',
            'ubicacion':'Ubicacion',
            'observaciones':'Observaciones',   
        }

class PolizaCrearForm(forms.ModelForm):
    class Meta:
        model = Poliza
        fields = '__all__'
        labels = {
            'sobre':'Sobre',
            'codigo_cliente':'Codigo Cliente',
            'identificacion':'Identificacion',
            'cliente':'Cliente',
            'cuenta':'Cuenta',
            'tarjeta':'Tarjeta',
            'sucursal':'Sucursal',
            'poliza': 'Póliza',
            'estado':'Estado',
            'observaciones':'Observaciones',
            'fecha_recepcion':'Fecha Recepcion',
            'caja':'Caja',
            'usuario_registro':'Usuario Registro',
        }
class PolizaEditarForm(forms.ModelForm):
    usuario_creacion = forms.ModelChoiceField(queryset=Profile.objects.all(),widget=forms.Select(), disabled=True)
    class Meta:
        model = Poliza
        fields = '__all__'
        labels = {
            'sobre':'Sobre',
            'estado':'Estado',
            'codigo_cliente':'Codigo Cliente',
            'identificacion':'Identificacion',
            'cliente':'Cliente',
            'cuenta':'Cuenta',
            'tarjeta':'Tarjeta',
            'sucursal':'Sucursal',
            'poliza': 'Póliza',
            'estado':'Estado',
            'observaciones':'Observaciones',
            'fecha_recepcion':'Fecha Recepcion',
            'caja':'Caja',
            'usuario_registro':'Usuario Registro',
        }
class AperturaCrearForm(forms.ModelForm):
    sobre = forms.ModelChoiceField(queryset=Sobre.objects.all(),widget=forms.Select(attrs={
        'class' : 'select2'
    }), required=False)
    class Meta:
        model = Apertura
        fields = '__all__'
        labels = {
            'sobre':'Sobre',
            'fecha_apertura':'Fecha Apertura',
            'producto':'Producto',
            'sucursal':'Sucursal',
            'agencia_apertura':'Agencia Apertura',
            'agencia_asignada':'Agencia Asignada',
            'codigo_cliente':'Codigo Cliente',
            'cliente':'Cliente',
            'cuenta':'Cuenta',
            'estado_cuenta':'Estado Cuenta',
            'segmento_cliente':'Segmento Cliente',
            'tipo':'Tipo',
            'saldo_captacion':'Saldo Captacion',
            'estado':'Estado',
            'fecha_recepcion':'Fecha Recepcion',
            'caja':'Caja',
        }

class AperturaEditarForm(forms.ModelForm):  
    usuario_creacion = forms.ModelChoiceField(queryset=Profile.objects.all(),widget=forms.Select(), disabled=True)
    sobre = forms.ModelChoiceField(queryset=Correspondencia.objects.filter(estado="Recibido"),widget=forms.Select(attrs={
        'class' : 'select2'
    }), required=False)
    class Meta:
        model = Apertura
        fields = '__all__'
        labels = {
            'sobre':'Sobre',
            'fecha_apertura':'Fecha Apertura',
            'producto':'Producto',
            'sucursal':'Sucursal',
            'agencia_apertura':'Agencia Apertura',
            'agencia_asignada':'Agencia Asignada',
            'codigo_cliente':'Codigo Cliente',
            'cliente':'Cliente',
            'cuenta':'Cuenta',
            'estado_cuenta':'Estado Cuenta',
            'segmento_cliente':'Segmento Cliente',
            'tipo':'Tipo',
            'saldo_captacion':'Saldo Captacion',
            'estado':'Estado',
            'fecha_recepcion':'Fecha Recepcion',
            'caja':'Caja',
        }

class CorrespondenciaEnviarForm(forms.ModelForm):
    desembolso = forms.ModelMultipleChoiceField(queryset=Desembolsos.objects.filter(estado='Pendiente'),widget=forms.SelectMultiple(attrs={
        'class' : 'select2'
    }), required=False) 

    documento_suelto = forms.ModelMultipleChoiceField(queryset=DocumentosSueltos.objects.filter(estado='Pendiente'),widget=forms.SelectMultiple(attrs={
        'class' : 'select2'
    }), required=False) 

    class Meta:
        model = Correspondencia
        fields = '__all__'
        labels = {
            'codigo_barras':'Código de Barras',
            'desembolso':'Desembolso',
            'documento_suelto':'Documento Suelto',
            'contenido':'Contenido',
            'descripcion':'Descripción',
            'fecha_envio':'Fecha de Envío',
            'fecha_recepcion':'Fecha de Recepción',
            'usuario_registro':'Usuario Registro',}

class CorrespondenciaRecibirForm(forms.ModelForm):
    desembolso = forms.ModelMultipleChoiceField(queryset=Desembolsos.objects.all(),widget=forms.SelectMultiple(attrs={
        'class' : 'select2'
    }), required=False, disabled=True)

    documento_suelto = forms.ModelMultipleChoiceField(queryset=DocumentosSueltos.objects.all(),widget=forms.SelectMultiple(attrs={
        'class' : 'select2'
    }), required=False, disabled=True) 
    codigo_barras = forms.CharField(disabled=True)
    contenido = forms.CharField(disabled=True)
    usuario_registro = forms.ModelChoiceField(queryset=Profile.objects.all(),disabled=True)

    class Meta:
        model = Correspondencia
        fields = '__all__'
        labels = {
            'codigo_barras':'Código de Barras',
            'desembolso':'Desembolso',
            'documento_suelto':'Documento Suelto',
            'contenido':'Contenido',
            'descripcion':'Descripción',
            'fecha_envio':'Fecha de Envío',
            'fecha_recepcion':'Fecha de Recepción',
            'conformidad':'Conformidad',
            'usuario_registro':'Enviado por'}
class CorrespondenciaModificarForm(forms.ModelForm):
    desembolso = forms.ModelMultipleChoiceField(queryset=Desembolsos.objects.all(),widget=forms.SelectMultiple(attrs={
        'class' : 'select2'
    }), required=False) 

    documento_suelto = forms.ModelMultipleChoiceField(queryset=DocumentosSueltos.objects.all(),widget=forms.SelectMultiple(attrs={
        'class' : 'select2'
    }), required=False)

    class Meta:
        model = Correspondencia
        fields = '__all__'
        exclude = ['estado']
        labels = {
            'codigo_barras':'Código de Barras',
            'desembolso':'Desembolso',
            'documento_suelto':'Documento Suelto',
            'contenido':'Contenido',
            'descripcion':'Descripción',
            'fecha_envio':'Fecha de Envío',
            'fecha_recepcion':'Fecha de Recepción',
            'usuario_registro':'Enviado por',}

class BuscarCajaForm(forms.Form):
    
    TIPO = (
        ('Empate','Empate'),
        ('Contrato','Contrato'),
        ('Inmueble','Garantía Inmueble'),
        ('Vehiculo','Garantía Vehicular'),
        ('Levantamientos','Levantamientos'),
        ('Apertura','Aperturas'),
        ('Poliza','Pólizas'),
        ('DocumentosSueltos','Documentos Sueltos'),
    )
    tipo = forms.CharField(label ='Base de datos a buscar',required=True, max_length=100, widget=forms.Select(choices=TIPO))
    caja = forms.IntegerField(required=True)

    def __init__(self,*args,**kwargs):
        super(BuscarCajaForm, self).__init__(*args, **kwargs)
        self.fields['tipo'].initial = 'Empate'
    
class ParametroForm(forms.ModelForm):
    class Meta:
        model = Parametro
        fields = '__all__'
        exclude =['usuario']
        labels = {
            'caja':'Caja Predeterminada',
            'email_politicas':'Email Politicas',
            'email_liquidaciones':'Email Liquidaciones',
            'email_jefe_custodia':'Email Jefe Custodia',
            'email_la_paz':'Email La Paz',
            'email_el_alto':'Email El Alto',
            'email_oruro':'Email Oruro',
            'email_potosi':'Email Potosi',
            'email_cochabamba':'Email Cochabamba',
            'email_sucre':'Email Sucre',
            'email_tarija':'Email Tarija',
            'email_pando':'Email Pando',
            'email_beni':'Email Beni',
            'email_santa_cruz':'Email Santa Cruz',
        }

class TareaCrearForm(forms.ModelForm):
    analista_asignado = forms.ModelChoiceField(queryset=Profile.objects.filter(cargo="Analista de Custodia Documental"), widget=forms.Select(attrs={
        'class': 'select2'
    }), required=True)
    class Meta:
        model = Tarea
        fields = '__all__'
        labels = {
        'nombre':'Tipo de Tarea',
        'tiempo':'Tiempo',
        'analista_asignado':'Analista Asignado',
        'descripcion':'Descripcion',
        'estado':'Estado',
        'fecha_creacion':'Fecha Creacion',
        'fecha_modificacion':'Fecha Modificacion',
        'usuario_creacion':'Usuario Creacion',
        'usuario_modificacion':'Usuario Modificacion',
        }

class TareaEditarForm(forms.ModelForm):
    nombre = forms.CharField(disabled=True)
    tiempo = forms.IntegerField(disabled=True)
    analista_asignado = forms.ModelChoiceField(queryset=Profile.objects.all(),widget=forms.Select(attrs={
        'class':'select2'
    }), disabled=True)
    
    class Meta:
        model = Tarea
        fields = '__all__'
        exclude = ['usuario_creacion']
        labels = {
        'nombre':'Tipo de Tarea',
        'tiempo':'Tiempo',
        'analista_asignado':'Analista Asignado',
        'descripcion':'Descripcion',
        'estado':'Estado',
        'fecha_creacion':'Fecha Creacion',
        'fecha_modificacion':'Fecha Modificacion',
        'usuario_creacion':'Usuario Creacion',
        'usuario_modificacion':'Usuario Modificacion',
        }
class ReporteForm(forms.Form):
    
    TIPO_REPORTE = (
        ('',''),
        ('Empate','Empate'),
        ('Contratos','Contratos'),
        ('Aperturas','Aperturas'),
        ('Pólizas','Pólizas'),
        ('Documentos Sueltos','Documentos Sueltos'),
        ('Levantamientos','Levantamientos'),
        ('Desembolsos','Desembolsos'),
        ('Sobres','Sobres'),
        ('Correspondencia','Correspondencia'),
    )
    reporte = forms.ChoiceField(required=True, choices=TIPO_REPORTE)
    caja = forms.IntegerField(required=False)
    fecha = forms.DateField(required=False, widget=DatePickerInput(attrs={
        'placeholder': 'Fecha', 
        'class': 'form-control',   
    }))

    def __init__(self, *args, **kwargs):
        super(ReporteForm, self).__init__(*args, **kwargs)
        self.fields['reporte'].initial = ''

class HistorialForm(forms.Form):
    
    TIPO = (
        ('',''),
        ('Empate','Empate'),
        ('Contratos','Contratos'),
        ('Apertura','Aperturas'),
        ('Póliza','Pólizas'),
        ('DocumentosSueltos','Documentos Sueltos'),
        ('Levantamientos','Levantamientos'),
        ('Desembolsos','Desembolsos'),
        ('Sobre','Sobres'),
        ('Correspondencia','Correspondencia'),
    )
    modelo = forms.ChoiceField(required=True, choices=TIPO, widget=forms.Select(attrs={'placeholder': 'Modelo'}))
    def __init__(self, *args, **kwargs):
        super(HistorialForm, self).__init__(*args, **kwargs)
        self.fields['modelo'].initial = ''

class HojaResumenForm(forms.Form):
    codigo_cliente = forms.IntegerField(required=False, label='', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Código Cliente'}))
    onbase = forms.IntegerField(required=False, label='',widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Onbase'}))
    operacion = forms.IntegerField(required=False, label='',widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Operación'}))
    cliente = forms.CharField(required=False, label='',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cliente'}))

class TipoOperacionForm(forms.ModelForm):
    nombre = forms.CharField(required=True)
    tiempo = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'minutos'}))
    class Meta:
        model = TipoOperacion
        fields = '__all__'

 


   

