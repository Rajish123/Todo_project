from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver


from Todo_project.util import unique_slug_generator

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # email = models.EmailField(null=False, blank = False, unique=True)
    avatar = models.ImageField(default = "default.jpg",upload_to ="profile")

    def __str__(self):
        return f"{self.user.username} profile"

# whenever user instances are created,automatically profile model are created
@receiver(post_save, sender = User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user = instance)

@receiver(post_save, sender=User)
def save_user_profile(sender,instance, **kwargs):
    instance.profile.save()


class Todo(models.Model):
    # choices:(actual name to store in model,name to show to user)

    COMPLETED = (
        ('Accomplished','Accomplished'),
        ('Unaccomplished','Unaccomplished'),
    )
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank = False, null = False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    completed = models.CharField(max_length=30, choices=COMPLETED,default='Unaccomplished')
    notify = models.BooleanField(default = False)
    slug = models.SlugField(max_length=250,null = True, blank=True)

    class Meta:
        ordering = ('-created_at', )

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