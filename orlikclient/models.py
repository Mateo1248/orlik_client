from django.db import models


# Create your models here.
class RegisterData(models.Model):
    email = models.TextField()
    password = models.TextField()
