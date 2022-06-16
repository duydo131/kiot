from rest_framework import serializers

from rest_framework import serializers

from apps.carts.models import CartProduct
from apps.terminals.models import Product
from apps.terminals.serializers.product import ProductSerializer
from core.serializer import BaseSerializer


class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        exclude = ["deleted"]
        read_only_fields = ["created_at", "updated_at"]


class CartProductReadOnlySerializer(BaseSerializer):
    id = serializers.UUIDField(read_only=True)
    fid = serializers.CharField(read_only=True)
    product = ProductSerializer(read_only=True)
    quantity = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)


class CartProductAdditionalSerializer(BaseSerializer):
    product_id = serializers.UUIDField(required=True)
    quantity = serializers.IntegerField(required=True)

    def validate(self, data):
        product_id = data['product_id']
        data['product'] = Product.objects.get(pk=product_id)
        return data
