from enum import Enum

from django.contrib.auth.models import AnonymousUser
from rest_framework import serializers

from apps.terminals.helper.product import generate_code_for_product
from apps.terminals.models import Product, Terminal, WareHouse
from config.settings.dev import DATETIME_FORMAT
from core.serializer import IntegerArrayField, BaseSerializer
from django.db import transaction as tran


class CatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ["deleted"]
        read_only_fields = ["created_at", "updated_at"]


class CatalogListInputSerializer(BaseSerializer):
    ids = IntegerArrayField(required=False)
    started_at_from = serializers.DateTimeField(required=False, input_formats=[DATETIME_FORMAT])
    ended_at_to = serializers.DateTimeField(required=False, input_formats=[DATETIME_FORMAT])
    user_id = serializers.UUIDField(required=False)
    status = serializers.CharField(required=False)
