from __future__ import unicode_literals

from django.db import migrations

from apps.users.models import User


def migrate_gender(apps, schema_editor):
    """create super user"""
    user_admin = 'admin'
    users = User.objects.filter(
        is_superuser=True,
        is_staff=True,
        is_active=True,
        username=user_admin,
        role='ADMIN'
    )
    if len(users) == 0:
        User.objects.create_superuser(username=user_admin, password=user_admin)


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0006_alter_gender')
    ]

    operations = [
        migrations.RunPython(migrate_gender),
    ]
