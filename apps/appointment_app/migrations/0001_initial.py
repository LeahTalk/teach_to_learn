# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-08-29 21:24
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('login_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=datetime.datetime(2019, 8, 29, 14, 24, 6, 878508))),
                ('location', models.CharField(max_length=255)),
                ('pending_credit', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('appointment_creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_appointments', to='login_app.Users')),
                ('appointment_student', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attending_appointments', to='login_app.Users')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='login_app.SubCategories')),
            ],
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField()),
                ('content', models.TextField()),
                ('role', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('appointment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='appointment_app.Appointments')),
                ('review_creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_reviews', to='login_app.Users')),
                ('review_receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_reviews', to='login_app.Users')),
            ],
        ),
    ]
