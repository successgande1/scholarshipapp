# Generated by Django 4.0.4 on 2022-05-02 16:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0018_remove_profile_profilestatus'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='appstatus',
        ),
    ]
