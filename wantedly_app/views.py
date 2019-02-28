import json
from urllib.parse import urlparse, urljoin
from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, get_user_model
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
User = get_user_model()

def home(request):
    """
    The View function for the top page and home.

    Args:
        request(object): The WSGI request objects containing request method, HttpRequest.user and so on.

    context(dict): The LoginForm().

    Returns:
        1: Return 'wantedly_app/home.html' if request.user is authenticated.
        2: Redirect 'home' if the following conditions are satisfied.
            - reauest.method == 'POST'.
            - The user exists in the DB and is active.
        3: Return 'wantedly/top.html' if request.user is not authenticated.
    """
    if request.user.is_authenticated:
        return render(request, 'wantedly_app/home.html')

    # Execute the below if the user is not authenticated.
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])

        # If the user exists in the DB,
        if user is not None:

            # If the user is active,
            if user.is_active:
                auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                messages.add_message(request, messages.SUCCESS, 'ログインしました！')
                return redirect('home')

            # If the user is not active,
            else:
                messages.add_message(request, messages.ERROR, 'ユーザーのアクティベーションがまだ完了していません。')

        # If the user does not exists in the DB,
        else:
            messages.add_message(request, messages.ERROR, 'ログインに失敗しました。ユーザーが存在しないかパスワードが間違っています。')

    context = {'login_form': LoginForm()}
    return render(request, 'wantedly_app/top.html', context)

def about(request):
    """
    The View function for the about page.

    Returns:
        Return 'wantedly_app/about.html'
    """
    return render(request, 'wantedly_app/about.html')

def sign_up(request):
    """
    The View function for the signup page.

    context(dict):
        The signup form and so on.

    Returns:
        1: Return 'sign_up.html' if request.method == 'GET'
        2: Redirect 'home' if request.method == 'POST'
    """
    context = {
        'signup_form': SignUpForm(),
        'profile_form': ProfileForm(),
        'login_form': LoginForm(),
    }

    if request.method == 'GET':
        return render(request, 'registration/sign_up.html', context)

    # Execute the below if the signup form is posted.
    if request.method == 'POST':
        context['signup_form'] = SignUpForm(request.POST)
        context['profile_form'] = ProfileForm(request.POST)
        if context['signup_form'].is_valid() and context['profile_form'].is_valid():
            username = context['signup_form'].cleaned_data.get('username')
            email = context['signup_form'].cleaned_data.get('email')
            password = context['signup_form'].cleaned_data.get('password')
            gender = context['profile_form'].cleaned_data.get('gender')
            birth_year = context['profile_form'].cleaned_data.get('birth_year')
            birth_month = context['profile_form'].cleaned_data.get('birth_month')
            birth_day = context['profile_form'].cleaned_data.get('birth_day')

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

def profile(request, id):
    """
    The View function for the Profile page.

    Args:
        request(object): The WSGI request objects containing request method, HttpRequest.user and so on.
        id(uuid): The uuid of User object.

    u(object): The User object where user_id='id(uuid)'.
    context(dict): The profile data where user_id='id(uuid)'.

    Returns:
        1: Return 404 if there is no user.
        2: Return 'wantedly_app/profile.html' if there is the user where user_id='id(uuid)'.
    """
    u = get_object_or_404(User, pk=id)
    context = ProfileContext(u).get_context()
    return render(request, 'wantedly_app/profile.html', context)

def profile_edit(request):
    """
    The View function for the Profile edit page.

    Args:
        request(object): The WSGI request objects containing request method, HttpRequest.user and so on.

    context(dict): The profile data.

    Returns:
        1: Return 'wantedly_app/profile_edit.html' if request.user is authenticated.
        2: Redirect 'home' if request.user is not authentiated.
    """
    if request.user.is_authenticated:
        u = request.user
        context = ProfileContext(u).get_context_with_form()
        context = calculate_char_in_textarea(context)
        return render(request, 'wantedly_app/profile_edit.html', context)
    else:
        return redirect('home')

