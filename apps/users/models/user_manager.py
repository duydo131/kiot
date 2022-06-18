from django.contrib.auth.base_user import BaseUserManager
from safedelete import DELETED_VISIBLE_BY_PK
from safedelete.managers import SafeDeleteManager


class CustomUserManager(SafeDeleteManager, BaseUserManager):
    _safedelete_visibility = DELETED_VISIBLE_BY_PK

    def create_superuser(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("Users must have an username")
        user = self.model(username=username)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        try:
            user.role = 'ADMIN'
            user.save(using=self._db)
        except Exception:
            raise ValueError("Error")
        return user
