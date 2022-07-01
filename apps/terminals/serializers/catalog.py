from rest_framework import serializers

from apps.terminals.models import CatalogImport
from config.settings.dev import DATETIME_FORMAT
from core.serializer import IntegerArrayField, BaseSerializer


class CatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogImport
        exclude = ["deleted"]
        read_only_fields = ["created_at", "updated_at"]


class CatalogReadonlySerializer(serializers.ModelSerializer):
    email = serializers.CharField(source='user.email')

    class Meta:
        model = CatalogImport
        exclude = ["deleted"]
        read_only_fields = ["created_at", "updated_at"]


class CatalogListInputSerializer(BaseSerializer):
    ids = IntegerArrayField(required=False)
    started_at_from = serializers.DateTimeField(required=False, input_formats=[DATETIME_FORMAT])
    ended_at_to = serializers.DateTimeField(required=False, input_formats=[DATETIME_FORMAT])
    user_id = serializers.UUIDField(required=False)
    status = serializers.CharField(required=False)


class CatalogImportSerializer(BaseSerializer):
    id = serializers.UUIDField()
