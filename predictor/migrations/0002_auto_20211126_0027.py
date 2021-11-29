# Generated by Django 3.2.8 on 2021-11-26 00:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predictor', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='goalScorers',
        ),
        migrations.AddField(
            model_name='match',
            name='goalScorers',
            field=models.ManyToManyField(related_name='goal_scorers', to='predictor.Player'),
        ),
    ]
