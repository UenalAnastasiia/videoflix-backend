# Generated by Django 5.0.2 on 2024-04-05 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0007_remove_video_category_video_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='category',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
