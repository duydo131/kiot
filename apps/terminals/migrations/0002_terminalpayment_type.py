# Generated by Django 3.2.13 on 2022-06-14 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('terminals', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='terminalpayment',
            name='type',
            field=models.CharField(choices=[('REGISTER', 'REGISTER'), ('EXTEND', 'EXTEND')], default='REGISTER', max_length=20),
        ),
    ]
