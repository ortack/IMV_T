from django import forms
from .models import Tarjeta
from django.utils.timezone import now

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
        fields = ('num_t', 'triaje_ini', 'edad', 'sexo', 'patologia', 'latitud', 'longitud', 'triaje', 'psa', 'pos_psa', 'psa_in')

        labels = {
            'num_t': 'Numero de Tarjeta',
            'triaje_ini': 'Triaje Inicial',
        }
        widgets = {
            'num_t': forms.TextInput(attrs={'readonly': 'readonly'}),
            'triaje_ini': forms.TextInput(attrs={'readonly': 'readonly'}),
            'latitud': forms.TextInput(attrs={'id': 'id_latitud', 'readonly': 'readonly'}),
            'longitud': forms.TextInput(attrs={'id': 'id_longitud', 'readonly': 'readonly'}),
            'psa_in': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%d/%m/%Y %H:%M'),
        } 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Inicializar el campo psa_in con la fecha y hora actual
        self.fields['psa_in'].initial = now().strftime('%d/%m/%Y %H:%M')
        
class Roll3Form(forms.Form):
    num_t = forms.CharField(label="Numero de Tarjeta", max_length=100)
        
class TarjetaPsaOutForm(forms.ModelForm):
    class Meta:
        model = Tarjeta
        fields = ('num_t', 'patologia', 'triaje', 'diagnostico', 'tratamiento', 'traslada_a', 'traslada_por', 'psa_out', 'filiacion')
        labels = {'num_t': 'Numero de Tarjeta',
            'traslado_a': 'Se traslada a ',
            'traslada_por': 'Se traslada por',
            'filiacion': 'Filiacion. si se dispone'
            }
        widgets = {
            'num_t': forms.TextInput(attrs={'readonly': 'readonly'}),
            'psa_out': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%d/%m/%Y %H:%M'),
            'diagnostico': forms.Textarea(attrs={'rows': 4, 'cols': 100}),  # Long text para diagnóstico
            'tratamiento': forms.Textarea(attrs={'rows': 4, 'cols': 100}),  # Long text para tratamiento
            'filiacion': forms.Textarea(attrs={'rows': 2, 'cols': 40}),  # Long text para tratamiento
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Inicializar el campo psa_in con la fecha y hora actual
        self.fields['psa_out'].initial = now().strftime('%d/%m/%Y %H:%M')
        
class TarjetaEditForm(forms.ModelForm):
    class Meta:
        model = Tarjeta
        fields = ('__all__')
        labels = {'num_t': 'Numero de Tarjeta',
            'traslado_a': 'Se traslada a ',
            'traslada_por': 'Se traslada por',
            'psa_in': 'Hora llegada al PSA',
            'psa_out': 'Hora salida del PSA',
            'dest_in': 'Hora llegada al hospital',
            'hora_fin': 'Hora finalizacion',
            'pos_psa': 'Lugar en el PSA',
            }
        widgets = {
            'psa_in': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%d/%m/%Y %H:%M'),
            'psa_out': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%d/%m/%Y %H:%M'),
            'dest_in': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%d/%m/%Y %H:%M'),
            'hora_fin': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%d/%m/%Y %H:%M'),
            'diagnostico': forms.Textarea(attrs={'rows': 4, 'cols': 100}),  # Long text para diagnóstico
            'tratamiento': forms.Textarea(attrs={'rows': 4, 'cols': 100}),  # Long text para tratamiento
            'filiacion': forms.Textarea(attrs={'rows': 2, 'cols': 40}),  # Long text para tratamiento
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Inicializar el campo psa_in con la fecha y hora actual
        self.fields['psa_out'].initial = now().strftime('%d/%m/%Y %H:%M')
        
class EstadoTrasladoForm(forms.ModelForm):
    class Meta:
        model = Tarjeta
        fields = ('num_t', 'estado_traslado', 'traslada_a', 'traslada_por' )
        labels = {
            'num_t': 'Numero de Tarjeta',
            'estado_traslado': 'Estado del traslado',
            'traslado_a': 'Se traslada a ',
            'traslada_por': 'Se traslada por',
        }
        widgets = {
            'num_t': forms.TextInput(attrs={'readonly': 'readonly'}),
        }