def profile_edit_post(request):
    """
    The function when POST action occurs in the Profile edit page. The POST data is sent by Ajax. The Ajax script is in main.js.

    Args:
        request(object): The WSGI request objects containing request method, HttpRequest.user and so on.

    Returns:
        Return The HttpResponse data as json.
    """
    if request.user.is_authenticated and request.method == 'POST':
        u = request.user
        rq = read_request_data(request)
        ji = judge_instance(u, rq, request)
        save_data_to_db(rq, ji, request)
        response = load_data_from_db(rq, ji)
        return HttpResponse(
            json.dumps(response),
            content_type="application/json"
        )
    return HttpResponse(
        json.dumps({"nothing to see": "this isn't happening"}),
        content_type="application/json"
    )

def organization(request, id):
    """
    The View function for the organization page.

    Args:
        request(object): The WSGI request objects containing request method, HttpRequest.user and so on.
        id(uuid): The uuid of the organization object.

    Returns:
        Return wantedly_app/org.html page.
    """
    org = get_object_or_404(Organization, pk=id)
    context = {
        'org': org,
        'cover': modify_image_url(str(org.cover), 'cover'),
        'logo': modify_image_url(str(org.logo), 'logo'),
        'mission': "",
        'values': "",
        'members': "",
    }

    context['mission'] = org.mission

    if org.value_set.exists():
        context['values'] = org.value_set.all()

    if org.membership_set.exists():
        membership = org.membership_set.all()
        context['members'] = []
        for member in membership:
            m = User.objects.get(pk=member.user_id)
            context['members'].append(m)

    return render(request, 'wantedly_app/org.html', context)


########################################
# Functions and Classes other than view.
########################################
class ProfileContext:
    """
    Pull the profile data from DB or set form data.

    Attributes:
        context(dict): The dictionary to store the pulled profile data from DB.
    """
    def __init__(self, u):
        """
        Pull the profile data from DB and add the data to the context.

        Args:
            u(object): The HttpRequest.user object.

        Returns:
            Return the context at the get_context() function.
        """
        self.context = {
            'u': u,
            'cover': modify_image_url(str(u.profile.cover), 'cover'),
            'avatar': modify_image_url(str(u.profile.avatar), 'avatar'),
            'organizations': "",
            'introduction': "",
            'statement': "",
            'work_history': "",
            'experiences': "",
            'related_link': "",
            'urls': "",
            'educational_bg': "",
            'educations': "",
            'portfolio': "",
            'works': "",
            'friends': [],
            'introductions_from_frends': "",
        }
        if u.organization_set.exists():
          self.context['organizations'] = u.organization_set.all()
        if Privacy.objects.exists():
          self.context['privacy'] = Privacy.objects.all()
        self.context['introduction'] = u.profile.introduction
        self.context['statement'] = u.profile.statement
        self.context['work_history'] = u.profile.workhistory
        if self.context['work_history'].experience_set.exists():
          self.context['experiences'] = self.context['work_history'].experience_set.all().order_by('-from_date')
        self.context['portfolio'] = u.profile.portfolio
        if self.context['portfolio'].work_set.exists():
          self.context['works'] = self.context['portfolio'].work_set.all().order_by('-made_at')
        self.context['related_link'] = u.profile.relatedlink
        if self.context['related_link'].url_set.exists():
          self.context['urls'] = self.context['related_link'].url_set.all()
        self.context['educational_bg'] = u.profile.educationalbackground
        if self.context['educational_bg'].education_set.exists():
          self.context['educations'] = self.context['educational_bg'].education_set.all().order_by('-graduated_at')

    def get_context(self):
        return self.context

    def get_context_with_form(self):
        """
        Add the form to the context.

        Return:
            context(object): The context that added some forms.
        """
        self.context['form'] = {
            'profile': ProfileEditForm(),
            'avatar': AvatarForm(),
            'cover': CoverForm(),
            'introduction': IntroductionForm(),
            'statement': StatementForm(),
            'experience': ExperienceForm(),
            'work': WorkForm(),
            'image': ImageForm(),
            'url': UrlForm(),
            'education': EducationForm(),
        }
        self.context['form']['introduction'] = IntroductionForm(
            initial={'introduction': self.context['introduction'].introduction}
        )
        self.context['form']['statement'] = StatementForm(
            initial={'statement': self.context['statement'].statement}
        )
        return self.context

