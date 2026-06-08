import bcrypt
import jwt
from datetime import datetime, timezone, timedelta
from django.conf import settings
from bson.objectid import ObjectId
from .mongo_client import get_db

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_access_token(user_id: str, email: str) -> str:
    payload = {
        'sub': user_id,
        'email': email,
        'exp': datetime.now(timezone.utc) + timedelta(hours=24),
        'type': 'access'
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

def create_refresh_token(user_id: str) -> str:
    payload = {
        'sub': user_id,
        'exp': datetime.now(timezone.utc) + timedelta(days=7),
        'type': 'refresh'
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception('Token expiré')
    except jwt.InvalidTokenError:
        raise Exception('Token invalide')

def get_current_user(request):
    token = request.COOKIES.get('access_token')
    if not token:
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if auth_header.startswith('Bearer '):
            token = auth_header[7:]
    
    if not token:
        raise Exception('Non authentifié')
    
    payload = decode_token(token)
    if payload.get('type') != 'access':
        raise Exception('Type de token invalide')
    
    db = get_db()
    user = db.users.find_one({'_id': ObjectId(payload['sub'])})
    if not user:
        raise Exception('Utilisateur non trouvé')
    
    user['_id'] = str(user['_id'])
    user.pop('password_hash', None)
    return user

def seed_admin():
    db = get_db()
    admin_email = settings.ADMIN_EMAIL
    admin_password = settings.ADMIN_PASSWORD
    
    existing = db.users.find_one({'email': admin_email})
    if existing is None:
        hashed = hash_password(admin_password)
        db.users.insert_one({
            'email': admin_email,
            'password_hash': hashed,
            'name': 'Administrateur',
            'role': 'admin',
            'created_at': datetime.now(timezone.utc)
        })
        print(f'Admin créé: {admin_email}')
    elif not verify_password(admin_password, existing['password_hash']):
        db.users.update_one(
            {'email': admin_email},
            {'$set': {'password_hash': hash_password(admin_password)}}
        )
        print(f'Mot de passe admin mis à jour')
    
    db.users.create_index('email', unique=True)
    
    with open('/app/memory/test_credentials.md', 'w') as f:
        f.write('# Identifiants de test - Apotheosis ACE\n\n')
        f.write('## Admin\n')
        f.write(f'- Email: {admin_email}\n')
        f.write(f'- Mot de passe: {admin_password}\n')
        f.write(f'- Rôle: admin\n\n')
        f.write('## Points de terminaison API\n')
        f.write('- POST /api/auth/login\n')
        f.write('- POST /api/auth/logout\n')
        f.write('- GET /api/auth/me\n')
        f.write('- GET /api/tables\n')
        f.write('- POST /api/tables/create\n')
        f.write('- GET /api/menu\n')
        f.write('- POST /api/menu/create\n')
        f.write('- POST /api/guests/register\n')
        f.write('- POST /api/orders/create\n')
        f.write('- PUT /api/orders/<id>/update\n')
        f.write('- GET /api/admin/results\n')
