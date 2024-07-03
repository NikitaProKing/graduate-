# Generated by Django 5.0.6 on 2024-07-02 02:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0020_delete_adddetail'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='editrecipesmodel',
            name='edit',
        ),
        migrations.CreateModel(
            name='Detail_Model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='images/', verbose_name='Изображение')),
                ('text', models.TextField(verbose_name='Описание')),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Detail',
        ),
        migrations.DeleteModel(
            name='EditRecipesModel',
        ),
    ]