from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
import bcrypt
import re
from django.http import JsonResponse
from geopy.geocoders import Nominatim

def index(request):
    if 'curUser' not in request.session:
        request.session['curUser'] = "logged out"
    return render(request, 'login_app/index.html')

def logout(request):
    request.session.clear()
    return redirect('/')

def register_login(request):
    return render(request, 'login_app/register_login.html')

def login(request):
    errors = Users.objects.user_validator(request.POST)
    user = Users.objects.filter(email=request.POST['email'])
    if user: 
        logged_user = user[0] 
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.pw_hash.encode()):
            request.session['curUser'] = logged_user.id
            return redirect('/dashboard')
        else:
            errors['badPassword'] = "The password is incorrect."
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
    else:
        errors['noUser'] = "There is no user with this email address!"  
        for key, value in errors.items():
            messages.error(request, value)  
        return redirect("/register_login")

def register(request):

    errors = Users.objects.user_validator(request.POST)

    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    if not EMAIL_REGEX.match(request.POST['email']):        
        errors['email'] = ("Invalid email address!")

    if Users.objects.filter(email=request.POST['email']).exists():
        errors['exists'] = "A user with this email already exists!"
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/register_login')
    password = request.POST['regPassword']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())  # create the hash    
    Users.objects.create(first_name=request.POST['first_name'], last_name = request.POST['last_name'],
            email = request.POST['email'], pw_hash=pw_hash)
    request.session['curUser'] = Users.objects.get(email = request.POST['email']).id
    return redirect('/register')

def continue_registration(request):
    current_user = Users.objects.get(id=request.session['curUser'])
    print(current_user.first_name)

    if 'current_category' not in request.session:
        request.session['current_category'] = ''
        current_category = Categories.objects.filter(name = request.session['current_category'])
        all_subcategories = SubCategories.objects.all()
    else:
        current_category = Categories.objects.filter(name = request.session['current_category'])
        all_subcategories = SubCategories.objects.filter(mainCategory = current_category)

    all_categories = Categories.objects.all()
    current_user = Users.objects.get(id = request.session['curUser'])

    context = {
        'current_user': current_user,
        'all_categories' : all_categories,
        'all_subcategories' : all_subcategories,
    }

    return render(request, "login_app/register.html", context)


def select_category(request):
    if request.method == "POST":
        if len(request.POST['add_category']) > 0:
            errors = Categories.objects.basic_validator(request.POST)
            if len(errors) > 0:

                send_to_ajax = error_message(errors)

                response = JsonResponse({'error': send_to_ajax })
                response.status_code = 403

                return response
            else:
                new_category = Categories.objects.create(name=request.POST['add_category'])
                new_category.save()
                request.session['current_category'] = new_category.name
                request.session.save()
                context = {
                    'current_category': new_category,
                    'all_subcategories': SubCategories.objects.filter(name=new_category.name),
                }
                print("category made")
                print(new_category.name)
                return render(request, 'login_app/subcategories.html', context)
        if request.POST['select_category']:
            request.session['current_category'] = request.POST['select_category']
            request.session.save()
            current_category = Categories.objects.get(id=request.POST['select_category'])
            context = {
                'current_category': current_category,
                'all_subcategories': SubCategories.objects.filter(mainCategory=current_category),
            }
            print("category selected")
            print(current_category.name)
            return render(request, 'login_app/subcategories.html', context)

def select_subcategory(request):
    if request.method == "POST":
        current_category = Categories.objects.get(id=request.POST['current_category'])
        current_user = Users.objects.get(id=request.session['curUser'])
        if len(request.POST['add_subcategory']) > 0:
            errors = SubCategories.objects.basic_validator(request.POST)
            if len(errors) > 0:

                send_to_ajax = error_message(errors)

                response = JsonResponse({'error': send_to_ajax })
                response.status_code = 403

                return response
            else:
                new_subcategory = SubCategories.objects.create(name=request.POST['add_subcategory'], mainCategory = current_category)
                new_subcategory.teachers.add(current_user)
                request.session.save()
                print("new subcategory created")
                all_teachers = new_subcategory.teachers.all()
                this_subs_teacher = all_teachers.filter(id = current_user.id)
                current_teacher = this_subs_teacher[0]
                print(current_teacher.first_name)
                print("is teaching")
                return render(request, 'login_app/location_form.html')

        if request.POST['select_subcategory']:
            current_subcategory = SubCategories.objects.get(id=request.POST['select_subcategory'])
            current_subcategory.teachers.add(current_user)
            print("subcategory selected to teach")
            print(current_subcategory.name)

            print("-----------------------")
            all_teachers = current_subcategory.teachers.all()
            this_subs_teacher = all_teachers.filter(id = current_user.id)
            current_teacher = this_subs_teacher[0]
            print(current_teacher.first_name)
            print("is teaching")
            print(current_subcategory.name)

        return render(request, 'login_app/location_form.html')

def location_form_process(request):
    if request.method == "POST":

        print("I'm before erros")
        errors = Users.objects.location_validator(request.POST)
        if len(errors) > 0:
            print("location has errors")
            send_to_ajax = error_message(errors)

            response = JsonResponse({'error': send_to_ajax })
            response.status_code = 403

            return response

        current_user = Users.objects.get(id=request.session['curUser'])
        user_location = request.POST['location']
        current_user.location = user_location
        current_user.save()

        print("location saved!")
        print(current_user.location)

        context = {
            'all_subcategories' : SubCategories.objects.all()
        }

        return render(request, 'login_app/learn_subcategories.html', context)

def choose_subcategories(request):
    print("I'm at choose_categories")
    print(request.POST)

    current_user = Users.objects.get(id=request.session['curUser'])
    all_subcategories = SubCategories.objects.all() 
    if request.method == "POST":
        for subcategory in all_subcategories:
            if subcategory.name in request.POST:
                # loop_subcategory = SubCategories.objects.get(id = int(request.POST[key]))
                loop_subcategory = SubCategories.objects.get(name__iexact=request.POST[subcategory.name])
                current_user.skills_to_learn.add(loop_subcategory)
                print(current_user.first_name)
                print("has added")
                print(loop_subcategory.name)
                print("to the skills they want to learn!")

    return redirect("/dashboard")


def error_message(errors):
    was_empty_string = ""

    for error in errors:
        was_empty_string += errors[error]
    
    return was_empty_string