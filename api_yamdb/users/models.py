from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"
    USER_ROLE_CHOICES = [
        (USER, "user"),
        (MODERATOR, "moderator"),
        (ADMIN, "admin"),
    ]
    username = models.CharField(
        verbose_name="Имя пользователя", max_length=150, null=True, unique=True
    )
    email = models.EmailField(unique=True)
    bio = models.TextField(
        verbose_name="Биография",
        blank=True,
    )
    role = models.CharField(
        max_length=30,
        verbose_name="Роль",
        choices=USER_ROLE_CHOICES,
        default=USER,
        blank=False,
    )

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN
