from django.contrib import admin
from .models.terminal import Terminal


class TerminalAdmin(admin.ModelAdmin):
    pass


admin.site.register(Terminal, TerminalAdmin)
