from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.response import Response

from apps.transactions.models import Transaction
from apps.transactions.serializers.transaction import TransactionSerializer, \
    PaymentSuccessSerializer, PaymentSuccessSerializer, PaymentFailSerializer
from core.base_view import BaseView
from core.mixins import GetSerializerClassMixin
from apps.transactions.task import handler_success, handler_fail
from rest_framework.decorators import action

from core.permissions import IsUser, IsManager


class PaymentViewSet(GetSerializerClassMixin, viewsets.ModelViewSet, BaseView):
    permission_classes = []
    queryset = Transaction.objects.filter()
    queryset_detail = Transaction.objects.filter()
    serializer_class = TransactionSerializer
    serializer_detail_class = TransactionSerializer
    http_method_names = ['post']
    filterset_class = None

    serializer_action_classes = {
        "list": TransactionSerializer,
        "retrieve": TransactionSerializer,
    }

    @swagger_auto_schema(
        operation_description="Webhook call when success payment",
        request_body=PaymentSuccessSerializer,
        responses={'201': TransactionSerializer},
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="success",
        url_name="success",
        filterset_class=None,
        permission_classes=[IsUser | IsManager],
        pagination_class=None,
    )
    def success(self, request, *args, **kwargs):
        serializer = PaymentSuccessSerializer(data=request.data)
        serializer.is_valid()
        validate_data = serializer.validated_data
        transaction = Transaction.objects.get(pk=validate_data.get('id'))
        # handler_success.delay(transaction)
        handler_success(transaction=transaction, user=request.user)
        return Response(data=TransactionSerializer(transaction).data)

    @swagger_auto_schema(
        operation_description="Webhook call when success payment",
        request_body=PaymentFailSerializer,
        responses={'201': TransactionSerializer},
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="fail",
        url_name="fail",
        filterset_class=None,
        permission_classes=[IsUser | IsManager],
        pagination_class=None,
    )
    def fail(self, request, *args, **kwargs):
        serializer = PaymentFailSerializer(data=request.data)
        serializer.is_valid()
        validate_data = serializer.validated_data
        # handler_success.delay(transaction)
        handler_fail(
            transaction_type=validate_data.get('transaction_type'),
            handler_id=validate_data.get('handler_id'),
            user=request.user
        )
        return Response(data="OK")
