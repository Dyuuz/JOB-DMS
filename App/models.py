from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Client(AbstractUser):
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username
