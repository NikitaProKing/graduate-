from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Add_a_recipe_Model




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

    class Meta:
        model = User
        fields = ['username', 'last_name', 'email', 'password1', 'password2']



class Add_a_recipe_Form(forms.ModelForm):
    class Meta:
        model = Add_a_recipe_Model
        fields = '__all__'