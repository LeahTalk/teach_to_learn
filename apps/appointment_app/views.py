from django.shortcuts import render, HttpResponse, redirect
from .models import *

def index(request):
    return render(request, 'appointment_app/index.html')
