from django.contrib import admin
from .models import Categorie, Plat


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
  list_display = ('nom', 'is_active')
  list_filter = ('is_active',)


@admin.register(Plat)
class PlatAdmin(admin.ModelAdmin):
  list_display = (
      'nom',
      'categorie',
      'prix',
      'disponible_du_jour',
      'is_active',
  )
  list_filter = ('is_active', 'disponible_du_jour', 'categorie')
  search_fields = ('nom',)