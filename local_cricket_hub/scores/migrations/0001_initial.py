# Generated by Django 5.1.7 on 2025-03-19 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('runs', models.IntegerField(default=0)),
                ('balls', models.IntegerField(default=0)),
                ('strike_rate', models.FloatField(default=0.0)),
            ],
        ),
    ]
