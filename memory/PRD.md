# PRD - Apotheosis ACE

## Problem Statement
Application de gestion de banquet pour une église. L'admin enregistre des tables numérotées avec un nombre de places et crée le menu. Les invités s'inscrivent sur la page d'accueil et, en fonction de leur numéro de table, ajoutent le plat qu'ils souhaitent. Sur la page admin, panneau "Voir les résultats" affichant les différentes tables dans l'ordre numérique et les différents plats demandés (1 - tel plat...). Possible d'ajouter autant de places que nécessaire à une table. Couleurs : or, vert sapin, blanc et noir. Titre : "Apotheosis ACE". Application en français avec versets bibliques et images de château doré au paradis avec arrière-plan vert sapin. Pour une église, bien décorée, fonctionnelle avec galerie intégrée. Utilise Django et Python. BD intégrée à Django (SQLite). Déployable sur PythonAnywhere.

## Stack
- Django 5.2 (templates HTML + ORM)
- SQLite (intégrée à Django)
- Tailwind CSS via CDN
- Lucide Icons
- Polices : Cormorant Garamond + Outfit
- Gunicorn (serveur production)
- Whitenoise (fichiers statiques)

## User Personas
1. **Administrateur d'église** : crée et gère les tables, le menu, consulte les résultats
2. **Invité du banquet** : s'inscrit, choisit son plat, peut modifier 2 min

## Core Requirements (statiques)
- Connexion admin sécurisée (Django auth)
- CRUD tables (numéro + places)
- CRUD plats (sans limite)
- Inscription invité (nom, email optionnel, table)
- Sélection de plat avec timer 2 minutes
- Verrouillage automatique après 2 minutes
- Page résultats par table en ordre numérique
- Galerie d'images religieuses
- Tout en français avec versets bibliques
- Couleurs : or (#D4AF37), vert sapin (#0F2F20), blanc, noir

## What's been implemented (08/06/2026)
- ✅ Configuration Django (settings, urls, wsgi)
- ✅ Modèles : Table, Dish, Guest, Order, **Candidate, Vote**
- ✅ Vues publiques : welcome, register, dish_selection, gallery, **vote, cast_vote**
- ✅ Vues admin : login, logout, dashboard, tables, menu, results, **candidates, vote_results**
- ✅ Formulaires Django (TableForm, DishForm, GuestForm, LoginForm, **CandidateForm avec ImageField**)
- ✅ 13 templates HTML avec design or/vert sapin
- ✅ Timer JavaScript pour décompte 2 minutes
- ✅ Galerie de 4 images religieuses avec versets
- ✅ **Vote présidentiel ACE** : candidats avec photo, vote unique par session, statistiques admin
- ✅ Configuration MEDIA pour uploads de photos
- ✅ Commande seed_admin pour création automatique admin
- ✅ Migrations SQLite appliquées (incluant Candidate + Vote)
- ✅ Documentation README.md
- ✅ Guide de déploiement PythonAnywhere

## Backlog (P1/P2 - améliorations futures)
- P1 : Export CSV/PDF des résultats par table
- P1 : Email de confirmation aux invités (avec leur table et plat)
- P2 : QR code par invité pour confirmer présence le jour J
- P2 : Statistiques avancées (plats les plus demandés)
- P2 : Possibilité d'ajouter des photos pour chaque plat
- P2 : Mode multi-événement (gérer plusieurs banquets)
- P2 : Personnalisation du verset et du titre par l'admin

## Identifiants admin
- Username: `admin`
- Password: `apotheosis2026`
