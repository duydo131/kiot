from enum import Enum

from django.contrib.auth.models import AnonymousUser
from rest_framework import serializers

from apps.terminals.helper.product import generate_code_for_product
from apps.terminals.models import Product, Terminal, WareHouse
from config.settings.dev import DATETIME_FORMAT
from core.serializer import IntegerArrayField, BaseSerializer
from django.db import transaction as tran


class AddProductType(Enum):
    SINGLE = 'SINGLE'
    WITH_FILE = 'WITH_FILE'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ["deleted"]
        read_only_fields = ["created_at", "updated_at"]


class ProductCreateSerializer(serializers.ModelSerializer):
    terminal_id = serializers.UUIDField(required=True)

    class Meta:
        model = Product
        exclude = ("code", "terminal", )

    def validate(self, data):
        request = self.context.get('request')
        seller = request.user
        if seller is None or isinstance(seller, AnonymousUser):
            raise serializers.ValidationError("seller not exists")
        terminal_id = data.pop('terminal_id')
        terminal = Terminal.objects.get(pk=terminal_id, seller_id=seller.id)

        data['terminal'] = terminal
        price = data.get('price')
        sku = data.get('sku')
        name = data.get('name')

        if price < 0:
            raise serializers.ValidationError("price not negative")

        products = Product.objects.filter(sku=sku, terminal_id=terminal.id)
        if len(products) > 0:
            raise serializers.ValidationError(f"sku {sku} already")

        products = Product.objects.filter(name=name, terminal_id=terminal.id)
        if len(products) > 0:
            raise serializers.ValidationError(f"name {name} already")

        if data.get('is_active') is None:
            data['is_active'] = terminal.status
        data['code'] = generate_code_for_product(data['sku'], terminal.code)
        return data


class ImportProductSerializer(BaseSerializer):
    name = serializers.CharField(required=True)
    sku = serializers.CharField(required=True)
    price = serializers.IntegerField(required=True)
    terminal_code = serializers.UUIDField(required=True)
    quantity = serializers.IntegerField(required=True)

    def validate(self, data):
        terminal_code = data.get('terminal_code')
        terminal = Terminal.objects.get(code=terminal_code)
        data['terminal'] = terminal
        return data


class AddProductSerializer(BaseSerializer):
    name = serializers.CharField(required=False)
    sku = serializers.CharField(required=False)
    price = serializers.IntegerField(required=False)
    image = serializers.CharField(required=False)
    is_active = serializers.BooleanField(required=False)
    terminal_id = serializers.UUIDField(required=True)
    add_type = serializers.ChoiceField(choices=[x.value for x in AddProductType])
    quantity = serializers.IntegerField(required=False)
    link_file = serializers.CharField(required=False)

    def validate(self, data):
        add_type = data.get('add_type')
        price = data.get('price')
        sku = data.get('sku')
        name = data.get('name')
        link_file = data.get('link_file')
        quantity = data.get('quantity')
        if add_type == AddProductType.SINGLE.value and None in [name, sku, price, quantity]:
            raise serializers.ValidationError("name or sku or price required")
        elif add_type == AddProductType.WITH_FILE.value and link_file is None:
            raise serializers.ValidationError("link_file required")

        if quantity is not None and quantity < 0:
            raise serializers.ValidationError("quantity not negative")

        return data

    @tran.atomic
    def create(self, validated_data):
        quantity = validated_data.pop('quantity', None)
        serializer = ProductCreateSerializer(data=validated_data, context=self.context)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        warehouse = WareHouse(product=product, quantity=quantity)
        warehouse.save()

        return product


class AddProductResponseSerializer(BaseSerializer):
    success = serializers.IntegerField()
    error = serializers.IntegerField()


class ProductListInputSerializer(BaseSerializer):
    ids = IntegerArrayField(required=False)
    started_at_from = serializers.DateTimeField(required=False, input_formats=[DATETIME_FORMAT])
    ended_at_to = serializers.DateTimeField(required=False, input_formats=[DATETIME_FORMAT])
    name = serializers.CharField(required=False)
    code = serializers.CharField(required=False)
    sku = serializers.CharField(required=False)
    terminal_id = serializers.UUIDField(required=False)
    min_price = serializers.IntegerField(required=False)
    max_price = serializers.IntegerField(required=False)


class ProductDetailSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(source='warehouse.quantity')

    class Meta:
        model = Product
        exclude = ["deleted"]
        read_only_fields = ["created_at", "updated_at"]
