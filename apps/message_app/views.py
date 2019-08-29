from django.shortcuts import render, HttpResponse, redirect
from .models import *
from apps.login_app.models import *
from apps.appointment_app.models import *
from django.contrib import messages
from geopy.geocoders import Nominatim


def index(request, appointment_id):
    # if user is not in seesion redicted to the login page , esle 
    # create your context and put and find the person you sent the message !
    # if not 'id' in request.session:
    #     return redirect("/")
    
    # else:

        appointment = Appointments.objects.get(id = appointment_id)
    #"2018-06-12T19:30"
        appointment.date = appointment.date.strftime("%Y-%m-%d"+ 'T' +"%H:%M")
        print(appointment.date)
        print("lllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll")

        request.session['appointment_id'] = appointment_id
        appointment_object = Appointments.objects.get(id = appointment_id)

        geolocator = Nominatim(user_agent="message_app")
        location = geolocator.geocode(appointment.location)
        if location == None:
            location = "Seattle"
        
        print("lat")
        print(location.latitude)
        print("long")
        print(location.longitude)

        context = {
            'user' : Users.objects.get(id=request.session['curUser']),
            'all_messages' : Messages.objects.filter(appointment = appointment_object),
            'appointment_Object': appointment,
            'latitude': location.latitude,
            'longitude': location.longitude,
        }
        
        return render(request, 'message_app/index.html' , context)


def send_message(request , appointment_id ):

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
        content_Message = request.POST["post"] 
        Messages.objects.create(content = content_Message , message_owner = User , appointment = appointment )
        return redirect(f'/messages/{appointment_id}')


def send_review(request , appointment_id ):

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
        rating = request.POST["rating"]
        review_content = request.POST["review_post"]
        # subCategory = Appointments_object.category
        reviewCreator = Users.objects.get(id = request.session['curUser'])

        if request.session['curUser'] == Appointments_object.appointment_creator.id:
            Reviews.objects.create(review_creator = reviewCreator ,review_receiver = Appointments_object.appointment_student, rating = rating , content = review_content , role = "Instructor")
            return redirect(f"/profile/{Appointments_object.appointment_student.id}")

        elif request.session['curUser'] == Appointments_object.appointment_student.id:
            Reviews.objects.create(review_creator = reviewCreator ,review_receiver = Appointments_object.appointment_creator, rating = rating , content = review_content , role = "Student")
            return redirect(f"/profile/{Appointments_object.appointment_creator.id}")

