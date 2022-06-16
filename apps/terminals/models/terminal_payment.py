import uuid

from django.db import models
from safedelete import HARD_DELETE
from safedelete.models import SafeDeleteMixin
from django.utils.translation import gettext_lazy as _

from apps.terminals.models.terminal import Terminal
from apps.transactions.models.transaction import Transaction


class TypeTerminalPayment(models.TextChoices):
    REGISTER = "REGISTER", _("REGISTER")
    EXTEND = "EXTEND", _("EXTEND")


class TerminalPayment(SafeDeleteMixin):
    _safedelete_policy = HARD_DELETE

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(
        choices=TypeTerminalPayment.choices,
        max_length=20,
        default=TypeTerminalPayment.REGISTER,
    )
    terminal = models.ForeignKey(
        Terminal,
        on_delete=models.CASCADE,
        related_name="payment_set",
    )
    transaction = models.OneToOneField(
        Transaction,
        on_delete=models.CASCADE,
        blank=True,
        related_name="terminals",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "terminal_payment"
        ordering = ["created_at"]

    def __str__(self):
        return str(self.id)
