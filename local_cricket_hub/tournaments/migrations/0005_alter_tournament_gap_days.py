# Generated by Django 5.1.7 on 2025-03-21 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0004_match_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='gap_days',
            field=models.IntegerField(default=0),
        ),
    ]
