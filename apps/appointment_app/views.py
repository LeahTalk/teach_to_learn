from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
from datetime import timedelta
import datetime
import time
import pytz
from pytz import timezone


def index(request):
    user = Users.objects.get(id = request.session['curUser'])
    created_appointments = user.created_appointments.all().order_by('date')
    reserved_appointments = []
    open_appointments = []
    for appointment in created_appointments:
        if appointment.appointment_student != None:
            reserved_appointments.append(appointment)
        else:
            open_appointments.append(appointment)
    attending_appointments = user.attending_appointments.all().order_by('date')
    context = {
        'user' : Users.objects.get(id = request.session['curUser']),
        #In this case the id would be the user_id from the URL
        'viewing_user' : Users.objects.get(id = request.session['curUser']),
        'all_teaching_appointments' : created_appointments,
        'reserved_teaching_appointments' : reserved_appointments,
        'learning_appointments' : attending_appointments,
        'open_appointments' : open_appointments
    }
    return render(request, 'appointment_app/index.html', context)

def process_new_appointment(request):
    errors = Appointments.objects.appointment_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/dashboard')
    user = Users.objects.get(id = request.session['curUser'])
    Appointments.objects.create(appointment_creator = user, date = request.POST['date'],
        location = request.POST['location'])    
    return redirect('/dashboard')

def cancel_appointment(request, appointment_id):
    #Add a check here to make sure the person cancelling is either the teacher or student - otherwise return redirect to dashboard
    appointment = Appointments.objects.get(id = appointment_id)
    user = Users.objects.get(id = request.session['curUser'])
    student = appointment.appointment_student
    #If the student cancelled
    if user == appointment.appointment_student:
        local = pytz.timezone ("America/Los_Angeles")
        naive = datetime.datetime.now()
        local_dt = local.localize(naive, is_dst=None)
        utc_dt = local_dt.astimezone(pytz.utc)
        d1 = appointment.date
        d2 = datetime.datetime.now()
        d1_ts = time.mktime(d1.timetuple())
        d2_ts = time.mktime(d2.timetuple())
        #Student cancelled with more than a day in advance, refund credit
        if (int(d2_ts-d1_ts) / 60) < -1440:
            student.credits += 1
            student.save()
        student.attending_appointments.remove(appointment)
        student.save()
        appointment.messages.all().delete()
    #If the teacher cancelled
    else:
        if student != None:
            student.credits += 1 
            student.save()
        appointment.delete()
    return redirect('/dashboard')

def reserve_appointment(request, appointment_id):
    context = {
        'appointment' : Appointments.objects.get(id = appointment_id)
    }
    return render(request, 'appointment_app/reserve_appointment.html', context)

def process_reservation(request):
    appointment = Appointments.objects.get(id = request.POST['id'])
    user = Users.objects.get(id = request.session['curUser'])
    appointment.appointment_student = user
    #category = SubCategories.objects.get(name = request.POST['category'])
    #appointment.category = category
    appointment.pending_credit = True
    user.credits -= 1
    user.save()
    appointment.save()
    return redirect('/dashboard')

def edit_appointment(request, appointment_id):
    appointment = Appointments.objects.get(id = appointment_id)
    #"2018-06-12T19:30"
    
    appointment.date = appointment.date.strftime("%Y-%m-%d"+ 'T' +"%H:%M")
    context = {
        'appointment' : appointment
    }
    return render(request, 'appointment_app/edit.html', context)

def process_edits(request, appointment_id):
    errors = Appointments.objects.appointment_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/messages/' + str(appointment_id))
    appointment = Appointments.objects.get(id = appointment_id)
    appointment.date = request.POST['date']
    appointment.location = request.POST['location']
    appointment.save()  
    return redirect('/dashboard')