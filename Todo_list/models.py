from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver

from Todo_project.util import unique_slug_generator
# from .managers import UserManager

# Create your models here.

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


# Extending the base class that Django has for User models.
class User(AbstractUser):
    # Removing the username field
    username = None

    # Making the email field required and unique.
    email = models.EmailField(_('email address'), unique=True)
    avatar = models.ImageField(default = 'default.jpg',upload_to = 'profile')

    # Telling Django that you are going to use the email field
    # as the USERNAME_FIELD
    USERNAME_FIELD = 'email'
    # Removing the email field from the REQUIRED_FIELDS settings
    # (it is automatically included as USERNAME_FIELD)
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

class Todo(models.Model):
    # choices:(actual name to store in model,name to show to user)
    PRIORITY_CHOICES = (
        ('Critical','Critical'),
        ('High','High'),
        ('Low','Low')
    )
    COMPLETED = (
        ('Accomplished','Accomplished'),
        ('Unaccomplished','Unaccomplished')
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank = False, null = False)
    priority = models.CharField(max_length = 30, choices=PRIORITY_CHOICES,default="High")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    completed = models.CharField(max_length=30, choices=COMPLETED,default='Unaccomplished')
    notify = models.BooleanField(default = False)
    slug = models.SlugField(max_length=250,null = True, blank=True)

    class Meta:
        ordering = ('-created_at', )

    def user(self):
        return self.user

    def priority(self):
        return self.priority

    def is_completed(self):
        return self.completed == "Accomplished"

    def __str__(self):
        return self.title

@receiver(pre_save,sender = Todo)
def pre_save_receiver(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)