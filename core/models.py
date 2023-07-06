from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from .manager import MyAccountManager



class Role(models.Model):
    name = models.CharField('Name', max_length=255)
    description = models.TextField('Description')

    def __str__(self):
        return self.name


class Permission(models.Model):
    name = models.CharField('Name', max_length=255)
    codename = models.CharField('Codename', max_length=100, unique=True)
    description = models.TextField('Description')

    def __str__(self):
        return self.name

class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('Email Address', max_length=60, unique=True)
    first_name = models.CharField('First Name', max_length=255)
    last_name = models.CharField('Last Name', max_length=255)
    date_joined = models.DateTimeField('Date Joined', auto_now_add=True)
    is_active = models.BooleanField('Active', default=True)    
    roles = models.ManyToManyField(Role, blank=True)
    permissions = models.ManyToManyField(Permission, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name


class AccountProfile(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField('Profile Avatar', upload_to='profile_avatars/')
    newsletter = models.BooleanField('Email Subscription for Site News', default=True)
    account_notes = models.TextField('Admin Notes on User', null=True, blank=True)

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f"{self.account.first_name} {self.account.last_name}"

    def get_first_name(self):
        return self.account.first_name

    def get_last_name(self):
        return self.account.last_name