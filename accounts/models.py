from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.crypto import get_random_string
import re
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError
from projects.models import Project


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email field is required!')
        email = self.normalize_email(email)
        user = self.model(email=email, password=password, **extra_fields)
        user.set_password(password)
        user.create_activation_code()
        user.save()
        return user

    def create_user(self, email, password, **extra_fields):
        user = self._create_user(email=email, password=password, **extra_fields)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email=email, password=password, **extra_fields)


class User(AbstractUser):
    id = models.CharField(max_length=50, unique=True, primary_key=True, blank=True)
    username = models.CharField(max_length=60, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    is_company = models.BooleanField(default=False)
    is_user = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=10, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.id} - {self.email}'

    def create_activation_code(self):
        code = get_random_string(length=10, allowed_chars='0123456789')
        self.activation_code = code

    def clean(self):
        if self.phone_number and not re.match(r'^\+?[0-9]+$', self.phone_number):
            raise ValidationError(_('Invalid phone number format'))
        super().clean()

    def save(self, *args, **kwargs):
        if not self.id:
            random_integer = get_random_string(length=5, allowed_chars='0123456789')
            self.id = f'{self.email}-{random_integer}'

        super().save(*args, **kwargs)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    languages = models.CharField(max_length=256, blank=True)
    programming_languages = models.CharField(max_length=256, blank=True)
    projects = models.ManyToManyField(Project, related_name='user', blank=True)
    education = models.TextField(blank=True)
    stack = models.CharField(max_length=50, blank=True)
    about = models.TextField(blank=True)
    age = models.IntegerField(blank=True)
    work_experience = models.TextField(blank=True)
    achievements = models.TextField(blank=True)
    image = models.ImageField(blank=True, upload_to='user/')

    def __str__(self):
        return self.user.email


class CompanyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='company', null=True, blank=True)
    members = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, related_name='company', null=True, blank=True)
    about = models.TextField(blank=True)
    achievements = models.TextField(blank=True)
    direction = models.TextField(blank=True)
    image = models.ImageField(blank=True, upload_to='company/')

    def __str__(self):
        return f'{self.user.email}'
