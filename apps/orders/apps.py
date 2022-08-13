from django.apps import AppConfig


class TerminalConfig(AppConfig):
    name = 'apps.orders'

    def ready(self):
        import apps.orders.signals
