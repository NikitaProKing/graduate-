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


class VisitedPage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    page_name = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} visited {self.page_name} at {self.timestamp}"


class Home_Model(models.Model):
    my_file = models.FileField(upload_to='files/')
    my_image = models.ImageField(upload_to='images/')

class Add_a_recipe_Model(models.Model):
    title = models.CharField(max_length=255)
    img = models.ImageField()
    slug = models.SlugField(unique=True, max_length=255)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    author = models.TextField()

    # def get_absolute_url(self):
    #     return reverse('blog_post_detail', args=[self.slug])
    #
    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(self.title)
    #     super(Post, self).save(*args, **kwargs)