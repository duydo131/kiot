from __future__ import unicode_literals

from django.db import migrations

from apps.users.models import User


def migrate_name_from_username(apps, schema_editor):
    users_not_name = User.objects.filter(name__isnull=True, username__isnull=False)
    users_update = []
    for user in users_not_name:
        user.name = user.username
        users_update.append(user)

    User.objects.bulk_update(users_update, ['name'])


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0004_alter_user_options')
    ]

    operations = [
        migrations.RunPython(migrate_name_from_username),
    ]
