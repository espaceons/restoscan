# commandes/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from .models import Commande
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from menu.models import Plat
from tables.models import Table
from .models import Commande, LigneCommande
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import get_user_model

User = get_user_model()


# commandes/views.py
from .models import Commande

@login_required
def cuisine_dashboard(request):
    # Le cuisinier a besoin de voir les commandes en attente et en préparation
    commandes = Commande.objects.filter(
        statut__in=['en_attente', 'en_preparation']).order_by('date_creation')
    return render(request, 'commandes/cuisine_dashboard.html', {'commandes': commandes})


# commandes/views.py
@method_decorator(login_required, name='dispatch')
class CommandeCreateView(View):

    def get(self, request):
        user = request.user
        # Si c'est un admin, il voit toutes les tables. Si c'est un serveur, il ne voit que ses tables.
        if user.is_superuser or getattr(user, 'role', '') == 'admin':
            tables = Table.objects.all()
        else:
            tables = Table.objects.filter(serveur=user)

        plats = Plat.objects.filter(disponible_du_jour=True)

        return render(
            request,
            'commandes/commande_form.html',
            {'tables': tables, 'plats': plats}
        )

    def post(self, request):
        table_id = request.POST.get('table')
        table = get_object_or_404(Table, pk=table_id)

        # 🎯 Le serveur de la commande devient automatiquement le serveur assigné à cette table !
        # Si aucun serveur n'est assigné à la table, on prend l'utilisateur connecté par défaut (ex: l'admin).
        serveur_commande = table.serveur if table.serveur else request.user

        # 1. Créer la commande principale
        commande = Commande.objects.create(
            table=table,
            serveur=serveur_commande,
            statut='en_attente'
        )

        # 2. Récupérer les plats et quantités soumis depuis le formulaire
        for key, value in request.POST.items():
            if key.startswith('plat_') and int(value) > 0:
                plat_id = key.split('_')[1]
                plat = get_object_or_404(Plat, pk=plat_id)
                quantite = int(value)

                LigneCommande.objects.create(
                    commande=commande,
                    plat=plat,
                    quantite=quantite
                )

        return redirect('commandes:commande_list')


@method_decorator(login_required, name='dispatch')
class CommandeListView(ListView):
    model = Commande
    template_name = 'commandes/commande_list.html'
    context_object_name = 'commandes'
    ordering = ['-date_creation']  # Les commandes les plus récentes en premier


@login_required
def update_commande_status(request, pk, statut):
    """Permet de faire progresser le statut d'une commande (ex: passer en préparation, prête, etc.)"""
    commande = get_object_or_404(Commande, pk=pk)

    # Vérifie si le statut demandé fait bien partie des choix autorisés
    valid_statuts = dict(Commande.STATUT_CHOICES).keys()
    if statut in valid_statuts:
        commande.statut = statut

        # Si aucun serveur n'est assigné et qu'un utilisateur agit, on peut l'enregistrer comme responsable
        if not commande.serveur and request.user.is_authenticated:
            commande.serveur = request.user

        commande.save()

    return redirect('commandes:commande_list')
