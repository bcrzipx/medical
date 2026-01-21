from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime

# Create your models here.
class Malade(models.Model):
    SEXE_CHOICES = [
        ('femme', 'Femme'),
        ('homme', 'Homme'),
    ]
    nom = models.CharField(max_length=100, null=False)
    prenom = models.CharField(max_length=100, null=False)
    sexe = models.CharField(max_length=20, choices=SEXE_CHOICES, null=False)
    date_naissance = models.DateField(null=False)
    email = models.EmailField(unique=True, null=False)
    telephone = models.CharField(max_length=20, null=False)
    adresse = models.CharField(max_length=500, null=False)

    def __str__(self):
        return f"{self.nom} {self.prenom}"

class Rendezvous(models.Model):
    date = models.DateField(default=timezone.now, null=False)
    heure = models.TimeField(default=timezone.now, null=False)
    raison = models.TextField()
    malade = models.ForeignKey(Malade, on_delete=models.CASCADE, related_name='rendezvous')
    def clean(self):
        # Check if the date is not in the past relative to today
        if self.date < timezone.now().date():
            raise ValidationError("La date ne peut pas être antérieure à aujourd'hui.")

        # Check for unique heure (time) for the same date
        if Rendezvous.objects.filter(date=self.date, heure=self.heure).exclude(id=self.id).exists():
            raise ValidationError("L'heure spécifiée est déjà occupée pour cette date.")

        # Check if heure is between 09:00 AM and 16:00 PM
        from datetime import time as time_class
        if not (self.heure >= time_class(9, 0) and self.heure <= time_class(16, 0)):
            raise ValidationError("L'heure doit être comprise entre 09:00 AM et 16:00 PM.")

    def save(self, *args, **kwargs):
        self.clean()  # Validate before saving
        super().save(*args, **kwargs)
    def __str__(self):
        return f"Rendez-vous de {self.malade.prenom} {self.malade.nom} le {self.date} à {self.heure}"

class Consultation(models.Model):
    date = models.DateField(default=timezone.now, null=False)
    heure = models.TimeField(default=timezone.now, null=False)     
    raison = models.TextField()
    etat_hydrodynamique = models.CharField(max_length=500, null=False)
    etat_respiratoire = models.CharField(max_length=500, null=False)
    echographie = models.CharField(max_length=500, null=False)
    poids = models.DecimalField(max_digits=5, decimal_places=2)
    tension = models.DecimalField(max_digits=5, decimal_places=2)
    fievre = models.DecimalField(max_digits=5, decimal_places=2)
    rendezvous = models.OneToOneField (Rendezvous,
        on_delete=models.CASCADE,
        related_name='consultation',
        null=False,
        limit_choices_to={'consultation__isnull': True}  # Restreindre les choix aux rendez-vous non encore pris par une consultation
     )
    def __str__(self):
      return f"Consultation de {self.rendezvous.malade.prenom} {self.rendezvous.malade.nom} le {self.date} à {self.heure}"

    
class Ordonnance(models.Model):
    date = models.DateField(default=timezone.now, null=False)
    heure = models.TimeField(default=timezone.now, null=False)     
    contenue = models.TextField()
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE)
    def __str__(self):
      return f"Ordonnance de {self.consultation.rendezvous.malade.prenom} {self.consultation.rendezvous.malade.nom} le {self.date} à {self.heure}"
    
 