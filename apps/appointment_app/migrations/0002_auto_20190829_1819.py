# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-08-30 01:19
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointments',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 29, 18, 19, 2, 68545)),
        ),
    ]
