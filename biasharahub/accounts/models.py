from statistics import mean

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.urls import reverse
from django.utils import timezone


class MyUserManager(BaseUserManager):
    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff,
            # is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff to True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser to True')
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=True)
    first_name = models.CharField('first name', max_length=30, blank=True)
    last_name = models.CharField('last name', max_length=150, blank=True)
    date_joined = models.DateTimeField('date joined', default=timezone.now)  # , auto_now_add=True)

    is_staff = models.BooleanField(default=False, )
    is_active = models.BooleanField(default=True, )
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True, blank=True)

    photo = models.ImageField(upload_to="user/photos", blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True, help_text="Please start with 'https://www.'")

    address = models.CharField(max_length=255, blank=True, )
    is_freelancer = models.BooleanField(default=False)
    is_entrepreneur = models.BooleanField(default=False)

    objects = MyUserManager()
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def get_absolute_url(self):
        return reverse('accounts:detail', kwargs={'pk': self.pk})

    @classmethod
    def get_email_field_name(self):
        return 'email'

    def average_rating(self):
        all_ratings = list(map(lambda x: x.rating, self.review_set.all()))

        if not all_ratings:
            return float('nan');
        else:
            return mean(all_ratings)


class Network(models.Model):
    network = models.CharField(max_length=254)
    icon = models.CharField(max_length=254)

    def __str__(self):
        return self.network


class SocialProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    username = models.CharField(max_length=254)
    url = models.URLField(max_length=500)

    def __str__(self):
        return self.username
