from builtins import ImportError

from drf_yasg.utils import swagger_auto_schema
from drf_yasg.utils import swagger_auto_schema
from django.http import FileResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.terminals.helper.catalog import get_by_catalog_import_input
from apps.terminals.models import CatalogImport
from apps.terminals.serializers.catalog import CatalogSerializer, CatalogListInputSerializer
from core.base_view import BaseView
from core.mixins import GetSerializerClassMixin
from core.importer import Importer
from core.permissions import IsManager


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

    @swagger_auto_schema(
        operation_description="Export Customer",
    )
    @action(
        methods=['GET'],
        detail=False,
        url_path='template-import',
        url_name='template_import',
        permission_classes=[IsManager],
    )
    def template_import(self, request, *args, **kwargs):
        user = request.user
        dest_file = f"/tmp/{user.id}-products.xlsx"
        Importer.import_products(dest_file)
        response = FileResponse(
            open(dest_file, 'rb'),
            filename="template_import_product.xlsx",
            content_type="application/vnd.ms-excel"
        )
        return response

    @swagger_auto_schema(
        operation_description="Export Customer",
    )
    @action(
        methods=['GET'],
        detail=False,
        url_path='import-product',
        url_name='import_product',
        permission_classes=[IsManager],
    )
    def import_product(self, request, *args, **kwargs):
        user = request.user
        dest_file = f"/tmp/{user.id}-products.xlsx"
        Importer.import_products(dest_file)
        response = FileResponse(
            open(dest_file, 'rb'),
            filename="template_import_product.xlsx",
            content_type="application/vnd.ms-excel"
        )
        return response
