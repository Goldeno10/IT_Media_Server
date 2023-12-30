import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """A custom user model with a UUID primary key"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self) -> str:
        return self.username
