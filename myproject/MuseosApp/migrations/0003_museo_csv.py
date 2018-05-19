# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MuseosApp', '0002_auto_20180519_0927'),
    ]

    operations = [
        migrations.CreateModel(
            name='Museo_CSV',
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
                ('num', models.FloatField()),
                ('localidad', models.CharField(max_length=64)),
                ('provincia', models.CharField(max_length=64)),
                ('codigo_postal', models.IntegerField(null=True)),
                ('barrio', models.CharField(max_length=64)),
                ('distrito', models.CharField(max_length=64)),
                ('telefono', models.TextField(null=True)),
                ('email', models.CharField(max_length=128, null=True)),
            ],
        ),
    ]
