from django.apps import AppConfig


class TerminalConfig(AppConfig):
    name = 'apps.terminals'

    def ready(self):
        import apps.terminals.signals
