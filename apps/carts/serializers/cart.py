from django.db import transaction as tran
from rest_framework import serializers

from apps.carts.models import Cart, CartProduct
from apps.carts.serializers.cart_product import CartProductReadOnlySerializer, CartProductAdditionalSerializer
from apps.terminals.models import Product
from core.serializer import BaseSerializer


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        exclude = ["deleted"]
        read_only_fields = ["created_at", "updated_at"]


class CartReadOnlySerializer(BaseSerializer):
    id = serializers.UUIDField(read_only=True)
    fid = serializers.CharField(read_only=True)
    user = serializers.UUIDField(read_only=True, source='user.id')
    details = CartProductReadOnlySerializer(read_only=True, many=True, source='cart_product')
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)


class CartAdditionalSerializer(BaseSerializer):
    products = CartProductAdditionalSerializer(many=True)

    def validate(self, data):
        cart = self.context.get('cart')
        if cart is None:
            raise serializers.ValidationError("Cart of user not found")
        data['cart'] = cart
        return data

    @tran.atomic
    def create(self, validated_data):
        cart = validated_data['cart']
        products = validated_data.get('products')
        if products is not None:
            new_cart_products = []
            update_cart_products = []
            product_ids = [p.get('product_id') for p in products]
            id_to_cart_products = {p.product_id: p for p in
                                   CartProduct.objects.filter(product_id__in=product_ids, cart_id=cart.id)}
            for p in products:
                exists_product = id_to_cart_products.get(p.get('product_id'))
                if exists_product is None:
                    new_cart_products.append(
                        CartProduct(
                            product=p.get('product'),
                            cart=cart,
                            quantity=p.get('quantity'),
                        )
                    )
                else:
                    exists_product.quantity = p.get('quantity')
                    update_cart_products.append(exists_product)
            if len(new_cart_products) > 0:
                CartProduct.objects.bulk_create(new_cart_products)
            if len(update_cart_products) > 0:
                CartProduct.objects.bulk_update(objs=update_cart_products, fields=['quantity'], batch_size=5)
        cart.refresh_from_db()
        return cart


class CartDeleteProductSerializer(BaseSerializer):
    product_id = serializers.UUIDField(required=True)

    def validate(self, data):
        product_id = data['product_id']
        products = Product.objects.filter(pk=product_id)
        if len(products) == 0:
            raise serializers.ValidationError(f"Product {product_id} not found")

        cart = self.context.get('cart')
        if cart is None:
            raise serializers.ValidationError("Cart of user not found")

        products = cart.cart_product.filter(product_id=product_id)
        if len(products) == 0:
            raise serializers.ValidationError(f"Product {product_id} not in cart of user")

        data['cart'] = cart
        return data

    @tran.atomic
    def create(self, validated_data):
        product_id = validated_data['product_id']
        cart = validated_data['cart']
        cart.cart_product.filter(product_id=product_id).delete()
        cart.refresh_from_db()
        return cart
