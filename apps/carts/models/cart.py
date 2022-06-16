import uuid

from django.db import models
from safedelete import HARD_DELETE
from safedelete.models import SafeDeleteMixin

from apps.users.models import User


class Cart(SafeDeleteMixin):
    _safedelete_policy = HARD_DELETE

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        blank=True,
        related_name="cart",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "carts"
        ordering = ["created_at"]

    def __str__(self):
        return self.user.name
