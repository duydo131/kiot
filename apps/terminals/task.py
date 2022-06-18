from django.db import transaction as tran

from apps.terminals.helper.catalog import ImportProductHandler
from apps.terminals.models import CatalogImport
from config.celery import app


@app.task
def import_product_handler(catalog: CatalogImport):
    ImportProductHandler(catalog).process()
