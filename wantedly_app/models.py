from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
# from django.core.mail import send_mail

class Job(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job = models.CharField(max_length=64, blank=True)
    def __str__(self):
        return self.job

class Privacy(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    privacy_level = models.CharField(max_length=32, blank=False)
    icon = models.CharField(max_length=128, blank=False, default='<i class="fas fa-users"></i>')

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not username:
            raise ValueError('Users must have an username')
        elif not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username = username,
            email = self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            username,
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=32, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=32, blank=True)
    last_name = models.CharField(max_length=32, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    # class Meta:
    #     verbose_name = 'user'
    #     verbose_name_plural = 'users'
    #
    # def email_user(self, subject, message, from_email=None, **kwargs):
    #     '''
    #     Sends an email to this User.
    #     '''
    #     send_mail(subject, message, from_email, [self.email], **kwargs)


########################################
# Save location.
########################################
def user_avatar_directory_path(instance, filename):
    return 'user-{0}/avatar/{1}'.format(instance.user.id, filename)

def user_cover_directory_path(instance, filename):
    return 'user-{0}/cover/{1}'.format(instance.user.id, filename)

def user_portfolio_directory_path(instance, filename):
    return 'user-{0}/portfolio/{1}'.format(instance.work.portfolio.profile.user.id, filename)

def organization_logo_directory_path(instance, filename):
    return 'org-{0}/logo/{1}'.format(instance.id, filename)

def organization_cover_directory_path(instance, filename):
    return 'org-{0}/cover/{1}'.format(instance.id, filename)

def recruitment_eyecatch_directory_path(instance, filename):
    return 'org-{0}/recruitment/eyecatch/{1}'.format(instance.organization.id, filename)

class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=16, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=64, blank=True)
    favorite_words = models.CharField(max_length=64, blank=True)
    avatar = models.ImageField(upload_to=user_avatar_directory_path, null=True, blank=True)
    cover = models.ImageField(upload_to=user_cover_directory_path, null=True, blank=True)
    job = models.ForeignKey(Job, on_delete=models.SET_NULL, null=True)
    privacy = models.ForeignKey(Privacy, on_delete=models.SET_NULL, null=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Introduction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    privacy = models.ForeignKey(Privacy, on_delete=models.SET_NULL, null=True)
    introduction = models.TextField(max_length=2048, blank=False)

class Statement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    privacy = models.ForeignKey(Privacy, on_delete=models.SET_NULL, null=True)
    statement = models.TextField(max_length=2048, blank=False)

class WorkHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    privacy = models.ForeignKey(Privacy, on_delete=models.SET_NULL, null=True)

class Experience(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    work_history = models.ForeignKey(WorkHistory, on_delete = models.CASCADE)
    organization = models.CharField(max_length=64, blank=False)
    job = models.CharField(max_length=64, blank=True)
    experience = models.TextField(max_length=256, blank=True)
    from_date = models.DateField(null=True, blank=True)
    to_date = models.DateField(null=True, blank=True)

class Portfolio(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    privacy = models.ForeignKey(Privacy, on_delete=models.SET_NULL, null=True)

# def user_directory_path(instance, ):
#     pass
class Work(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    portfolio = models.ForeignKey(Portfolio, on_delete = models.CASCADE)
    title = models.CharField(max_length=64, blank=False)
    made_at = models.DateField(null=True, blank=True)
    detail = models.TextField(max_length=256, blank=True)
    url = models.URLField(max_length=256, blank=True)

class RelatedLink(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    privacy = models.ForeignKey(Privacy, on_delete=models.SET_NULL, null=True)

class Url(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    related_link = models.ForeignKey(RelatedLink, on_delete = models.CASCADE)
    url = models.URLField(max_length=256, blank=False)

class EducationalBackground(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    privacy = models.ForeignKey(Privacy, on_delete=models.SET_NULL, null=True)

class Education(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    educational_background = models.ForeignKey(EducationalBackground, on_delete=models.CASCADE)
    school = models.CharField(max_length=64, blank=False)
    major = models.CharField(max_length=64, blank=True)
    graduated_at = models.DateField(null=True, blank=True)
    detail = models.TextField(max_length=256, blank=True)

class Organization(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.CharField(max_length=64, blank=True)
    logo = models.ImageField(upload_to=organization_logo_directory_path, null=True, blank=True)
    cover = models.ImageField(upload_to=organization_cover_directory_path, null=True, blank=True)
    established_at = models.DateField(null=True, blank=True)
    ceo = models.CharField(max_length=64, blank=True)
    members = models.ManyToManyField(
        User,
        through='Membership',
        through_fields=('organization', 'user'),
    )
    location = models.CharField(max_length=128, blank=True)
    mission = models.CharField(max_length=64, blank=True)
    mission_detail = models.TextField(max_length=256, blank=True)
    url = models.URLField(max_length=256, blank=True)

class Membership(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class FriendRelationship(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    follower_user = models.ForeignKey(User, related_name='%(class)s_follower', on_delete=models.CASCADE)
    followed_user = models.ForeignKey(User, related_name='%(class)s_followed', on_delete=models.CASCADE)

class IntroductionFromFriend(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    friend_user = models.ForeignKey(User, related_name='%(class)s_friend', on_delete=models.CASCADE)
    introduced_user = models.ForeignKey(User, related_name='%(class)s_introduced_user', on_delete=models.CASCADE)
    introduction = models.TextField(max_length=128, blank=False)

class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    work = models.ForeignKey(Work, on_delete = models.CASCADE)
    image = models.ImageField(upload_to=user_portfolio_directory_path, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Recruitment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    title = models.CharField(max_length=64, blank=False)
    looking_for = models.CharField(max_length=64, blank=False)
    article = models.TextField(max_length=2048, blank=False)
    eyecatch = models.ImageField(upload_to=recruitment_eyecatch_directory_path, null=True, blank=True)

class Value(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.CharField(max_length=64, blank=False)
    detail = models.TextField(max_length=256, blank=True)
