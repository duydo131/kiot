from django.contrib import admin
from .models.transaction import Transaction


class TransactionAdmin(admin.ModelAdmin):
    pass


admin.site.register(Transaction, TransactionAdmin)
