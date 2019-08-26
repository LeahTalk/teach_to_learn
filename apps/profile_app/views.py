from django.shortcuts import render, HttpResponse, redirect
from .models import *

def index(request):
    return HttpResponse("placeholder")

