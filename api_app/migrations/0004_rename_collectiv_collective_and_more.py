# Generated by Django 4.2 on 2023-05-12 17:17

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api_app', '0003_post_username'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Collectiv',
            new_name='Collective',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='collectiv',
            new_name='collective',
        ),
    ]
