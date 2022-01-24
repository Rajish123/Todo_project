from tkinter.tix import Tree
from django.contrib.auth import forms
from django.core.exceptions import ValidationError
from django.db.models import fields
from .models import *
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(label = "email", widget=forms.EmailInput, required=True)

    # def __init__(self,*args,**kwargs):
    #     super().__init__(*args,**kwargs)
    #     self.fields["username"].widget.attrs.update({
    #         'required' : ' ',
    #         'name': 'username',
    #         'id' : 'username',
    #         'type' : 'text',
    #         'class' : 'form-input',
    #         'placeholder' : 'username'
    #     })

    class Meta:
        model = User
        fields = ('username','email','password1','password2')

    def save(self,commit=Tree):
        user = super(UserRegistrationForm, self).save(commit = False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(max_length=30,required = True, widget=forms.TextInput)
    email = forms.EmailField(required=True, widget=forms.EmailInput)
    
    class Meta:
        model = User
        fields = ['username','email']

class ProfileUpdateForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput)
    
    class Meta:
        model = Profile
        fields = ['avatar']

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = "__all__"
        exclude = ['profile','slug'] 
        
           