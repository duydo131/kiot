from __future__ import unicode_literals

from django.db import migrations

from apps.users.models import User


def migrate_account_admin(apps, schema_editor):
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
        return
    user = users.first()
    user.name = 'admin'
    user.save()


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0007_alter_account_admin')
    ]

    operations = [
        migrations.RunPython(migrate_account_admin),
    ]
