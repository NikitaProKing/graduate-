from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import Add_a_recipe_Model, CommentModel, Detail


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


def validate_image_size(image):
    max_size = 5 * 1024 * 1024  # 5MB
    if image.size > max_size:
        raise ValidationError(f'Размер файла не должен превышать {max_size // (1024 * 1024)}MB.')

class Add_a_recipe_Form(forms.ModelForm):
    class Meta:
        model = Add_a_recipe_Model
        fields = '__all__'
        exclude = ['author']


class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentModel
        fields = ['text']


class DetailForm(forms.ModelForm):
    class Meta:
        model = Detail
        fields = ['photo', 'text']

        def clean_image(self):
            image = self.cleaned_data.get('photo')
            validate_image_size(image)
            return image


class EditRecipesForm(forms.ModelForm):
    class Meta:
        model = Add_a_recipe_Model
        fields = '__all__'
