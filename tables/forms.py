# tables/forms.py
from django import forms
from .models import Table
from accounts.models import User


class TableForm(forms.ModelForm):

  class Meta:
    model = Table
    fields = ('numero', 'serveur', 'is_active')

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    # Filtrer pour ne lister que les utilisateurs qui ont le rôle 'serveur' dans le menu déroulant
    self.fields['serveur'].queryset = User.objects.filter(
        role='serveur', is_active=True
    )
