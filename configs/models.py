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

    def __str__(self):
        return f"Config for {self.user.username}"

class DiscordAuthToken(models.Model):
    access_token = models.TextField()
    expires_in = models.IntegerField()
    refresh_token = models.TextField()
    config = models.OneToOneField(
        Config,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    def __str__(self):
        return f"Discord auth token for {self.config.user.username}"
