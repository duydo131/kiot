# Generated by Django 3.2.13 on 2022-06-16 15:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('terminals', '0011_alter_terminal_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='CatalogImport',
            fields=[
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('source_file', models.CharField(max_length=256)),
                ('result_file', models.CharField(blank=True, max_length=256, null=True)),
                ('status', models.CharField(choices=[('UPLOAD', 'UPLOAD'), ('PROCESS', 'PROCESS'), ('SUCCESS', 'SUCCESS'), ('FAIL', 'FAIL')], default='UPLOAD', max_length=10)),
                ('quantity_product', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imports', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'catalog_import',
                'ordering': ['created_at'],
            },
        ),
    ]
