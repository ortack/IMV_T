from django.urls import path
from . import views

urlpatterns = [
    path('roll_1/', views.roll_1, name='roll_1'),
    path('roll_2/', views.roll_2, name='roll_2'),
    path('roll_3/', views.roll_3, name='roll_3'),
    path('roll_4/', views.roll_4, name='roll_4'),
    path('roll/', views.roll, name='roll'),
    path('tarjetas_list/', views.tarjetas_list, name='tarjetas_list'),
    path('tarjeta_psa_in/<int:tarjeta_id>/', views.tarjeta_psa_in, name='tarjeta_psa_in'),
]


