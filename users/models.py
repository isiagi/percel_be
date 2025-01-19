from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager

# Create your models here.

class CustomUser(AbstractUser):
    # is_employer = models.BooleanField(default=False)
    # is_applicant = models.BooleanField(default=False)   

    objects = CustomUserManager()

    def __str__(self):
        if self.username:
            return str(self.username)
        elif self.email:
            return str(self.email)
        return f"User {str(self.id)}"



