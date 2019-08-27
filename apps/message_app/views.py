from django.shortcuts import render, HttpResponse, redirect
from .models import *
from apps.login_app.models import *
from apps.appointment_app.models import *
from django.contrib import messages


def index(request, appointment_id):
    # if user is not in seesion redicted to the login page , esle 
    # create your context and put and find the person you sent the message !
    # if not 'id' in request.session:
    #     return redirect("/")
    
    # else:
        request.session['appointment_id'] = appointment_id
        appointment_object = Appointments.objects.get(id = appointment_id)
        context = {
            'all_messages' : Messages.objects.filter(appointment = appointment_object)
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




