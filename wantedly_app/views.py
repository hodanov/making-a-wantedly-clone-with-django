from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login

def home(request):
    return render(request, 'wantedly_app/home.html')

def about(request):
    return render(request, 'wantedly_app/about.html')

def sign_up(request):
    return render(request, 'registration/sign_up.html')

def create_user(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        ...
    else:
        # Return an 'invalid login' error message.
        ...

def login(request):
    return render(request, 'registration/login.html')
