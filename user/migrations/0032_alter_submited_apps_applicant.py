# Generated by Django 4.0.4 on 2022-05-06 10:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0031_alter_education_applicant_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submited_apps',
            name='applicant',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
