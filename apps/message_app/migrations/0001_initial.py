# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-08-26 21:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('appointment_app', '0001_initial'),
        ('login_app', '0008_categories_subcategories'),
    ]

    operations = [
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('appointment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='appointment_app.Appointments')),
                ('message_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='login_app.Users')),
            ],
        ),
    ]