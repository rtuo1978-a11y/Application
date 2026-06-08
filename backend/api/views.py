import json
from datetime import datetime, timezone, timedelta
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from bson.objectid import ObjectId
from .mongo_client import get_db
from .auth import hash_password, verify_password, create_access_token, create_refresh_token, get_current_user

def json_serialize(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f'Type {type(obj)} non sérialisable')

@csrf_exempt
@require_http_methods(['POST'])
def login_view(request):
    try:
        data = json.loads(request.body)
        email = data.get('email', '').lower().strip()
        password = data.get('password', '')
        
        if not email or not password:
            return JsonResponse({'detail': 'Email et mot de passe requis'}, status=400)
        
        db = get_db()
        user = db.users.find_one({'email': email})
        
        if not user or not verify_password(password, user['password_hash']):
            return JsonResponse({'detail': 'Email ou mot de passe incorrect'}, status=401)
        
        access_token = create_access_token(str(user['_id']), user['email'])
        refresh_token = create_refresh_token(str(user['_id']))
        
        response = JsonResponse({
            '_id': str(user['_id']),
            'email': user['email'],
            'name': user.get('name', ''),
            'role': user.get('role', 'user')
        })
        
        response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=True,
            secure=False,
            samesite='Lax',
            max_age=86400,
            path='/'
        )
        
        response.set_cookie(
            key='refresh_token',
            value=refresh_token,
            httponly=True,
            secure=False,
            samesite='Lax',
            max_age=604800,
            path='/'
        )
        
        return response
    except Exception as e:
        return JsonResponse({'detail': str(e)}, status=500)

@csrf_exempt
@require_http_methods(['POST'])
def logout_view(request):
    response = JsonResponse({'message': 'Déconnexion réussie'})
    response.delete_cookie('access_token', path='/')
    response.delete_cookie('refresh_token', path='/')
    return response

@csrf_exempt
@require_http_methods(['GET'])
def me_view(request):
    try:
        user = get_current_user(request)
        return JsonResponse(user)
    except Exception as e:
        return JsonResponse({'detail': str(e)}, status=401)

@csrf_exempt
@require_http_methods(['GET'])
def tables_view(request):
    try:
        db = get_db()
        tables = list(db.tables.find({}, {'_id': 0}).sort('table_number', 1))
        return JsonResponse(tables, safe=False)
    except Exception as e:
        return JsonResponse({'detail': str(e)}, status=500)

@csrf_exempt
@require_http_methods(['POST'])
def create_table_view(request):
    try:
        user = get_current_user(request)
        if user.get('role') != 'admin':
            return JsonResponse({'detail': 'Accès non autorisé'}, status=403)
        
        data = json.loads(request.body)
        table_number = data.get('table_number')
        places = data.get('places', 1)
        
        if not table_number:
            return JsonResponse({'detail': 'Numéro de table requis'}, status=400)
        
        db = get_db()
        existing = db.tables.find_one({'table_number': table_number})
        if existing:
            return JsonResponse({'detail': 'Ce numéro de table existe déjà'}, status=400)
        
        table = {
            'table_number': table_number,
            'places': places,
            'created_at': datetime.now(timezone.utc)
        }
        db.tables.insert_one(table)
        table.pop('_id', None)
        
        return JsonResponse(table, status=201)
    except Exception as e:
        return JsonResponse({'detail': str(e)}, status=500)

@csrf_exempt
@require_http_methods(['GET'])
def menu_view(request):
    try:
        db = get_db()
        dishes = list(db.dishes.find({}, {'_id': 0}))
        return JsonResponse(dishes, safe=False)
    except Exception as e:
        return JsonResponse({'detail': str(e)}, status=500)

@csrf_exempt
@require_http_methods(['POST'])
def create_dish_view(request):
    try:
        user = get_current_user(request)
        if user.get('role') != 'admin':
            return JsonResponse({'detail': 'Accès non autorisé'}, status=403)
        
        data = json.loads(request.body)
        name = data.get('name', '').strip()
        description = data.get('description', '').strip()
        
        if not name:
            return JsonResponse({'detail': 'Nom du plat requis'}, status=400)
        
        db = get_db()
        dish = {
            'name': name,
            'description': description,
            'created_at': datetime.now(timezone.utc)
        }
        result = db.dishes.insert_one(dish)
        dish['_id'] = str(result.inserted_id)
        
        return JsonResponse(dish, status=201)
    except Exception as e:
        return JsonResponse({'detail': str(e)}, status=500)

