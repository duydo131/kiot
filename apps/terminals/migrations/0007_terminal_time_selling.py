# Generated by Django 3.2.13 on 2022-06-16 02:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('terminals', '0006_alter_terminal_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='terminal',
            name='time_selling',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]