import uuid

from django.db import models
from safedelete import HARD_DELETE
from safedelete.models import SafeDeleteMixin

from apps.orders.models.order import Order
from apps.terminals.models.product import Product


class OrderDetail(SafeDeleteMixin):
    _safedelete_policy = HARD_DELETE

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="order_product",
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="details",
    )
    quantity = models.IntegerField(blank=True, null=True)
    sell_price = models.BigIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "order_detail"
        ordering = ["-created_at"]

    def __str__(self):
        return str(self.id)
