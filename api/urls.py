from django.urls import path
from . import views



urlpatterns = [
    path('', views.getRoutes, name='getRoutes'),
    path('eventos/', views.getEventos, name='getEventos'),
    path('destinos/', views.getDestinos, name='getDestinos'),
    path('patologias/', views.getPatologias, name='getPatologias'),
    path('tarjetas/<int:evento_id>', views.getTarjetas, name='getTarjetas'),
    path('psas/<int:evento_id>', views.getPsas, name='getPsas'),
    path('tarjeta/create', views.createTarjeta, name = 'createTarjeta'),
    path('tarjeta/psain', views.psaIn, name = 'psaIn'),
    path('tarjeta/psaout', views.psaOut, name = 'psaOut'),
]

