# Generated by Django 4.0.4 on 2022-05-06 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0033_submited_apps_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submited_apps',
            name='profile',
        ),
        migrations.AddField(
            model_name='submited_apps',
            name='approved',
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
    ]