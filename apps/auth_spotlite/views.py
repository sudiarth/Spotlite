from django.shortcuts import render, redirect
import random, re
from . import models as m

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
                email = request.POST['html_email']
                firstname = request.POST['html_firstname']
                surname = request.POST['html_surname']
                password = request.POST['html_password']
                
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
                    user.password = password
                    user.profilepic = ""
                    user.save()
                    start_session(request, user)
            except:
                raise
                return redirect('auth_spotlite:register')
            return redirect('app_spotlite:index')
        return redirect('auth_spotlite:register')
    elif action == 'login':
        if request.method == 'POST':
            try:
                user = m.User.objects.get(email=request.POST['html_email'])
                start_session(request, user)
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

