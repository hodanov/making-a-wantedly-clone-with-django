from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login as auth_login, get_user_model
User = get_user_model()
from django.contrib import messages
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ObjectDoesNotExist
from .forms import *
from .models import *
from datetime import date
import json
from urllib.parse import urlparse

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

    cover = str(u.profile.cover)
    avatar = str(u.profile.avatar)
    cover = modify_image_path(cover, 'cover')
    avatar = modify_image_path(avatar, 'avatar')

    try:
        organizations = u.organization_set.all()
    except Organization.DoesNotExist:
        organizations = False

    try:
        introduction = u.profile.introduction.introduction
    except Introduction.DoesNotExist:
        introduction = False

    try:
        statement = u.profile.statement.statement
    except Statement.DoesNotExist:
        statement = False

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
    except FriendRelationship.DoesNotExist:
        friends = False

    try:
        introductions_from_frends = u.introductionfromfriend_introduced_user.all()
    except IntroductionFromFriend.DoesNotExist:
        introductions_from_frends = False

    context = {
        'u': u,
        'organizations': organizations,
        'introduction': introduction,
        'statement': statement,
        'work_history': work_history,
        'experiences': experiences,
        'related_link': related_link,
        'urls': urls,
        'educational_bg': educational_bg,
        'educations': educations,
        'portfolio': portfolio,
        'works': works,
        'friends': friends,
        'introductions_from_frends': introductions_from_frends,
        'cover': cover,
        'avatar': avatar,
    }
    return render(request, 'wantedly_app/profile.html', context)

def profile_edit(request):
    if request.user.is_authenticated:
        user = request.user

        ########################################
        # Get profile data from DB.
        # Set form data.
        ########################################
        form = {}
        form['profile'] = ProfileEditForm()
        form['avatar'] = AvatarForm()
        form['cover'] = CoverForm()

        cover = str(user.profile.cover)
        avatar = str(user.profile.avatar)
        cover = modify_image_path(cover, 'cover')
        avatar = modify_image_path(avatar, 'avatar')

        try:
            organizations = user.organization_set.all()
        except Organization.DoesNotExist:
            organizations = ""

        try:
            privacy = Privacy.objects.all()
        except Privacy.DoesNotExist:
            privacy = ""

        try:
            introduction = user.profile.introduction
            form['introduction'] = IntroductionForm(initial={'introduction': introduction.introduction})
        except Introduction.DoesNotExist:
            introduction = ""
            form['introduction'] = IntroductionForm()

        try:
            statement = user.profile.statement
            form['statement'] = StatementForm(initial={'statement': statement.statement})
        except Statement.DoesNotExist:
            statement = ""
            form['statement'] = StatementForm()

        try:
            work_history = user.profile.workhistory
            try:
                experiences = work_history.experience_set.all().order_by('-from_date')
            except Experience.DoesNotExist:
                experiences = ""
        except WorkHistory.DoesNotExist:
            work_history = ""
            experiences = ""
        form['experience'] = ExperienceForm()

        try:
            portfolio = user.profile.portfolio
            works = portfolio.work_set.all().order_by('-made_at')
        except Portfolio.DoesNotExist:
            portfolio = ""
            works = ""
        form['work'] = WorkForm()
        form['image'] = ImageForm()

        try:
            related_link = user.profile.relatedlink
            try:
                urls = related_link.url_set.all()
            except Url.DoesNotExist:
                urls = ""
        except RelatedLink.DoesNotExist:
            related_link = ""
            urls = ""
        form['url'] = UrlForm()

        try:
            educational_bg = user.profile.educationalbackground
            try:
                educations = educational_bg.education_set.all().order_by('-graduated_at')
            except Education.DoesNotExist:
                educations = ""
        except EducationalBackground.DoesNotExist:
            educational_bg = ""
            educations = ""
        form['education'] = EducationForm()

        ########################################
        # Get max_length of text column in DB
        # Used to calculate the number of characters that can be entered.
        ########################################
        max_length = {}
        remaining_length = {}

        introduction_max_length = Introduction._meta.get_field('introduction').max_length
        max_length['introduction'] = introduction_max_length
        if introduction:
            remaining_length['introduction'] = introduction_max_length - len(introduction.introduction)
        else:
            remaining_length['introduction'] = introduction_max_length

        statement_max_length = Statement._meta.get_field('statement').max_length
        max_length['statement'] = statement_max_length
        if statement:
            remaining_length['statement'] = statement_max_length - len(statement.statement)
        else:
            remaining_length['statement'] = statement_max_length

        experience_max_length = Experience._meta.get_field('experience').max_length
        max_length['experience'] = experience_max_length

        work_detail_max_length = Work._meta.get_field('detail').max_length
        max_length['work_detail'] = work_detail_max_length

        ########################################
        # Add profile and form as context.
        ########################################
        context = {
            'cover': cover,
            'avatar': avatar,
            'organizations': organizations,
            'privacy': privacy,
            'introduction': introduction,
            'statement': statement,
            'work_history': work_history,
            'experiences': experiences,
            'related_link': related_link,
            'urls': urls,
            'educational_bg': educational_bg,
            'educations': educations,
            'portfolio': portfolio,
            'works': works,
            'max_length': max_length,
            'remaining_length': remaining_length,
            'form': form,
        }
        return render(request, 'wantedly_app/profile_edit.html', context)
    else:
        return redirect('home')

