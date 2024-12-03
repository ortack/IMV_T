from django.shortcuts import render
from api.serializers import TarjetasSerializer, EventosSerializer, DestinosSerializer, PsasSerializer, PatologiasSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from tarjetas.models import *
from tarjetas.forms import *
from django.utils import timezone
from django.conf import settings
from rest_framework import status
from IMV_T.config import DJANGO_LOGGER
import json
import logging
logger = logging.getLogger(DJANGO_LOGGER)
from django.db import transaction
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from datetime import datetime,timedelta
from django.utils.timezone import now


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getRoutes(request):
    routtes = [

        {
            'Endpoint': '/api/eventos/',
            'method': 'GET',
            'body': None,
            'description': 'Retorna todos los eventos'
        },
        {
            'Endpoint': '/api/destinos/',
            'method': 'GET',
            'body': None,
            'description': 'Retorna todos los destinos activos'
        },
        {
            'Endpoint': '/api/patologias/',
            'method': 'GET',
            'body': None,
            'description': 'Retorna todos las patologias'
        },
        {
            'Endpoint': '/api/tarjetas/<int:evento_id>/',
            'method': 'GET',
            'body': None,
            'description': 'Retorna todas las tarjetas de un evento por id'
        },
        {
            'Endpoint': '/api/psas/<int:evento_id>/',
            'method': 'GET',
            'body': None,
            'description': 'Retorna todos los Psas de un evento por id'
        },
        {
            'Endpoint': '/api/tarjeta/create/',
            'method': 'POST',
            'body': {'message'},
            'description': 'Crea una Tarjeta'
        },
        {
            'Endpoint': '/api/tarjeta/psa_in/',
            'method': 'POST',
            'body': {'message'},
            'description': 'Entrada al psa de una Tarjeta'
        },
        {
            'Endpoint': '/api/tarjeta/psa_out/',
            'method': 'POST',
            'body': {'message'},
            'description': 'Salida psa de una Tarjeta'
        },
        
    ]
    return Response(routtes)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getEventos(request):
    eventos = Evento.objects.all()
    serializer = EventosSerializer(eventos, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getDestinos(request):
    destinos = Destino.objects.filter(activo = True)
    serializer = DestinosSerializer(destinos, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getPatologias(request):
    patologias = Patologia.objects.all()
    serializer = PatologiasSerializer(patologias, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getTarjetas(request, evento_id):
    tarjetas = Tarjeta.objects.filter(evento = evento_id)
    serializer = TarjetasSerializer(tarjetas, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getPsas(request, evento_id):
    psas = Psa.objects.filter(evento = evento_id)
    serializer = PsasSerializer(psas, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@transaction.atomic
def createTarjeta(request):
    data = request.data
    evento_nombre = data[0]['evento']
    hora_tarjeta_ini = datetime.now()
    #print(form_tarjeta)
    try:
        tarjeta = Tarjeta()
        evento = Evento.objects.get(nombre = evento_nombre)
        tarjeta.evento = evento
        tarjeta.hora_ini = hora_tarjeta_ini
        tarjeta.triaje_ini = data[0]["triaje_ini"]
        tarjeta.triaje = data[0]["triaje_ini"]
        tarjeta.num_t = data[0]["num_t"]
        tarjeta.edad = data[0]["edad"]
        tarjeta.sexo = data[0]["sexo"]
        tarjeta.latitud = data[0]["latitud"]
        tarjeta.longitud = data[0]["longitud"]
        tarjeta.estado_traslado = 'PENDIENTE'
        tarjeta.save()  # Guardar el objeto en la base de datos
        # para actualizar los datos en tiempo real
        # channel_layer = get_channel_layer()
        # async_to_sync(channel_layer.group_send)(
        #     'actualizacion_grupo',  # Nombre del grupo definido en el WebSocket Consumer
        #     {
        #         'type': 'updated_data',  # Método para manejar la actualización
        #     }
        # )
        tarjeta = Tarjeta.objects.filter(id = tarjeta.id)
        serializer = TarjetasSerializer(tarjeta, many=True)
        return Response(serializer.data)
        #return Response("ok")
    except Exception as e:
        logger.error(e)
        return Response("error: " + str(e))
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@transaction.atomic
def psaIn(request):
    data = request.data
    id_tarjeta = int(data[0]['id_tarjeta'])
    psa_in_date = datetime.now().replace(tzinfo=timezone.utc)
    try:
        tarjeta = Tarjeta.objects.get(id = id_tarjeta)
        tarjeta.psa_in = psa_in_date
        print(psa_in_date,tarjeta.psa_in)
        tarjeta.triaje = data[0]["triaje"]
        tarjeta.edad = data[0]["edad"]
        tarjeta.sexo = data[0]["sexo"]
        tarjeta.latitud = data[0]["latitud"]
        tarjeta.longitud = data[0]["longitud"]
        tarjeta.psa = Psa.objects.get(nombre = data[0]["psa_nombre"])
        tarjeta.pos_psa = data[0]["pos_psa"]
        tarjeta.patologia = Patologia.objects.get(tipo = data[0]["patologia"])
        tarjeta.save()  # Guardar el objeto en la base de datos
        # para actualizar los datos en tiempo real
        # channel_layer = get_channel_layer()
        # async_to_sync(channel_layer.group_send)(
        #     'actualizacion_grupo',  # Nombre del grupo definido en el WebSocket Consumer
        #     {
        #         'type': 'updated_data',  # Método para manejar la actualización
        #     }
        # )
        tarjeta = Tarjeta.objects.filter(id = tarjeta.id)
        serializer = TarjetasSerializer(tarjeta, many=True)
        return Response(serializer.data)
        #return Response("ok")
    except Exception as e:
        logger.error(e)
        return Response("error: " + str(e))
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@transaction.atomic
def psaOut(request):
    data = request.data
    id_tarjeta = int(data[0]['id_tarjeta'])
    psa_out_date = datetime.now().replace(tzinfo=timezone.utc)
    #print(form_tarjeta)
    try:
        tarjeta = Tarjeta.objects.get(id = id_tarjeta)
        tarjeta.psa_out = psa_out_date
        tarjeta.triaje = data[0]["triaje"]
        tarjeta.filiacion = data[0]["filiacion"]
        tarjeta.diagnostico = data[0]["diagnostico"]
        tarjeta.tratamiento = data[0]["tratamiento"]
        tarjeta.traslada_a = Destino.objects.get(lugar = data[0]["traslada_a"])
        tarjeta.traslada_por = data[0]["traslada_por"]
        tarjeta.estado_traslado = 'SALIDA_PSA'
        tarjeta.patologia = Patologia.objects.get(tipo = data[0]["patologia"])
        tarjeta.save()  # Guardar el objeto en la base de datos
        # para actualizar los datos en tiempo real
        # channel_layer = get_channel_layer()
        # async_to_sync(channel_layer.group_send)(
        #     'actualizacion_grupo',  # Nombre del grupo definido en el WebSocket Consumer
        #     {
        #         'type': 'updated_data',  # Método para manejar la actualización
        #     }
        # )
        tarjeta = Tarjeta.objects.filter(id = tarjeta.id)
        serializer = TarjetasSerializer(tarjeta, many=True)
        return Response(serializer.data)
        #return Response("ok")
    except Exception as e:
        logger.error(e)
        return Response("error: " + str(e))

