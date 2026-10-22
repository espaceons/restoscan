from django.db import models


class Categorie(models.Model):
  nom = models.CharField(max_length=100, unique=True)
  is_active = models.BooleanField(default=True)

  def __str__(self):
    return self.nom


class Plat(models.Model):
  categorie = models.ForeignKey(
      Categorie, on_delete=models.CASCADE, related_name='plats'
  )
  nom = models.CharField(max_length=150)
  description = models.TextField(blank=True, null=True)
  prix = models.DecimalField(max_digits=6, decimal_places=2)
  disponible_du_jour = models.BooleanField(default=True)
  is_active = models.BooleanField(default=True)
  image = models.ImageField(upload_to='plats/', blank=True, null=True)

  def __str__(self):
    return self.nom