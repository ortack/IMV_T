from django.contrib import admin
from .models import Evento, Tarjeta, Roll, Destino, Historial,Patologia,Psa
    
# Register your models here.
admin.site.register(Evento)
admin.site.register(Tarjeta)
admin.site.register(Roll)
admin.site.register(Destino)
admin.site.register(Patologia)
admin.site.register(Historial)
admin.site.register(Psa)