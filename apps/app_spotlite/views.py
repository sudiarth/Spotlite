from django.shortcuts import render

def index(request):
    return render(request, 'app_spotlite/index.html')

def dashboard(request):
    return render(request, 'app_spotlite/dashboard.html')

def profile(request):
    pass

def settings(request):
    pass