# Generated by Django 5.0.1 on 2024-01-27 22:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social_network_app', '0002_rename_author_post_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='user',
            new_name='author',
        ),
    ]
