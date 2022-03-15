from asyncio.log import logger
from django.contrib import admin
from django.db.models.fields.related import ForeignKey
from .models import *
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget


class EmpateResource(resources.ModelResource):
    class Meta:
        model = Empate
        
class EmpateAdmin(ImportExportModelAdmin):
    resource_class=EmpateResource
    
class ContratosResource(resources.ModelResource):
    class Meta:
        model = Contratos

class ContratosAdmin(ImportExportModelAdmin):
    resource_class=ContratosResource

class DocumentosSueltosResource(resources.ModelResource):
    class Meta:
        model = DocumentosSueltos

class DocumentosSueltosAdmin(ImportExportModelAdmin):
    resource_class=DocumentosSueltosResource

class LevantamientosResource(resources.ModelResource):
    class Meta:
        model = Levantamientos

class LevantamientosAdmin(ImportExportModelAdmin):
    resource_class=LevantamientosResource

# class GarantiasResource(resources.ModelResource):
#     class Meta:
#         model = Garantias

# class GarantiasAdmin(ImportExportModelAdmin):
#     resource_class=GarantiasResource

class DesembolsosResource(resources.ModelResource):
    class Meta:
        model = Desembolsos

class DesembolsosAdmin(ImportExportModelAdmin):
    resource_class=DesembolsosResource

class DistribucionResource(resources.ModelResource):
    class Meta:
        model = Distribucion

class DistribucionAdmin(ImportExportModelAdmin):
    resource_class=DistribucionResource

class InmuebleResource(resources.ModelResource):
    class Meta:
        model = Inmueble

class InmuebleAdmin(ImportExportModelAdmin):
    resource_class=InmuebleResource

class VehiculoResource(resources.ModelResource):
    class Meta:
        model = Vehiculo

class VehiculoAdmin(ImportExportModelAdmin):
    resource_class=VehiculoResource

class CorrespondenciaResource(resources.ModelResource):
    class Meta:
        model=Correspondencia

class CorrespondenciaAdmin(ImportExportModelAdmin):
    recource_class = CorrespondenciaResource

class SobreResource(resources.ModelResource):
    class Meta:
        model=Sobre

class SobreaAdmin(ImportExportModelAdmin):
    recource_class = SobreResource

class PrestamoResource(resources.ModelResource):
    class Meta:
        model=Prestamo

class PrestamoAdmin(ImportExportModelAdmin):
    recource_class = PrestamoResource

class AperturaResource(resources.ModelResource):
    class Meta:
        model=Apertura

class AperturaAdmin(ImportExportModelAdmin):
    recource_class = AperturaResource

class PolizaResource(resources.ModelResource):
    class Meta:
        model=Poliza

class PolizaAdmin(ImportExportModelAdmin):
    recource_class = PolizaResource

class TipoOperacionResource(resources.ModelResource):
    class Meta:
        model=TipoOperacion

class TipoOperacionAdmin(ImportExportModelAdmin):
    recource_class = TipoOperacionResource

class ObservacionesResource(resources.ModelResource):
    class Meta:
        model=Observaciones

class ObservacionesAdmin(ImportExportModelAdmin):
    recource_class = ObservacionesResource

class CategoriaObservacionResource(resources.ModelResource):
    class Meta:
        model=CategoriaObservacion

class CategoriaObservacionAdmin(ImportExportModelAdmin):
    recource_class = CategoriaObservacionResource

class SubCategoriaObservacionResource(resources.ModelResource):
    class Meta:
        model=SubCategoriaObservacion

class SubCategoriaObservacionAdmin(ImportExportModelAdmin):
    recource_class = SubCategoriaObservacionResource

class ItemObservacionResource(resources.ModelResource):
    class Meta:
        model=ItemObservacion

class ItemObservacionAdmin(ImportExportModelAdmin):
    recource_class = ItemObservacionResource

class ParametroResource(resources.ModelResource):
    class Meta:
        model=Parametro

class ParametroAdmin(ImportExportModelAdmin):
    recource_class = ParametroResource

class TareaResource(resources.ModelResource):
    class Meta:
        model=Tarea

class TareaAdmin(ImportExportModelAdmin):
    recource_class = TareaResource

class FormatoContratoResource(resources.ModelResource):
    class Meta:
        model = FormatoContrato

class FormatoContratoAdmin(ImportExportModelAdmin):
    resource_class = FormatoContratoResource


admin.site.register(Empate,EmpateAdmin)
admin.site.register(Contratos,ContratosAdmin)
admin.site.register(DocumentosSueltos,DocumentosSueltosAdmin)
admin.site.register(Levantamientos,LevantamientosAdmin)
admin.site.register(Desembolsos,DesembolsosAdmin)
admin.site.register(Distribucion,DistribucionAdmin)
admin.site.register(Inmueble,InmuebleAdmin)
admin.site.register(Vehiculo,VehiculoAdmin)
admin.site.register(Correspondencia,CorrespondenciaAdmin)
admin.site.register(Sobre,SobreaAdmin)
admin.site.register(Prestamo,PrestamoAdmin)
admin.site.register(Apertura,AperturaAdmin)
admin.site.register(Poliza,PolizaAdmin)
admin.site.register(TipoOperacion,TipoOperacionAdmin)
admin.site.register(Observaciones,ObservacionesAdmin)
admin.site.register(CategoriaObservacion,CategoriaObservacionAdmin)
admin.site.register(SubCategoriaObservacion,SubCategoriaObservacionAdmin)
admin.site.register(ItemObservacion,ItemObservacionAdmin)
admin.site.register(Parametro,ParametroAdmin)
admin.site.register(Tarea,TareaAdmin)
admin.site.register(FormatoContrato,FormatoContratoAdmin)
admin.site.register(Profile)

# Register your models here.
