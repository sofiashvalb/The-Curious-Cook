# Generated by Django 4.2.11 on 2025-02-06 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cookbook', '0009_sessionlike_card_session_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='like_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
