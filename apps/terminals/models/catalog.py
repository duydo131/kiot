import uuid

from django.db import models
from safedelete import HARD_DELETE
from safedelete.models import SafeDeleteMixin

from django.utils.translation import gettext_lazy as _

from apps.users.models import User


class ImportStatus(models.TextChoices):
    UPLOAD = "UPLOAD", _("UPLOAD")
    EXTRACT = "EXTRACT", _("EXTRACT")
    PROCESS = "PROCESS", _("PROCESS")
    SUCCESS = "SUCCESS", _("SUCCESS")
    FAIL = "FAIL", _("FAIL")


class CatalogImport(SafeDeleteMixin):
    _safedelete_policy = HARD_DELETE

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="imports",
    )
    source_file = models.CharField(max_length=256, null=False, blank=False)
    result_file = models.CharField(max_length=256, null=True, blank=True)
    status = models.CharField(
        choices=ImportStatus.choices,
        max_length=10,
        default=ImportStatus.UPLOAD,
    )
    quantity_product = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "catalog_import"
        ordering = ["-created_at"]

    def __str__(self):
        return str(self.id)
