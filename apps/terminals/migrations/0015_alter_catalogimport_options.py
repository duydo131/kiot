# Generated by Django 3.2.13 on 2022-06-18 10:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('terminals', '0014_alter_catalogimport_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='catalogimport',
            options={'ordering': ['-created_at']},
        ),
    ]