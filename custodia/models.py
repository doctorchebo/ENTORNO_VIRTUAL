from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.deletion import CASCADE, PROTECT
from django.db.models.fields import (
    BigAutoField,
    BigIntegerField,
    CharField,
    DateField,
    DateTimeField,
    IntegerField,
    NullBooleanField,
    TextField,
)
from django.db.models.fields.related import ForeignObject, OneToOneField


class Profile(models.Model):
    user = OneToOneField(User, null=True, on_delete=models.CASCADE)
    nombre = CharField(max_length=100, blank=True)
    codigo_banco = BigIntegerField(blank=True, null=True)
    cargo = CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.nombre}"


class Parametro(models.Model):
    usuario = OneToOneField(User, on_delete=models.CASCADE)
    caja = models.BigIntegerField(blank=True, null=True)
    email_politicas = models.EmailField(max_length=254, blank=True, null=True)
    email_liquidaciones = models.EmailField(max_length=254, blank=True, null=True)
    email_jefe_custodia = models.EmailField(max_length=254, blank=True, null=True)
    email_la_paz = models.EmailField(max_length=254, blank=True, null=True)
    email_el_alto = models.EmailField(max_length=254, blank=True, null=True)
    email_oruro = models.EmailField(max_length=254, blank=True, null=True)
    email_potosi = models.EmailField(max_length=254, blank=True, null=True)
    email_cochabamba = models.EmailField(max_length=254, blank=True, null=True)
    email_sucre = models.EmailField(max_length=254, blank=True, null=True)
    email_tarija = models.EmailField(max_length=254, blank=True, null=True)
    email_pando = models.EmailField(max_length=254, blank=True, null=True)
    email_beni = models.EmailField(max_length=254, blank=True, null=True)
    email_santa_cruz = models.EmailField(max_length=254, blank=True, null=True)


class Desembolsos(models.Model):
    ESTADO = (
        ("Pendiente", "Pendiente"),
        ("Enviado", "Enviado"),
        ("Recibido", "Recibido"),
        ("Distribuido", "Distribuido"),
        ("Empatado", "Empatado"),
        ("Observado", "Observado"),
        ("Desestimada", "Desestimada"),
    )

    class Meta:
        permissions = [("borrar_desembolso", "Puede borrar desembolsos")]

    fecha_desembolso = models.DateField(blank=True, null=True)
    producto = models.CharField(max_length=45, blank=True, null=True)
    tipo = models.CharField(max_length=45, blank=True, null=True)
    codigo_cliente = models.BigIntegerField(
        blank=True,
        null=True,
    )
    cliente = models.CharField(max_length=45, blank=True, null=True)
    operacion = models.BigIntegerField(blank=True, null=True)
    monto = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
    )
    desembolso_parcial = models.CharField(max_length=45, blank=True, null=True)
    ejecutivo = models.CharField(max_length=100, blank=True, null=True)
    onbase = models.BigIntegerField(blank=True, null=True)
    sucursal = models.CharField(max_length=50, blank=True, null=True)
    agencia = models.CharField(max_length=50, blank=True, null=True)
    tipo_banca = models.CharField(max_length=50, blank=True, null=True)
    tipo_trabajo = models.CharField(max_length=50, blank=True, null=True)
    instancia_aprobacion = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=50, blank=True, null=True, choices=ESTADO)
    usuario_creacion = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="usuario_creacion_desembolso",
    )
    usuario_modificacion = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="usuario_modificacion_desembolso",
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    fecha_modificacion = models.DateTimeField(auto_now=True, blank=True, null=True)
    history = AuditlogHistoryField()

    def __str__(self):
        return f"FISA {self.codigo_cliente} OB {self.onbase} OP {self.operacion} {self.cliente} {self.estado}"

    @property
    def empate(self):
        return self.distribucion_set.all()


class TipoOperacion(models.Model):
    nombre = models.CharField(max_length=100, blank=True, null=True)
    tiempo = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.nombre}"


class Distribucion(models.Model):
    desembolso = models.ForeignKey(
        Desembolsos, on_delete=models.SET_NULL, blank=True, null=True
    )
    tipo = models.ForeignKey(
        TipoOperacion, on_delete=models.SET_NULL, blank=True, null=True
    )
    analista_asignado = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="distribuido_a",
    )
    usuario_creacion = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="usuario_creacion_distribucion",
    )
    usuario_modificacion = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="usuario_modificacion_distribucion",
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    history = AuditlogHistoryField()

    def __str__(self):
        return f"{self.desembolso.codigo_cliente}-{self.desembolso.onbase}-{self.desembolso.operacion}-{self.analista_asignado}"


