# Generated by Django 4.0.4 on 2022-05-06 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0034_remove_submited_apps_profile_submited_apps_approved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submited_apps',
            name='approved',
            field=models.BooleanField(default=0),
        ),
    ]
