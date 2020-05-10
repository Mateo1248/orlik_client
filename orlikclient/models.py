from django.db import models


# Create your models here.
class RegisterData(models.Model):
    email = models.TextField()
    password = models.TextField()


class Reservation(models.Model):
    reservation_id = models.TextField()
    date = models.DateField()
    start_hour = models.TextField()
    end_hour = models.TextField()
    pitch_name = models.TextField()