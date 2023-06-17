# Generated by Django 4.1.4 on 2023-06-17 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ft', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ft',
            options={'verbose_name_plural': 'fts'},
        ),
        migrations.AddField(
            model_name='ft',
            name='company_name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='ft',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
        migrations.AddField(
            model_name='ft',
            name='seats_available',
            field=models.PositiveIntegerField(default=0),
        ),
    ]