# Generated by Django 2.1.4 on 2018-12-29 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0013_useralbum'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='audio_file',
            field=models.FileField(default='', upload_to=''),
        ),
    ]