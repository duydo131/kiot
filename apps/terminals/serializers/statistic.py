from rest_framework import serializers

from config.settings.dev import DAYTIME_FORMAT
from core.serializer import BaseSerializer, IntegerArrayField, UUIDArrayField


class StatisticProductRequestSerializer(BaseSerializer):
    ids = UUIDArrayField(required=False)
    started_at_from = serializers.DateTimeField(required=False, input_formats=[DAYTIME_FORMAT])
    ended_at_to = serializers.DateTimeField(required=False, input_formats=[DAYTIME_FORMAT])
    limit = serializers.IntegerField(required=False)


class StatisticProductSerializer(BaseSerializer):
    id = serializers.UUIDField(read_only=True)
    name = serializers.CharField(read_only=True)
    code = serializers.CharField(read_only=True)
    revenue = serializers.IntegerField(read_only=True)
    cost = serializers.IntegerField(read_only=True)
