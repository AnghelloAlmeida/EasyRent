# Generated by Django 5.2.1 on 2025-06-03 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('propiedades', '0015_rename_imagen_propiedad_imagen_principal_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='propiedad',
            name='ia_calificacion',
            field=models.IntegerField(blank=True, choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], null=True, verbose_name='Calificación IA (1-5)'),
        ),
        migrations.AddField(
            model_name='propiedad',
            name='ia_reseña_generada',
            field=models.TextField(blank=True, null=True, verbose_name='Reseña IA'),
        ),
    ]
