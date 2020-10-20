from django.db import models

class Location(models.Model):
    city = models.CharField(max_length=200)
    street = models.CharField(max_length=200)
    building = models.CharField(max_length=200)

class Nodes(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    number = models.IntegerField()
    token = models.CharField(max_length=256)


