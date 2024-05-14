from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Good



class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'input100',
                'placeholder': 'Email'
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'input100',
                'placeholder': 'Password'
            }
        )
    )

class RegForm(UserCreationForm):
    email = forms.EmailField()
    password = forms.CharField(max_length=16)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class SampleModelForm(ModelForm):
    class Meta:
        model = Good
        fields='__all__'

