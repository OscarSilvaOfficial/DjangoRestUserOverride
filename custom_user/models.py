import re
from django.db import models
from django.core import validators
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.models import UserManager
from django.apps import apps
from django.contrib.auth.hashers import make_password
class UserManager(BaseUserManager):
    
  def _create_user(self, username, email, password, **extra_fields):

        if not username:
            raise ValueError('The given username must be set')
          
        email = self.normalize_email(email)
        GlobalUserModel = apps.get_model(self.model._meta.app_label, self.model._meta.object_name)
        username = GlobalUserModel.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        
        return user
    
  def create_user(self, username, email=None, password=None, **extra_fields):
    return self._create_user(username, email, password, False, False,**extra_fields)
  
  def create_superuser(self, username, email, password, **extra_fields):
    user = self._create_user(
      username, email, password, True, True,
      **extra_fields
    )
    user.is_active=True
    user.save(using=self._db)
    return user
  
class User(AbstractBaseUser, PermissionsMixin):
  username = models.CharField(
    _('username'), max_length=15, unique=True,
    
    help_text=_(
      'Required. 15 characters or fewer. Letters, \
      numbers and @/./+/-/_ characters'
    ),
    
    validators=[
      validators.RegexValidator(
        re.compile('^[\w.@+-]+$'),
        _('Enter a valid username.'),
        _('invalid')
      )
    ]
  )
  
  is_staff = models.BooleanField(
    _('staff status'), default=False,
    help_text=_('Designates whether the user can log into this admin site.')
  )
  
  is_active = models.BooleanField(
    _('active'), default=True,
    help_text=_('Designates whether this user should be treated as active. \
    Unselect this instead of deleting accounts.')
  )
  
  is_trusty = models.BooleanField(
    _('trusty'), default=False,
    help_text=_('Designates whether this user has confirmed his account.')
  )
  
  first_name = models.CharField(_('first name'), max_length=30)
  last_name = models.CharField(_('last name'), max_length=30)
  email = models.EmailField(_('email address'), max_length=255, unique=True)
  date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
  
  objects = UserManager()
  
  class Meta:
    verbose_name = _('user')
    verbose_name_plural = _('users')
    
