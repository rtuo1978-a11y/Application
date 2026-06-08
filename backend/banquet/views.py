"""
Vues (controllers) Django pour l'application Apotheosis ACE.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from .models import Table, Dish, Guest, Order, Candidate, Vote
from .forms import TableForm, DishForm, GuestForm, LoginForm, CandidateForm


# ============ Images de la galerie sacrée ============
GALLERY_IMAGES = [
    {
        'url': 'https://images.unsplash.com/flagged/photo-1572392640988-ba48d1a74457',
        'description': 'Fresque de plafond baroque',
        'verse': '« Car Dieu a tant aimé le monde » - Jean 3:16'
    },
    {
        'url': 'https://images.unsplash.com/photo-1584727638096-042c45049ebe',
        'description': 'Moine en prière',
        'verse': '« Heureux les cœurs purs, car ils verront Dieu » - Matthieu 5:8'
    },
    {
        'url': 'https://images.unsplash.com/photo-1532337414163-b344fcae7bc2',
        'description': 'Agneau sur la Bible',
        'verse': '« Voici l\'Agneau de Dieu » - Jean 1:29'
    },
    {
        'url': 'https://images.unsplash.com/photo-1583119912267-cc97c911e416',
        'description': 'Fresque avec chérubins',
        'verse': '« Les anges se réjouissent dans le ciel » - Luc 15:10'
    },
]


def is_admin(user):
    """Vérifie si l'utilisateur est administrateur."""
    return user.is_authenticated and user.is_staff


# ============ Pages publiques (invités) ============

def welcome_view(request):
    """Page d'accueil du banquet."""
    return render(request, 'banquet/welcome.html')


def gallery_view(request):
    """Galerie d'images religieuses."""
    return render(request, 'banquet/gallery.html', {'gallery': GALLERY_IMAGES})


def register_guest_view(request):
    """Inscription d'un nouvel invité."""
    if not Table.objects.exists():
        messages.warning(request, 'Aucune table n\'est encore disponible. Veuillez patienter.')
        return redirect('welcome')
    
    if request.method == 'POST':
        form = GuestForm(request.POST)
        if form.is_valid():
            guest = form.save()
            messages.success(request, f'Bienvenue {guest.name} ! Choisissez votre plat.')
            return redirect('dish_selection', guest_id=guest.id)
    else:
        form = GuestForm()
    
    return render(request, 'banquet/register.html', {'form': form})


def dish_selection_view(request, guest_id):
    """Sélection ou modification du plat par un invité."""
    guest = get_object_or_404(Guest, id=guest_id)
    dishes = Dish.objects.all()
    
    if not dishes.exists():
        messages.warning(request, 'Aucun plat n\'est encore disponible au menu.')
        return redirect('welcome')
    
    existing_order = Order.objects.filter(guest=guest).first()
    
    if request.method == 'POST':
        dish_id = request.POST.get('dish_id')
        if not dish_id:
            messages.error(request, 'Veuillez sélectionner un plat.')
        else:
            dish = get_object_or_404(Dish, id=dish_id)
            
            if existing_order:
                if existing_order.is_locked:
                    messages.error(request, 'La période de modification est expirée (2 minutes).')
                else:
                    existing_order.dish = dish
                    existing_order.save()
                    messages.success(request, f'Votre plat a été modifié : {dish.name}')
            else:
                Order.objects.create(guest=guest, dish=dish)
                messages.success(request, f'Plat sélectionné : {dish.name}. Vous avez 2 minutes pour modifier.')
            
            return redirect('dish_selection', guest_id=guest.id)
    
    return render(request, 'banquet/dish_selection.html', {
        'guest': guest,
        'dishes': dishes,
        'existing_order': existing_order,
    })


def order_status_api(request, order_id):
    """API JSON pour obtenir le statut d'une commande (utilisé par le timer JS)."""
    order = get_object_or_404(Order, id=order_id)
    return JsonResponse({
        'is_locked': order.is_locked,
        'seconds_remaining': order.seconds_remaining,
        'dish_name': order.dish.name,
    })


# ============ Pages administrateur ============

def admin_login_view(request):
    """Connexion de l'administrateur."""
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None and user.is_staff:
                login(request, user)
                messages.success(request, f'Bienvenue {user.username}')
                return redirect('admin_dashboard')
            else:
                messages.error(request, 'Identifiants incorrects ou accès refusé.')
    else:
        form = LoginForm()
    
    return render(request, 'banquet/admin_login.html', {'form': form})


@login_required(login_url='/admin-panel/login/')
def admin_logout_view(request):
    """Déconnexion de l'administrateur."""
    logout(request)
    messages.info(request, 'Vous êtes déconnecté.')
    return redirect('welcome')


@user_passes_test(is_admin, login_url='/admin-panel/login/')
def admin_dashboard_view(request):
    """Tableau de bord administrateur."""
    stats = {
        'total_tables': Table.objects.count(),
        'total_dishes': Dish.objects.count(),
        'total_guests': Guest.objects.count(),
        'total_orders': Order.objects.count(),
        'total_candidates': Candidate.objects.count(),
        'total_votes': Vote.objects.count(),
    }
    return render(request, 'banquet/admin_dashboard.html', {'stats': stats})


@user_passes_test(is_admin, login_url='/admin-panel/login/')
def admin_tables_view(request):
    """Gestion des tables."""
    if request.method == 'POST':
        form = TableForm(request.POST)
        if form.is_valid():
            table = form.save()
            messages.success(request, f'Table {table.table_number} créée avec succès.')
            return redirect('admin_tables')
    else:
        form = TableForm()
    
    tables = Table.objects.all().order_by('table_number')
    return render(request, 'banquet/admin_tables.html', {
        'form': form,
        'tables': tables
    })