def modify_image_url(image_url, type=''):
    """
    Modify image url each types and return it.

    Args:
        image_url(str): The pulled image url from DB.
        type(str): The type of image. Profile cover, avatar or so on.

    Returns:
        image_url(str): The modyfied image url.
    """
    parsed_uri = urlparse(image_url)
    if parsed_uri.scheme == 'https' or parsed_uri.scheme == 'http':
        pass
    elif image_url == '':
        image_url = '/media/default_' + type + '.jpg'
    else:
        image_url = '/media/' + image_url
    return image_url

def calculate_char_in_textarea(context):
    """
    Pull max_length of text column in DB and calculate the number of characters that can be entered to textarea. And add calculated data to the context.

    Args:
        context(dict): The created context in ProfileContext.

    Returns:
        context(dict): The context that added the calculated data.
    """
    context['max_length'] = {}
    context['remaining_length'] = {}
    introduction_max_length = Introduction._meta.get_field('introduction').max_length
    context['max_length']['introduction'] = introduction_max_length

    if context['introduction']:
        context['remaining_length']['introduction'] = (
            introduction_max_length - len(context['introduction'].introduction)
        )
    else:
        context['remaining_length']['introduction'] = introduction_max_length

    statement_max_length = Statement._meta.get_field('statement').max_length
    context['max_length']['statement'] = statement_max_length

    if context['statement']:
        context['remaining_length']['statement'] = (
            statement_max_length - len(context['statement'].statement)
        )
    else:
        context['remaining_length']['statement'] = statement_max_length

    experience_max_length = Experience._meta.get_field('experience').max_length
    context['max_length']['experience'] = experience_max_length

    work_detail_max_length = Work._meta.get_field('detail').max_length
    context['max_length']['work_detail'] = work_detail_max_length

    return context

def read_request_data(request):
    """
    Read the request.POST and the request.FILES data. The function is called in the profile_edit_post function.

    Args:
        request(object): The WSGI request objects.
            - request.POST: The posted object. The object has information for judging the instance to be edited.
            - request.FILES: The image posted by user.

    Returns:
        rq(dict): The request.POST or request.FILES.
    """
    print(request.POST)
    print(request.FILES)
    rq = {
        'change_privacy_level': request.POST.get('change-privacy-level', False),
        'target_instance_name': request.POST.get('target-instance-name', False),
        'edit_target_instance_id': request.POST.get('uuid', False),
        'add_new_profile_data': request.POST.get('add-new-profile-data', False),
        'delete_img_flag': request.POST.get('delete-image', False),
        'delete_target_instance_id': request.POST.get('delete-target-instance-id', False),
        'portfolio_images': request.FILES.getlist('image', False),
    }
    return rq

