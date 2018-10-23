from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login, get_user_model
User = get_user_model()
from django.contrib import messages
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ObjectDoesNotExist
from .forms import SignUpForm, ProfileForm, LoginForm
from .models import Profile
from datetime import date

def home(request):
    if request.user.is_authenticated:
        return render(request, 'wantedly_app/home.html')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    messages.add_message(request, messages.SUCCESS, 'ログインしました！')
                    return redirect('home')
                else:
                    messages.add_message(request, messages.ERROR, 'ユーザーのアクティベーションがまだ完了していません。')
            else:
                messages.add_message(request, messages.ERROR, 'ログインに失敗しました。ユーザーが存在しないかパスワードが間違っています。')

        login_form = LoginForm()
        context = {'login_form': login_form}
        return render(request, 'wantedly_app/top.html', context)

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

    login_form = LoginForm()
    context = {
        'signup_form': signup_form,
        'profile_form': profile_form,
        'login_form': login_form
    }
    return render(request, 'registration/sign_up.html', context)
