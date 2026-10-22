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
  token_qr = models.CharField(max_length=255, unique=True, blank=True)
  is_active = models.BooleanField(default=True)

  def __str__(self):
    status = 'Active' if self.is_active else 'Inactive'
    return f'Table {self.numero} [{status}]'