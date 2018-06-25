from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from apps.auth_spotlite import models as m

def index(request):
    return render(request, 'app_spotlite/index.html')

def dashboard(request):
    return render(request, 'app_spotlite/dashboard.html')

def profile(request):
    return render(request, 'app_spotlite/profile.html')

def settings(request):
    return render(request, 'app_spotlite/settings.html')

def picture_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)

        user = m.User.objects.get(id=request.session['user_id'])
        user.profilepic = uploaded_file_url
        user.save()

        request.session['profilepic'] = user.profilepic
        return render(request, 'app_spotlite/profile.html')

    return render(request, 'app_spotlite/profile.html')

def update_settings(request):
    user = m.User.objects.get(id=request.session['user_id'])
    user.email = request.POST['html_email']
    user.firstname = request.POST['html_firstname']
    user.surname = request.POST['html_surname']
    user.save()
    request.session['user_id'] = user.id
    request.session['email'] = user.email
    request.session['firstname'] = user.firstname
    request.session['surname'] = user.surname
    return redirect('app_spotlite:settings')
    
def update_password(request):
    user = m.User.objects.get(id=request.session['user_id'])
    if request.POST['html_password'] == request.POST['html_confirm'] and len(request.POST['html_password']) > 0:
        user.password = request.POST['html_password']
        user.save()
    return redirect('app_spotlite:settings')
    