# Generated by Django 4.1.4 on 2023-06-17 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ft',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_journey', models.DateField()),
                ('source', models.CharField(max_length=100)),
                ('destination', models.CharField(max_length=100)),
            ],
        ),
    ]