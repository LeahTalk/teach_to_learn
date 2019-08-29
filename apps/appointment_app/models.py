from __future__ import unicode_literals
from django.db import models
from apps.login_app.models import *
import datetime
from geopy.geocoders import Nominatim

class AppointmentManager(models.Manager):
    def appointment_validator(self, postData):
        errors = {}
        if len(postData['date']) < 1:
            errors['date'] = "You must choose a date!"
        if postData['date'] < str(datetime.datetime.today()):
            errors['starttime'] = "You cannot make an appointment in the past!"
        if len(postData['location']) < 2:
            errors['location'] = "Location must be at least two characters"
        geolocator = Nominatim(user_agent="login_app")
        location = geolocator.geocode(postData['location'])
        if location == None:
            errors['location'] = "The city or location you have inputted does not exist, please try again"
        return errors

    def location_validator(self, postData):
        errors = {}

        if 'location' in postData:
            if len(postData['location']) < 2:
                errors['location'] = "Location must be at least two characters"

            geolocator = Nominatim(user_agent="login_app")
            location = geolocator.geocode(postData['location'])
            if location == None:
                errors['location'] = "The city or location you have inputted does not exist, please try again"
        return errors

class reviewManager(models.Manager):
    def rewiew_validator(self, postData):
        errors = {}
        if len(postData['review_post']) < 1:
            errors['review_post'] = "You must enter a review!"
        if postData['rating'] == "":
            errors['rating'] = "Please select a rating !"
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
    appointment = models.ForeignKey(Appointments, related_name = 'reviews', null = True, blank = True)
    role = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = reviewManager()     