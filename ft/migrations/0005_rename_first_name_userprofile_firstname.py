# Generated by Django 4.1.4 on 2023-06-18 05:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ft', '0004_userprofile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='first_name',
            new_name='Firstname',
        ),
    ]
