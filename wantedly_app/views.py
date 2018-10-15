from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

def home(request):
    return render(request, 'wantedly_app/home.html')

def about(request):
    return render(request, 'wantedly_app/about.html')

def sign_up(request):
    if request.method == 'POST':
        username = request.POST['username']
        gender = request.POST['gender']
        email = request.POST['email']
        password = request.POST['password']
        year = request.POST['year']
        month = request.POST['month']
        date = request.POST['date']
        birth_date = year + "-" + month + "-" + date

        user = User.objects.create_user(username, email, password)
        user.profile.gender = gender
        user.profile.birth_date = birth_date
        user.save()

        user = authenticate(username=username, password=password)
        auth_login(request, user)
        return redirect('home')
    return render(request, 'registration/sign_up.html')

def login(request):
    return render(request, 'registration/login.html')
