# Generated by Django 3.2.13 on 2022-06-18 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('terminals', '0013_alter_catalogimport_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catalogimport',
            name='status',
            field=models.CharField(choices=[('UPLOAD', 'UPLOAD'), ('EXTRACT', 'EXTRACT'), ('PROCESS', 'PROCESS'), ('SUCCESS', 'SUCCESS'), ('FAIL', 'FAIL')], default='UPLOAD', max_length=10),
        ),
    ]