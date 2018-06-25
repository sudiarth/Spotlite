from django.shortcuts import render, redirect
import random

def index(request):
    return render(request, 'auth_spotlite/index.html')

def register(request):
    return render(request, 'auth_spotlite/register.html')

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
                
                if len(email) == 0 or len(fullname) == 0 or len(password) == 0:
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
                return redirect('auth_spotlite:register')
            return redirect('auth_spotlite:index')
        return redirect('auth_spotlite:register')
    elif action == 'login':
        if request.method == 'POST':
            try:
                user = m.User.objects.get(email=request.POST['html_email'])
                start_session(request, user)
            except:
                raise
                errors.append("User does not exist.")
                return redirect('auth_spotlite:login')
            return redirect('auth_spotlite:index')
        return redirect('auth_spotlite:login')

def logout(request):
    request.session.clear()
    return redirect('auth_spotlite:index')

def start_session(request, user):
    request.session['user_id'] = user.index
    request.session['email'] = user.email
    request.session['firstname'] = user.firstname
    request.session['surname'] = user.surname

