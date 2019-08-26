from django.shortcuts import render, HttpResponse, redirect
from .models import *

def index(request):
    return render(request, 'profile_app/index.html')

def view_profile(request, user_id):
    return render(request, 'profile_app/profile.html')

def view_history(request):
    return render(request, 'profile_app/history.html')

def categories(request):
    return render(request, 'profile_app/categories.html')
