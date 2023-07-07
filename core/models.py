from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from .manager import MyAccountManager
from .fields import EncryptedCharField

SUPPORTED_LANGUAGES = [
    ('en', 'English'),
    # TODO: Add in more supported languages once we have a bases for english created.
]

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
    
class SiteConfiguration(models.Model):
    site_name = models.CharField(max_length=255, default="PandaCMS")
    site_slogan = models.CharField(max_length=255, default="A Panda in Every CMS!")
    site_logo = models.ImageField(upload_to='site/')
    favicon = models.ImageField(upload_to='site/')
    default_language = models.CharField(max_length=50, choices=SUPPORTED_LANGUAGES, default='en')

    # Email Site Settings
    smtp_host_user = EncryptedCharField(max_length=255, null=True, blank=True)
    smtp_host_password = EncryptedCharField(max_length=255, null=True, blank=True)

    # Set up email notifications for staff.
    email_notifications = models.ManyToManyField(Account, blank=True)

    def save(self, *args, **kwargs):
        # Encrypt the SMTP host user and password
        if self.smtp_host_user:
            self.smtp_host_user = EncryptedCharField.encrypt(self.smtp_host_user)
        if self.smtp_host_password:
            self.smtp_host_password = EncryptedCharField.encrypt(self.smtp_host_password)
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.site_name
    
    def get_favicon(self):
        return self.favicon
    
    def get_slogan(self):
        return self.site_slogan
    
    def get_name(self):
        return self.site_name

class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    width = models.IntegerField()
    height = models.IntegerField()
    size = models.PositiveIntegerField()
    uploaded_by = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
class Video(models.Model):
    video = models.FileField(upload_to='videos/')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    resolution_width = models.IntegerField()
    resolution_height = models.IntegerField()
    size = models.PositiveIntegerField()
    uploaded_by = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
class Audio(models.Model):
    audio = models.FileField(upload_to='audio/')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    quality = models.CharField(max_length=100)
    uploaded_by = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
class Document(models.Model):
    document = models.FileField(upload_to='documents/')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    size = models.PositiveIntegerField()
    uploaded_by = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