class Correspondencia(models.Model):
    CONTENIDO = (
        ("Operaciones Crediticias", "Operaciones Crediticias"),
        ("Documentos Sueltos", "Documentos Sueltos"),
        ("Captaciones", "Captaciones"),
    )
    ESTADO = (
        ("Enviado", "Enviado"),
        ("Recibido", "Recibido"),
    )
    codigo_barras = models.BigIntegerField(null=True)
    contenido = models.CharField(
        max_length=100, blank=True, null=True, choices=CONTENIDO
    )
    desembolso = models.ManyToManyField(Desembolsos, blank=True)
    documento_suelto = models.ManyToManyField("DocumentosSueltos", blank=True)
    descripcion = models.TextField()
    estado = models.CharField(max_length=50, blank=True, null=True, choices=ESTADO)
    recibido = models.BooleanField(blank=True, default=False)
    fecha_recepcion = models.DateTimeField(auto_now_add=True)
    fecha_envio = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    conformidad = models.BooleanField(blank=True, default=False)
    usuario_registro = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="usuario_envio_correspondencia",
    )
    usuario_recepcion = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="usuario_recepcion_correspondencia",
    )
    history = AuditlogHistoryField()

    def __str__(self) -> str:
        return f"{self.codigo_barras}"


# @receiver(m2m_changed, sender=Correspondencia.desembolso.through)
# def follow_by_follow_add_or_remove(sender, **kwargs):
#     if kwargs.get('action') == 'post_add':
#         print (kwargs.get('instance').follow.all())

#         print (list(kwargs.get('pk_set'))[0])


class DocumentosSueltos(models.Model):
    ESTADO = (
        ("Recibido", "Recibido"),
        ("Anulado", "Anulado"),
        ("Pendiente", "Pendiente"),
    )
    sobre = models.ForeignKey(
        Correspondencia, on_delete=models.SET_NULL, blank=True, null=True
    )
    sucursal = models.CharField(max_length=50, blank=True, null=True)
    agencia = models.CharField(max_length=50, blank=True, null=True)
    descripcion = models.CharField(max_length=50, blank=True, null=True)
    codigo_cliente = models.BigIntegerField(blank=True, null=True)
    cliente = models.CharField(max_length=50, blank=True, null=True)
    operacion = models.BigIntegerField(blank=True, null=True)
    oficina = models.CharField(max_length=50, blank=True, null=True)
    observacion_agencia = models.CharField(max_length=100, blank=True, null=True)
    observacion_custodia = models.CharField(max_length=100, blank=True, null=True)
    digitalizado = models.BooleanField(default=False, blank=True)
    bloque = models.PositiveIntegerField(null=True)
    caja = models.PositiveIntegerField(null=True)
    estado = models.CharField(max_length=20, blank=True, null=True, choices=ESTADO)
    usuario_creacion = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="usuario_creacion_documento_suelto",
    )
    usuario_modificacion = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="usuario_modificacion_documento_suelto",
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    fecha_modificacion = models.DateTimeField(auto_now=True, blank=True, null=True)
    history = AuditlogHistoryField()

    def __str__(self) -> str:
        return f"{self.codigo_cliente} {self.operacion} {self.cliente} {self.descripcion} {self.estado}"


class FormatoContrato(models.Model):
    nombre = CharField(max_length=100, blank=True, null=True)
    cantidad = IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre}"


