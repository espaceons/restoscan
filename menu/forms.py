# menu/forms.py
from django import forms
from .models import Categorie, Plat


class CategorieForm(forms.ModelForm):

  class Meta:
    model = Categorie
    fields = ('nom', 'description')


class PlatForm(forms.ModelForm):

  class Meta:
    model = Plat
    fields = (
        'categorie',
        'nom',
        'description',
        'prix',
        'disponible_du_jour',
        'is_active',
        'image',
    )
