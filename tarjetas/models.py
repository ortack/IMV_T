from django.db import models
from django.utils import timezone
#from mirage import fields
import datetime
from django.utils.timezone import now

class Evento(models.Model):
    nombre = models.CharField(max_length=100, blank=False, null=False)
    descripcion = models.CharField(max_length=200, blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    lugar = models.CharField(max_length=100, blank=True, null=True)
    latitud = models.FloatField(blank=False, null=False)
    longitud = models.FloatField(blank=False, null=False)
    codigo = models.CharField(max_length=10, blank=False, null=False)

    def __str__(self):
        return self.nombre
    
class Psa(models.Model):
    nombre = models.CharField(max_length=100, blank=False, null=False)
    descripcion = models.CharField(max_length=200, blank=True, null=True)
    lugar = models.CharField(max_length=100, blank=True, null=True)
    latitud = models.FloatField(blank=False, null=False)
    longitud = models.FloatField(blank=False, null=False)
    codigo = models.CharField(max_length=10, blank=False, null=False)
    evento = models.ForeignKey(Evento, models.DO_NOTHING, db_column='evento', blank=True, null=True)

    def __str__(self):
        return self.nombre

class Patologia(models.Model):
    tipo = models.CharField(max_length=100)

    def __str__(self):
        return self.tipo
    
class Destino(models.Model):
    lugar = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.lugar

class Psa(models.Model):
    lugar = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)
    evento = models.ForeignKey(Evento, models.DO_NOTHING, db_column='evento', blank=True, null=True)

    def __str__(self):
        return self.lugar



class Tarjeta(models.Model):
    TRIAJE = (
        ('VERDE', 'VERDE'),
        ('AMARILLO','AMARILLO'),
        ('ROJO', 'ROJO'),
        ('MORADO', 'MORADO'),
        ('NEGRO', 'NEGRO'),
    )
    ESTADO_TRASLADO = (
        ('PENDIENTE', 'PENDIENTE'),
        ('SOLICITADO', 'SOLICITADO'),
        ('GESTIONADO', 'GESTIONADO'),
        ('SALIDA_PSA', 'SALIDA_PSA'),
        ('REALIZADO', 'REALIZADO'),
        ('ALTA LUGAR', 'ALTA LUGAR'),
    ) 
    SEXO = (
        ('HOMBRE', 'HOMBRE'),
        ('MUJER','MUJER'),
        ('NSNC', 'NS/NC'),
    )
    
    num_t = models.CharField(max_length=100, blank=False)
    edad = models.IntegerField(blank=True, null=True)
    sexo = models.CharField(max_length=32,choices=SEXO)
    #filiacion = fields.EncryptedCharField(max_length=200, blank=True)
    filiacion = models.CharField(max_length=200, blank=True)
    patologia = models.ForeignKey(Patologia, models.DO_NOTHING, db_column='patologia', blank=True, null=True)
    diagnostico = models.CharField(max_length=500, blank=True)
    tratamiento = models.CharField(max_length=500, blank=True)
    traslada_a = models.ForeignKey(Destino, models.DO_NOTHING, db_column='destino', blank=True, null=True)
    traslada_por = models.CharField(max_length=50, blank=True)
    triaje_ini = models.CharField(max_length=10,choices=TRIAJE)
    triaje = models.CharField(max_length=10,choices=TRIAJE)
    estado_traslado = models.CharField(max_length=32,choices=ESTADO_TRASLADO)
    latitud = models.FloatField(blank=True, null=True)
    longitud = models.FloatField(blank=True, null=True)
    evento = models.ForeignKey(Evento, models.DO_NOTHING, db_column='evento', blank=True, null=True)
    hora_ini = models.DateTimeField(auto_now_add=True)
    psa_in = models.DateTimeField(blank=True, null=True)
    psa_out = models.DateTimeField(blank=True, null=True)
    dest_in = models.DateTimeField(blank=True, null=True)
    hora_fin = models.DateTimeField(blank=True, null=True)
    pos_psa = models.CharField(max_length=100, blank=True)
    psa = models.ForeignKey(Psa, models.DO_NOTHING, db_column='psa', blank=True, null=True)
    
    def __str__(self):
        return self.num_t
    
class Roll(models.Model):
    nombre = models.CharField(max_length=100, blank=False)
    
    def __str__(self):
        return self.nombre
    
class Historial(models.Model):
    latitud = models.FloatField(blank=True, null=True)
    longitud = models.FloatField(blank=True, null=True)
    hora = models.DateTimeField(auto_now_add=True)
    observaciones = models.CharField(max_length=150, blank=True)
    roll = models.ForeignKey(Roll, models.DO_NOTHING, db_column='roll', blank=False, null=False)
    tarjeta = models.ForeignKey(Tarjeta, models.DO_NOTHING, db_column='tarjeta', blank=False, null=False)

    def __str__(self):
        return self.equipo.nombre, self.hora_fin