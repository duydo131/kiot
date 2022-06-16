import uuid
from django.db import models
from django.db.models.signals import post_save
from safedelete import SOFT_DELETE_CASCADE
from safedelete.models import SafeDeleteModel, SafeDeleteManager


class CustomBulkSafeDeleteManager(SafeDeleteManager):
    
    def bulk_create(self, objs, **kwargs):
        a = super(models.Manager, self).bulk_create(objs, **kwargs)
        for i in objs:
            post_save.send(i.__class__, instance=i, created=True, **kwargs)
        return a

    def bulk_update(self, objs, fields, **kwargs):
        ret = super().bulk_update(objs, fields, **kwargs)
        kwargs["fields"] = fields
        for i in objs:
            post_save.send(i.__class__, instance=i, created=False, **kwargs)
        return ret


class BaseSafeDeleteModel(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseBulkSafeDeleteModel(BaseSafeDeleteModel):
    objects = CustomBulkSafeDeleteManager()

    class Meta:
        abstract = True


