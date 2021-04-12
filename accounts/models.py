import uuid
from datetime import datetime, timedelta

import jwt
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models

# Create your models here.
from rest_framework_jwt.settings import api_settings

from marian import settings


class UserManager(BaseUserManager):
    def create_user(self, username, email, first_name, phone_number, last_name=None, password=None):
        user = self.model(username=username, email=self.normalize_email(email), first_name=first_name,
                          last_name=last_name, phone_number=phone_number)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, first_name, phone_number, password, last_name=None):
        if password is None:
            raise TypeError("Superuser must have a password!")
        user = self.create_user(username, email, first_name=first_name,
                                phone_number=phone_number, last_name=last_name, password=password)
        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=255, unique=True, blank=False, null=False)
    first_name = models.CharField(max_length=255, blank=False, null=False)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True, blank=False, null=False)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Enter phone number in format: '+999999999'. "
                                                                   "Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone_number', 'email', 'first_name']

    objects = UserManager()

    @property
    def token(self):
        return self.get_token()

    def get_token(self):
        payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = payload_handler(self)
        return encode_handler(payload)

    def get_full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def get_short_name(self):
        return self.first_name

    # This is not been used, is an earlier implementation
    def _generate_jwt_token(self):
        date = datetime.now() + timedelta(days=15)
        token = jwt.encode({
            "id": str(self.pk),
            "exp": int(date.strftime('%d%m%y%H%M%S'))
        }, settings.SECRET_KEY, algorithm='HS256')
        return token.encode('utf-8')
