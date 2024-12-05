from django.apps import apps
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
import json
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync
import logging
from IMV_T.config import MSG_LOGGER

logger = logging.getLogger(MSG_LOGGER)

def my_consumer_function():
    # Import models when needed
    Tarjeta = apps.get_model('tarjetas', 'Tarjeta')
    return Tarjeta.objects.all()
    # Now you can use MyModel in your consumer logic

class TableData(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add(
            'actualizacion_grupo',  # Nombre del grupo
            self.channel_name
        )
        evento_id = self.scope['session']['evento_id']
        tarjetas = await self.get_tarjetas(evento_id)
        tarjetas_count = await self.get_tarjetas_count(evento_id)
        tarjetas_count_open = await self.get_tarjetas_count_open(evento_id)
        await self.send(text_data=json.dumps({
            'tarjetas': tarjetas,
            'tarjetas_count': tarjetas_count,
            'tarjetas_count_open': tarjetas_count_open
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            'actualizacion_grupo',  # Nombre del grupo
            self.channel_name
        )

    async def updated_data(self, event):
        await self.channel_layer.group_add(
            'actualizacion_grupo',  # Nombre del grupo
            self.channel_name
        )
        evento_id = self.scope['session']['evento_id']
        tarjetas = await self.get_tarjetas(evento_id)
        tarjetas_count = await self.get_tarjetas_count(evento_id)
        tarjetas_count_open = await self.get_tarjetas_count_open(evento_id)
        await self.send(text_data=json.dumps({
            'tarjetas': tarjetas,
            'tarjetas_count': tarjetas_count,
            'tarjetas_count_open': tarjetas_count_open
        }))

    @database_sync_to_async
    def get_tarjetas(self, evento_id):
        Tarjeta = apps.get_model('tarjetas', 'Tarjeta')
        tarjetas = Tarjeta.objects.filter(evento=evento_id).order_by('-id').values('id','num_t', 'hora_ini', 'edad','sexo','triaje','patologia','traslada_a','traslada_por','estado_traslado','psa', 'pos_psa' ) 
        for tarjeta in tarjetas:
            tarjeta['hora_ini'] = tarjeta['hora_ini'].strftime('%d-%m-%Y %H:%M:%S')
        #print(tarjetas)
        tarjetas_list = [
            {
                'id':tarjeta['id'],
                'num_t':tarjeta['num_t'],
                'hora_ini': tarjeta['hora_ini'],
                'edad': tarjeta['edad'],
                'sexo': tarjeta['sexo'],
                'triaje': tarjeta['triaje'],
                'patologia': tarjeta['patologia'],
                'traslada_a': tarjeta['traslada_a'], 
                'traslada_por': tarjeta['traslada_por'],
                'psa': tarjeta['psa'],
                'pos_psa': tarjeta['pos_psa'],
            }
            for tarjeta in tarjetas
        ]
        #print(tarjetas_list)
        return tarjetas_list
    
    @database_sync_to_async
    def get_tarjetas_count(self, evento_id):
        Tarjeta = apps.get_model('tarjetas', 'Tarjeta')
        count = Tarjeta.objects.filter(evento=evento_id).count()
        return count
    
    @database_sync_to_async
    def get_tarjetas_count_open(self, evento_id):
        Tarjeta = apps.get_model('tarjetas', 'Tarjeta')
        count_open = Tarjeta.objects.filter(evento=evento_id).exclude(estado_traslado__in=['REALIZADO', 'ALTA LUGAR', 'SALIDA_PSA' ]).count()
        return count_open
    
class TableDataOpen(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add(
            'actualizacion_grupo',  # Nombre del grupo
            self.channel_name
        )
        evento_id = self.scope['session']['evento_id']
        tarjetas = await self.get_tarjetas(evento_id)
        tarjetas_count = await self.get_tarjetas_count(evento_id)
        tarjetas_count_open = await self.get_tarjetas_count_open(evento_id)
        await self.send(text_data=json.dumps({
            'tarjetas': tarjetas,
            'tarjetas_count': tarjetas_count,
            'tarjetas_count_open': tarjetas_count_open
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            'actualizacion_grupo',  # Nombre del grupo
            self.channel_name
        )

    async def updated_data(self, event):
        await self.channel_layer.group_add(
            'actualizacion_grupo',  # Nombre del grupo
            self.channel_name
        )
        evento_id = self.scope['session']['evento_id']
        tarjetas = await self.get_tarjetas(evento_id)
        tarjetas_count = await self.get_tarjetas_count(evento_id)
        tarjetas_count_open = await self.get_tarjetas_count_open(evento_id)
        await self.send(text_data=json.dumps({
            'tarjetas': tarjetas,
            'tarjetas_count': tarjetas_count,
            'tarjetas_count_open': tarjetas_count_open
        }))
        
    @database_sync_to_async
    def get_tarjetas(self, evento_id):
        Tarjeta = apps.get_model('tarjetas', 'Tarjeta')
        tarjetas = Tarjeta.objects.filter(evento=evento_id).order_by('-id').values('id','num_t', 'hora_ini', 'edad','sexo','triaje','patologia','traslada_a','traslada_por','estado_traslado','psa', 'pos_psa' ) 
        for tarjeta in tarjetas:
            tarjeta['hora_ini'] = tarjeta['hora_ini'].strftime('%d-%m-%Y %H:%M:%S')
        #print(tarjetas)
        tarjetas_list = [
            {
                'id':tarjeta['id'],
                'num_t':tarjeta['num_t'],
                'hora_ini': tarjeta['hora_ini'],
                'edad': tarjeta['edad'],
                'sexo': tarjeta['sexo'],
                'triaje': tarjeta['triaje'],
                'patologia': tarjeta['patologia'],
                'traslada_a': tarjeta['traslada_a'], 
                'traslada_por': tarjeta['traslada_por'],
                'psa': tarjeta['psa'],
                'pos_psa': tarjeta['pos_psa'],
            }
            for tarjeta in tarjetas
        ]
        #print(tarjetas_list)
        return tarjetas_list

    
    @database_sync_to_async
    def get_tarjetas_count(self, evento_id):
        Tarjeta = apps.get_model('tarjetas', 'Tarjeta')
        count = Tarjeta.objects.filter(evento=evento_id).count()
        return count
    
    @database_sync_to_async
    def get_tarjetas_count_open(self, evento_id):
        Tarjeta = apps.get_model('tarjetas', 'Tarjeta')
        count_open = Tarjeta.objects.filter(evento=evento_id).exclude(estado_traslado__in=['REALIZADO', 'ALTA LUGAR', 'SALIDA_PSA' ]).count()
        return count_open