from django.contrib.auth.models import AnonymousUser
from django.db.models import Count
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.terminals.helper.terminal import get_by_terminal_input, calculate_price_register_terminal, \
    calculate_price_extend_terminal
from apps.terminals.models import Terminal
from apps.terminals.models.terminal import TerminalStatus
from apps.terminals.serializers.product import ProductSerializer, ProductListInputSerializer
from apps.terminals.serializers.terminal import TerminalSerializer, TerminalListInputSerializer, \
    TerminalRegisterSerializer, TerminalPriceSerializer, TerminalExtendSerializer, TerminalReadOnlySerializer
from core.base_view import BaseView
from core.mixins import GetSerializerClassMixin
from core.permissions import IsManager, IsAdmin
from core.swagger_schemas import ManualParametersAutoSchema


class TerminalViewSet(GetSerializerClassMixin, viewsets.ModelViewSet, BaseView):
    permission_classes = []
    queryset = Terminal.objects.filter()
    queryset_detail = Terminal.objects.filter()
    serializer_class = TerminalSerializer
    serializer_detail_class = TerminalSerializer
    inp_serializer_cls = TerminalListInputSerializer
    filterset_class = None

    serializer_action_classes = {
        "list": TerminalReadOnlySerializer,
        "retrieve": TerminalReadOnlySerializer,
    }

    def get_queryset(self):
        queryset = self.queryset.filter()
        request_data = self.request_data
        seller = self.request.user
        if seller.is_manager:
            queryset = get_by_terminal_input(queryset, request_data, seller_id=seller.id)
        else:
            queryset = get_by_terminal_input(queryset, request_data)

        queryset = queryset.filter(type__in=[TerminalStatus.PAID, TerminalStatus.EXTEND_FAIL, TerminalStatus.EXTEND])\
            .annotate(total_product=Count('products'))

        return queryset.order_by('-total_product')

    @swagger_auto_schema(
        operation_description="Detail",
        auto_schema=ManualParametersAutoSchema,
        responses={200: ProductSerializer},
    )
    def retrieve(self, request, pk=None, *args, **kwargs):
        terminal = Terminal.objects.annotate(total_product=Count('products')).get(pk=pk)
        return Response(data=TerminalReadOnlySerializer(terminal).data, status=status.HTTP_200_OK)

    @action(
        methods=["GET"],
        detail=False,
        url_path="all",
        url_name="all",
        pagination_class=None,
        filterset_class=None,
        permission_classes=[IsManager | IsAdmin],
    )
    def all(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = TerminalReadOnlySerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = TerminalReadOnlySerializer(queryset, many=True)
        return Response(serializer.data)

    @action(
        methods=["POST"],
        detail=False,
        url_path="register",
        url_name="register",
        filterset_class=None,
        permission_classes=[IsManager],
        pagination_class=None,
    )
    def register(self, request, *args, **kwargs):
        serializer = TerminalRegisterSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        terminal = serializer.save()
        total_price = calculate_price_register_terminal(terminal)
        data = {
            'total_price': total_price,
            'terminal': terminal
        }
        return Response(data=TerminalPriceSerializer(data).data, status=status.HTTP_200_OK)

    @action(
        methods=["POST"],
        detail=False,
        url_path="extend",
        url_name="extend",
        filterset_class=None,
        permission_classes=[IsManager],
        pagination_class=None,
    )
    def extend(self, request, *args, **kwargs):
        serializer = TerminalExtendSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        terminal = serializer.save()
        total_price = calculate_price_extend_terminal(terminal)
        data = {
            'total_price': total_price,
            'terminal': terminal
        }
        return Response(data=TerminalPriceSerializer(data).data, status=status.HTTP_200_OK)
