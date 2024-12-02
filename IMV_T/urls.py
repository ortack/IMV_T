from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.loginPage, name='login'),
    # Para filtrar los equipos por evento
    path('logout/', views.logoutUser, name='logout'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('tarjetas/', include('tarjetas.urls')),
    #path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
