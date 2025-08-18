from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
# Create your models here.


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=20)
    postal_address = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True, null=False)
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name","phone_number"]
