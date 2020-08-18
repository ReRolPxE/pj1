from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password, **extra_fields):
        """
        Creates and saves a staff user with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        return self.create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)
    
class User(AbstractBaseUser, PermissionsMixin):
    """Custom for User Model"""
    objects = CustomUserManager()
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
        
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    # notice the absence of a "Password field", that is built in.

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Email & Password are required by default.

    def __str__(self):              # __unicode__ on Python 2
        return self.email

class Form(models.Model):
    '''  dsfas '''
    # Fields
    title = models.CharField(max_length=200)
    recipient = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name='recipient_form')
    sender = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name='sender_form')
    created_at = models.DateField(null=True, blank=True)
    division = models.ForeignKey('Division', on_delete=models.SET_NULL, null=True)
    content = models.TextField(max_length=1000)
    compensation_from = models.DateField(null=False)
    compensation_to = models.DateField(null=False)
    leave_from = models.DateField(null=False)
    leave_to = models.DateField(null=False)
    checkin_time = models.DateField(null=False)
    checkout_time = models.DateField(null=False) 
    
    FORM_TYPE = (
        ('rp', 'Report'),
        ('le', 'Leave Early'),
        ('lo', 'Leave Out'),
        ('il', 'In Late'),
    )

    form_type = models.CharField(
        max_length=2,
        choices=FORM_TYPE,
        blank=True,
        default='rp',
        help_text='Form type',
    )

    FORM_STATUS = (
        ('a', 'Approved'),
        ('c', 'Canceled'),
        ('f', 'Forwarded'),
        ('p', 'Pending'),
        ('r', 'Rejected'),
    )

    status = models.CharField(
        max_length=1,
        choices=FORM_STATUS,
        blank=True,
        default='p',
        help_text='Form status',
    )
    # Methods
    def get_absolute_url(self):
        """Returns the url to access a particular instance of MyModelName."""
        return reverse('form', args=[str(self.id)])
    
    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.title
    
    # def display_genre(self):
    #     """Create a string for the Genre. This is required to display genre in Admin."""
    #     return ', '.join(genre.name for genre in self.genre.all()[:3])
    
    # display_genre.short_description = 'Genre'

class Notification(models.Model):
    """ Notification """
    # Fields
    created_at = models.DateField(null=True, blank=True)
    recipient = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name='recipient')
    sender = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name='sender')
    is_read = models.BooleanField(default=False)
    form_id = models.ForeignKey('Form', on_delete=models.SET_NULL, null=True)
    type_notification = models.CharField(max_length=50)
    content = models.CharField(max_length=50)
    class Meta:
        ordering = ['created_at']
        
    # Methods
    def get_absolute_url(self):
        return reverse('notification', args=[str(self.id)])
    
    def __str__(self):
        return self.content

class Skill(models.Model):
    """ Model of Genre """
    # Fields
    name = models.TextField(max_length=50, help_text='Enter a skill (e.g. Python)')
    # Methods
    def __str__(self):
        return self.name

class Position(models.Model):
    """Position"""
    name = models.TextField(max_length=50, help_text='Enter your position (e.g. Deverloper)')
    # Method
    def __str__(self):
        return self.name

class Division(models.Model):
    """Division"""
    name = models.TextField(max_length=50, help_text='Enter your division (e.g. Education Team)')
    manage_id = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    parent_id = models.ForeignKey('Division', on_delete=models.SET_NULL, null=True)
    # Method
    def __str__(self):
        return self.name

class TimeKeeping(models.Model):
    """Model Timekeeping"""
    user_id = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    checkin_time = models.DateField(null=True, blank=True)
    checkout_time = models.DateField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)
