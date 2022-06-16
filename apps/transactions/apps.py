from django.apps import AppConfig


class TransactionConfig(AppConfig):
    name = 'apps.transactions'

    def ready(self):
        import apps.transactions.signals
