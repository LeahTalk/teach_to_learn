from __future__ import unicode_literals
from django.db import models
from apps.login_app.models import *
import datetime

class AppointmentManager(models.Manager):
    def appointment_validator(self, postData):
        errors = {}
        if len(postData['date']) < 1:
            errors['date'] = "You must choose a date!"
        if postData['date'] < str(datetime.datetime.today()):
            errors['starttime'] = "You cannot make an appointment in the past!"
        if len(postData['location']) < 1:
            errors['location'] = "You must choose a location!"
        return errors

class Appointments(models.Model):
    appointment_creator = models.ForeignKey(Users, related_name = 'created_appointments')
    appointment_student = models.ForeignKey(Users, related_name = 'attending_appointments', null = True, blank=True)
    date = models.DateTimeField(default = datetime.datetime.now())
    location = models.CharField(max_length = 255)
    pending_credit = models.BooleanField(default = False)
    category = models.ForeignKey(SubCategories, related_name = 'appointments', null = True, blank=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = AppointmentManager()

class Reviews(models.Model):
    review_creator = models.ForeignKey(Users, related_name = 'created_reviews')
    review_receiver = models.ForeignKey(Users, related_name = 'received_reviews')
    rating = models.IntegerField()
    content = models.TextField()
    category = models.ForeignKey(SubCategories, related_name = 'related_reviews')
    role = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
