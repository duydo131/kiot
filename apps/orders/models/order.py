import uuid

from django.db import models
from safedelete import HARD_DELETE
from safedelete.models import SafeDeleteMixin

from apps.transactions.models.transaction import Transaction
from apps.users.models import User
from django.utils.translation import gettext_lazy as _


class OrderType(models.TextChoices):
    CREATE = "CREATE", _("CREATE")
    PAID = "PAID", _("PAID")
    FAIL = "FAIL", _("FAIL")
    DONE = "DONE", _("DONE")


class Order(SafeDeleteMixin):
    _safedelete_policy = HARD_DELETE

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders",
    )
    total_price = models.BigIntegerField(blank=True, null=True)
    transaction = models.OneToOneField(
        Transaction,
        on_delete=models.CASCADE,
        related_name="orders",
        blank=True,
        null=True
    )
    type = models.CharField(
        choices=OrderType.choices,
        max_length=20,
        default=OrderType.CREATE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "orders"
        ordering = ["-created_at"]

    def __str__(self):
        return str(self.id)
