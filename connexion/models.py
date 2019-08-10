from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profil(models.Model):
    phone = models.CharField(max_length=16, null=True)
    profilPic = models.URLField(null=True)
    coverPic = models.URLField(null=True)
    biographie = models.TextField(null=True)
    dateNaissance = models.DateTimeField(null=True)
    sexe = models.CharField(max_length=2, null=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    adresse = models.CharField(max_length=30, null=True)
    ville = models.CharField(max_length=30, null=True)
