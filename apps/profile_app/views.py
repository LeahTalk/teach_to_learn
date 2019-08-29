from django.shortcuts import render, HttpResponse, redirect
from .models import *
from apps.login_app.models import *
from django.contrib import messages
import bcrypt
import re
import os
import boto3
import base64
from geopy.geocoders import Nominatim
import random
from random import sample, randrange

def upload_photo(request):
    if 'profile_img' in request.FILES:
        encoded_string = base64.b64encode(request.FILES['profile_img'].read())
        user = Users.objects.get(id = request.session['curUser'])
        user.image_base = encoded_string
        user.save()
    return redirect('/profile/' + str(request.session['curUser']))

def index(request):
    user = Users.objects.get(id = request.session['curUser'])
    created_appointments = user.created_appointments.all().order_by('date')
    reserved_appointments = []
    for appointment in created_appointments:
        if appointment.appointment_student != None:
            reserved_appointments.append(appointment)
    attending_appointments = user.attending_appointments.all().order_by('date')

    geolocator = Nominatim(user_agent="profile_app")
    location = geolocator.geocode(user.location)
    print("lat")
    print(location.latitude)
    print("long")
    print(location.longitude)

    # count = Users.objects.all().count()
    # slice = random.random() * (count - 3)
    # newArr = set()
    # something = Users.objects.exclude(id=request.session['curUser'])  #
    # while len(newArr) < 3:
    #     x = randrange(len(something) - 1)
    #     newArr.add(something[x])
    # print(newArr)
    
    # SubCategories.objects.get(id=).teachers.all()
    # Users.objects.get(id=request.session['curUser']).skills_to_teach.all()

    # Users.objects.exclude(id=request.session['curUser']).all(), 
    # Users.objects.exclude(id=request.session['curUser']).order_by('?')[3:]

    context = {
        'user' : Users.objects.get(id = request.session['curUser']),
        'all_teaching_appointments' : created_appointments,
        'reserved_teaching_appointments' : reserved_appointments,
        'learning_appointments' : attending_appointments,
        'skills_to_learn' : user.skills_to_learn.all(),
        'all_users': Users.objects.exclude(id=request.session['curUser']).order_by('?')[:8],                      # only show all other users that teach the subject, do not include logged user
        'latitude': location.latitude,
        'longitude': location.longitude,

    }
    return render(request, 'profile_app/index.html', context)

def edit_profile(request):
    if 'curUser' not in request.session:
        return redirect('/') 
    context = {
        'user' : Users.objects.get(id = request.session['curUser'])
    }
    return render(request, "profile_app/user_settings.html", context)

def process_profile_edits(request):
    if 'curUser' not in request.session:
        return redirect('/') 
    errors = Users.objects.user_validator(request.POST)
    #Make sure we don't compare against the user's original email if they keep it the same
    user = Users.objects.get(id = request.session['curUser'])
    
    users = Users.objects.filter(email = request.POST['email'])
    if len(users) > 0 and users[0].id != request.session['curUser']:
        errors['exists'] = "A user with this email already exists!"

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/edit_profile')

    user.email = request.POST['email']
    user.first_name = request.POST['first_name']
    user.last_name = request.POST['last_name']
    user.save()
    return redirect('/profile/' + str(user.id))

def process_password_edits(request):
    print("I am here")
    if 'curUser' not in request.session:
        return redirect('/') 
    errors = Users.objects.user_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/edit_profile')
    password = request.POST['regPassword']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()) 
    user = Users.objects.get(id = request.session['curUser'])
    user.pw_hash = pw_hash
    user.save()
    return redirect('/profile/' + str(user.id))

def process_description_edits(request):
    if 'curUser' not in request.session:
        return redirect('/') 
    user = Users.objects.get(id = request.session['curUser'])
    user.desc = request.POST['desc']
    user.save()
    return redirect('/profile/' + str(user.id))

def view_profile(request, user_id):
    print(request.session['curUser'])
    view_user = Users.objects.get(id = user_id)
    created_appointments = view_user.created_appointments.all().order_by('date')
    open_appointments = []
    for appointment in created_appointments:
        if appointment.appointment_student == None:
            open_appointments.append(appointment)

    context = {
        'user' : Users.objects.get(id = request.session['curUser']),
        'viewing_user' : view_user,
        'open_appointments' : open_appointments,
        'skills': view_user.skills_to_teach.all(),
    }
    return render(request, 'profile_app/profile.html', context)

def view_history(request):
    context = {
        "classes_taken" : Users.objects.get(id=request.session['curUser']).attending_appointments.all(),
        "classes_taught" : Users.objects.get(id=request.session['curUser']).created_appointments.all(),
    }
    return render(request, 'profile_app/history.html', context)

def categories(request):
    current_user = Users.objects.get(id=request.session['curUser'])
    context = {
        'user': current_user,
        "all_categories" : Categories.objects.all(),
    }
    return render(request, 'profile_app/categories.html', context)

def populate_subcategories_display(request):
    print("I'm over here!")
    if request.method == "POST":
        print("I'm in the Post!")
        selected_category = Categories.objects.get(name=request.POST['select_category'])

        selected_categories_subs = SubCategories.objects.filter(mainCategory = selected_category)

        context = {
            'selected_categories_subs' : selected_categories_subs,
        }

        return render(request, 'profile_app/selected_categories.html', context)


# jonathan@test.com testpassword chair@wheels.com  testpassword