# Generated by Django 5.0.2 on 2024-04-02 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_rename_adress_customuser_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_email_verified',
            field=models.BooleanField(default=False),
        ),
    ]