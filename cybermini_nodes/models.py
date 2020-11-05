from django.db import models
from django.contrib.auth.models import User

class Location(models.Model):
    city = models.CharField(max_length=200)
    street = models.CharField(max_length=200)
    building = models.CharField(max_length=200)

class Nodes(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    number = models.IntegerField()
    token = models.CharField(max_length=256)
    channel_name = models.TextField(default="")

class Schedule(models.Model):
    node = models.ForeignKey(Nodes, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    begin = models.DateTimeField()
    end = models.DateTimeField()
    key = models.CharField(max_length=4)



