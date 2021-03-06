from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import *
from datetime import datetime

class SignUpForm(UserCreationForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password1 = forms.CharField(required=False)
    password2 = password1

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class ProfileForm(forms.ModelForm):
    CHOICES = (
        ('female', '女性',),
        ('male', '男性',),
        ('not_applicable', '秘密',)
    )
    gender = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES, required=False)

    def make_select_object(from_x, to_y, dates, increment=True):
        if increment:
            for i in range(from_x, to_y):
                dates.append([i, i])
        else:
            for i in range(from_x, to_y, -1):
                dates.append([i, i])
        return dates

    def make_select_field(select_object):
        dates_field = forms.ChoiceField(
            widget=forms.Select,
            choices=select_object,
            required=False
        )
        return dates_field

    years = [["",""]]
    current_year = datetime.now().year
    years = make_select_object(current_year, current_year-80, years, increment=False)
    birth_year = make_select_field(years)

    months = [["",""]]
    months = make_select_object(1, 13, months)
    birth_month = make_select_field(months)

    days = [["",""]]
    days = make_select_object(1, 32, days)
    birth_day = make_select_field(days)

    class Meta:
        model = Profile
        fields = ('gender', 'birth_year', 'birth_month', 'birth_day')

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'ユーザー名'}))
    password = forms.CharField(max_length=128, widget=forms.PasswordInput(attrs={'placeholder': 'パスワード'}))

########################################
# Form to edit profile.
########################################
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('gender', 'birth_date', 'location', 'favorite_words', 'job')

class AvatarForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('avatar', )

class CoverForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('cover', )

class IntroductionForm(forms.ModelForm):
    introduction = forms.CharField(
        widget=forms.Textarea,
        required=False
    )
    class Meta:
        model = Introduction
        fields = ('introduction',)

class StatementForm(forms.ModelForm):
    statement = forms.CharField(
        widget=forms.Textarea,
        required=False
    )
    class Meta:
        model = Statement
        fields = ('statement',)

class ExperienceForm(forms.ModelForm):
    work_history_id = forms.UUIDField(
        required=False,
    )
    class Meta:
        model = Experience
        fields = ('work_history_id', 'organization', 'job', 'experience', 'from_date', 'to_date' )

class WorkForm(forms.ModelForm):
    portfolio_id = forms.UUIDField(
        required=False,
    )
    class Meta:
        model = Work
        fields = ('portfolio_id', 'title', 'made_at', 'detail', 'url' )

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('image',)

class UrlForm(forms.ModelForm):
    related_link_id = forms.UUIDField(
        required=False,
    )
    class Meta:
        model = Url
        fields = ('related_link_id', 'url',)

class EducationForm(forms.ModelForm):
    educational_bg_id = forms.UUIDField(
        required=False,
    )
    class Meta:
        model = Education
        fields = ('educational_bg_id', 'school', 'major', 'graduated_at', 'detail' )
