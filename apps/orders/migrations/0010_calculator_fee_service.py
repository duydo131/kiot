from __future__ import unicode_literals

from django.db import migrations
from django.db.models import Sum, F
from django.db.models.functions import Coalesce

from apps.orders.helper.order import calculate_fee
from apps.orders.models import Order
from apps.orders.models.order import OrderType


def migrate_calculator_fee_service(apps, schema_editor):
    """migrate_calculator_fee_service"""
    orders = Order.objects.filter(type=OrderType.PAID, fee=0)\
        .annotate(total_amount=Coalesce(Sum(F('details__sell_price') * F('details__quantity')), 0))
    update_orders = []
    for order in orders:
        order.total_price = order.total_amount
        order.fee = calculate_fee(order.total_amount)
        update_orders.append(order)

    Order.objects.bulk_update(update_orders, fields=['total_price', 'fee'])


class Migration(migrations.Migration):
    dependencies = [
        ('orders', '0009_alter_order_fee')
    ]

    operations = [
        migrations.RunPython(migrate_calculator_fee_service),
    ]
