from django.contrib.auth import forms
from django.core.exceptions import ValidationError
from django.db.models import fields
from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm

class UserRegistrationForm(UserCreationForm):
    email = forms.CharField(label = "Email", widget=forms.EmailInput)

    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = "__all__"
    