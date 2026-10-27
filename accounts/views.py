# accounts/views.py

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, UpdateView
from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import User
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


# accounts/views.py

# profile


@login_required
def profile_view(request):
  """Affiche simplement le profil de l'utilisateur connecté."""
  return render(request, 'accounts/profile.html')


# accounts/views.py
@login_required
def profile_edit_view(request):
  if request.method == 'POST':
    username = request.POST.get('username')
    email = request.POST.get('email')
    tel = request.POST.get('tel')
    photo = request.FILES.get('photo')  # 👈 Récupération du fichier image

    user = request.user
    if username:
      user.username = username
    if email is not None:
      user.email = email
    if tel is not None:
      user.tel = tel
    if photo:
      user.photo = photo  # 👈 Sauvegarde de la nouvelle photo

    user.save()
    messages.success(request, 'Votre profil a été mis à jour avec succès !')
    return redirect('accounts:profile')

  return render(request, 'accounts/profile_edit.html')

# Vue pour la page d'accueil globale
def home_view(request):
  return render(request, 'accounts/home.html')


# Connexion
# class CustomLoginView(LoginView):
#   template_name = 'accounts/login.html'
#   redirect_authenticated_user = True

#   def get_success_url(self):
#     # Rediriger vers la liste des utilisateurs ou une page d'accueil après connexion
#     return reverse_lazy('accounts:user_list')

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user
        if user.role == 'admin':
            return reverse('accounts:admin_dashboard')
        elif user.role == 'serveur':
            return reverse('tables:serveur_dashboard')
        elif user.role == 'cuisine':
            return reverse('commandes:cuisine_dashboard')
        return reverse('accounts:home')

# Déconnexion
# class CustomLogoutView(LogoutView):
#   next_page = 'accounts:home'


def CustomLogoutView(request):
  logout(request)
  return redirect('accounts:home')


# Inscription (Ajout d'un employé/admin)

class RegisterView(CreateView):
  model = User
  form_class = CustomUserCreationForm
  template_name = 'accounts/register.html'
  success_url = reverse_lazy('accounts:user_list')

  def form_valid(self, form):
    response = super().form_valid(form)
    messages.success(
        self.request,
        'Compte créé avec succès ! Il est actuellement inactif en attente'
        " d'activation par un administrateur.",
    )
    return response


# Liste des utilisateurs (pour voir les serveurs, cuisiniers, les activer/désactiver)
class UserListView(ListView):
  model = User
  template_name = 'accounts/user_list.html'
  context_object_name = 'users'


# accounts/views.py

User = get_user_model()


@login_required
def admin_dashboard(request):
  # Vérifier que l'utilisateur est admin ou superuser
  if not request.user.is_superuser and getattr(request.user, 'role', '') != 'admin':
    return redirect('accounts:home')

  # Récupérer tous les utilisateurs pour les afficher dans le dashboard
  users = User.objects.all().order_by('username')

  context = {
      'users': users,
  }

  return render(request, 'accounts/admin_dashboard.html', context)


# Modification d'un utilisateur (Changer rôle, Activer/Désactiver)
class UserUpdateView(UpdateView):
  model = User
  form_class = CustomUserChangeForm
  template_name = 'accounts/user_form.html'
  success_url = reverse_lazy('accounts:user_list')


# Vue pour activer ou désactiver un utilisateur en un clic
def toggle_user_status(request, pk):
  user = get_object_or_404(User, pk=pk)
  # Inverse le statut actuel (si True devient False, si False devient True)
  user.is_active = not user.is_active
  user.save()
  return redirect('accounts:user_list')
