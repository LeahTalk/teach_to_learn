from django.shortcuts import render, HttpResponse, redirect
from .models import *
from apps.login_app.models import *

def index(request):
    current_user = Users.objects.get(id=request.session['curUser'])
    first_name = current_user.first_name
    currency = current_user.credits
    context = {
        "first_name" : first_name,
        "currency" : currency,
    }
    return render(request, 'profile_app/index.html', context)

def view_profile(request, user_id):
    context = {
        "first_name" : Users.objects.get(id=user_id).first_name,
        "user_bio" : Users.objects.get(id=user_id).desc,
        "all_received_reviews" : Users.objects.get(id=user_id).received_reviews.all(),
        "course_taught" : Users.objects.get(id=user_id).skills_to_teach.all(),
        "availability" : Users.objects.get(id=user_id).created_appointments.all(),
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