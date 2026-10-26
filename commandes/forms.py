# commandes/forms.py
from django import forms
from .models import Commande, LigneCommande


class CommandeForm(forms.ModelForm):
    class Meta:
        model = Commande
        fields = ['table']


class LigneCommandeForm(forms.ModelForm):
    class Meta:
        model = LigneCommande
        fields = ['plat', 'quantite']