# Generated by Django 5.0.2 on 2024-03-19 21:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0004_video_categorie'),
    ]

    operations = [
        migrations.RenameField(
            model_name='video',
            old_name='categorie',
            new_name='category',
        ),
    ]