from __future__ import unicode_literals
from django.db import models
from apps.login_app.models import *

class Appointments(models.Model):
    appointment_creator = models.ForeignKey(Users, related_name = 'created_appointments')
    appointment_student = models.ForeignKey(Users, related_name = 'attending_appointments')
    appointment_date = models.DateField()
    appointment_time = models.FloatField()
    appointment_location = models.CharField(max_length = 255)
    teacher_attended = models.BooleanField(default = False)
    student_attended = models.BooleanField(default = False)
    category = models.ForeignKey(SubCategories, related_name = 'appointments')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)


