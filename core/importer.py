import openpyxl

from config.settings.dev import IMPORT_PRODUCT_TEMPLATE


class Importer:
    @classmethod
    def import_products(cls, dest_file):
        wb = openpyxl.load_workbook(IMPORT_PRODUCT_TEMPLATE)
        wb.save(dest_file)
