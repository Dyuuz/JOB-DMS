from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Client(AbstractUser):
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class DocumentForm(models.Model):
    document = models.FileField(upload_to='documents/')
    description = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return self.description
