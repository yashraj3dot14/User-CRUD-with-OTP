from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager, PermissionsMixin
# Create your models here.

class CustomAccountManager(BaseUserManager):

    def create_superuser(self, username, email, first_name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_superuser', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned is_staff=True')

        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned is_superuser=True')

        return self.create_superuser(username, email, first_name, password, **other_fields)

    def create_user(self, username, email, first_name, password, **other_fields):

        if not username:
            raise ValueError('You must have to provide username')

        if not email:
            raise ValueError('You must have to provide email')

        if not other_fields.get('mobile'):
            raise ValueError('You must have to provide Mobile')

        email = self.normalize_email(email)
        user = self.model(username= username, email= email, first_name= first_name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class MyCustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length= 20, unique= True)
    email = models.EmailField(_('Email address'), unique= True)
    first_name = models.CharField(max_length= 100)
    last_name = models.CharField(max_length= 100)
    mobile = models.CharField(max_length= 12)
    sec_email = models.EmailField(_('Secondary Email'), unique= True)
    start_date =models.DateTimeField(default= timezone.now())
    is_staff =models.BooleanField(default= False)
    is_active = models.BooleanField(default= False)


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name','mobile','sec_email']
    objects = CustomAccountManager()

    def __str__(self):
        return self.email


class PhoneOTP(models.Model):
    phone_regex = RegexValidator( regex   =r'^\+?1?\d{9,14}$', message ="Phone number must be entered in the format: '+999999999'. Up to 14 digits allowed.")
    phone       = models.CharField(validators=[phone_regex], max_length=17, unique=True)
    otp         = models.CharField(max_length = 9, blank = True, null= True)
    count       = models.IntegerField(default = 0, help_text = 'Number of otp sent')
    logged      = models.BooleanField(default = False, help_text = 'If otp verification got successful')
    forgot      = models.BooleanField(default = False, help_text = 'only true for forgot password')
    forgot_logged = models.BooleanField(default = False, help_text = 'Only true if validdate otp forgot get successful')


    def __str__(self):
        return str(self.phone) + ' is sent ' + str(self.otp)