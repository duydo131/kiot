from django.apps import AppConfig


class CartConfig(AppConfig):
    name = 'apps.carts'

    def ready(self):
        import apps.carts.signals
