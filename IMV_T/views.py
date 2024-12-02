from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.shortcuts import render
from tarjetas.models import *
#from tarjetas.forms import *
from django.http import JsonResponse

def loginPage(request):
    if request.method == "POST":
        username =request.POST.get('username')
        password = request.POST.get('password')
        roll = request.POST.get('roll')
        evento = request.POST.get('evento')
        user = authenticate(request, username=username, password =password )
        if user is not None:
            login (request, user)
            request.session['evento_id'] = evento
            request.session['evento'] = Evento.objects.filter(id = evento).values()[0]['nombre'] # Guarda el evento en la sesion
            request.session['roll'] = roll # Guarda el roll en la sesion
            if roll != '':
                roll_id = Roll.objects.filter(nombre = roll).values()[0]['id']
                request.session['roll_id'] = roll_id # Guarda el roll en la sesion
                if roll_id == 1:
                    return redirect('/tarjetas/roll_1/')
                elif roll_id == 2 :
                    return redirect('/tarjetas/roll_2/')
                elif roll_id == 3 :
                    return redirect('/tarjetas/roll_3/')
                elif roll_id == 4 :
                    return redirect('/tarjetas/roll_4/')
                else:
                    return redirect('/tarjetas/roll/')
            return redirect('index')
    eventos = Evento.objects.all()
    rolls = Roll.objects.all()
    context = {'rolls':rolls, 'eventos':eventos}
    return render(request , 'tarjetas/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')


@login_required(login_url='login') # quitar comentario para que se requiera login en la pagina principal
def index(request):
    try:
        evento = Evento.objects.filter(id = request.session['evento_id'])
        nombre = evento.values()[0]['nombre']
    except:
        return redirect('login')
    #print(evento.values())
    
    descripcion = evento.values()[0]['descripcion']
    latitud = evento.values()[0]['latitud']
    longitud = evento.values()[0]['longitud']
    lat = str(latitud).replace(',','.')
    lon = str(longitud).replace(',','.')
    tarjetas_count = Tarjeta.objects.filter(evento = request.session['evento_id']).count()
    return render(request, 'tarjetas/index.html', { 'descripcion':descripcion, 'tarjetas_count':tarjetas_count, 'latitud':lat, 'longitud':lon,})