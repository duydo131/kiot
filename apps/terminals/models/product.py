import uuid

from django.db import models
from safedelete import HARD_DELETE
from safedelete.models import SafeDeleteMixin

from apps.terminals.models.terminal import Terminal


class Product(SafeDeleteMixin):
    _safedelete_policy = HARD_DELETE

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=50, unique=True)
    sku = models.CharField(max_length=50, blank=False, null=False)
    price = models.BigIntegerField(blank=False, null=False)
    image = models.CharField(max_length=50, blank=True, null=True)
    terminal = models.ForeignKey(
        Terminal,
        on_delete=models.CASCADE,
        related_name="products",
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "product"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
