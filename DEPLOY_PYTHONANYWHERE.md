# Déploiement sur PythonAnywhere

Guide pas-à-pas pour déployer **Apotheosis ACE** sur [PythonAnywhere](https://www.pythonanywhere.com/).

## 1. Créer un compte PythonAnywhere

- Aller sur [pythonanywhere.com](https://www.pythonanywhere.com/) et créer un compte gratuit ("Beginner").
- Le compte gratuit suffit pour une église de taille modeste.

## 2. Téléverser le code

### Option A : Via Git (recommandé)

1. Pousser votre code sur GitHub.
2. Ouvrir une console Bash sur PythonAnywhere : `Consoles → Bash`.
3. Cloner le projet :
   ```bash
   git clone https://github.com/VOTRE-USER/apotheosis-ace.git
   cd apotheosis-ace/backend
   ```

### Option B : Via upload ZIP

1. Compresser le dossier `backend/` en ZIP.
2. Aller dans `Files` sur PythonAnywhere et téléverser le ZIP.
3. Décompresser via la console : `unzip backend.zip`.

## 3. Créer un environnement virtuel

Dans la console Bash :

```bash
cd ~/apotheosis-ace/backend
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 4. Configurer le fichier .env

Créer `backend/.env` :

```bash
nano .env
```

Contenu :
```
DJANGO_SECRET_KEY="GENEREZ_UNE_CLE_ALEATOIRE_DE_50_CARACTERES"
ADMIN_USERNAME="admin"
ADMIN_EMAIL="admin@votre-eglise.com"
ADMIN_PASSWORD="MotDePasseSecurise2026"
```

Pour générer une clé secrète :
```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

## 5. Préparer la base de données

```bash
python manage.py migrate
python manage.py seed_admin
python manage.py collectstatic --noinput
```

## 6. Créer une application Web

1. Sur PythonAnywhere, aller dans **Web → Add a new web app**.
2. Choisir **Manual configuration** (PAS Django, on configure manuellement).
3. Sélectionner **Python 3.11**.

## 7. Configurer le chemin du code

Dans la section **"Code"** de la page Web :

- **Source code** : `/home/VOTRE-USER/apotheosis-ace/backend`
- **Working directory** : `/home/VOTRE-USER/apotheosis-ace/backend`

## 8. Configurer le fichier WSGI

Cliquer sur le fichier WSGI (lien dans la section "Code") et remplacer **tout** le contenu par :

```python
import os
import sys

# Chemin du projet
project_home = '/home/VOTRE-USER/apotheosis-ace/backend'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Charger les variables d'environnement depuis .env
from dotenv import load_dotenv
load_dotenv(os.path.join(project_home, '.env'))

# Configurer Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'apotheosis.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**Remplacez `VOTRE-USER` par votre nom d'utilisateur PythonAnywhere.**

## 9. Configurer l'environnement virtuel

Dans la section **"Virtualenv"** :
- Saisir : `/home/VOTRE-USER/apotheosis-ace/backend/venv`

## 10. Configurer les fichiers statiques

Dans la section **"Static files"**, ajouter :

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/VOTRE-USER/apotheosis-ace/backend/staticfiles` |

## 11. Ajuster les paramètres Django pour la production

Éditer `apotheosis/settings.py` sur PythonAnywhere :

```python
DEBUG = False
ALLOWED_HOSTS = ['VOTRE-USER.pythonanywhere.com']

CSRF_TRUSTED_ORIGINS = [
    'https://VOTRE-USER.pythonanywhere.com',
]
```

## 12. Lancer l'application

1. Retourner sur la page **Web** de PythonAnywhere.
2. Cliquer sur le gros bouton vert **"Reload"**.
3. Visiter `https://VOTRE-USER.pythonanywhere.com/`.

## 13. Accès admin

- URL : `https://VOTRE-USER.pythonanywhere.com/admin-panel/login/`
- Nom d'utilisateur : `admin`
- Mot de passe : celui défini dans `.env`

## Mise à jour future

Pour mettre à jour l'application :

```bash
cd ~/apotheosis-ace
git pull
cd backend
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```

Puis cliquer sur **"Reload"** dans la page Web de PythonAnywhere.

## Sauvegarde de la base de données

La base SQLite se trouve dans `backend/db.sqlite3`. Pour la sauvegarder :

```bash
cp ~/apotheosis-ace/backend/db.sqlite3 ~/backup-$(date +%Y%m%d).sqlite3
```

## Conseils

- **Sécurité** : changez immédiatement le mot de passe admin par défaut.
- **HTTPS** : PythonAnywhere fournit HTTPS gratuitement.
- **Domaine personnalisé** : disponible avec un compte payant.

## Dépannage

### Erreur "DisallowedHost"
→ Ajouter le domaine dans `ALLOWED_HOSTS` dans `settings.py`.

### Erreur CSRF
→ Ajouter le domaine dans `CSRF_TRUSTED_ORIGINS` dans `settings.py`.

### Fichiers statiques manquants
→ Exécuter `python manage.py collectstatic --noinput` et vérifier la configuration Static files.

### Logs d'erreur
- **Error log** : disponible sur la page Web de PythonAnywhere.
- **Server log** : également accessible depuis cette page.

## Coûts

- **Compte Beginner (gratuit)** : 1 application Web, 512 MB de stockage, suffisant pour une église
- **Compte Hacker (5 USD/mois)** : domaine personnalisé, plus de stockage
