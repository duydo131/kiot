from django.contrib.auth.models import AnonymousUser
from rest_framework import serializers
from django.db import transaction as tran

from apps.orders.helper.order import calculate_fee
from apps.orders.models import Order, OrderDetail
from apps.orders.serializers.order_detail import OrderDetailReadOnlySerializer
from apps.terminals.models import Product, WareHouse
from core.serializer import BaseSerializer
from config.settings.dev import PER_CENT_ORDER, CEILING_PRICE


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = ["deleted"]
        read_only_fields = ["created_at", "updated_at"]


class OrderReadOnlySerializer(BaseSerializer):
    id = serializers.UUIDField(read_only=True)
    fid = serializers.CharField(read_only=True)
    user = serializers.UUIDField(read_only=True, source='user.id')
    total_price = serializers.IntegerField(read_only=True)
    transaction = serializers.UUIDField(read_only=True, source='transaction.id')
    type = serializers.CharField(read_only=True)
    details = OrderDetailReadOnlySerializer(read_only=True, many=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)


class OrderProductSerializer(BaseSerializer):
    product_id = serializers.UUIDField(required=True)
    quantity = serializers.IntegerField(required=True)

    def validate(self, data):
        product_id = data['product_id']
        quantity = data['quantity']
        product = Product.objects.get(pk=product_id)
        warehouse = product.warehouse
        if warehouse.quantity < quantity:
            raise serializers.ValidationError(f"Quantity product {product.name} not enough")
        data['product'] = product
        data['warehouse'] = warehouse
        return data


class OrderDetailSerializer(BaseSerializer):
    details = OrderProductSerializer(many=True, required=True)

    def validate(self, data):
        details = data['details']
        if len(details) == 0:
            raise serializers.ValidationError(f"Order must contain product")
        return data

    @tran.atomic
    def create(self, validated_data):
        details = validated_data.get('details')
        request = self.context.get('request')
        seller = request.user
        if seller is None or isinstance(seller, AnonymousUser):
            raise serializers.ValidationError("seller not exists")
        warehouses = []
        order_detail = []
        total_price = 0
        order = Order(user=seller)
        for item in details:
            warehouse = item['warehouse']
            product = item['product']
            quantity = item['quantity']
            if warehouse.quantity < quantity:
                raise serializers.ValidationError(f"Quantity product {product.name} not enough")

            warehouse.quantity = warehouse.quantity - quantity
            warehouses.append(warehouse)

            order_detail.append(OrderDetail(
                product=product,
                sell_price=product.price,
                quantity=quantity,
                order=order,
            ))

            total_price += quantity * product.price

        order.total_price = total_price
        order.fee = calculate_fee(total_price)
        order.save()
        order.refresh_from_db()
        if len(warehouses) > 0:
            WareHouse.objects.bulk_update(warehouses, ['quantity'], batch_size=5)
        if len(order_detail) > 0:
            OrderDetail.objects.bulk_create(order_detail)

        return order


class OrderFeeSerializer(BaseSerializer):
    per_cent_order = serializers.FloatField(read_only=True)
    ceiling_price = serializers.IntegerField(read_only=True)
