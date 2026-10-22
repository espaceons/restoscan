from rest_framework import viewsets
from .models import Categorie, Plat
from .serializers import CategorieSerializer, PlatSerializer


class CategorieViewSet(viewsets.ModelViewSet):
  queryset = Categorie.objects.all()
  serializer_class = CategorieSerializer


class PlatViewSet(viewsets.ModelViewSet):
  queryset = Plat.objects.all()
  serializer_class = PlatSerializer