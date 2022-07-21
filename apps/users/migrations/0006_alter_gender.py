from __future__ import unicode_literals

from django.db import migrations

from apps.users.models import User
from apps.users.models.user import UserGender


def migrate_gender(apps, schema_editor):
    """apply is male for user is unknown gender at the moment"""
    users_not_gender = User.objects.filter(gender=UserGender.UNKNOWN.value)
    users_update = []
    for user in users_not_gender:
        user.gender = UserGender.MALE.value
        users_update.append(user)

    User.objects.bulk_update(users_update, ['gender'])


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0005_alter_name')
    ]

    operations = [
        migrations.RunPython(migrate_gender),
    ]
