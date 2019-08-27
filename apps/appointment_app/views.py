from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages

def index(request):
    user = Users.objects.get(id = request.session['curUser'])
    created_appointments = user.created_appointments.all().order_by('date', 'time')
    reserved_appointments = []
    open_appointments = []
    for appointment in created_appointments:
        if appointment.appointment_student != None:
            reserved_appointments.append(appointment)
        else:
            open_appointments.append(appointment)
    attending_appointments = user.attending_appointments.all().order_by('date', 'time')
    print(created_appointments)
    print(reserved_appointments)
    print(attending_appointments)
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
        return redirect('/appointment')
    user = Users.objects.get(id = request.session['curUser'])
    Appointments.objects.create(appointment_creator = user, date = request.POST['date'],
        time = request.POST['time'], location = request.POST['location'])    
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
    user.credits = user.credits - 1
    user.save()
    appointment.save()
    return redirect('/dashboard')

def edit_appointment(request):
    context = {
        'appointment' : Appointments.objects.get(id = appointment_id)
    }
    return render(request, 'appointment_app/edit.html', context)