class Contratos(models.Model):

    CANTIDAD = (
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
    )

    ESTADO_CONTRATO = (
        ("Enviado", "Enviado"),
        ("Recibido", "Recibido"),
        ("Observado", "Observado"),
    )

    desembolso = models.ForeignKey(
        Desembolsos, on_delete=models.SET_NULL, blank=True, null=True
    )
    adenda = models.BooleanField(default=False, blank=True)
    minuta = models.BooleanField(default=False, blank=True)
    cantidad_minuta = models.CharField(
        max_length=1, blank=True, null=True, choices=CANTIDAD
    )
    estado_minuta = models.ForeignKey(
        FormatoContrato,
        on_delete=models.SET_NULL,
        max_length=50,
        blank=True,
        null=True,
        related_name="+",
    )
    testimonio = models.BooleanField(default=False, blank=True)
    num_testimonio = models.CharField(max_length=50, blank=True, null=True)
    reg_testimonio = models.CharField(max_length=50, blank=True, null=True)
    cantidad_testimonio = models.CharField(
        max_length=1, blank=True, null=True, choices=CANTIDAD
    )
    estado_testimonio = models.ForeignKey(
        FormatoContrato,
        on_delete=models.SET_NULL,
        max_length=50,
        blank=True,
        null=True,
        related_name="+",
    )
    contrato_privado = models.BooleanField(default=False, blank=True)
    cantidad_contrato = models.CharField(
        max_length=1, blank=True, null=True, choices=CANTIDAD
    )
    estado_contrato = models.ForeignKey(
        FormatoContrato,
        on_delete=models.SET_NULL,
        max_length=50,
        blank=True,
        null=True,
        related_name="+",
    )
    rec_firmas = models.BooleanField(default=False, blank=True)
    num_rec_firmas = models.BigIntegerField(blank=True, null=True)
    reg_rec_firmas = models.BigIntegerField(blank=True, null=True)
    cantidad_rec_firmas = models.CharField(
        max_length=1, blank=True, null=True, choices=CANTIDAD
    )
    estado_rec_firmas = models.ForeignKey(
        FormatoContrato,
        on_delete=models.SET_NULL,
        max_length=50,
        blank=True,
        null=True,
        related_name="+",
    )
    cert_tdr = models.BooleanField(default=False, blank=True)
    cantidad_cert_tdr = models.CharField(
        max_length=1, blank=True, null=True, choices=CANTIDAD
    )
    estado_cert_tdr = models.ForeignKey(
        FormatoContrato,
        on_delete=models.SET_NULL,
        max_length=50,
        blank=True,
        null=True,
        related_name="+",
    )
    cert_desgravamen = models.BooleanField(default=False, blank=True)
    cantidad_cert_desgravamen = models.CharField(
        max_length=1, blank=True, null=True, choices=CANTIDAD
    )
    estado_cert_desgravamen = models.ForeignKey(
        FormatoContrato,
        on_delete=models.SET_NULL,
        max_length=50,
        blank=True,
        null=True,
        related_name="+",
    )
    seguro_cesantia = models.BooleanField(default=False, blank=True)
    cantidad_seguro_cesantia = models.CharField(
        max_length=1, blank=True, null=True, choices=CANTIDAD
    )
    estado_seguro_cesantia = models.ForeignKey(
        FormatoContrato,
        on_delete=models.SET_NULL,
        max_length=50,
        blank=True,
        null=True,
        related_name="+",
    )
    seguro_dima = models.BooleanField(default=False, blank=True)
    cantidad_seguro_dima = models.CharField(
        max_length=1, blank=True, null=True, choices=CANTIDAD
    )
    estado_seguro_dima = models.ForeignKey(
        FormatoContrato,
        on_delete=models.SET_NULL,
        max_length=50,
        blank=True,
        null=True,
        related_name="+",
    )
    anexos_seguros = models.BooleanField(default=False, blank=True)
    cert_gravamen = models.BooleanField(default=False, blank=True)
    cantidad_cert_gravamen = models.CharField(
        max_length=1, blank=True, null=True, choices=CANTIDAD
    )
    estado_cert_gravamen = models.ForeignKey(
        FormatoContrato,
        on_delete=models.SET_NULL,
        max_length=50,
        blank=True,
        null=True,
        related_name="+",
    )
    glosa_cert_gravamen = models.CharField(max_length=100, blank=True, null=True)
    reg_cert_gravamen = models.CharField(max_length=100, blank=True, null=True)
    cert_fundempresa = models.BooleanField(default=False, blank=True)
    cantidad_cert_fundempresa = models.CharField(
        max_length=1, blank=True, null=True, choices=CANTIDAD
    )
    estado_cert_fundempresa = models.ForeignKey(
        FormatoContrato,
        on_delete=models.SET_NULL,
        max_length=50,
        blank=True,
        null=True,
        related_name="+",
    )
    glosa_cert_fundempresa = models.CharField(max_length=100, blank=True, null=True)
    reg_cert_fundempresa = models.CharField(max_length=100, blank=True, null=True)
    folio = models.BooleanField(default=False, blank=True)
    cantidad_folio = models.CharField(
        max_length=1, blank=True, null=True, choices=CANTIDAD
    )
    estado_folio = models.ForeignKey(
        FormatoContrato,
        on_delete=models.SET_NULL,
        max_length=50,
        blank=True,
        null=True,
        related_name="+",
    )
    glosa_folio = models.CharField(max_length=100, blank=True, null=True)
    reg_folio = models.CharField(max_length=100, blank=True, null=True)
    inf_rapido = models.BooleanField(default=False, blank=True)
    cantidad_inf_rapido = models.CharField(
        max_length=1, blank=True, null=True, choices=CANTIDAD
    )
    estado_inf_rapido = models.ForeignKey(
        FormatoContrato,
        on_delete=models.SET_NULL,
        max_length=50,
        blank=True,
        null=True,
        related_name="+",
    )
    glosa_inf_rapido = models.CharField(max_length=100, blank=True, null=True)
    reg_inf_rapido = models.CharField(max_length=100, blank=True, null=True)
    notas = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(
        max_length=20, blank=True, null=True, choices=ESTADO_CONTRATO
    )
    conformidad = models.BooleanField(blank=True, default=False)
    ubicacion = models.CharField(max_length=100, blank=True, null=True)
    usuario_modificacion_legal = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="usuario_mod_contrato_legal",
    )
    usuario_modificacion_empate = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="usuario_mod_contrato_empate",
    )
    usuario_creacion = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="usuario_creacion_contrato",
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    fecha_modificacion = models.DateTimeField(auto_now=True, blank=True, null=True)
    history = AuditlogHistoryField()

    def __str__(self) -> str:
        return f"{self.desembolso.cliente} OB {self.desembolso.onbase} EP {self.num_testimonio} - {self.estado}"


