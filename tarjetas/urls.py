from django.urls import path
from . import views

urlpatterns = [
    path('roll_1/', views.roll_1, name='roll_1'),
    path('roll_2/', views.roll_2, name='roll_2'),
    path('roll_3/', views.roll_3, name='roll_3'),
    path('roll_4/', views.roll_4, name='roll_4'),
    path('roll/', views.roll, name='roll'),
    path('tarjeta_edit/<int:tarjeta_id>', views.tarjeta_edit, name='tarjeta_edit'),
    path('tarjetas_list/', views.tarjetas_list, name='tarjetas_list'),
    path('tarjetas_list_pendientes/', views.tarjetas_list_pendientes, name='tarjetas_list_pendientes'),
    path('tarjeta_psa_in/<int:tarjeta_id>/', views.tarjeta_psa_in, name='tarjeta_psa_in'),
    path('tarjeta_psa_out/<int:tarjeta_id>/', views.tarjeta_psa_out, name='tarjeta_psa_out'),
    path('estado_traslado/<int:tarjeta_id>/', views.estado_traslado, name='estado_traslado'),
]


