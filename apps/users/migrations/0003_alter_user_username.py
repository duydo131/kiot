# Generated by Django 3.2.13 on 2022-06-16 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_is_staff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(default='abc', max_length=100, unique=True),
            preserve_default=False,
        ),
    ]