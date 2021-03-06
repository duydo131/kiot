# Generated by Django 3.2.13 on 2022-06-13 17:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('code', models.CharField(max_length=50, unique=True)),
                ('sku', models.CharField(max_length=50)),
                ('price', models.BigIntegerField()),
                ('image', models.CharField(blank=True, max_length=50, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'product',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='Terminal',
            fields=[
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=20, null=True)),
                ('time_open', models.DateTimeField(blank=True, null=True)),
                ('expired_at', models.DateTimeField(blank=True, null=True)),
                ('max_quantity_product', models.IntegerField()),
                ('status', models.BooleanField(default=True)),
                ('image_url', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='terminals', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'terminals',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='WareHouse',
            fields=[
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('quantity', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('product', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='warehouse', to='terminals.product')),
            ],
            options={
                'db_table': 'warehouse',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='TerminalPayment',
            fields=[
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('terminal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_set', to='terminals.terminal')),
                ('transaction', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='terminals', to='transactions.transaction')),
            ],
            options={
                'db_table': 'terminal_payment',
                'ordering': ['created_at'],
            },
        ),
        migrations.AddField(
            model_name='product',
            name='terminal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='terminals.terminal'),
        ),
    ]
