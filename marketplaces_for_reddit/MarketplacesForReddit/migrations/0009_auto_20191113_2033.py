# Generated by Django 2.2.5 on 2019-11-13 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MarketplacesForReddit', '0008_auto_20191113_2029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='searchlog',
            name='date',
            field=models.DateField(),
        ),
    ]
