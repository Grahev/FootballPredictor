# Generated by Django 3.2.8 on 2021-11-28 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predictor', '0002_auto_20211126_0027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='goalScorers',
            field=models.ManyToManyField(blank=True, null=True, related_name='goal_scorers', to='predictor.Player'),
        ),
    ]
