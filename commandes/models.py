# commandes/models.py
from django.conf import settings
from django.db import models
from menu.models import Plat
from tables.models import Table


class Commande(models.Model):
    STATUT_CHOICES = (
        ('en_attente', 'En attente (Confirmée par serveur)'),
        ('en_preparation', 'En préparation (Cuisine)'),
        ('prete', 'Prête à servir'),
        ('servie', 'Servie à la table'),
        ('annulee', 'Annulée'),
        ('payee', 'Payée & Clôturée'),
    )

    table = models.ForeignKey(
        Table, on_delete=models.CASCADE, related_name='commandes'
    )
    serveur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='commandes_gerees',
    )
    statut = models.CharField(
        max_length=20, choices=STATUT_CHOICES, default='en_attente'
    )
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Commande #{self.pk} - Table {self.table.numero} ({self.get_statut_display()})'


class LigneCommande(models.Model):
    commande = models.ForeignKey(
        Commande, on_delete=models.CASCADE, related_name='lignes'
    )
    plat = models.ForeignKey(Plat, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantite}x {self.plat.nom} (Cmd #{self.commande.pk})'
