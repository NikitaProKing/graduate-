from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MaxLengthValidator
from django.forms import forms


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    email = models.EmailField()
    password = models.CharField(max_length=16)

class News(models.Model):
    def clean_name(self):
        name = self.cleaned_data['name']
        if not name:
            raise forms.ValidationError('Поле не должно быть пустым.')
        return name
    name = models.CharField('Name:', max_length=30)
    category = models.CharField('Category:', max_length=50)
    full_text = models.TextField('Publication:', max_length=200)
    date = models.DateTimeField('Publication date:', validators=[clean_name])
    slug = models.SlugField(null=False, unique=True)

class Good(models.Model):
    name = models.CharField('Имя', max_length=20, validators=[MaxLengthValidator(10)])
    anons = models.CharField('фамилия', max_length=250)
    date = models.DateTimeField('Дата публикации')
    slug = models.SlugField(unique=True, max_length=100, blank=True, null=False)

class VisitedPage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    page_name = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} visited {self.page_name} at {self.timestamp}"