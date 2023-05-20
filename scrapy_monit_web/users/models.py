from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.urls.base import reverse





class ProfileManager(BaseUserManager):

    def create_superuser(self, email, user_name, first_name, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)
        return self.create_user(email, user_name, first_name, password, **kwargs)

    def create_user(self, email, user_name, first_name, password, **kwargs):
        email = self.normalize_email(email)
        user = self.model(email = email, user_name=user_name, first_name=first_name, **kwargs)
        user.set_password(password)
        ## do some validations
        user.save()
        return user



class Profile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    user_name = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    start_date = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default = True)
    is_active = models.BooleanField(default = True)
    objects = ProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', 'first_name']

    objects = ProfileManager()
    
    def get_absolute_url(self):
        return reverse('user', kwargs = {'pk': self.pk})
    
    def __str__(self):
        return f'ScrapyMonitorUser: {self.user_name}'