class Inmueble(models.Model):
    desembolso = models.ForeignKey(
        Desembolsos, on_delete=models.SET_NULL, blank=True, null=True
    )
    escritura_publica = models.CharField(max_length=50, blank=True, null=True)
    folio = models.BigIntegerField(blank=True, null=True)
    catastro = models.BigIntegerField(blank=True, null=True)
    plano = models.CharField(max_length=50, blank=True, null=True)
    plano_cebolla = models.CharField(max_length=50, blank=True, null=True)
    plano_construccion = models.CharField(max_length=50, blank=True, null=True)
    informe_rapido = models.BooleanField(default=False, blank=True)
    otros = models.CharField(max_length=50, blank=True, null=True)
    observaciones = models.CharField(max_length=255, blank=True, null=True)
    checklist = models.BooleanField(default=False, blank=True)
    call_center = models.BooleanField(default=False, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    usuario_creacion = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="usuario_creacion_inmueble",
    )
    usuario_modificacion = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="usuario_modificacion_inmueble",
    )
    history = AuditlogHistoryField()

    def __str__(self) -> str:
        return f"{self.desembolso.cliente} {self.folio} EP {self.escritura_publica}"


class Vehiculo(models.Model):
    desembolso = models.ForeignKey(
        Desembolsos, on_delete=models.SET_NULL, blank=True, null=True
    )
    crpva = models.BigIntegerField(blank=True, null=True)
    talon = models.BooleanField(default=False, blank=True)
    placa = models.CharField(max_length=50, blank=True, null=True)
    resolucion_inscripcion = models.CharField(max_length=50, blank=True, null=True)
    formulario_registro_vehicular = models.CharField(
        max_length=100, blank=True, null=True
    )
    poliza_importacion = models.BigIntegerField(blank=True, null=True)
    declarcion_mercancias = models.CharField(max_length=50, blank=True, null=True)
    dim = models.CharField(max_length=50, blank=True, null=True)
    anexo_subrogacion = models.BooleanField(default=False, blank=True)
    resolucion_transferencia = models.BooleanField(default=False, blank=True)
    informe_tecnico = models.BooleanField(default=False, blank=True)
    impuestos = models.CharField(max_length=50, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    usuario_creacion = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="usuario_creacion_vehiculo",
    )
    usuario_modificacion = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="usuario_modificacion_vehiculo",
    )
    history = AuditlogHistoryField()

    def __str__(self) -> str:
        return f"{self.desembolso.cliente} {self.crpva} {self.placa}"