@csrf_exempt
@require_http_methods(['POST'])
def register_guest_view(request):
    try:
        data = json.loads(request.body)
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        table_number = data.get('table_number')
        
        if not name or not table_number:
            return JsonResponse({'detail': 'Nom et numéro de table requis'}, status=400)
        
        db = get_db()
        table = db.tables.find_one({'table_number': table_number})
        if not table:
            return JsonResponse({'detail': 'Table non trouvée'}, status=404)
        
        guest = {
            'name': name,
            'email': email,
            'table_number': table_number,
            'registration_time': datetime.now(timezone.utc)
        }
        result = db.guests.insert_one(guest)
        guest['_id'] = str(result.inserted_id)
        
        return JsonResponse(guest, status=201)
    except Exception as e:
        return JsonResponse({'detail': str(e)}, status=500)

@csrf_exempt
@require_http_methods(['GET'])
def guest_detail_view(request, guest_id):
    try:
        db = get_db()
        guest = db.guests.find_one({'_id': ObjectId(guest_id)})
        if not guest:
            return JsonResponse({'detail': 'Invité non trouvé'}, status=404)
        
        guest['_id'] = str(guest['_id'])
        return JsonResponse(guest)
    except Exception as e:
        return JsonResponse({'detail': str(e)}, status=500)

@csrf_exempt
@require_http_methods(['POST'])
def create_order_view(request):
    try:
        data = json.loads(request.body)
        guest_id = data.get('guest_id')
        dish_name = data.get('dish_name', '').strip()
        
        if not guest_id or not dish_name:
            return JsonResponse({'detail': 'ID invité et nom du plat requis'}, status=400)
        
        db = get_db()
        guest = db.guests.find_one({'_id': ObjectId(guest_id)})
        if not guest:
            return JsonResponse({'detail': 'Invité non trouvé'}, status=404)
        
        existing_order = db.orders.find_one({'guest_id': guest_id})
        if existing_order:
            return JsonResponse({'detail': 'Une commande existe déjà pour cet invité'}, status=400)
        
        order = {
            'guest_id': guest_id,
            'dish_name': dish_name,
            'created_at': datetime.now(timezone.utc),
            'locked_at': datetime.now(timezone.utc) + timedelta(minutes=2),
            'is_locked': False
        }
        result = db.orders.insert_one(order)
        order['_id'] = str(result.inserted_id)
        
        return JsonResponse(order, status=201)
    except Exception as e:
        return JsonResponse({'detail': str(e)}, status=500)

@csrf_exempt
@require_http_methods(['PUT'])
def update_order_view(request, order_id):
    try:
        data = json.loads(request.body)
        dish_name = data.get('dish_name', '').strip()
        
        if not dish_name:
            return JsonResponse({'detail': 'Nom du plat requis'}, status=400)
        
        db = get_db()
        order = db.orders.find_one({'_id': ObjectId(order_id)})
        if not order:
            return JsonResponse({'detail': 'Commande non trouvée'}, status=404)
        
        now = datetime.now(timezone.utc)
        if now > order['locked_at'] or order.get('is_locked'):
            return JsonResponse({'detail': 'La période de modification est expirée (2 minutes)'}, status=400)
        
        db.orders.update_one(
            {'_id': ObjectId(order_id)},
            {'$set': {'dish_name': dish_name}}
        )
        
        updated_order = db.orders.find_one({'_id': ObjectId(order_id)})
        updated_order['_id'] = str(updated_order['_id'])
        
        return JsonResponse(updated_order)
    except Exception as e:
        return JsonResponse({'detail': str(e)}, status=500)

@csrf_exempt
@require_http_methods(['GET'])
def admin_results_view(request):
    try:
        user = get_current_user(request)
        if user.get('role') != 'admin':
            return JsonResponse({'detail': 'Accès non autorisé'}, status=403)
        
        db = get_db()
        tables = list(db.tables.find({}).sort('table_number', 1))
        
        results = []
        for table in tables:
            table_number = table['table_number']
            guests = list(db.guests.find({'table_number': table_number}))
            
            orders_data = []
            for guest in guests:
                guest_id = str(guest['_id'])
                order = db.orders.find_one({'guest_id': guest_id})
                if order:
                    orders_data.append({
                        'guest_name': guest['name'],
                        'dish_name': order['dish_name']
                    })
            
            results.append({
                'table_number': table_number,
                'places': table.get('places', 0),
                'orders': orders_data
            })
        
        return JsonResponse(results, safe=False)
    except Exception as e:
        return JsonResponse({'detail': str(e)}, status=500)

@csrf_exempt
@require_http_methods(['GET'])
def gallery_view(request):
    gallery_images = [
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
        }
    ]
    return JsonResponse(gallery_images, safe=False)
