# Generated by Django 4.0.4 on 2022-05-02 21:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user', '0019_remove_profile_appstatus'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank', models.CharField(blank=True, choices=[('UBA', 'UBA')], max_length=6, null=True)),
                ('account', models.CharField(blank=True, max_length=16, null=True)),
                ('name', models.CharField(blank=True, max_length=60, null=True)),
                ('branch', models.CharField(blank=True, max_length=60, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('applicant', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]