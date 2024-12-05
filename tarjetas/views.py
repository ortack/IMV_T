from .models import Tarjeta,Evento
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from .forms import Roll1Form, TarjetaPsaInForm, Roll2Form, EstadoTrasladoForm, Roll3Form, TarjetaPsaOutForm, TarjetaEditForm
import csv
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.contrib.auth.decorators import user_passes_test
from django.db import transaction
import logging
from IMV_T.config import MSG_LOGGER
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


logger = logging.getLogger(MSG_LOGGER)

# Create your views here.

# Para actualizar el tareaface
def update_tareaface():
        # para actualizar los datos en tiempo real
        #print('entro update tareaface')
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'actualizacion_grupo',  # Nombre del grupo definido en el WebSocket Consumer
            {
                'type': 'updated_data',  # Método para manejar la actualización
            }
        )

#Roll de primer interviente
#@login_required(login_url='login')
def roll_1(request):
    if request.method == "POST":
        form = Roll1Form(request.POST.copy())
        if form.is_valid():
            evento = Evento.objects.get(id=request.session['evento_id'])
            tarjeta = form.save(commit=False) 
            tarjeta.evento = evento
            tarjeta.triaje = tarjeta.triaje_ini
            tarjeta.estado_traslado = "PENDIENTE"
            tarjeta.save()
            # para actualizar los datos en tiempo real
            update_tareaface()
            form = Roll1Form()
    else:
        form = Roll1Form()
    return render(request, 'tarjetas/tarjeta_new.html', {'form': form})

# PSA Entrada
#@login_required(login_url='login')
def roll_2(request):
    if request.method == "POST":
        form = Roll2Form(request.POST)
        if form.is_valid():
            num_t = form.cleaned_data['num_t']
            try:
                tarjeta = Tarjeta.objects.get(num_t=num_t)
                return redirect('tarjeta_psa_in', tarjeta_id=tarjeta.id)  # Redirige a la vista de edición
            except Tarjeta.DoesNotExist:
                form.add_error('num_t', 'Tarjeta no encontrada')
    else:
        form = Roll2Form()
    form = Roll2Form()
    return render(request, 'tarjetas/roll2.html', {'form': form})

def tarjeta_psa_in(request, tarjeta_id):
    post = get_object_or_404(Tarjeta,id=tarjeta_id)
    if request.method == "POST":
        form = TarjetaPsaInForm(request.POST.copy(), instance=post)
        if form.is_valid():
            post = form.save()
            post.save()
            # para actualizar los datos en tiempo real
            update_tareaface()
            return redirect('roll_2', )
    else:
        form = TarjetaPsaInForm(instance=post)
    return render(request, 'tarjetas/tarjeta_psa_in.html', {'form': form})

# Salida del PSA
#@login_required(login_url='login')
def roll_3(request):
    if request.method == "POST":
        form = Roll3Form(request.POST)
        if form.is_valid():
            num_t = form.cleaned_data['num_t']
            try:
                tarjeta = Tarjeta.objects.get(num_t=num_t)
                return redirect('tarjeta_psa_out', tarjeta_id=tarjeta.id)  # Redirige a la vista de edición
            except Tarjeta.DoesNotExist:
                form.add_error('num_t', 'Tarjeta no encontrada')
    else:
        form = Roll3Form()
    form = Roll3Form()
    return render(request, 'tarjetas/roll3.html', {'form': form})

def tarjeta_psa_out(request, tarjeta_id):
    post = get_object_or_404(Tarjeta,id=tarjeta_id)
    if request.method == "POST":
        form = TarjetaPsaOutForm(request.POST.copy(), instance=post)
        if form.is_valid():
            post = form.save()
            post.estado_traslado = 'SALIDA_PSA'
            post.save()
            # para actualizar los datos en tiempo real
            update_tareaface()
            return redirect('roll_3', )
    else:
        form = TarjetaPsaOutForm(instance=post)
    return render(request, 'tarjetas/tarjeta_psa_out.html', {'form': form})

def tarjeta_edit(request, tarjeta_id):
    post = get_object_or_404(Tarjeta,id=tarjeta_id)
    if request.method == "POST":
        form = TarjetaEditForm(request.POST.copy(), instance=post)
        if form.is_valid():
            post = form.save()
            post.save()
            # para actualizar los datos en tiempo real
            update_tareaface()
            return redirect('tarjetas_list', )
    else:
        form = TarjetaEditForm(instance=post)
    return render(request, 'tarjetas/tarjeta_edit.html', {'form': form})

@login_required(login_url='login')
def roll_4(request):
    return None

@login_required(login_url='login')
def roll(request):
    return None


@login_required(login_url='login')
def tarjetas_list(request):
    tarjetas = Tarjeta.objects.filter(evento = request.session['evento_id']).order_by('-id')
    tarjetas_count = Tarjeta.objects.filter(evento = request.session['evento_id']).count()
    return render(request, 'tarjetas/tarjetas_list.html', {'tarjetas': tarjetas,'tarjetas_count': tarjetas_count}) 

@login_required(login_url='login')
def tarjetas_list_pendientes(request):
    tarjetas = Tarjeta.objects.filter(evento=request.session['evento_id']).exclude(estado_traslado__in=['REALIZADO', 'ALTA LUGAR', 'SALIDA_PSA' ]).order_by('-id')
    tarjetas_count = Tarjeta.objects.filter(evento=request.session['evento_id']).exclude(estado_traslado__in=['REALIZADO', 'ALTA LUGAR', 'SALIDA_PSA' ]).count()
    return render(request, 'tarjetas/tarjetas_list.html', {'tarjetas': tarjetas,'tarjetas_count': tarjetas_count})   

def estado_traslado(request, tarjeta_id):
    post = get_object_or_404(Tarjeta,id=tarjeta_id)
    if request.method == "POST":
        form = EstadoTrasladoForm(request.POST.copy(), instance=post)
        if form.is_valid():
            post = form.save()
            post.save()
            # para actualizar los datos en tiempo real
            update_tareaface()
            return redirect('tarjetas_list', )
    else:
        form = EstadoTrasladoForm(instance=post)
    return render(request, 'tarjetas/estado_traslados.html', {'form': form})