# menu/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from .forms import CategorieForm, PlatForm
from .models import Categorie, Plat


# --- Gestion des Catégories ---
@method_decorator(login_required, name='dispatch')
class CategorieListView(ListView):
    model = Categorie
    template_name = 'menu/categorie_list.html'
    context_object_name = 'categories'


@method_decorator(login_required, name='dispatch')
class CategorieCreateView(CreateView):
    model = Categorie
    form_class = CategorieForm
    template_name = 'menu/categorie_form.html'
    success_url = reverse_lazy('menu:categorie_list')


@method_decorator(login_required, name='dispatch')
class CategorieUpdateView(UpdateView):
    model = Categorie
    form_class = CategorieForm
    template_name = 'menu/categorie_form.html'
    success_url = reverse_lazy('menu:categorie_list')


@method_decorator(login_required, name='dispatch')
class CategorieDeleteView(DeleteView):
    model = Categorie
    template_name = 'menu/categorie_confirm_delete.html'
    success_url = reverse_lazy('menu:categorie_list')


# --- Gestion des Plats ---
@method_decorator(login_required, name='dispatch')
class PlatListView(ListView):
    model = Plat
    template_name = 'menu/plat_list.html'
    context_object_name = 'plats'


@method_decorator(login_required, name='dispatch')
class PlatCreateView(CreateView):
    model = Plat
    form_class = PlatForm
    template_name = 'menu/plat_form.html'
    success_url = reverse_lazy('menu:plat_list')


@method_decorator(login_required, name='dispatch')
class PlatUpdateView(UpdateView):
    model = Plat
    form_class = PlatForm
    template_name = 'menu/plat_form.html'
    success_url = reverse_lazy('menu:plat_list')


@method_decorator(login_required, name='dispatch')
class PlatDeleteView(DeleteView):
  model = Plat
  template_name = 'menu/plat_confirm_delete.html'
  success_url = reverse_lazy('menu:plat_list')


@login_required
def toggle_plat_status(request, pk):
    plat = get_object_or_404(Plat, pk=pk)
    # On utilise bien le champ disponible_du_jour défini dans votre modèle
    plat.disponible_du_jour = not plat.disponible_du_jour
    plat.save()
    return redirect('menu:plat_list')
