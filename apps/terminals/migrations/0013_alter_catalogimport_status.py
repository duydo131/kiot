# Generated by Django 3.2.13 on 2022-06-16 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('terminals', '0012_catalogimport'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catalogimport',
            name='status',
            field=models.CharField(choices=[('UPLOAD', 'UPLOAD'), ('VALIDATE', 'VALIDATE'), ('PROCESS', 'PROCESS'), ('SUCCESS', 'SUCCESS'), ('FAIL', 'FAIL')], default='UPLOAD', max_length=10),
        ),
    ]
