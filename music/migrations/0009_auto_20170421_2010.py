# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-21 20:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0008_album_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='audio_file',
            field=models.FileField(default=b'', upload_to=b'two/'),
        ),
    ]
