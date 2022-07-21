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
    revenue = serializers.IntegerField(read_only=True)
    cost = serializers.IntegerField(read_only=True)


class StatisticOrderRequestSerializer(BaseSerializer):
    time_range = serializers.IntegerField(required=False, default=7)  # days


class StatisticOrderSerializer(BaseSerializer):
    name = serializers.CharField(read_only=True)
    total_orders = serializers.ListField(read_only=True)


class StatisticOrderResponseSerializer(BaseSerializer):
    date_of_orders = serializers.ListField(read_only=True)
    terminal_to_list_total_order = StatisticOrderSerializer(read_only=True, many=True)
