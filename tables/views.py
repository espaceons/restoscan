# tables/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView
from django.urls import reverse_lazy
from .forms import TableForm
from .models import Table
from commandes.models import Commande

# 1. Liste et gestion des tables pour l'Admin
@method_decorator(login_required, name='dispatch')
class TableListView(ListView):
  model = Table
  template_name = 'tables/table_list.html'
  context_object_name = 'tables'


@method_decorator(login_required, name='dispatch')
class TableCreateView(CreateView):
  model = Table
  form_class = TableForm
  template_name = 'tables/table_form.html'
  success_url = reverse_lazy('tables:table_list')


@method_decorator(login_required, name='dispatch')
class TableUpdateView(UpdateView):
  model = Table
  form_class = TableForm
  template_name = 'tables/table_form.html'
  success_url = reverse_lazy('tables:table_list')


@login_required
def toggle_table_status(request, pk):
  table = get_object_or_404(Table, pk=pk)
  table.is_active = not table.is_active
  table.save()
  return redirect('tables:table_list')


# 2. Dashboard dédié au Serveur (uniquement ses tables)
  # Pensez à importer Commande si ce n'est pas fait

@login_required
def serveur_dashboard(request):
    if request.user.role != 'serveur' and request.user.role != 'admin':
        return redirect('accounts:home')

    # Filtrer les tables selon le rôle
    if request.user.role == 'serveur':
        tables = Table.objects.filter(serveur=request.user, is_active=True)
        # Récupérer uniquement les commandes liées aux tables de ce serveur
        commandes = Commande.objects.filter(
            table__in=tables).order_by('-date_creation')
    else:
        tables = Table.objects.all()
        commandes = Commande.objects.all().order_by('-date_creation')

    return render(request, 'tables/serveur_dashboard.html', {
        'tables': tables,
        'commandes': commandes
    })
