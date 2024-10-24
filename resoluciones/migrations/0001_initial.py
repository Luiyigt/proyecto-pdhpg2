# Generated by Django 4.1.7 on 2024-08-21 16:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ResolucionFinal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expediente', models.CharField(max_length=50, unique=True)),
                ('denunciante', models.CharField(max_length=255)),
                ('victima', models.CharField(max_length=255)),
                ('derecho_humano_violado', models.CharField(max_length=255)),
                ('resolucion', models.TextField()),
                ('calificacion', models.CharField(max_length=50)),
                ('direccion', models.CharField(blank=True, max_length=255, null=True)),
                ('fecha_resolucion', models.DateField()),
                ('responsable', models.CharField(blank=True, max_length=255, null=True)),
                ('estado', models.CharField(choices=[('Pendiente', 'Pendiente'), ('Resuelta', 'Resuelta'), ('En Proceso', 'En Proceso')], max_length=50)),
                ('archivo_adjunto', models.FileField(blank=True, null=True, upload_to='')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('creado_por', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Resolución Final',
                'verbose_name_plural': 'Resoluciones Finales',
                'ordering': ['-fecha_resolucion'],
            },
        ),
    ]
