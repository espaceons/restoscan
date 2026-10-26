# tables/models.py
import uuid
from django.conf import settings
from django.db import models


class Table(models.Model):
  numero = models.IntegerField(unique=True)
  serveur = models.ForeignKey(
      settings.AUTH_USER_MODEL,
      on_delete=models.SET_NULL,
      null=True,
      blank=True,
      limit_choices_to={'role': 'serveur'},
      related_name='tables',
  )
  token_qr = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
  is_active = models.BooleanField(default=True)

  def __str__(self):
    status = 'Active' if self.is_active else 'Inactive'
    serveur_nom = self.serveur.username if self.serveur else 'Aucun serveur'
    return f'Table {self.numero} (Serveur: {serveur_nom}) [{status}]'
