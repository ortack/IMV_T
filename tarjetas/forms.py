from django import forms
from .models import Tarjeta

class Roll1Form(forms.ModelForm):
    class Meta:
        model = Tarjeta
        fields = ('num_t', 'triaje_ini','edad', 'sexo','latitud','longitud')
        labels = {
            'num_t': 'Numero de Tarjeta',
            'triaje_ini': 'Triaje Inicial',
        }
        widgets = {
            'latitud': forms.TextInput(attrs={'id': 'id_latitud', 'readonly': 'readonly'}),
            'longitud': forms.TextInput(attrs={'id': 'id_longitud', 'readonly': 'readonly'}),
        }
        
class Roll2Form(forms.Form):
    num_t = forms.CharField(label="Numero de Tarjeta", max_length=100)

class TarjetaPsaInForm(forms.ModelForm):
    class Meta:
        model = Tarjeta
        fields = ('num_t', 'triaje_ini','edad', 'sexo','patologia','latitud','longitud','triaje','psa','pos_psa')
        labels = {
            'num_t': 'Numero de Tarjeta',
            'triaje_ini': 'Triaje Inicial',
        }
        widgets = {
            'num_t': forms.TextInput(attrs={'readonly': 'readonly'}),
            'triaje_ini': forms.TextInput(attrs={'readonly': 'readonly'}),
            'latitud': forms.TextInput(attrs={'id': 'id_latitud', 'readonly': 'readonly'}),
            'longitud': forms.TextInput(attrs={'id': 'id_longitud', 'readonly': 'readonly'}),
        }