# Apotheosis ACE — Application Django de gestion de banquet pour église

Application web Django pour gérer un banquet d'église : tables, menu, inscriptions invités et choix de plats avec une période de modification de 2 minutes.

## Stack technique

- **Backend & Frontend** : Django 5.2 (templates HTML)
- **Base de données** : SQLite (intégrée à Django)
- **Style** : Tailwind CSS (via CDN) + polices Google Fonts
- **Icônes** : Lucide Icons (via CDN)
- **Langue** : Français
- **Couleurs** : Or (#D4AF37), Vert sapin (#0F2F20), Blanc, Noir

## Fonctionnalités

### Espace public (invités)
- Page d'accueil avec versets bibliques
- Inscription au banquet (nom, email optionnel, sélection de table)
- Choix de plat avec menu dynamique
- **Modification possible pendant 2 minutes** puis verrouillage automatique
- Galerie sacrée avec images religieuses et versets

### Espace administrateur
- Connexion sécurisée par mot de passe
- Tableau de bord avec statistiques
- Gestion des tables (créer/supprimer, avec nombre de places)
- Gestion du menu (créer/supprimer des plats, pas de limite)
- **Vue résultats** : tables en ordre numérique avec les commandes (1 - plat, 2 - plat...)

## Installation locale

### Prérequis
- Python 3.11+
- pip

### Étapes

```bash
# 1. Cloner ou télécharger le projet
cd backend/

# 2. Créer un environnement virtuel
python -m venv venv

# Activer l'environnement
# Linux/Mac :
source venv/bin/activate
# Windows :
venv\Scripts\activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Créer le fichier .env (voir section ci-dessous)

# 5. Appliquer les migrations
python manage.py migrate

# 6. Créer le superutilisateur admin
python manage.py seed_admin

# 7. Lancer le serveur
python manage.py runserver
```

L'application sera accessible sur **http://localhost:8000**.

## Fichier .env

Créez `backend/.env` :

```
DJANGO_SECRET_KEY="changez-cette-cle-en-production"
ADMIN_USERNAME="admin"
ADMIN_EMAIL="admin@apotheosis.com"
ADMIN_PASSWORD="apotheosis2026"
```

## Identifiants admin par défaut

- **Nom d'utilisateur** : `admin`
- **Mot de passe** : `apotheosis2026`
- URL admin : `/admin-panel/login/`

## Déploiement sur PythonAnywhere

Voir le fichier [`DEPLOY_PYTHONANYWHERE.md`](DEPLOY_PYTHONANYWHERE.md) pour les instructions détaillées.

## Structure du projet

```
backend/
├── apotheosis/              # Configuration Django
│   ├── settings.py          # Paramètres
│   ├── urls.py              # URLs principales
│   └── wsgi.py
├── banquet/                 # Application principale
│   ├── models.py            # Modèles (Table, Dish, Guest, Order)
│   ├── views.py             # Vues (controllers)
│   ├── forms.py             # Formulaires
│   ├── urls.py              # URLs de l'app
│   ├── admin.py             # Configuration admin Django
│   ├── templates/banquet/   # Templates HTML
│   │   ├── base.html
│   │   ├── welcome.html
│   │   ├── register.html
│   │   ├── dish_selection.html
│   │   ├── gallery.html
│   │   ├── admin_login.html
│   │   ├── admin_dashboard.html
│   │   ├── admin_tables.html
│   │   ├── admin_menu.html
│   │   └── admin_results.html
│   └── management/commands/
│       └── seed_admin.py    # Création admin
├── db.sqlite3               # Base de données SQLite
├── manage.py
├── requirements.txt
└── .env
```

## Modèles de données

- **Table** : numéro de table, nombre de places
- **Dish** : nom du plat, description
- **Guest** : nom, email, table
- **Order** : commande d'un invité (plat choisi, créée_à) — verrouillage après 2 minutes

## Routes principales

| URL | Description |
|-----|-------------|
| `/` | Page d'accueil |
| `/register/` | Inscription invité |
| `/menu/<id>/` | Choix de plat |
| `/gallery/` | Galerie sacrée |
| `/admin-panel/login/` | Connexion admin |
| `/admin-panel/dashboard/` | Tableau de bord |
| `/admin-panel/tables/` | Gestion tables |
| `/admin-panel/menu/` | Gestion menu |
| `/admin-panel/results/` | Voir les résultats |
| `/django-admin/` | Interface admin Django |
