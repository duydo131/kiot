import uuid

from django.db import models
from safedelete import HARD_DELETE
from safedelete.models import SafeDeleteMixin

from apps.users.models import User
from django.utils.translation import gettext_lazy as _


class TerminalStatus(models.TextChoices):
    REGISTER = "REGISTER", _("REGISTER")
    EXTEND = "EXTEND", _("EXTEND")
    PAID = "PAID", _("PAID")
    EXPIRED = "EXPIRED", _("EXPIRED")
    UNKNOWN = "UNKNOWN", _("UNKNOWN")
    FAIL = "FAIL", _("FAIL")
    EXTEND_FAIL = "EXTEND_FAIL", _("EXTEND_FAIL")


class Terminal(SafeDeleteMixin):
    _safedelete_policy = HARD_DELETE

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="terminals",
    )
    name = models.CharField(max_length=20, null=True, blank=True)
    code = models.CharField(max_length=20, null=False, blank=False)
    time_register = models.DateTimeField(null=True, blank=True)
    time_open = models.DateTimeField(null=True, blank=True)
    expired_at = models.DateTimeField(null=True, blank=True)
    max_quantity_product = models.IntegerField(null=False, blank=False)
    status = models.BooleanField(default=True)
    type = models.CharField(
        choices=TerminalStatus.choices,
        max_length=20,
        default=TerminalStatus.UNKNOWN,
    )
    time_selling = models.IntegerField(null=True, blank=True)
    image_url = models.CharField(max_length=100, null=True, blank=True)
    extend_max_quantity_product = models.IntegerField(default=0)
    extend_time_selling = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "terminals"
        ordering = ["name"]

    def __str__(self):
        return self.name
