from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login, get_user_model
User = get_user_model()
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ObjectDoesNotExist
from .forms import SignUpForm, ProfileForm
from .models import Profile
from datetime import date

def home(request):
    return render(request, 'wantedly_app/home.html')

def about(request):
    return render(request, 'wantedly_app/about.html')

def sign_up(request):
    if request.method == 'POST':
        signup_form = SignUpForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if signup_form.is_valid() and profile_form.is_valid():
            username = signup_form.cleaned_data.get('username')
            email = signup_form.cleaned_data.get('email')
            password = signup_form.cleaned_data.get('password')
            gender = profile_form.cleaned_data.get('gender')
            birth_year = profile_form.cleaned_data.get('birth_year')
            birth_month = profile_form.cleaned_data.get('birth_month')
            birth_day = profile_form.cleaned_data.get('birth_day')

            user = User.objects.create_user(username, email, password)
            user.profile.gender = gender
            if birth_day and birth_month and birth_year:
                birth_date = date(int(birth_year), int(birth_month), int(birth_day)).isoformat()
                user.profile.birth_date = birth_date
            user.save()

            user = authenticate(request, username=username, password=password)
            auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.add_message(request, messages.SUCCESS, 'ユーザー登録が完了しました！')
            return redirect('home')
    else:
        signup_form = SignUpForm()
        profile_form = ProfileForm()

    return render(request, 'registration/sign_up.html', {
        'signup_form': signup_form,
        'profile_form': profile_form
    })

def login(request):
    return render(request, 'registration/login.html')