def profile_edit_post(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            change_privacy_level = request.POST.get('change-privacy-level', False)
            target_instance_name = request.POST.get('target-instance-name', False)
            edit_target_instance_id = request.POST.get('uuid', False)
            add_new_profile_data = request.POST.get('add-new-profile-data', False)
            delete_img_flag = request.POST.get('delete-image', False)
            delete_target_instance_id = request.POST.get('delete-target-instance-id', False)
            portfolio_images = request.FILES.getlist('image', False)
            print(request.POST)
            print(request.FILES)

            ########################################
            # Judge instance to be edited.
            ########################################
            if target_instance_name == 'profile':
                instance = user.profile
                form = ProfileEditForm(request.POST or None, instance=instance)
            elif target_instance_name == 'cover':
                instance = user.profile
                if delete_img_flag:
                    instance.cover = ''
                else:
                    form = CoverForm(request.POST, request.FILES, instance=instance)
            elif target_instance_name == 'avatar':
                instance = user.profile
                if delete_img_flag:
                    instance.avatar = ''
                else:
                    form = AvatarForm(request.POST, request.FILES, instance=instance)
            elif target_instance_name == 'introduction':
                try:
                    user.profile.introduction
                except ObjectDoesNotExist:
                    tmp = Introduction(profile=user.profile)
                    tmp.save()
                instance = user.profile.introduction
                form = IntroductionForm(request.POST or None, instance=instance)
            elif target_instance_name == 'statement':
                try:
                    user.profile.statement
                except ObjectDoesNotExist:
                    tmp = Statement(profile=user.profile)
                    tmp.save()
                instance = user.profile.statement
                form = StatementForm(request.POST or None, instance=instance)
            elif target_instance_name == 'work-history':
                try:
                    user.profile.workhistory
                except ObjectDoesNotExist:
                    tmp = WorkHistory(profile=user.profile)
                    tmp.save()
                if change_privacy_level:
                    instance = user.profile.workhistory
                elif edit_target_instance_id:
                    instance = get_object_or_404(Experience, pk=edit_target_instance_id)
                    form = ExperienceForm(request.POST or None, instance=instance)
                elif add_new_profile_data:
                    form = ExperienceForm(request.POST)
                    instance = form.save(commit=False)
                    instance.work_history_id = user.profile.workhistory.id
                elif delete_target_instance_id:
                    instance = get_object_or_404(Experience, pk=delete_target_instance_id)
            elif target_instance_name == 'portfolio':
                try:
                    user.profile.portfolio
                except ObjectDoesNotExist:
                    tmp = Portfolio(profile=user.profile)
                    tmp.save()
                if change_privacy_level:
                    instance = user.profile.portfolio
                elif edit_target_instance_id:
                    instance = get_object_or_404(Work, pk=edit_target_instance_id)
                    form = WorkForm(request.POST or None, instance=instance)
                elif add_new_profile_data:
                    form = WorkForm(request.POST)
                    instance = form.save(commit=False)
                    instance.portfolio_id = user.profile.portfolio.id
                elif delete_target_instance_id:
                    instance = get_object_or_404(Work, pk=delete_target_instance_id)
                if portfolio_images:
                    image_form = ImageForm(request.FILES)
                else:
                    instance_image = False
            elif target_instance_name == 'portfolio-image':
                if delete_target_instance_id:
                    instance = get_object_or_404(Image, pk=delete_target_instance_id)
            elif target_instance_name == 'related-link':
                try:
                    user.profile.relatedlink
                except ObjectDoesNotExist:
                    tmp = RelatedLink(profile=user.profile)
                    tmp.save()
                if change_privacy_level:
                    instance = user.profile.relatedlink
                elif edit_target_instance_id:
                    instance = get_object_or_404(Url, pk=edit_target_instance_id)
                    form = UrlForm(request.POST or None, instance=instance)
                elif add_new_profile_data:
                    form = UrlForm(request.POST)
                    instance = form.save(commit=False)
                    instance.related_link_id = user.profile.relatedlink.id
                elif delete_target_instance_id:
                    instance = get_object_or_404(Url, pk=delete_target_instance_id)
            elif target_instance_name == 'educational-bg':
                try:
                    user.profile.educationalbackground
                except ObjectDoesNotExist:
                    tmp = EducationalBackground(profile=user.profile)
                    tmp.save()
                if change_privacy_level:
                    instance = user.profile.educationalbackground
                elif edit_target_instance_id:
                    instance = get_object_or_404(Education, pk=edit_target_instance_id)
                    form = EducationForm(request.POST or None, instance=instance)
                elif add_new_profile_data:
                    form = EducationForm(request.POST)
                    instance = form.save(commit=False)
                    instance.educational_background_id = user.profile.educationalbackground.id
                elif delete_target_instance_id:
                    instance = get_object_or_404(Education, pk=delete_target_instance_id)

            ########################################
            # Save the edited or added profile data.
            ########################################
            if change_privacy_level:
                privacy_id = request.POST.get('privacy-id', False)
                instance.privacy = Privacy(pk=privacy_id)
                instance.save()
            elif delete_img_flag:
                instance.save()
            elif delete_target_instance_id:
                instance.delete()
            elif form.is_valid():
                if add_new_profile_data:
                    instance.save()
                    print("success adding new data.")
                else:
                    form.save()
                    print("success editing data.")
                if portfolio_images and image_form.is_valid():
                    for idx, image in enumerate(portfolio_images):
                        image_instance = Image(
                            work_id=instance.id,
                            image=image,
                        )
                        image_instance.save()
                        if idx == 0:
                            instance_image = image_instance.image
                        print("success save images.")

            ########################################
            # Get the saved data.
            ########################################
            response_data = {}
            response_data['result'] = '設定が更新されました！'
            response_data['uuid'] = str(instance.id)
            response_data['target_instance_name'] = target_instance_name
            response_data['change_privacy_level'] = change_privacy_level
            response_data['add_new_profile_data'] = add_new_profile_data
            response_data['delete_target_instance_id'] = delete_target_instance_id
            if change_privacy_level:
                p_instance = Privacy.objects.get(pk=instance.privacy.id)
                response_data['privacy_level'] = p_instance.privacy_level
                response_data['icon'] = p_instance.icon
            elif target_instance_name == 'profile':
                # response_data['gender'] = instance.gender
                # response_data['birth_date'] = str(instance.birth_date)
                response_data['location'] = instance.location
                response_data['favorite_words'] = instance.favorite_words
                response_data['job'] = instance.job.job
            elif target_instance_name == 'avatar':
                avatar = str(instance.avatar)
                avatar = modify_image_path(avatar, 'avatar')
                response_data['avatar'] = avatar
            elif target_instance_name == 'cover':
                cover = str(instance.cover)
                cover = modify_image_path(cover, 'cover')
                response_data['cover'] = cover
            elif target_instance_name == 'introduction':
                response_data['introduction'] = instance.introduction
            elif target_instance_name == 'statement':
                response_data['statement'] = instance.statement
            elif target_instance_name == 'work-history':
                response_data['organization'] = instance.organization
                response_data['job'] = instance.job
                response_data['from_date'] = str(instance.from_date)
                response_data['to_date'] = str(instance.to_date)
                response_data['experience'] = instance.experience
                response_data['work_history_id'] = str(instance.work_history.id)
            elif target_instance_name == 'portfolio':
                response_data['title'] = instance.title
                response_data['url'] = instance.url
                response_data['made_at'] = str(instance.made_at)
                response_data['detail'] = instance.detail
                response_data['image'] = str(instance_image)
                response_data['portfolio_id'] = str(instance.portfolio.id)
            elif target_instance_name == 'related-link':
                response_data['url'] = instance.url
                response_data['related_link_id'] = str(instance.related_link.id)
            elif target_instance_name == 'educational-bg':
                response_data['school'] = instance.school
                response_data['major'] = instance.major
                response_data['graduated_at'] = str(instance.graduated_at)
                response_data['detail'] = instance.detail
                response_data['educational_bg_id'] = str(instance.educational_background_id)

            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )
        else:
            return HttpResponse(
                json.dumps({"nothing to see": "this isn't happening"}),
                content_type="application/json"
            )

def organization(request, id):
    ########################################
    # Function for organization view.
    # Get organization, values and so on.
    # Return wantedly_app/org.html page.
    ########################################
    org = get_object_or_404(Organization, pk=id)

    cover = str(org.cover)
    logo = str(org.logo)
    cover = modify_image_path(cover, 'org_cover')
    logo = modify_image_path(logo, 'logo')

    mission = org.mission
    try:
        values = org.value_set.all()
    except Organization.DoesNotExist:
        values = False
    try:
        membership = org.membership_set.all()
        members = []
        for member in membership:
            m = User.objects.get(pk=member.user_id)
            members.append(m)
    except Membership.DoesNotExist:
        members = False

    context = {
        'org': org,
        'cover': cover,
        'logo': logo,
        'mission': mission,
        'values': values,
        'members': members,
    }
    return render(request, 'wantedly_app/org.html', context)

def modify_image_path(image_path, type=''):
    ########################################
    # Modify images path each type and return it.
    ########################################
    parsed_uri = urlparse(image_path)
    if parsed_uri.scheme == 'https' or parsed_uri.scheme == 'http':
        pass
    elif image_path == '':
        image_path = '/media/default_' + type + '.jpg'
    else:
        image_path = '/media/' + image_path
    return image_path