class Empate(models.Model):

    FORMATO = (
        ("F", "F"),
        ("D", "D"),
        ("FD", "FD"),
        ("N/A", "N/A"),
        ("O", "O"),
    )

    LUGAR = (
        ("N/A", "N/A"),
        ("SI C", "SI C"),
        ("SI L", "SI L"),
        ("NO", "NO"),
    )

    ESTADO = (
        ("Pendiente", "Pendiente"),
        ("Empatado", "Empatado"),
    )

    TIPO = (("BL", "Bajo línea"), ("OP", "Operación Paralela"))

    TRABAJO = (
        ("Dependiente", "Dependiente"),
        ("Independiente", "Independiente"),
        ("Corporativo/Empresa", "Corporativo"),
    )

    INSTANCIA = (
        ("DFA", "Delegación de Facultades Adicionales"),
        ("AC MPE", "Facultad Analistas de Riesgo Crediticio MPE"),
        ("AC PYME", "Facultad Analistas de Riesgo Crediticio PYME"),
        ("AC IND", "Facultad Analistas de Riesgo Crediticio Independientes"),
        ("CR", "Comité Regional de Créditos"),
        ("CN", "Comité Nacional de Créditos"),
        ("Directorio", "Directorio"),
    )

    # INFORMACIÓN BÁSICA
    distribucion = models.ForeignKey(
        Distribucion, on_delete=models.SET_NULL, blank=True, null=True
    )
    estado = models.CharField(max_length=20, blank=True, null=True, choices=ESTADO)
    tipo_operacion = models.CharField(
        max_length=50, choices=TIPO, blank=True, null=True
    )
    onbase_referencia = models.BigIntegerField(blank=True, null=True)
    # CONTRATO, GARANTIA Y PÓLIZA

    # CHECKLIST
    propuesta = models.CharField(max_length=5, choices=FORMATO, blank=True, null=True)
    flujo = models.CharField(max_length=5, choices=FORMATO, blank=True, null=True)
    respaldos_ingresos = models.CharField(
        max_length=5, choices=FORMATO, blank=True, null=True
    )
    autorizacion_investigacion = models.CharField(
        max_length=5, choices=FORMATO, blank=True, null=True
    )
    cic_cod_con_ext = models.CharField(
        max_length=5, choices=FORMATO, blank=True, null=True
    )
    cic_cod_sin_ext = models.CharField(
        max_length=5, choices=FORMATO, blank=True, null=True
    )
    cic_hist_con_ext = models.CharField(
        max_length=5, choices=FORMATO, blank=True, null=True
    )
    cic_hist_sin_ext = models.CharField(
        max_length=5, choices=FORMATO, blank=True, null=True
    )
    cic_nombre = models.CharField(max_length=5, choices=FORMATO, blank=True, null=True)
    bi_codigo = models.CharField(max_length=5, choices=FORMATO, blank=True, null=True)
    bi_nombre = models.CharField(max_length=5, choices=FORMATO, blank=True, null=True)
    hoja_riesgos = models.CharField(
        max_length=5, choices=FORMATO, blank=True, null=True
    )
    lista_confidencial = models.CharField(
        max_length=5, choices=FORMATO, blank=True, null=True
    )
    atencion_preferente = models.CharField(
        max_length=5, choices=FORMATO, blank=True, null=True
    )
    retenciones_judiciales = models.CharField(
        max_length=5, choices=FORMATO, blank=True, null=True
    )
    cliente_pleno_oportuno_pago = models.CharField(
        max_length=5, choices=FORMATO, blank=True, null=True
    )
    segip = models.CharField(max_length=5, choices=FORMATO, blank=True, null=True)
    carnet_identidad = models.CharField(
        max_length=5, choices=FORMATO, blank=True, null=True
    )
    cic_cod_con_ext_desembolso = models.CharField(
        max_length=5, choices=FORMATO, blank=True, null=True
    )
    cic_cod_sin_ext_desembolso = models.CharField(
        max_length=5, choices=FORMATO, blank=True, null=True
    )
    cic_nombre_desembolso = models.CharField(
        max_length=5, choices=FORMATO, blank=True, null=True
    )
    bi_codigo_desembolso = models.CharField(
        max_length=5, choices=FORMATO, blank=True, null=True
    )
    bi_nombre_desembolso = models.CharField(
        max_length=5, choices=FORMATO, blank=True, null=True
    )
    plan_pagos = models.CharField(max_length=5, choices=FORMATO, blank=True, null=True)
    nota_credito = models.CharField(
        max_length=5, choices=FORMATO, blank=True, null=True
    )
    formulario_solicitud = models.CharField(
        max_length=5, choices=FORMATO, blank=True, null=True
    )
    verif_domiciliaria = models.CharField(
        max_length=5, choices=FORMATO, blank=True, null=True
    )
    verif_laboral = models.CharField(
        max_length=5, choices=FORMATO, blank=True, null=True
    )
    ddjj_bienes = models.CharField(max_length=5, choices=FORMATO, blank=True, null=True)
    copia_boleta_garantia = models.CharField(
        max_length=5, choices=FORMATO, blank=True, null=True
    )
    solicitud_seguro_desgravamen = models.CharField(
        max_length=5, choices=FORMATO, blank=True, null=True
    )
    solicitud_seguro_cesantia = models.CharField(
        max_length=5, choices=FORMATO, blank=True, null=True
    )
    solicitud_seguro_dima = models.CharField(
        max_length=5, choices=FORMATO, blank=True, null=True
    )
    notas = models.CharField(max_length=1000, blank=True, null=True)
    fecha_empate = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    fecha_modificacion = models.DateTimeField(auto_now=True, blank=True, null=True)
    caja = models.BigIntegerField(null=True)
    usuario_empate = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="usuario_empate",
    )
    empatado = models.BooleanField(default=False, blank=True)
    tiempo_empate = models.DecimalField(
        max_digits=10, decimal_places=1, blank=True, null=True
    )
    history = AuditlogHistoryField()

    def __str__(self):
        return f"FISA {self.distribucion.desembolso.codigo_cliente} OB {self.distribucion.desembolso.onbase} OP {self.distribucion.desembolso.operacion}"

    @property
    def observaciones(self):
        return self.observaciones_set.all()


