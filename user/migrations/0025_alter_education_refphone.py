# Generated by Django 4.0.4 on 2022-05-03 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0024_rename_submited_submitedapps_confirm'),
    ]

    operations = [
        migrations.AlterField(
            model_name='education',
            name='refphone',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
