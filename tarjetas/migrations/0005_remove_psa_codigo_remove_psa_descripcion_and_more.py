# Generated by Django 4.2.11 on 2024-12-02 13:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tarjetas', '0004_rename_triaje_fin_tarjeta_triaje_tarjeta_pos_psa'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='psa',
            name='codigo',
        ),
        migrations.RemoveField(
            model_name='psa',
            name='descripcion',
        ),
        migrations.RemoveField(
            model_name='psa',
            name='latitud',
        ),
        migrations.RemoveField(
            model_name='psa',
            name='longitud',
        ),
        migrations.RemoveField(
            model_name='psa',
            name='nombre',
        ),
        migrations.AddField(
            model_name='psa',
            name='activo',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='tarjeta',
            name='psa',
            field=models.ForeignKey(blank=True, db_column='psa', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='tarjetas.psa'),
        ),
        migrations.AlterField(
            model_name='psa',
            name='lugar',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