# class Garantias(models.Model):
#     desembolso = models.ForeignKey(Desembolsos,on_delete=models.SET_NULL,blank=True, null=True)
#     analista = models.ForeignKey(Profile, on_delete=models.SET_NULL,blank=True,null=True,related_name='usuario_garantias')
#     fecha_registro = models.DateTimeField(blank=True,null=True)
#     tipo = models.ManyToManyField(TipoGarantia,blank=True)
class CategoriaObservacion(models.Model):
    nombre = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.nombre}"


class SubCategoriaObservacion(models.Model):
    nombre = models.CharField(max_length=50, blank=True, null=True)
    categoria = models.ForeignKey(
        CategoriaObservacion, on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return f"{self.nombre}"


class ItemObservacion(models.Model):
    nombre = models.CharField(max_length=50, blank=True, null=True)
    sub_categoria = models.ForeignKey(
        SubCategoriaObservacion, on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return f"{self.nombre}"


class Observaciones(models.Model):

    DESTINO = (
        ("Comercial", "Comercial"),
        ("Políticas", "Políticas"),
        ("Liquidaciones", "Liquidaciones"),
    )

    ESTADO = (
        ("Observado", "Observado"),
        ("Subsanado", "Subsanado"),
        ("Por revisar", "Por revisar"),
        ("Insubsanable", "Insubsanable"),
    )
    empate = models.ForeignKey(Empate, blank=True, null=True, on_delete=models.SET_NULL)
    destino = models.CharField(max_length=100, choices=DESTINO)
    categoria = models.ForeignKey(
        CategoriaObservacion, null=True, on_delete=models.SET_NULL
    )
    sub_categoria = models.ForeignKey(
        SubCategoriaObservacion, null=True, on_delete=models.SET_NULL
    )
    observacion = models.ForeignKey(
        ItemObservacion, null=True, on_delete=models.SET_NULL
    )
    glosa = models.CharField(max_length=100)
    estado = models.CharField(max_length=15, choices=ESTADO)
    fecha_observación = DateTimeField(auto_now_add=True, blank=True, null=True)
    fecha_modificacion = DateTimeField(auto_now=True, blank=True, null=True)
    comentarios_custodia = models.CharField(max_length=255, blank=True, null=True)
    comentarios_area_observada = models.CharField(max_length=255, blank=True, null=True)
    usuario_observacion = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="usuario_observacion",
    )
    usuario_revision = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="usuario_revision",
    )
    history = AuditlogHistoryField()

    def __str__(self):
        return f"{self.empate.distribucion.desembolso.onbase} {self.empate.distribucion.desembolso.cliente}"


