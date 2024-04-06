# Generated by Django 5.0.2 on 2024-04-05 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0001_initial'),
        ('video', '0005_rename_categorie_video_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='category',
        ),
        migrations.AddField(
            model_name='video',
            name='category',
            field=models.ManyToManyField(null=True, to='category.category'),
        ),
    ]
