from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.orders.models import Order
from apps.orders.serializers.order import OrderSerializer, OrderFeeSerializer, OrderDetailSerializer, \
    OrderReadOnlySerializer
from config.settings.dev import PER_CENT_ORDER, CEILING_PRICE
from core.base_view import BaseView
from core.mixins import GetSerializerClassMixin
from core.permissions import IsUser


class OrderViewSet(GetSerializerClassMixin, viewsets.ModelViewSet, BaseView):
    permission_classes = []
    queryset = Order.objects.filter()
    queryset_detail = Order.objects.filter()
    serializer_class = OrderSerializer
    serializer_detail_class = OrderSerializer
    filterset_class = None

    serializer_action_classes = {
        "list": OrderSerializer,
        "retrieve": OrderSerializer,
    }

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(user_id=user.id)

    @swagger_auto_schema(
        operation_description="Create new terminal",
        request_body=OrderDetailSerializer,
        responses={'201': OrderSerializer},
        permission_classes=[IsUser]
    )
    def create(self, request, *args, **kwargs):
        serializer = OrderDetailSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(data=OrderSerializer(instance).data)

    @action(
        methods=["GET"],
        detail=False,
        url_path="fee",
        url_name="fee",
        filterset_class=None,
        permission_classes=[],
        pagination_class=None,
    )
    def fee(self, request, *args, **kwargs):
        fee = {
            'per_cent_order': PER_CENT_ORDER,
            'ceiling_price': CEILING_PRICE,
        }
        return Response(data=OrderFeeSerializer(fee).data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        order = Order.objects.prefetch_related('details', 'details__product').get(pk=pk)
        return Response(data=OrderReadOnlySerializer(order).data)