def judge_instance(u, rq, request):
    """
    Judge the instance to be edited. The function is called in the profile_edit_post function.

    Args:
        u(object): The
        request(object): The WSGI request objects.
            - request.user: The authenticated user object.
            - request.POST: The posted object. The object has information for judging the instance to be edited.
            - request.FILES: The image posted by user.

    Returns:
        ji(dict):
            - instance: The information of the target instance.
            - form: The posted form data.
            - image_form: The posted image data.
    """
    ji = {
        'instance': '',
        'form': '',
        'image_form': '',
    }

    if rq['target_instance_name'] == 'profile':
        ji['instance'] = u.profile
        ji['form'] = ProfileEditForm(request.POST or None, instance=ji['instance'])
    elif rq['target_instance_name'] == 'cover':
        ji['instance'] = u.profile
        if rq['delete_img_flag']:
            ji['instance'].cover = ''
        else:
            ji['form'] = CoverForm(request.POST, request.FILES, instance=ji['instance'])
    elif rq['target_instance_name'] == 'avatar':
        ji['instance'] = u.profile
        if rq['delete_img_flag']:
            ji['instance'].avatar = ''
        else:
            ji['form'] = AvatarForm(request.POST, request.FILES, instance=ji['instance'])
    elif rq['target_instance_name'] == 'introduction':
        ji['instance'] = u.profile.introduction
        ji['form'] = IntroductionForm(request.POST or None, instance=ji['instance'])
    elif rq['target_instance_name'] == 'statement':
        ji['instance'] = u.profile.statement
        ji['form'] = StatementForm(request.POST or None, instance=ji['instance'])
    elif rq['target_instance_name'] == 'work-history':
        if rq['change_privacy_level']:
            ji['instance'] = u.profile.workhistory
        elif rq['edit_target_instance_id']:
            ji['instance'] = get_object_or_404(Experience, pk=rq['edit_target_instance_id'])
            ji['form'] = ExperienceForm(request.POST or None, instance=ji['instance'])
        elif rq['add_new_profile_data']:
            ji['form'] = ExperienceForm(request.POST)
            ji['instance'] = ji['form'].save(commit=False)
            ji['instance'].work_history_id = u.profile.workhistory.id
        elif rq['delete_target_instance_id']:
            ji['instance'] = get_object_or_404(Experience, pk=rq['delete_target_instance_id'])
    elif rq['target_instance_name'] == 'portfolio':
        if rq['change_privacy_level']:
            ji['instance'] = u.profile.portfolio
        elif rq['edit_target_instance_id']:
            ji['instance'] = get_object_or_404(Work, pk=rq['edit_target_instance_id'])
            ji['form'] = WorkForm(request.POST or None, instance=ji['instance'])
        elif rq['add_new_profile_data']:
            ji['form'] = WorkForm(request.POST)
            ji['instance'] = ji['form'].save(commit=False)
            ji['instance'].portfolio_id = u.profile.portfolio.id
        elif rq['delete_target_instance_id']:
            ji['instance'] = get_object_or_404(Work, pk=rq['delete_target_instance_id'])
        if rq['portfolio_images']:
            ji['image_form'] = ImageForm(request.FILES)
        else:
            ji['instance_image'] = False
    elif rq['target_instance_name'] == 'portfolio-image':
        if rq['delete_target_instance_id']:
            ji['instance'] = get_object_or_404(Image, pk=rq['delete_target_instance_id'])
    elif rq['target_instance_name'] == 'related-link':
        if rq['change_privacy_level']:
            ji['instance'] = u.profile.relatedlink
        elif rq['edit_target_instance_id']:
            ji['instance'] = get_object_or_404(Url, pk=rq['edit_target_instance_id'])
            ji['form'] = UrlForm(request.POST or None, instance=ji['instance'])
        elif rq['add_new_profile_data']:
            ji['form'] = UrlForm(request.POST)
            ji['instance'] = ji['form'].save(commit=False)
            ji['instance'].related_link_id = u.profile.relatedlink.id
        elif rq['delete_target_instance_id']:
            ji['instance'] = get_object_or_404(Url, pk=rq['delete_target_instance_id'])
    elif rq['target_instance_name'] == 'educational-bg':
        if rq['change_privacy_level']:
            ji['instance'] = u.profile.educationalbackground
        elif rq['edit_target_instance_id']:
            ji['instance'] = get_object_or_404(Education, pk=rq['edit_target_instance_id'])
            ji['form'] = EducationForm(request.POST or None, instance=ji['instance'])
        elif rq['add_new_profile_data']:
            ji['form'] = EducationForm(request.POST)
            ji['instance'] = ji['form'].save(commit=False)
            ji['instance'].educational_background_id = u.profile.educationalbackground.id
        elif rq['delete_target_instance_id']:
            ji['instance'] = get_object_or_404(Education, pk=rq['delete_target_instance_id'])

    return ji

