# Generated by Django 4.0.4 on 2022-05-02 23:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0020_bankdetails'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubmitedApps',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('application', models.CharField(max_length=255, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('applicant', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
