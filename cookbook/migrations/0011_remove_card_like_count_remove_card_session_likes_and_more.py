# Generated by Django 4.2.11 on 2025-02-06 21:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cookbook', '0010_card_like_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='like_count',
        ),
        migrations.RemoveField(
            model_name='card',
            name='session_likes',
        ),
        migrations.DeleteModel(
            name='SessionLike',
        ),
    ]
