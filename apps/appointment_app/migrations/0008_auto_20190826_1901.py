# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-08-27 02:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appointment_app', '0007_auto_20190826_1842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointments',
            name='appointment_student',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attending_appointments', to='login_app.Users'),
        ),
        migrations.AlterField(
            model_name='appointments',
            name='category',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='login_app.SubCategories'),
        ),
    ]