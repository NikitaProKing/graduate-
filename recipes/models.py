from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MaxLengthValidator
from django.forms import forms
from django.template.defaultfilters import slugify
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    email = models.EmailField()
    password = models.CharField(max_length=16)


class VisitedPage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    page_name = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} visited {self.page_name} at {self.timestamp}"


class Categories(models.Model):
    name = models.CharField('Категория', max_length=50)

    def __str__(self):
        return self.name


class Home_Model(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def str(self):
        return self.title

class Add_a_recipe_Model(models.Model):
    title = models.CharField('Название', max_length=255)
    img = models.ImageField('Изображение')
    slug = models.SlugField(unique=True, max_length=255)
    content = models.TextField('Описание')
    created_on = models.DateTimeField('Дата', auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.ForeignKey(Categories, on_delete=models.CASCADE)
    is_published = models.BooleanField(default=False)


    def __str__(self):
        return self.title


class Detail(models.Model):
    photo = models.ImageField('Изображение', upload_to='images/')
    text = models.TextField('Описание')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def str(self):
        return self.title



class CommentModel(models.Model):
    post = models.ForeignKey(Add_a_recipe_Model, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'

class EditRecipesModel(models.Model):
    edit = models.ForeignKey(Add_a_recipe_Model, on_delete=models.CASCADE)

