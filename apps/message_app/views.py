from django.shortcuts import render, HttpResponse, redirect
from .models import *

def index(request, appointment_id):
    return render(request, 'message_app/messages.html')

