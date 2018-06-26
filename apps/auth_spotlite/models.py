from django.db import models

# Create your models here.

class User(models.Model):
    email = models.CharField(max_length=64, unique=True)
    firstname = models.CharField(max_length=32)
    surname = models.CharField(max_length=32)
    password = models.CharField(max_length=128)
    profilepic = models.CharField(max_length=128)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)