# Generated by Django 2.2.7 on 2020-01-04 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accountApp', '0003_auto_20191228_1502'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='age_range',
            field=models.CharField(blank=True, choices=[(10, '10'), (20, '20'), (30, '30'), (40, '40'), (50, '50'), (60, '60')], max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=1, null=True),
        ),
    ]