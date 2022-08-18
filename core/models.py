from django.db import models


class NewUser(models.Model):
    username = models.CharField(max_length=200)


class Room(models.Model):
    room_name = models.CharField(max_length=200)
