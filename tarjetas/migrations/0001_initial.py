# Generated by Django 4.2.11 on 2024-12-02 09:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Destino',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lugar', models.CharField(max_length=100)),
                ('activo', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.CharField(blank=True, max_length=200, null=True)),
                ('fecha', models.DateField(blank=True, null=True)),
                ('lugar', models.CharField(blank=True, max_length=100, null=True)),
                ('latitud', models.FloatField()),
                ('longitud', models.FloatField()),
                ('codigo', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Patologia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Roll',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Tarjeta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_t', models.CharField(max_length=100)),
                ('edad', models.IntegerField(blank=True, null=True)),
                ('sexo', models.CharField(choices=[('HOMBRE', 'HOMBRE'), ('MUJER', 'MUJER'), ('NSNC', 'NS/NC')], max_length=32)),
                ('filiacion', models.CharField(blank=True, max_length=200)),
                ('diagnostico', models.CharField(blank=True, max_length=500)),
                ('tratamiento', models.CharField(blank=True, max_length=500)),
                ('traslada_por', models.CharField(blank=True, max_length=50)),
                ('triaje_ini', models.CharField(choices=[('VERDE', 'VERDE'), ('AMARILLO', 'AMARILLO'), ('ROJO', 'ROJO'), ('MORADO', 'MORADO'), ('NEGRO', 'NEGRO')], max_length=10)),
                ('triaje_fin', models.CharField(choices=[('VERDE', 'VERDE'), ('AMARILLO', 'AMARILLO'), ('ROJO', 'ROJO'), ('MORADO', 'MORADO'), ('NEGRO', 'NEGRO')], max_length=10)),
                ('estado_traslado', models.CharField(choices=[('SOLICITADO', 'SOLICITADO'), ('GESTIONADO', 'GESTIONADO'), ('SALIDO_PSA', 'SALIDO_PSA'), ('REALIZADO', 'REALIZADO'), ('ALTA LUGAR', 'ALTA LUGAR')], max_length=32)),
                ('latitud', models.FloatField(blank=True, null=True)),
                ('longitud', models.FloatField(blank=True, null=True)),
                ('evento', models.ForeignKey(blank=True, db_column='evento', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='tarjetas.evento')),
                ('patologia', models.ForeignKey(blank=True, db_column='patologia', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='tarjetas.patologia')),
                ('traslada_a', models.ForeignKey(blank=True, db_column='destino', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='tarjetas.destino')),
            ],
        ),
        migrations.CreateModel(
            name='Hora',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hora_ini', models.DateTimeField(auto_now_add=True)),
                ('psa_in', models.DateTimeField(blank=True, null=True)),
                ('psa_out', models.DateTimeField(blank=True, null=True)),
                ('dest_in', models.DateTimeField(blank=True, null=True)),
                ('hora_fin', models.DateTimeField(blank=True, null=True)),
                ('tarjeta', models.ForeignKey(db_column='tarjeta', on_delete=django.db.models.deletion.DO_NOTHING, to='tarjetas.tarjeta')),
            ],
        ),
        migrations.CreateModel(
            name='Historial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitud', models.FloatField(blank=True, null=True)),
                ('longitud', models.FloatField(blank=True, null=True)),
                ('hora', models.DateTimeField(auto_now_add=True)),
                ('observaciones', models.CharField(blank=True, max_length=150)),
                ('roll', models.ForeignKey(db_column='roll', on_delete=django.db.models.deletion.DO_NOTHING, to='tarjetas.roll')),
                ('tarjeta', models.ForeignKey(db_column='tarjeta', on_delete=django.db.models.deletion.DO_NOTHING, to='tarjetas.tarjeta')),
            ],
        ),
    ]
