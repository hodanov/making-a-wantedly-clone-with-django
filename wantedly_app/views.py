from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login, get_user_model
User = get_user_model()
from django.contrib import messages
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ObjectDoesNotExist
from .forms import SignUpForm, ProfileForm, LoginForm
from .models import *
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

def profile(request, id):
    u = get_object_or_404(User, pk=id)

    try:
        organizations = u.organization_set.all()
    except Organization.DoesNotExist:
        organizations = False

    try:
        work_history = u.profile.workhistory
        try:
            experiences = work_history.experience_set.all().order_by('-from_date')
        except Experience.DoesNotExist:
            experiences = False
    except WorkHistory.DoesNotExist:
        work_history = False
        experiences = False

    try:
        portfolio = u.profile.portfolio
        try:
            works = portfolio.work_set.all().order_by('-made_at')
        except Work.DoesNotExist:
            works = False
    except Portfolio.DoesNotExist:
        portfolio = False
        works = False

    try:
        related_link = u.profile.relatedlink
        try:
            urls = related_link.url_set.all()
        except Url.DoesNotExist:
            urls = False
    except RelatedLink.DoesNotExist:
        related_link = False
        urls = False

    try:
        educational_bg = u.profile.educationalbackground
        try:
            educations = educational_bg.education_set.all().order_by('-graduated_at')
        except Education.DoesNotExist:
            educations = False
    except EducationalBackground.DoesNotExist:
        educational_bg = False
        educations = False

    try:
        friend_relationships = u.friendrelationship_follower.all()
        friends = []
        for fr in friend_relationships:
            f = User.objects.get(pk=fr.followed_user_id)
            friends.append(f)
            try:
                f_organizations = f.organization_set.all()
            except Organization.DoesNotExist:
                f_organizations = False
    except FriendRelationship.DoesNotExist:
        friends = False

    context = {
        'u': u,
        'experiences': experiences,
        'urls': urls,
        'educations': educations,
        'works': works,
        'organizations': organizations,
        'friends': friends,
        'f_organizations': f_organizations,
    }
    return render(request, 'wantedly_app/profile.html', context)

def profile_edit(request):
    if request.user.is_authenticated:
        return render(request, 'wantedly_app/profile_edit.html')
    else:
        return render(request, 'regeistration/request_login.html')
