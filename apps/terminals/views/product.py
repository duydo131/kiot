from django.contrib.auth import authenticate
from django.db.models import F
from django.utils.translation import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status, exceptions
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from apps.terminals.helper.product import get_by_product_input
from apps.terminals.models import Product, CatalogImport
from apps.terminals.serializers.catalog import CatalogImportSerializer
from apps.terminals.serializers.product import ProductSerializer, ProductListInputSerializer, ProductCreateSerializer, \
    AddProductSerializer, ProductDetailSerializer, ProductBulkCreateSerializer, AddSingleProductSerializer, \
    ProductReadOnlySerializer, GetTerminalOfProductSerializer
from apps.terminals.serializers.terminal import TerminalReadOnlySerializer, TerminalSerializer
from apps.terminals.task import import_product_handler
from apps.users.serializers import LoginSerializer
from rest_framework.decorators import action
from core.base_view import BaseView
from core.mixins import GetSerializerClassMixin
from core.permissions import IsManager, IsAdmin
from core.swagger_schemas import ManualParametersAutoSchema


class ProductViewSet(GetSerializerClassMixin, viewsets.ModelViewSet, BaseView):
    permission_classes = []
    queryset = Product.objects.filter()
    queryset_detail = Product.objects.filter()
    serializer_class = ProductSerializer
    serializer_detail_class = ProductSerializer
    filterset_class = None
    inp_serializer_cls = ProductListInputSerializer

    serializer_action_classes = {
        "list": ProductReadOnlySerializer,
        "retrieve": ProductDetailSerializer,
    }

    def get_queryset(self):
        queryset = self.queryset.filter()
        request_data = self.request_data
        user = self.request.user
        if user.is_manager:
            queryset = queryset.filter(terminal__seller_id=user.id)
        queryset = get_by_product_input(queryset, request_data)
        queryset = queryset.annotate(terminal_name=F('terminal__name'))
        return queryset

    @swagger_auto_schema(
        operation_description="Detail",
        auto_schema=ManualParametersAutoSchema,
        responses={200: ProductDetailSerializer},
    )
    def retrieve(self, request, pk=None, *args, **kwargs):
        product = Product.objects.get(pk=pk)
        return Response(data=ProductDetailSerializer(product).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="List",
        query_serializer=ProductListInputSerializer(),
        auto_schema=ManualParametersAutoSchema,
        responses={200: ProductSerializer},
    )
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(
        methods=["GET"],
        detail=False,
        url_path="terminal",
        url_name="terminal",
        permission_classes=[IsManager | IsAdmin],
        filterset_class=None,
        pagination_class=None,
    )
    def terminal(self, request, *args, **kwargs):
        serializer = GetTerminalOfProductSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        product_id = serializer.validated_data['id']
        product = Product.objects.get(pk=product_id)
        serializer = TerminalSerializer(instance=product.terminal)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create new product",
        request_body=AddSingleProductSerializer,
        responses={'201': ProductSerializer},
        permission_classes=[IsManager]
    )
    def create(self, request, *args, **kwargs):
        serializer = AddSingleProductSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        return Response(data=ProductSerializer(result).data)

    @action(
        methods=["POST"],
        detail=False,
        url_path="import",
        url_name="bulk_create",
        permission_classes=[IsManager],
        filterset_class=None,
        pagination_class=None,
    )
    def bulk_create(self, request, *args, **kwargs):
        serializer = ProductBulkCreateSerializer(data=request.data)
        serializer.is_valid()
        file_url = serializer.validated_data['file_url']
        user = request.user
        catalog = CatalogImport(user=user, source_file=file_url)
        catalog.save()
        import_product_handler(catalog)

        return Response(data=CatalogImportSerializer(catalog).data, status=status.HTTP_200_OK)
