from rest_framework.serializers import ModelSerializer
from tarjetas.models import *

class EventosSerializer(ModelSerializer):
    class Meta:
        model = Evento
        fields = '__all__'
        
class DestinosSerializer(ModelSerializer):
    class Meta:
        model = Destino
        fields = '__all__'
        
class PatologiasSerializer(ModelSerializer):
    class Meta:
        model = Patologia
        fields = '__all__'
        
class TarjetasSerializer(ModelSerializer):
    class Meta:
        model = Tarjeta
        fields = '__all__'
        
class PsasSerializer(ModelSerializer):
    class Meta:
        model = Psa
        fields = '__all__'
        
