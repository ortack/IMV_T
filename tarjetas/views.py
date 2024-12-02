from .models import Tarjeta,Evento
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from .forms import Roll1Form, TarjetaPsaInForm, Roll2Form
import csv
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.contrib.auth.decorators import user_passes_test
from django.db import transaction
import logging
from IMV_T.config import MSG_LOGGER


logger = logging.getLogger(MSG_LOGGER)

# Create your views here.

#Roll de primer interviente
def roll_1(request):
    if request.method == "POST":
        form = Roll1Form(request.POST.copy())
        if form.is_valid():
            evento = Evento.objects.get(id=request.session['evento_id'])
            tarjeta = form.save(commit=False) 
            tarjeta.evento = evento
            tarjeta.triaje = tarjeta.triaje_ini
            tarjeta.save()
            form = Roll1Form()
    else:
        form = Roll1Form()
    return render(request, 'tarjetas/tarjeta_new.html', {'form': form})

# PSA Entrada
@login_required(login_url='login')
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
            return render(request, 'tarjeta/roll2.html', )
    else:
        form = TarjetaPsaInForm(instance=post)
    return render(request, 'tarjetas/tarjeta_psa_in.html', {'form': form})


@login_required(login_url='login')
def roll_3(request):
    return None

@login_required(login_url='login')
def roll_4(request):
    return None

@login_required(login_url='login')
def roll(request):
    return None


@login_required(login_url='login')
def tarjetas_list(request):
    tarjetas = Tarjeta.objects.filter(evento = request.session['evento_id']).order_by('-id')
    
    evento_id = request.session['evento_id']
    tarjetas_count = Tarjeta.objects.filter(evento = request.session['evento_id']).count()
    return render(request, 'tarjetas/tarjetas_list.html', {'tarjetas': tarjetas,'tarjetas_count': tarjetas_count})  