from django.shortcuts import render, redirect
import random, re
from . import models as m
import bcrypt

EMAIL_REGEX = re.compile(r'^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$')


def index(request):
    imagenr = random.randint(1,8)
    image = '/static/base_spotlite/img/bg{}.jpg'.format(imagenr)
    context = {
        'img_url' : image
    }
    return render(request, 'auth_spotlite/index.html', context)

def register(request):
    imagenr = random.randint(1,8)
    image = '/static/base_spotlite/img/bg{}.jpg'.format(imagenr)
    context = {
        'img_url' : image
    }
    return render(request, 'auth_spotlite/register.html', context)

def login(request):
    return render(request, 'auth_spotlite/login.html')

def authenticate(request, action):
    errors = []
    if action == 'register':
        if request.method == 'POST':
            try: 
                user = m.User.objects.get(email=request.session['html_email'])
                errors.append("There is already an account with the e-mail address.")
                print(errors)
                return redirect('auth_spotlite:register')

            except:
                try:
                    email = request.POST['html_email']
                    firstname = request.POST['html_firstname']
                    surname = request.POST['html_surname']
                    password = request.POST['html_password']
                    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
                    
                    if len(email) == 0 or len(firstname) == 0 or len(surname) == 0 or len(password) == 0:
                        errors.append("Fields cannot be blank.")
                    if password != request.POST['html_confirm']:
                        errors.append("Passwords do not match.")
                    if len(password) < 6:
                        errors.append("Password must be longer than 6 characters.")
                    if not EMAIL_REGEX.match(email):
                        errors.append("Invalid e-mail.")
                    
                    if len(errors) == 0:
                        user = m.User() 
                        user.email = email
                        user.firstname = firstname
                        user.surname = surname
                        user.password = hashed_password
                        user.premium = 0
                        user.profilepic = "/media/profile_blank.jpg"
                        user.save()
                        start_session(request, user)
                        return redirect('app_spotlite:index')
                except:
                    raise
                    return redirect('auth_spotlite:register')
        return redirect('auth_spotlite:register')

    elif action == 'login':
        if request.method == 'POST':
            try:
                user = m.User.objects.get(email=request.POST['html_email'])
                password = request.POST['html_password'] 
                if bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
                    start_session(request, user)
                else:
                    errors.append("Passwords do not match.")
                    return redirect('app_spotlite:index')
            except:
                errors.append("User does not exist.")
        return redirect('app_spotlite:index')

def logout(request):
    request.session.clear()
    return redirect('auth_spotlite:index')

def start_session(request, user):
    request.session['user_id'] = user.id
    request.session['email'] = user.email
    request.session['firstname'] = user.firstname
    request.session['surname'] = user.surname
    request.session['profilepic'] = user.profilepic
    request.session['premium'] = user.premium

