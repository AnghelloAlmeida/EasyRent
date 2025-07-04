# Generated by Django 5.0.4 on 2025-05-24 23:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('propiedades', '0007_propiedad_disponible_alter_propiedad_propietario'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='propiedad',
            name='pais',
            field=models.CharField(default='Ecuador', max_length=100),
        ),
        migrations.AddField(
            model_name='propiedad',
            name='tipo_propiedad',
            field=models.CharField(choices=[('casa', 'Casa'), ('apartamento', 'Apartamento'), ('terreno', 'Terreno'), ('local_comercial', 'Local Comercial'), ('oficina', 'Oficina'), ('otro', 'Otro')], default='casa', max_length=50),
        ),
        migrations.AlterField(
            model_name='propiedad',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='propiedades_pics/'),
        ),
        migrations.AlterField(
            model_name='propiedad',
            name='metros_cuadrados',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='propiedad',
            name='num_banos',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='propiedad',
            name='num_habitaciones',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='propiedad',
            name='propietario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
