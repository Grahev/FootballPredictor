# Generated by Django 3.2.8 on 2021-10-31 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predictor', '0002_auto_20211031_2338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='matchday',
            field=models.CharField(max_length=50),
        ),
    ]
