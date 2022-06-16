import uuid

from django.db import models
from safedelete import HARD_DELETE
from safedelete.models import SafeDeleteMixin

from apps.users.models import User
from django.utils.translation import gettext_lazy as _


class TransactionType(models.TextChoices):
    REGISTER_TERMINAL = "REGISTER_TERMINAL", _("REGISTER_TERMINAL")
    EXTEND_TERMINAL = "EXTEND_TERMINAL", _("EXTEND_TERMINAL")
    ORDER = "ORDER", _("ORDER")


class Transaction(SafeDeleteMixin):
    _safedelete_policy = HARD_DELETE

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.BigIntegerField(null=False, blank=False)
    create_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="transaction_set",
    )
    bank = models.CharField(max_length=50, null=False, blank=False)
    card_id = models.CharField(max_length=50, null=False, blank=False)
    type = models.CharField(
        choices=TransactionType.choices,
        max_length=20,
        default=TransactionType.ORDER,
    )
    status = models.BooleanField(default=True)
    handler_id = models.UUIDField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "transactions"
        ordering = ["created_at"]

    def __str__(self):
        return str(self.id)
