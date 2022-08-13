from uuid import UUID

from django.db import transaction as tran

from apps.terminals.helper.catalog import ImportProductHandler
from apps.terminals.models import CatalogImport
from config.celery import app


@app.task(serializer='json')
def import_product_handler(catalog_id: UUID):
    catalog = CatalogImport.objects.get(pk=catalog_id)
    ImportProductHandler(catalog).process()
