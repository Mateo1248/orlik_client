from django.db import models


# Create your models here.
class RegisterData(models.Model):
    email = models.TextField()
    password = models.TextField()


class LoginData(models.Model):
    email = models.TextField()
    password = models.TextField()


class PitchReservation(models.Model):
    reservation_id = models.TextField()
    date = models.DateField()
    start_hour = models.TextField()
    end_hour = models.TextField()
    pitch_id = models.TextField()
    user_name = models.TextField()


class Reservation(models.Model):
    reservation_id = models.TextField()
    date = models.DateField()
    start_hour = models.TextField()
    end_hour = models.TextField()
    pitch_id = models.TextField()


class Pitch(models.Model):
    pitch_name = models.TextField()
    coordinateX = models.TextField()
    coordinateY = models.TextField()


class Pitch_list(models.Model):
    pitch_id = models.TextField()
    pitch_name = models.TextField()
    latitude = models.TextField()
    longitude = models.TextField()
    reservations = models.TextField()
    ratings = models.TextField()
