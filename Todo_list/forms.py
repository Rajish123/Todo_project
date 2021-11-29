from django.contrib.auth import forms
from .models import *
from django import forms

class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(label = "Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label = "Repeat Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email','password1','password2']

        def clean_password(self):
            password1 = self.cleaned_data.get('password1')
            password2 = self.cleaned_data.get('password2')
            if password1 and password2 and password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['Password does not match.']
                )
            return password2

        def save(self,commit = True):
            user = super().save(commit = False)
            user.set_password(self.cleaned_data['password1'])
            if commit:
                user.save()
            return user

class LoginForm(forms.Form):
    email = forms.CharField(label="email",widget=forms.EmailInput)
    password = forms.CharField(label = "password", widget=forms.PasswordInput)


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = "__all__"