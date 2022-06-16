from datetime import timedelta

from django.contrib.auth.models import AnonymousUser
from rest_framework import serializers

from apps.terminals.models import Terminal, TerminalPayment
from apps.terminals.models.terminal_payment import TypeTerminalPayment
from apps.terminals.serializers.terminal_payment import TerminalPaymentSerializer
from apps.transactions.models import Transaction
from config.settings.dev import DATETIME_FORMAT
from core.serializer import IntegerArrayField, BaseSerializer
from django.utils import timezone

from django.db import transaction as tran


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        exclude = ["deleted"]
        read_only_fields = ["created_at", "updated_at"]


class TransactionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        exclude = ["create_by"]

    def validate(self, data):
        request = self.context.get('request')
        user = request.user
        if user is None or isinstance(user, AnonymousUser):
            raise serializers.ValidationError("user not exists")
        data['create_by'] = user
        return data


class PaymentSuccessSerializer(BaseSerializer):
    id = serializers.UUIDField(required=True)


class PaymentFailSerializer(BaseSerializer):
    handler_id = serializers.UUIDField(required=True)
    transaction_type = serializers.CharField(required=True)
