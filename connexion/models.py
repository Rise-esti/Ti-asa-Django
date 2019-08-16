from django.db import models
from django.contrib.auth.models import User
import datetime 
from django.utils import timezone 

# Create your models here.

class Profil(models.Model):
    phone = models.CharField(max_length=16, null=True)
    biographie = models.TextField(null=True)
    dateNaissance = models.DateTimeField(null=True)
    sexe = models.CharField(max_length=2, null=True)
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    adresse = models.CharField(max_length=30, null=True)
    ville = models.CharField(max_length=30, null=True)
    poste = models.CharField(max_length=100, default='')
    lieu = models.CharField(max_length=30, default='')
    profilpic = models.URLField(default="connexion/images/av.png")
    coverpic = models.URLField(default="connexion/images/resources/timeline-1.jpg")

    def __str__(self):
        username = User.objects.filter(id=self.username_id)[0].username
        return username
    

class Formation(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    mois_debut = models.CharField(null=True, max_length=20)
    annee_debut = models.IntegerField()
    mois_fin = models.CharField(null=True, max_length=20)
    annee_fin = models.CharField(null=True, max_length=20)
    filiere = models.CharField(max_length=50, null=True)
    niveau = models.CharField(max_length=30, null=True)
    lieu = models.CharField(max_length=50)
    obtention = models.CharField(max_length=50, null=True)
    
    def __str__(self):
        username = User.objects.filter(id=self.username_id)[0].username
        return username
        

class Competence(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    competence = models.CharField(max_length=128)
    description = models.TextField(null=True)
    niveau = models.CharField(max_length=30, null=True)

    def __str__(self):
        username = User.objects.get(id=self.username_id).username
        return username
    

class Experience(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    mois_debut = models.CharField(null=True, max_length=20)
    annee_debut = models.IntegerField()
    mois_fin = models.CharField(null=True, max_length=20)
    annee_fin = models.CharField(null=True, max_length=20)
    poste = models.CharField(max_length=50, null=True)
    lieu = models.CharField(max_length=50)
    description = models.TextField(null=True)

    def __str__(self):
        username = User.objects.get(id=self.username_id).username
        return username

        
class Interet(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    interet = models.CharField(max_length=50)
    description = models.TextField(null=True)

    def __str__(self):
        username = User.objects.get(id=self.username_id).username
        return username


class Publication(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    legende = models.TextField(null=True)
    date_upload = models.DateTimeField(default=timezone.now)
    date_limit_jour = models.IntegerField(null=True)
    date_limit_mois = models.CharField(null=True, max_length=20)
    valable = models.BooleanField(default=True)
    experience = models.TextField(null=True)
    competence = models.TextField(null=True)
    formation = models.TextField(null=True)
    personnalite = models.TextField(null=True)
    langue = models.TextField(null=True)
    image = models.URLField(null=True)
    lieu = models.TextField(null=True)
    mission = models.TextField(null=True)

    def __str__(self):
        username = User.objects.get(id=self.username_id).username
        return username


