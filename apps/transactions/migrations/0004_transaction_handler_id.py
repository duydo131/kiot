# Generated by Django 3.2.13 on 2022-06-15 16:40

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0003_auto_20220615_2333'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='handler_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
