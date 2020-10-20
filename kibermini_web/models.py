from django.db import models

class Users(models.Model):
    phone = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)