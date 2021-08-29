from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from django_countries.fields import CountryField


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, user_name, password, **other_fields):
        other_fields.setdefault('is_staff', True)  # age is_staff val ndsht , True mishe vel esh
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_superuser', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Seperuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, user_name, password, **other_fields)

    def create_user(self, email, user_name, password, **other_fields):
        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name, **other_fields)

        user.set_password(password)
        user.save()
        return user

class BaseUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    user_name = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    about = models.TextField(_('about'), blank=True)
    #delivery details
    country = CountryField()
    phone_number = models.CharField(max_length=11, unique=True, blank=True)
    post_code = models.CharField(max_length=15, unique=True, blank=True)
    address_line_1 = models.CharField(max_length=150, blank=True)
    town_city = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    objects = CustomAccountManager();

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name']


    class Meta:
        verbose_name = 'Accounts'
        verbose_name_plural = 'Accounts'


    def __str__(self):
        return self.user_name
