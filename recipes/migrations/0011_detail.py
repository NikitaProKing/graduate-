# Generated by Django 5.0.6 on 2024-05-30 14:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0010_rename_content_commentmodel_text'),
    ]

    operations = [
        migrations.CreateModel(
            name='Detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.add_a_recipe_model')),
            ],
        ),
    ]
