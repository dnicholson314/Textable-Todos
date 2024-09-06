from typing import Any
from django.db import models
from django.contrib.auth.models import User

class EncryptedTextField(models.TextField):
    pass

class Config(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    discord_id = models.IntegerField(
        blank=True,
        default=0,
        unique=True,
    )
    discord_username = models.CharField(
        max_length=200,
        blank=True,
        default="",
        unique=True,
    )

    def __str__(self):
        return f"Config for {self.user.username}"