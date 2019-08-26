# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-08-26 21:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_app', '0010_users_desc'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='skills_to_learn',
            field=models.ManyToManyField(related_name='students', to='login_app.SubCategories'),
        ),
        migrations.AddField(
            model_name='users',
            name='skills_to_teach',
            field=models.ManyToManyField(related_name='teachers', to='login_app.SubCategories'),
        ),
    ]
