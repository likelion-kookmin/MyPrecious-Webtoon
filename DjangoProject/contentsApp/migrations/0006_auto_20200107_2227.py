# Generated by Django 2.2.7 on 2020-01-07 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contentsApp', '0005_auto_20200107_1325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='webtoon',
            name='tags',
            field=models.ManyToManyField(blank=True, to='contentsApp.Tag'),
        ),
    ]
