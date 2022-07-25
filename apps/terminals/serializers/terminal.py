from datetime import timedelta

from django.contrib.auth.models import AnonymousUser
from rest_framework import serializers

from apps.terminals.models import Terminal, TerminalPayment
from apps.terminals.models.terminal import TerminalStatus
from apps.terminals.models.terminal_payment import TypeTerminalPayment
from apps.transactions.models import Transaction
from config.settings.dev import DATETIME_FORMAT
from core.serializer import IntegerArrayField, BaseSerializer
from django.utils import timezone

from django.db import transaction as tran


class TypeTimeOpen:
    NOW = "NOW"
    AFTER = "AFTER"


class TerminalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Terminal
        exclude = ["deleted"]
        read_only_fields = ["created_at", "updated_at"]


class TerminalReadOnlySerializer(serializers.ModelSerializer):
    total_product = serializers.IntegerField()

    class Meta:
        model = Terminal
        exclude = ["deleted"]
        read_only_fields = ["created_at", "updated_at"]


class TerminalRegisterSerializer(serializers.ModelSerializer):
    time_open = serializers.DateTimeField(input_formats=[DATETIME_FORMAT], required=True)
    type_time_open = serializers.CharField(required=True)

    class Meta:
        model = Terminal
        exclude = ("seller", )

    def validate_name(self, name):
        if Terminal.objects.filter(name=name).count() > 0:
            raise serializers.ValidationError("Terminal name is unique")
        return name

    def validate_code(self, code):
        if Terminal.objects.filter(code=code).count() > 0:
            raise serializers.ValidationError("Terminal code is unique")
        return code

    def validate(self, data):
        type_time_open = data.pop('type_time_open')
        time_open = data.get('time_open')
        time_selling = data.get('time_selling')
        now = timezone.now()
        request = self.context.get('request')
        seller = request.user
        if seller is None or isinstance(seller, AnonymousUser):
            raise serializers.ValidationError("seller not exists")
        if type_time_open == TypeTimeOpen.AFTER and now > time_open:
            raise serializers.ValidationError("Time open terminal must after now")
        if time_selling is None:
            raise serializers.ValidationError("time_selling can not be null")
        if type_time_open == TypeTimeOpen.NOW:
            data['time_open'] = now
        data['time_register'] = data['time_open']
        data['type'] = TerminalStatus.REGISTER
        data['status'] = False
        data['seller'] = seller

        return data


class TerminalExtendSerializer(BaseSerializer):
    terminal_id = serializers.UUIDField(required=True)
    extend_max_quantity_product = serializers.IntegerField(required=False)
    extend_time_selling = serializers.IntegerField(required=False)

    def validate(self, data):
        terminal = Terminal.objects.get(pk=data['terminal_id'])
        extend_max_quantity_product = data.get('extend_max_quantity_product')
        extend_time_selling = data.get('extend_time_selling')
        if extend_max_quantity_product is None and extend_time_selling is None:
            raise serializers.ValidationError("max_quantity_product or end_at must not null")

        if extend_max_quantity_product is not None and extend_max_quantity_product < terminal.max_quantity_product:
            raise serializers.ValidationError("new extend_max_quantity_product less than old max_quantity_product")

        if extend_time_selling is not None and extend_time_selling < 0:
            raise serializers.ValidationError("extend_time_selling less than 0")

        data['terminal'] = terminal
        return data

    def create(self, validated_data):
        terminal = validated_data['terminal']
        extend_max_quantity_product = validated_data.get('extend_max_quantity_product')
        extend_time_selling = validated_data.get('extend_time_selling')
        if extend_max_quantity_product is not None:
            terminal.extend_max_quantity_product = extend_max_quantity_product
        if extend_time_selling is not None:
            terminal.extend_time_selling = extend_time_selling
        terminal.type = TerminalStatus.EXTEND
        terminal.save()
        return terminal


# class TerminalExtendSerializer(TerminalUpdateSerializer):
#     transaction_id = serializers.UUIDField(required=True)
#
#     def validate(self, data):
#         super().validate(data)
#         max_quantity_product = data.get('max_quantity_product')
#         end_at = data.get('end_at')
#         terminal = data['terminal']
#         if max_quantity_product is not None:
#             terminal.max_quantity_product = max_quantity_product
#         if end_at is not None:
#             terminal.expired_at = end_at
#         return data
#
#     @tran.atomic
#     def create(self, validated_data):
#         terminal = validated_data['terminal']
#         terminal.save()
#
#         transaction = Transaction.objects.get(pk=validated_data['transaction_id'])
#         terminal_payment = TerminalPayment(
#             transaction=transaction,
#             terminal=terminal,
#             type=TypeTerminalPayment.EXTEND,
#         )
#         terminal_payment.save()
#         return terminal


class TerminalListInputSerializer(BaseSerializer):
    ids = IntegerArrayField(required=False)
    is_expired = serializers.BooleanField(required=False)
    status = serializers.BooleanField(required=False)
    page = serializers.IntegerField(required=False)
    page_size = serializers.IntegerField(required=False)
    name = serializers.CharField(required=False)
    code = serializers.CharField(required=False)


class TerminalPriceSerializer(BaseSerializer):
    total_price = serializers.IntegerField(read_only=True)
    terminal = TerminalSerializer(read_only=True)
