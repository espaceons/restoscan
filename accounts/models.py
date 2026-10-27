# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
  ROLE_CHOICES = (
      ('admin', 'Administrateur'),
      ('serveur', 'Serveur'),
      ('cuisine', 'Cuisinier'),
  )
  role = models.CharField(
      max_length=20, choices=ROLE_CHOICES, default='serveur'
  )
  # Nouveaux champs
  tel = models.CharField(max_length=20, blank=True, null=True)
  photo = models.ImageField(upload_to='profils/', blank=True, null=True)

  def __str__(self):
    return f'{self.username} ({self.get_role_display()})'