# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MuseosApp', '0003_museo_csv'),
    ]

    operations = [
        migrations.AddField(
            model_name='museo',
            name='puntuacion',
            field=models.IntegerField(default=0),
        ),
    ]
