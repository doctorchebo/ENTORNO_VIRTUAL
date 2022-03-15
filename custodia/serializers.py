
from rest_framework import serializers
from .models import *

class EmpateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empate
        fields = '__all__'
class DesembolsosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Desembolsos
        fields = '__all__'

class ObservacionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Observaciones
        fields = ['destino','categoria','sub_categoria','observacion','glosa','subsanado','fecha_observación','fecha_respuesta','fecha_seguimiento','comentarios_custodia','comentarios_area_observada','usuario_observacion']
    
    def create(self, validated_data):
        empate_id = self.context['empate_id']
        return Observaciones.objects.create(empate_id=empate_id, **validated_data)
class PerfilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user','nombre','codigo_banco','cargo']
        