@user_passes_test(is_admin, login_url='/admin-panel/login/')
def admin_delete_table_view(request, table_id):
    """Supprimer une table."""
    table = get_object_or_404(Table, id=table_id)
    if request.method == 'POST':
        table_number = table.table_number
        table.delete()
        messages.success(request, f'Table {table_number} supprimée.')
    return redirect('admin_tables')


@user_passes_test(is_admin, login_url='/admin-panel/login/')
def admin_menu_view(request):
    """Gestion du menu."""
    if request.method == 'POST':
        form = DishForm(request.POST)
        if form.is_valid():
            dish = form.save()
            messages.success(request, f'Plat "{dish.name}" ajouté au menu.')
            return redirect('admin_menu')
    else:
        form = DishForm()
    
    dishes = Dish.objects.all().order_by('name')
    return render(request, 'banquet/admin_menu.html', {
        'form': form,
        'dishes': dishes
    })


@user_passes_test(is_admin, login_url='/admin-panel/login/')
def admin_delete_dish_view(request, dish_id):
    """Supprimer un plat."""
    dish = get_object_or_404(Dish, id=dish_id)
    if request.method == 'POST':
        dish_name = dish.name
        dish.delete()
        messages.success(request, f'Plat "{dish_name}" supprimé.')
    return redirect('admin_menu')


@user_passes_test(is_admin, login_url='/admin-panel/login/')
def admin_results_view(request):
    """Vue des résultats : tables en ordre numérique avec les plats commandés."""
    tables = Table.objects.all().order_by('table_number').prefetch_related('guests__order__dish')
    
    results = []
    for table in tables:
        guests_with_orders = []
        for guest in table.guests.all():
            order = Order.objects.filter(guest=guest).first()
            guests_with_orders.append({
                'guest': guest,
                'order': order,
            })
        results.append({
            'table': table,
            'guests': guests_with_orders,
        })
    
    return render(request, 'banquet/admin_results.html', {'results': results})


# ============ Vote Présidentiel ACE ============

def vote_view(request):
    """Page de vote présidentiel pour élire le leader ACE."""
    # S'assurer qu'une session existe
    if not request.session.session_key:
        request.session.save()
    
    session_key = request.session.session_key
    candidates = Candidate.objects.all()
    user_vote = Vote.objects.filter(session_key=session_key).first()
    
    return render(request, 'banquet/vote.html', {
        'candidates': candidates,
        'user_vote': user_vote,
        'has_voted': user_vote is not None,
    })


def cast_vote_view(request):
    """Enregistre le vote d'un utilisateur (une fois par session)."""
    if request.method != 'POST':
        return redirect('vote')
    
    if not request.session.session_key:
        request.session.save()
    session_key = request.session.session_key
    
    # Vérifier si l'utilisateur a déjà voté
    if Vote.objects.filter(session_key=session_key).exists():
        messages.warning(request, 'Vous avez déjà voté. Une seule voix est autorisée par personne.')
        return redirect('vote')
    
    candidate_id = request.POST.get('candidate_id')
    if not candidate_id:
        messages.error(request, 'Veuillez sélectionner un candidat.')
        return redirect('vote')
    
    candidate = get_object_or_404(Candidate, id=candidate_id)
    Vote.objects.create(candidate=candidate, session_key=session_key)
    messages.success(request, f'Votre vote pour {candidate.name} a été enregistré. Merci !')
    return redirect('vote')


@user_passes_test(is_admin, login_url='/admin-panel/login/')
def admin_candidates_view(request):
    """Gestion des candidats à l'élection ACE."""
    if request.method == 'POST':
        form = CandidateForm(request.POST, request.FILES)
        if form.is_valid():
            candidate = form.save()
            messages.success(request, f'Candidat "{candidate.name}" ajouté avec succès.')
            return redirect('admin_candidates')
    else:
        form = CandidateForm()
    
    candidates = Candidate.objects.all().order_by('name')
    return render(request, 'banquet/admin_candidates.html', {
        'form': form,
        'candidates': candidates
    })


@user_passes_test(is_admin, login_url='/admin-panel/login/')
def admin_delete_candidate_view(request, candidate_id):
    """Supprimer un candidat."""
    candidate = get_object_or_404(Candidate, id=candidate_id)
    if request.method == 'POST':
        name = candidate.name
        # Supprimer aussi la photo du système de fichiers
        if candidate.photo:
            candidate.photo.delete(save=False)
        candidate.delete()
        messages.success(request, f'Candidat "{name}" supprimé.')
    return redirect('admin_candidates')


@user_passes_test(is_admin, login_url='/admin-panel/login/')
def admin_vote_results_view(request):
    """Statistiques de vote pour l'élection ACE (visible admin uniquement)."""
    candidates = Candidate.objects.all()
    total_votes = Vote.objects.count()
    
    results = []
    for candidate in candidates:
        count = candidate.vote_count
        percentage = (count / total_votes * 100) if total_votes > 0 else 0
        results.append({
            'candidate': candidate,
            'count': count,
            'percentage': round(percentage, 1),
        })
    
    # Trier par nombre de votes décroissant
    results.sort(key=lambda x: x['count'], reverse=True)
    
    winner = results[0] if results and results[0]['count'] > 0 else None
    
    return render(request, 'banquet/admin_vote_results.html', {
        'results': results,
        'total_votes': total_votes,
        'winner': winner,
    })
