from django.contrib import admin
from .models import Table


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
  list_display = ('numero', 'serveur', 'is_active')
  list_filter = ('is_active', 'serveur')
  search_fields = ('numero',)