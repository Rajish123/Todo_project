from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _
# from .forms import UserCreationForm, UserChangeForm
from .models import *


# Register your models here.
admin.site.register(Profile)
admin.site.register(Todo)