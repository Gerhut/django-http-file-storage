# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import project.storages


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('file', models.FileField(storage=project.storages.HTTPStorage(b'http://localhost:5000/'), upload_to=b'')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
