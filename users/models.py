from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Электронная почта")
    avatar = models.ImageField(
        upload_to="users/avatar",
        blank=True,
        null=True,
        verbose_name="Аватар",
    )
    phone = models.CharField(blank=True, null=True, max_length=20)
    country = models.CharField(blank=True, null=True, max_length=20)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
