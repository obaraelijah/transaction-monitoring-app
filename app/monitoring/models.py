from datetime import datetime, timezone

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import AuditableModel

from .enums import TIER_AMOUNT
from .managers import CustomUserManager

class User(AbstractBaseUser, AuditableModel):
    TIER_CHOICES = [
        ("T1", "Tier 1"),
        ("T2", "Tier 2"),
        ("T3", "Tier 3"),
    ]
    email = models.EmailField(_("email address"), null=True, blank=True, unique=True)
    password = models.CharField(max_length=255)
    firstname = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_flagged = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    tier = models.CharField(max_length=20, choices=TIER_CHOICES, default="T1")
    last_login = models.DateTimeField(null=True, blank=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return self.email

    def save_last_login(self) -> None:
        self.last_login = datetime.now(timezone.utc)
        self.save()