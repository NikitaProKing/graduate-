from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.Form):
    useremail = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class RegForm(UserCreationForm):
    email = forms.EmailField()
    password = forms.CharField(max_length=16)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']