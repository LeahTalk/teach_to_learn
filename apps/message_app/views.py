from django.shortcuts import render, HttpResponse, redirect
from .models import *
from apps.login_app.models import *
from apps.appointment_app.models import *
from django.contrib import messages
from geopy.geocoders import Nominatim
from datetime import datetime


def index(request, appointment_id):
    if 'curUser' not in request.session or request.session['curUser'] == 'logged out':
        return redirect('/')
    if len(Appointments.objects.filter(id = appointment_id)) == 0:
        return redirect('/dashboard')
    user = Users.objects.get(id=request.session['curUser'])
    appointment = Appointments.objects.get(id = appointment_id)
    if (user != appointment.appointment_student) and (user != appointment.appointment_creator):
        return redirect('/dashboard')
    showReview = False
    showDelete = True
    if (str(appointment.date) < str(datetime.today())):
        showDelete = False
        if appointment.reviews == None:
            showReview = True
        elif (user == appointment.appointment_creator) and len(appointment.reviews.filter(role = 'Instructor')) == 0:
            showReview = True
        elif (user == appointment.appointment_student) and len(appointment.reviews.filter(role = 'Student')) == 0:
            showReview = True
    if user == appointment.appointment_creator:
        appointment.date = appointment.date.strftime("%Y-%m-%d"+ 'T' +"%H:%M")
    request.session['appointment_id'] = appointment_id
    appointment_object = Appointments.objects.get(id = appointment_id)
    geolocator = Nominatim(user_agent="message_app")
    location = geolocator.geocode(appointment.location)
    if location == None:
        location = "Seattle"
    context = {
        'user' : user,
        'all_messages' : Messages.objects.filter(appointment = appointment_object),
        'appointment_Object': appointment,
        'latitude': location.latitude,
        'longitude': location.longitude,
        'showReview' : showReview,
        'showDelete' : showDelete
    }
    return render(request, 'message_app/index.html' , context)


def send_message(request , appointment_id ):
    if 'curUser' not in request.session or request.session['curUser'] == 'logged out':
        return redirect('/')
    # pass the post data to the method we wrote and save the response in a variable called errors
    errors = Messages.objects.message_validator(request.POST)
    # check if the errors dictionary has anything in it
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        # redirect the user back to the form to fix the errors
        return redirect(f'/messages/{appointment_id}')
    else:
        appointment = Appointments.objects.get(id = appointment_id)
        User = Users.objects.get(id = request.session['curUser'])
        if (User != appointment.appointment_student) and (User != appointment.appointment_creator):
            return redirect('/dashboard')
        content_Message = request.POST["post"] 
        Messages.objects.create(content = content_Message , message_owner = User , appointment = appointment )
        return redirect(f'/messages/{appointment_id}')


def send_review(request , appointment_id ):
    if 'curUser' not in request.session or request.session['curUser'] == 'logged out':
        return redirect('/')
    # pass the post data to the method we wrote and save the response in a variable called errors
    errors = Reviews.objects.rewiew_validator(request.POST)
    # check if the errors dictionary has anything in it
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        # redirect the user back to the form to fix the errors
        return redirect(f'/messages/{appointment_id}')

    else:
        Appointments_object = Appointments.objects.get(id = appointment_id)  
        User = Users.objects.get(id = request.session['curUser'])
        if (User != Appointments_object.appointment_student) and (User != Appointments_object.appointment_creator):
            return redirect('/dashboard') 
        rating = request.POST["rating"]
        review_content = request.POST["review_post"]
        # subCategory = Appointments_object.category
        reviewCreator = Users.objects.get(id = request.session['curUser'])
        if request.session['curUser'] == Appointments_object.appointment_creator.id:
            Reviews.objects.create(review_creator = reviewCreator ,review_receiver = Appointments_object.appointment_student, rating = rating , content = review_content , role = "Instructor", appointment = Appointments_object)
            return redirect(f"/profile/{Appointments_object.appointment_student.id}")

        elif request.session['curUser'] == Appointments_object.appointment_student.id:
            Reviews.objects.create(review_creator = reviewCreator ,review_receiver = Appointments_object.appointment_creator, rating = rating , content = review_content , role = "Student", appointment = Appointments_object)
            return redirect(f"/profile/{Appointments_object.appointment_creator.id}")

