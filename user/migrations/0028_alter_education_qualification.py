# Generated by Django 4.0.4 on 2022-05-03 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0027_alter_bankdetails_account'),
    ]

    operations = [
        migrations.AlterField(
            model_name='education',
            name='qualification',
            field=models.CharField(choices=[('Tertiary Institution', 'Tertiary Institution'), ('Secondary School', 'Secondary School')], default=None, max_length=60, null=True),
        ),
    ]
