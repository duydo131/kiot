# Generated by Django 3.2.13 on 2022-06-15 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0005_alter_transaction_handler_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='handler_id',
            field=models.UUIDField(),
        ),
    ]
