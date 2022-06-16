from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status, exceptions
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from apps.terminals.helper.product import get_by_product_input
from apps.terminals.models import Product
from apps.terminals.serializers.product import ProductSerializer, ProductListInputSerializer
from apps.transactions.models import Transaction
from apps.transactions.serializers.transaction import TransactionSerializer, TransactionCreateSerializer
from apps.users.serializers import LoginSerializer
from core.base_view import BaseView
from core.mixins import GetSerializerClassMixin
from core.swagger_schemas import ManualParametersAutoSchema



class TransactionViewSet(GetSerializerClassMixin, viewsets.ModelViewSet, BaseView):
    permission_classes = []
    queryset = Transaction.objects.filter()
    queryset_detail = Transaction.objects.filter()
    serializer_class = TransactionSerializer
    serializer_detail_class = TransactionSerializer

    serializer_action_classes = {
        "list": TransactionSerializer,
        "retrieve": TransactionSerializer,
    }

    @swagger_auto_schema(
        operation_description="Create new transaction",
        request_body=TransactionCreateSerializer,
        responses={'201': TransactionSerializer},
    )
    def create(self, request, *args, **kwargs):
        serializer = TransactionCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(data=TransactionSerializer(instance).data)

