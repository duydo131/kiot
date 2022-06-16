import uuid
from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from safedelete import SOFT_DELETE_CASCADE, HARD_DELETE
from safedelete.models import SafeDeleteMixin

from apps.users.models.user_manager import CustomUserManager


class UserGender(models.TextChoices):
    MALE = "MALE", _("MALE")
    FEMALE = "FEMALE", _("FEMALE")
    UNKNOWN = "UNKNOWN", _("UNKNOWN")


class UserRole(models.TextChoices):
    USER = "USER", _("USER")
    MANAGER = "MANAGER", _("MANAGER")
    ADMIN = "ADMIN", _("ADMIN")


class User(SafeDeleteMixin, AbstractBaseUser):
    _safedelete_policy = HARD_DELETE
    USERNAME_FIELD = "username"

    objects = CustomUserManager()

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=100, null=False, blank=False, unique=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    address = models.TextField(max_length=100, null=True, blank=True)
    avatar_url = models.CharField(max_length=1000, null=True, blank=True)
    gender = models.CharField(
        choices=UserGender.choices,
        max_length=20,
        default=UserGender.UNKNOWN,
    )
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.CharField(
        choices=UserRole.choices,
        max_length=20,
        default=UserRole.USER,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_user(self):
        return self.role == UserRole.USER

    @property
    def is_manager(self):
        return self.role == UserRole.MANAGER

    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN

    @property
    def token(self):
        return self._generate_jwt_token()

    def clean(self):
        super().clean()

    class Meta:
        db_table = "user"
        ordering = ["created_at"]

    def _generate_jwt_token(self):
        iat = datetime.now()
        exp = iat + timedelta(days=60)
        payload = {
            "id": str(self.id),
            "name": self.name,
            "email": self.email,
            "exp": exp,
            "iat": iat,
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

        return token.decode("utf-8")

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return self.username if self.username else self.name if self.name else ""
