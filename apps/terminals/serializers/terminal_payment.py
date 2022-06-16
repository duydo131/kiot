from rest_framework import serializers

from apps.terminals.models import TerminalPayment


class TerminalPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TerminalPayment
        exclude = ["deleted"]
        read_only_fields = ["created_at", "updated_at"]
