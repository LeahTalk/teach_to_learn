from django.shortcuts import render, HttpResponse, redirect
from .models import *
from apps.login_app.models import *
from django.contrib import messages
from datetime import datetime
import bcrypt
import re
import os
import boto3
import base64
from geopy.geocoders import Nominatim
import random
import statistics

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
    open_appointments = []
    attending_appointments = []
    old_appointments = []
    for appointment in created_appointments:
        if (str(appointment.date) < str(datetime.today())):
            #If the teacher is owed credit, and the appointment has occurred then give credit
            if appointment.pending_credit == True:
                appointment.pending_credit = False
                appointment.save()
                user.credits += 1
                user.save()
                old_appointments.append(appointment)
            elif appointment.appointment_student == None:
                appointment.delete()
            else:
                old_appointments.append(appointment)
        if (str(appointment.date) > str(datetime.now())):
            if appointment.appointment_student != None:
                reserved_appointments.append(appointment)
            else:
                open_appointments.append(appointment)
    all_attended = user.attending_appointments.all().order_by('date')
    for appointment in all_attended:
        if (str(appointment.date) > str(datetime.now())):
            attending_appointments.append(appointment)
        else:
            old_appointments.append(appointment)
    geolocator = Nominatim(user_agent="profile_app")
    location = geolocator.geocode(user.location)
    #Sort past appointments taught and learned by date and take the most recent 3
    old_appointments.sort(key=lambda x: str(x.date), reverse=True)
    old_appointments = old_appointments[:3]


    user = Users.objects.get(id = request.session['curUser'])
    skills_to_learn = user.skills_to_learn.all()
    instructors = {}
    for skill in skills_to_learn:
        instructors[skill.name] = Users.objects.exclude(id=request.session['curUser']).filter(skills_to_teach=skill).order_by('?')[:3]
      
    context = {
        'user' :user,
        'open_appointments' : open_appointments,
        'reserved_teaching_appointments' : reserved_appointments,
        'learning_appointments' : attending_appointments,
        'skills_to_learn' : skills_to_learn,
        'all_users': instructors,
        'latitude': location.latitude,
        'longitude': location.longitude,
    }
    return render(request, 'profile_app/index.html', context)

def add_skill(request):
    if 'category' not in request.POST:
        return redirect('/profile/' + str(request.session['curUser']))
    category = SubCategories.objects.get(name = request.POST['category'])
    user = request.session['curUser']
    category.teachers.add(user)
    return redirect('/profile/' + str(request.session['curUser']))

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
        if (appointment.appointment_student == None) and (str(appointment.date) > str(datetime.now())):
            open_appointments.append(appointment)
    all_skills = SubCategories.objects.all()

    #  
    getUser = Users.objects.get(id = user_id )
    user_reviews = Reviews.objects.filter(review_receiver = getUser)

    arr_rating =[]
    
    for x in user_reviews:
        print(x.rating)
        arr_rating.append(x.rating)
        
    average_reviews = ""
    if len(arr_rating)>0 :
        x = statistics.mean(arr_rating)
        average_reviews = (int(round(x)))
    geolocator = Nominatim(user_agent="profile_app")
    location = geolocator.geocode(view_user.location)

    context = {
        'user' : Users.objects.get(id = request.session['curUser']),
        'viewing_user' : view_user,
        'open_appointments' : open_appointments,
        'skills': view_user.skills_to_teach.all(),
        'all_skills' : SubCategories.objects.exclude(teachers = Users.objects.filter(id = request.session['curUser'])).order_by('name'),
        'user_reviews' : user_reviews,
        'average_reviews' : average_reviews,
        'latitude': location.latitude,
        'longitude': location.longitude,
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