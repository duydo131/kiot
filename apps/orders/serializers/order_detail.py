from rest_framework import serializers

from apps.orders.models import OrderDetail
from apps.terminals.serializers.product import ProductSerializer
from core.serializer import BaseSerializer


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        exclude = ["deleted"]
        read_only_fields = ["created_at", "updated_at"]


class OrderDetailReadOnlySerializer(BaseSerializer):
    id = serializers.UUIDField(read_only=True)
    fid = serializers.CharField(read_only=True)
    quantity = serializers.IntegerField(read_only=True)
    sell_price = serializers.IntegerField(read_only=True)
    product = ProductSerializer(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
