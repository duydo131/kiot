from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status, exceptions
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from apps.terminals.helper.catalog import get_by_catalog_import_input
from apps.terminals.helper.product import get_by_product_input
from apps.terminals.models import Product, CatalogImport
from apps.terminals.serializers.catalog import CatalogSerializer, CatalogListInputSerializer
from apps.terminals.serializers.product import ProductSerializer, ProductListInputSerializer, ProductCreateSerializer, \
    AddProductSerializer, ProductDetailSerializer
from apps.users.serializers import LoginSerializer
from core.base_view import BaseView
from core.mixins import GetSerializerClassMixin
from core.permissions import IsManager
from core.swagger_schemas import ManualParametersAutoSchema


class CatalogViewSet(GetSerializerClassMixin, viewsets.ModelViewSet, BaseView):
    permission_classes = []
    queryset = CatalogImport.objects.filter()
    queryset_detail = CatalogImport.objects.filter()
    serializer_class = CatalogSerializer
    serializer_detail_class = CatalogSerializer
    inp_serializer_cls = CatalogListInputSerializer
    http_method_names = ['get']

    serializer_action_classes = {
        "list": CatalogSerializer,
        "retrieve": CatalogSerializer,
    }

    def get_queryset(self):
        queryset = self.queryset.filter()
        request_data = self.request_data
        queryset = get_by_catalog_import_input(queryset, request_data)
        return queryset

    def retrieve(self, request, pk=None, *args, **kwargs):
        catalog = CatalogImport.objects.get(pk=pk)
        return Response(data=CatalogSerializer(catalog).data)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