def save_data_to_db(rq, ji, request):
    """
    Save the edited or added profile data. The function is called in the profile_edit_post function.

    Args:
        rq:
        ji:
    """
    if rq['change_privacy_level']:
        privacy_id = request.POST.get('privacy-id', False)
        ji['instance'].privacy = Privacy(pk=privacy_id)
        ji['instance'].save()
    elif rq['delete_img_flag']:
        ji['instance'].save()
    elif rq['delete_target_instance_id']:
        ji['instance'].delete()
    elif ji['form'].is_valid():
        if rq['add_new_profile_data']:
            ji['instance'].save()
            print("success adding new data.")
        else:
            ji['form'].save()
            print("success editing data.")
        if rq['portfolio_images'] and ji['image_form'].is_valid():
            for idx, image in enumerate(rq['portfolio_images']):
                image_instance = Image(
                    work_id=ji['instance'].id,
                    image=image,
                )
                image_instance.save()
                if idx == 0:
                    ji['instance_image'] = image_instance.image
                print("success save images.")

def load_data_from_db(rq, ji):
    """
    Load the saved data. The function is called in the profile_edit_post function.

    Args:
        rq:
        ji:

    Returns:
        response(dict): The response data.
    """
    response = {
        'result': '設定が更新されました！',
        'uuid': str(ji['instance'].id),
        'target_instance_name': rq['target_instance_name'],
        'change_privacy_level': rq['change_privacy_level'],
        'add_new_profile_data': rq['add_new_profile_data'],
        'delete_target_instance_id': rq['delete_target_instance_id'],
    }
    if rq['change_privacy_level']:
        p_instance = Privacy.objects.get(pk=ji['instance'].privacy.id)
        response['privacy_level'] = p_instance.privacy_level
        response['icon'] = p_instance.icon
    elif rq['target_instance_name'] == 'profile':
        response['location'] = ji['instance'].location
        response['favorite_words'] = ji['instance'].favorite_words
        response['job'] = ji['instance'].job.job
    elif rq['target_instance_name'] == 'avatar':
        avatar = str(ji['instance'].avatar)
        avatar = modify_image_url(avatar, 'avatar')
        response['avatar'] = avatar
    elif rq['target_instance_name'] == 'cover':
        cover = str(ji['instance'].cover)
        cover = modify_image_url(cover, 'cover')
        response['cover'] = cover
    elif rq['target_instance_name'] == 'introduction':
        response['introduction'] = ji['instance'].introduction
    elif rq['target_instance_name'] == 'statement':
        response['statement'] = ji['instance'].statement
    elif rq['target_instance_name'] == 'work-history':
        response['organization'] = ji['instance'].organization
        response['job'] = ji['instance'].job
        response['from_date'] = str(ji['instance'].from_date)
        response['to_date'] = str(ji['instance'].to_date)
        response['experience'] = ji['instance'].experience
        response['work_history_id'] = str(ji['instance'].work_history.id)
    elif rq['target_instance_name'] == 'portfolio':
        response['title'] = ji['instance'].title
        response['url'] = ji['instance'].url
        response['made_at'] = str(ji['instance'].made_at)
        response['detail'] = ji['instance'].detail
        response['image'] = str(ji['instance_image'])
        response['portfolio_id'] = str(ji['instance'].portfolio.id)
    elif rq['target_instance_name'] == 'related-link':
        response['url'] = ji['instance'].url
        response['related_link_id'] = str(ji['instance'].related_link.id)
    elif rq['target_instance_name'] == 'educational-bg':
        response['school'] = ji['instance'].school
        response['major'] = ji['instance'].major
        response['graduated_at'] = str(ji['instance'].graduated_at)
        response['detail'] = ji['instance'].detail
        response['educational_bg_id'] = str(ji['instance'].educational_background_id)

    return response
