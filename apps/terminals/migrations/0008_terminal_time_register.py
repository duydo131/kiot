# Generated by Django 3.2.13 on 2022-06-16 03:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('terminals', '0007_terminal_time_selling'),
    ]

    operations = [
        migrations.AddField(
            model_name='terminal',
            name='time_register',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