class Levantamientos(models.Model):
    TIPO = (
        ("Hipotecario", "Hipotecario"),
        ("Prendario", "Prendario"),
    )
    ESTADO = (
        ("Entregado", "Entregado"),
        ("Listo Para Entrega", "Listo Para Entrega"),
        ("En Estante", "En Estante"),
        ("Concluido", "Concluido"),
        ("En Proceso", "En Proceso"),
    )
    desembolso = models.ForeignKey(
        Desembolsos, on_delete=models.SET_NULL, blank=True, null=True
    )
    sucursal = models.CharField(max_length=20, blank=True, null=True)
    codigo_cliente = models.PositiveIntegerField(blank=True, null=True)
    cliente = models.CharField(max_length=100, blank=True, null=True)
    onbase = models.BigIntegerField(blank=True, null=True)
    operacion = models.BigIntegerField(blank=True, null=True)
    tipo = models.CharField(max_length=100, blank=True, null=True, choices=TIPO)
    fecha_ingreso = models.DateField(blank=True, null=True)
    referencia_legal = models.CharField(max_length=100, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    analista = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="usuario_levantamientos",
    )
    solicitante = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="usuario_solicitante",
    )
    fecha_entrega = models.DateField(blank=True, null=True)
    enviado_a = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, blank=True, null=True
    )
    fecha_devolucion = models.DateTimeField(blank=True, null=True)
    estado = models.CharField(max_length=100, blank=True, null=True, choices=ESTADO)
    observaciones = models.CharField(max_length=255, blank=True, null=True)
    caja = models.PositiveIntegerField(blank=True, null=True)
    carpeta = models.PositiveIntegerField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    fecha_modificacion = models.DateTimeField(auto_now=True, blank=True, null=True)
    usuario_creacion = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="usuario_creacion_levantamiento",
    )
    usuario_modificacion = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="usuario_modificacion_levantamiento",
    )
    enviado_por = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="usuario_levantamientos_formulario",
    )
    history = AuditlogHistoryField()

    def __str__(self):
        return f"{self.codigo_cliente} {self.operacion} {self.cliente}"


class Sobre(models.Model):
    ESTADO = (
        ("Archivado", "Archivado"),
        ("Prestado", "Prestado"),
        ("Depurado", "Depurado"),
    )
    codigo = models.PositiveIntegerField()
    nombre = models.CharField(max_length=100)
    desembolso = models.ManyToManyField(Desembolsos, blank=True)
    estado = models.CharField(max_length=100, blank=True, null=True, choices=ESTADO)
    ubicacion = models.CharField(max_length=50, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    usuario_creacion = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="usuario_modificacion_sobre",
    )
    usuario_modificacion = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="usuario_creacion_sobre",
    )
    history = AuditlogHistoryField()

    def __str__(self):
        return f"{self.codigo} - {self.nombre} - {self.estado}"


class Prestamo(models.Model):
    ESTADO = (
        ("Solicitado", "Solicitado"),
        ("Prestado", "Prestado"),
        ("Devuelto", "Devuelto"),
    )
    sobre = models.ManyToManyField(Sobre, blank=True)
    estado = models.CharField(max_length=100, blank=True, null=True, choices=ESTADO)
    custodio = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, blank=True, null=True
    )
    notas = models.TextField(max_length=500, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    usuario_solicitante = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="usuario_prestamo",
    )
    usuario_custodio = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="usuario_custodio",
    )
    history = AuditlogHistoryField()

    def __str__(self):
        return f"{self.sobre} - {self.usuario_solicitante.nombre} - {self.estado}"


