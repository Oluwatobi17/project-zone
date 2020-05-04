# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2020-04-23 16:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='comment',
            field=models.CharField(default=None, max_length=1000),
        ),
        migrations.AlterField(
            model_name='project',
            name='picture',
            field=models.FileField(default='defaultproject.jpg', upload_to='ProjectPic/'),
        ),
    ]
