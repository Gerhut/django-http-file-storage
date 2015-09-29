# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import project.storages


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='media',
            name='height',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='media',
            name='width',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='media',
            name='file',
            field=models.ImageField(height_field=b'height', storage=project.storages.HTTPStorage(b'http://localhost:5000/'), width_field=b'width', upload_to=b''),
            preserve_default=True,
        ),
    ]
