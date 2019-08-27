from django.shortcuts import render, HttpResponse, redirect
from .models import *
from apps.login_app.models import *

def index(request):
    user = Users.objects.get(id = request.session['curUser'])
    created_appointments = user.created_appointments.all().order_by('date')
    reserved_appointments = []
    for appointment in created_appointments:
        if appointment.appointment_student != None:
            reserved_appointments.append(appointment)
    attending_appointments = user.attending_appointments.all().order_by('date')
    context = {
        'user' : Users.objects.get(id = request.session['curUser']),
        'all_teaching_appointments' : created_appointments,
        'reserved_teaching_appointments' : reserved_appointments,
        'learning_appointments' : attending_appointments,
    }
    return render(request, 'profile_app/index.html', context)

def view_profile(request, user_id):
    view_user = Users.objects.get(id = user_id)
    created_appointments = view_user.created_appointments.all().order_by('date')
    open_appointments = []
    for appointment in created_appointments:
        if appointment.appointment_student == None:
            open_appointments.append(appointment)
    context = {
        'user' : Users.objects.get(id = request.session['curUser']),
        'viewing_user' : view_user,
        'open_appointments' : open_appointments
    }
    return render(request, 'profile_app/profile.html', context)

def view_history(request):
    context = {
        "classes_taken" : Users.objects.get(id=request.session['curUser']).attending_appointments.all(),
        "classes_taught" : Users.objects.get(id=request.session['curUser']).created_appointments.all(),
    }
    return render(request, 'profile_app/history.html', context)

def categories(request):
    context = {
        "all_categories" : Categories.objects.all(),
    }
    return render(request, 'profile_app/categories.html', context)


# jonathan@test.com testpassword chair@wheels.com  testpassword