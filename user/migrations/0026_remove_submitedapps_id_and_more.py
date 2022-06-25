# Generated by Django 4.0.4 on 2022-05-03 14:41

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0025_alter_education_refphone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submitedapps',
            name='id',
        ),
        migrations.AlterField(
            model_name='submitedapps',
            name='application',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]