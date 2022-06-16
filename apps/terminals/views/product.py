from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status, exceptions
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from apps.terminals.helper.product import get_by_product_input
from apps.terminals.models import Product
from apps.terminals.serializers.product import ProductSerializer, ProductListInputSerializer, ProductCreateSerializer, \
    AddProductSerializer, ProductDetailSerializer
from apps.users.serializers import LoginSerializer
from core.base_view import BaseView
from core.mixins import GetSerializerClassMixin
from core.permissions import IsManager
from core.swagger_schemas import ManualParametersAutoSchema


class ProductViewSet(GetSerializerClassMixin, viewsets.ModelViewSet, BaseView):
    permission_classes = []
    queryset = Product.objects.filter()
    queryset_detail = Product.objects.filter()
    serializer_class = ProductSerializer
    serializer_detail_class = ProductSerializer
    inp_serializer_cls = ProductListInputSerializer

    serializer_action_classes = {
        "list": ProductSerializer,
        "retrieve": ProductDetailSerializer,
    }

    def get_queryset(self):
        queryset = self.queryset.filter()
        request_data = self.request_data
        queryset = get_by_product_input(queryset, request_data)

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

    @swagger_auto_schema(
        operation_description="Create new product",
        request_body=AddProductSerializer,
        responses={'201': ProductSerializer},
        permission_classes=[IsManager]
    )
    def create(self, request, *args, **kwargs):
        serializer = AddProductSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        return Response(data=ProductSerializer(result).data)