class Apertura(models.Model):
    ESTADO = (
        ("Recibido", "Recibido"),
        ("Anulado", "Anulado"),
        ("Empatado", "Empleado"),
        ("Pendiente", "Pendiente"),
    )
    sobre = models.ForeignKey(
        Correspondencia, on_delete=models.SET_NULL, blank=True, null=True
    )
    fecha_apertura = models.DateTimeField(blank=True, null=True)
    producto = models.CharField(max_length=100, blank=True, null=True)
    sucursal = models.CharField(max_length=100, blank=True, null=True)
    agencia_apertura = models.CharField(max_length=100, blank=True, null=True)
    agencia_asignada = models.CharField(max_length=100, blank=True, null=True)
    codigo_cliente = models.PositiveIntegerField(blank=True, null=True)
    cliente = models.CharField(max_length=100, blank=True, null=True)
    cuenta = models.BigIntegerField()
    estado_cuenta = models.CharField(max_length=100, blank=True, null=True)
    segmento_cliente = models.CharField(max_length=100, blank=True, null=True)
    tipo = models.CharField(max_length=100, blank=True, null=True)
    saldo_captacion = models.DecimalField(
        max_digits=20, decimal_places=2, blank=True, null=True
    )
    estado = models.CharField(max_length=15, blank=True, null=True, choices=ESTADO)
    fecha_creacion = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    fecha_modificacion = models.DateTimeField(auto_now=True, blank=True, null=True)
    usuario_creacion = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="usuario_creacion_apertura",
    )
    usuario_modificacion = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="usuario_modificacion_apertura",
    )
    caja = models.BigIntegerField(null=True)
    bloque = models.PositiveIntegerField(null=True)
    history = AuditlogHistoryField()

    def __str__(self):
        return f"{self.codigo_cliente} - {self.cliente} - {self.cuenta}"


class Poliza(models.Model):
    ESTADO = (
        ("Pendiente", "Pendiente"),
        ("Recibido", "Recibido"),
        ("Anulado", "Anulado"),
    )
    sobre = models.ForeignKey(
        Correspondencia, on_delete=models.SET_NULL, blank=True, null=True
    )
    codigo_cliente = models.BigIntegerField(blank=True, null=True)
    identificacion = models.CharField(max_length=100, blank=True, null=True)
    cliente = models.CharField(max_length=100, blank=True, null=True)
    cuenta = models.BigIntegerField(blank=True, null=True)
    tarjeta = models.CharField(max_length=100, blank=True, null=True)
    sucursal = models.CharField(max_length=100, blank=True, null=True)
    poliza = models.BigIntegerField(blank=True, null=True)
    estado = models.CharField(max_length=15, blank=True, null=True, choices=ESTADO)
    observaciones = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    caja = models.BigIntegerField(null=True)
    bloque = models.PositiveIntegerField(null=True)
    usuario_creacion = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="usuario_creacion_poliza",
    )
    usuario_modificacion = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="usuario_modificacion_poliza",
    )
    history = AuditlogHistoryField()

    def __str__(self):
        return f"{self.codigo_cliente} - {self.cliente} - {self.poliza}"


class Tarea(models.Model):
    TAREAS = (
        ("Empate", "Empate"),
        ("Distribución", "Distribución"),
        ("Aperturas", "Aperturas"),
        ("Pólizas", "Pólizas"),
        ("Documentos Sueltos", "Documentos Sueltos"),
        ("Garantias", "Garantias"),
        ("Contratos", "Contratos"),
        ("Otros", "Otros"),
    )

    ESTADO = (
        ("Asignado", "Asignado"),
        ("Completado", "Completado"),
    )
    nombre = models.CharField(max_length=100, choices=TAREAS)
    tiempo = models.BigIntegerField(help_text="En minutos")
    analista_asignado = models.ForeignKey(
        Profile, blank=True, null=True, on_delete=models.SET_NULL
    )
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    estado = models.CharField(max_length=100, blank=True, null=True, choices=ESTADO)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    usuario_creacion = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="usuario_creacion_tarea",
    )
    usuario_modificacion = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="usuario_modificacion_tarea",
    )
    history = AuditlogHistoryField()

    def __str__(self):
        return f"{self.nombre} - {self.analista_asignado} - {self.descripcion}"


# AUDIT LOG

auditlog.register(Apertura)
auditlog.register(Contratos)
auditlog.register(Correspondencia)
auditlog.register(Desembolsos)
auditlog.register(Distribucion)
auditlog.register(DocumentosSueltos)
auditlog.register(Empate)
auditlog.register(Inmueble)
auditlog.register(Levantamientos)
auditlog.register(Observaciones)
auditlog.register(Poliza)
auditlog.register(Prestamo)
auditlog.register(Sobre)
auditlog.register(Tarea)
auditlog.register(Vehiculo)
