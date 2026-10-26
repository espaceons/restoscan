# accounts/forms.py
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import User


class CustomUserCreationForm(UserCreationForm):

  class Meta:
    model = User
    fields = ('username', 'email', 'role')

  def save(self, commit=True):
    user = super().save(commit=False)
    # Forcer le compte à inactif par défaut à l'inscription
    user.is_active = False
    if commit:
      user.save()
    return user


class CustomUserChangeForm(UserChangeForm):
  password = None

  class Meta:
    model = User
    fields = ('username', 'email', 'role', 'is_active')