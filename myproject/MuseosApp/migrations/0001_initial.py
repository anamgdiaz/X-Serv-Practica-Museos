# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cambio_Estilo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('tamaño', models.CharField(max_length=32)),
                ('color', models.CharField(max_length=32)),
                ('titulo', models.CharField(max_length=32)),
                ('usuario', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comentarios',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('txt', models.TextField()),
                ('usuario', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Museo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('id_museo', models.IntegerField()),
                ('nombre', models.CharField(max_length=128)),
                ('descripcion', models.TextField(null=True)),
                ('horario', models.TextField(null=True)),
                ('equipamiento', models.TextField(null=True)),
                ('transporte', models.TextField(null=True)),
                ('accesibilidad', models.CharField(max_length=8)),
                ('content_url', models.URLField()),
                ('nombre_via', models.CharField(max_length=128)),
                ('clase_vial', models.CharField(max_length=64)),
                ('num', models.FloatField()),
                ('localidad', models.CharField(max_length=64)),
                ('provincia', models.CharField(max_length=64)),
                ('codigo_postal', models.IntegerField(null=True)),
                ('barrio', models.CharField(max_length=64)),
                ('distrito', models.CharField(max_length=64)),
                ('coordenada_x', models.IntegerField(null=True)),
                ('coordenada_y', models.IntegerField(null=True)),
                ('latitud', models.FloatField(null=True)),
                ('longitud', models.FloatField(null=True)),
                ('telefono', models.TextField(null=True)),
                ('email', models.CharField(max_length=128, null=True)),
                ('num_comentario', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Museo_Seleccionado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('fecha', models.DateField()),
                ('museo', models.ForeignKey(to='MuseosApp.Museo')),
                ('usuario', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='comentarios',
            name='museo',
            field=models.ForeignKey(to='MuseosApp.Museo'),
        ),
    ]
