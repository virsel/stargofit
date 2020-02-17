from django.db import models
from django.conf import settings
from django.contrib.auth.models import Group
from django_countries.fields import CountryField
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .managers import CustomUserManager


class Contact(models.Model):
    member_from = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    related_name='rel_from_set',
                                    on_delete=models.CASCADE)
    member_to = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  related_name='rel_to_set',
                                  on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True,
                                   db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} follows {}'.format(self.member_from,
                                      self.member_to)

    # Add following field to User dynamically


class Member(AbstractBaseUser, PermissionsMixin):
    membername = models.CharField(max_length=100, unique=True)
    email = models.EmailField(
        verbose_name='email address', max_length=254, unique=True)
    first_name = models.CharField(max_length=100)
    password = models.TextField(max_length=100)
    last_name = models.CharField(max_length=100)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, default='M')
    USERNAME_FIELD = 'membername'
    REQUIRED_FIELDS = ['email']
    user_permissions = models.ManyToManyField(Group, related_name="members")
    objects = CustomUserManager()
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    following = models.ManyToManyField(
        'self', through=Contact, related_name='followers', symmetrical=False)
    total_followers = models.PositiveIntegerField(db_index=True, default=0)
    date_of_birth = models.DateField(blank=True, null=True)

    def age(self):
        import datetime
        if self.date_of_birth is None:
            return None
        return int((datetime.date.today() - self.date_of_birth).days / 365.25)

    def __str__(self):
        return self.email

    def get_full_name(self):
        if self.first_name is None and self.last_name is None:
            return None
        return '{} {}'.format(self.first_name, self.last_name)

    def GetCountry(self):
        return self.profile.country.name


class Profile(models.Model):
    member = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='profile', on_delete=models.CASCADE)

    def get_default_image():
        return 'default_avatar.svg'
    photo = models.ImageField(
        upload_to='members', blank=True, default=get_default_image)
    country = CountryField(blank_label='Deutschland', default='DE')

    def __str__(self):
        return 'Profile for member {}'.format(self.member.membername)


class LikeDislikeManager(models.Manager):
    use_for_related_fields = True

    def likes(self):
        # take the queryset with records greater than 0
        return self.get_queryset().filter(vote__gt=0)

    def dislikes(self):
        # take the queryset with records less than 0
        return self.get_queryset().filter(vote__lt=0)

    def sum_rating(self):
        # We take the total rating
        return self.get_queryset().aggregate(Sum('vote')).get('vote__sum') or 0

    def images(self):
        return self.get_queryset().filter(content_type__model='image').order_by('-images__pub_date')

    def exercises(self):
        return self.get_queryset().filter(content_type__model='exercise').order_by('-exercises__pub_date')


class LikeDislike(models.Model):
    like = 1
    dislike = -1

    votes = (
        (dislike, 'dislike'),
        (like, 'like')
    )

    vote = models.SmallIntegerField(verbose_name='voting', choices=votes)
    member = models.ForeignKey(
        Member, verbose_name='voter', on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()  # id of related object
    # uses automatic content_type and object_id to create polymorphic relationships
    content_object = GenericForeignKey()

    # facilitates (erleichtern) to getting seperateliy Like and Dislike and total rating
    objects = LikeDislikeManager()
