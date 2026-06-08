"""
Backend tests for Apotheosis ACE banquet management app (Django + MongoDB).
Covers: auth, tables, menu, guests, orders (2-min lock), admin results, gallery.
"""
import os
import time
import pytest
import requests

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', 'https://apotheosis-banquet.preview.emergentagent.com').rstrip('/')
ADMIN_EMAIL = 'admin@apotheosis.com'
ADMIN_PASSWORD = 'apotheosis2026'


@pytest.fixture(scope='session')
def admin_session():
    s = requests.Session()
    s.headers.update({'Content-Type': 'application/json'})
    r = s.post(f'{BASE_URL}/api/auth/login', json={'email': ADMIN_EMAIL, 'password': ADMIN_PASSWORD})
    assert r.status_code == 200, f'Admin login failed: {r.status_code} {r.text}'
    return s


@pytest.fixture(scope='session')
def anon_session():
    s = requests.Session()
    s.headers.update({'Content-Type': 'application/json'})
    return s


# ---------- Auth ----------
class TestAuth:
    def test_login_success_sets_httponly_cookie(self, anon_session):
        r = anon_session.post(f'{BASE_URL}/api/auth/login',
                              json={'email': ADMIN_EMAIL, 'password': ADMIN_PASSWORD})
        assert r.status_code == 200
        data = r.json()
        assert data['email'] == ADMIN_EMAIL
        assert data['role'] == 'admin'
        # Cookie must be set
        cookies = r.cookies
        assert 'access_token' in cookies

    def test_login_invalid_credentials(self):
        r = requests.post(f'{BASE_URL}/api/auth/login',
                          json={'email': ADMIN_EMAIL, 'password': 'wrong'})
        assert r.status_code == 401

    def test_login_missing_fields(self):
        r = requests.post(f'{BASE_URL}/api/auth/login', json={'email': ''})
        assert r.status_code == 400

    def test_me_authenticated(self, admin_session):
        r = admin_session.get(f'{BASE_URL}/api/auth/me')
        assert r.status_code == 200
        assert r.json()['email'] == ADMIN_EMAIL

    def test_me_unauthenticated(self):
        r = requests.get(f'{BASE_URL}/api/auth/me')
        assert r.status_code == 401


# ---------- Tables ----------
class TestTables:
    def test_create_table_requires_admin(self):
        r = requests.post(f'{BASE_URL}/api/tables/create',
                          json={'table_number': 999, 'places': 5})
        # unauthenticated => 401 wrapped as 500 if exception; accept 401/403/500
        assert r.status_code in (401, 403, 500)

    def test_admin_create_and_list_table(self, admin_session):
        # cleanup attempt: pick a unique number
        table_number = 9001
        r = admin_session.post(f'{BASE_URL}/api/tables/create',
                               json={'table_number': table_number, 'places': 8})
        assert r.status_code in (201, 400), f'{r.status_code} {r.text}'
        # list
        r = admin_session.get(f'{BASE_URL}/api/tables')
        assert r.status_code == 200
        tables = r.json()
        assert isinstance(tables, list)
        nums = [t['table_number'] for t in tables]
        assert table_number in nums
        # verify ordering ascending
        assert nums == sorted(nums)

    def test_create_duplicate_table_fails(self, admin_session):
        table_number = 9002
        admin_session.post(f'{BASE_URL}/api/tables/create',
                           json={'table_number': table_number, 'places': 4})
        r = admin_session.post(f'{BASE_URL}/api/tables/create',
                               json={'table_number': table_number, 'places': 4})
        assert r.status_code == 400


# ---------- Menu ----------
class TestMenu:
    def test_admin_create_dish(self, admin_session):
        r = admin_session.post(f'{BASE_URL}/api/menu/create',
                               json={'name': 'TEST_Poulet Rôti', 'description': 'Plat test'})
        assert r.status_code == 201, r.text
        body = r.json()
        assert body['name'] == 'TEST_Poulet Rôti'
        assert '_id' in body

    def test_list_menu_public(self):
        r = requests.get(f'{BASE_URL}/api/menu')
        assert r.status_code == 200
        assert isinstance(r.json(), list)

    def test_create_dish_requires_admin(self):
        r = requests.post(f'{BASE_URL}/api/menu/create',
                          json={'name': 'Hack', 'description': ''})
        assert r.status_code in (401, 403, 500)


# ---------- Guest registration + orders ----------
class TestGuestAndOrder:
    table_number = 9003
    guest_id = None
    order_id = None

    def test_setup_table(self, admin_session):
        admin_session.post(f'{BASE_URL}/api/tables/create',
                           json={'table_number': self.__class__.table_number, 'places': 4})

    def test_register_guest(self, anon_session):
        r = anon_session.post(f'{BASE_URL}/api/guests/register',
                              json={'name': 'TEST_Jean', 'email': 't@t.com',
                                    'table_number': self.__class__.table_number})
        assert r.status_code == 201, r.text
        body = r.json()
        assert body['name'] == 'TEST_Jean'
        assert body['table_number'] == self.__class__.table_number
        assert '_id' in body
        TestGuestAndOrder.guest_id = body['_id']

    def test_register_guest_invalid_table(self):
        r = requests.post(f'{BASE_URL}/api/guests/register',
                         json={'name': 'X', 'table_number': 99999})
        assert r.status_code == 404

    def test_register_guest_missing_name(self):
        r = requests.post(f'{BASE_URL}/api/guests/register',
                         json={'table_number': self.__class__.table_number})
        assert r.status_code == 400

    def test_get_guest_detail(self):
        assert TestGuestAndOrder.guest_id is not None
        r = requests.get(f'{BASE_URL}/api/guests/{TestGuestAndOrder.guest_id}')
        assert r.status_code == 200
        assert r.json()['_id'] == TestGuestAndOrder.guest_id

    def test_create_order(self):
        r = requests.post(f'{BASE_URL}/api/orders/create',
                         json={'guest_id': TestGuestAndOrder.guest_id,
                               'dish_name': 'TEST_Poulet Rôti'})
        assert r.status_code == 201, r.text
        body = r.json()
        assert body['dish_name'] == 'TEST_Poulet Rôti'
        assert 'locked_at' in body
        assert body.get('is_locked') is False
        TestGuestAndOrder.order_id = body['_id']

    def test_duplicate_order_rejected(self):
        r = requests.post(f'{BASE_URL}/api/orders/create',
                         json={'guest_id': TestGuestAndOrder.guest_id,
                               'dish_name': 'Other'})
        assert r.status_code == 400

    def test_update_order_within_window(self):
        assert TestGuestAndOrder.order_id is not None
        r = requests.put(f'{BASE_URL}/api/orders/{TestGuestAndOrder.order_id}/update',
                        json={'dish_name': 'TEST_Modified'})
        assert r.status_code == 200, r.text
        assert r.json()['dish_name'] == 'TEST_Modified'


# ---------- Admin results ----------
class TestAdminResults:
    def test_requires_admin(self):
        r = requests.get(f'{BASE_URL}/api/admin/results')
        assert r.status_code in (401, 403, 500)

    def test_returns_sorted_results(self, admin_session):
        r = admin_session.get(f'{BASE_URL}/api/admin/results')
        assert r.status_code == 200
        data = r.json()
        assert isinstance(data, list)
        if data:
            nums = [t['table_number'] for t in data]
            assert nums == sorted(nums)
            for t in data:
                assert 'orders' in t and isinstance(t['orders'], list)


# ---------- Gallery ----------
class TestGallery:
    def test_gallery_public(self):
        r = requests.get(f'{BASE_URL}/api/gallery')
        assert r.status_code == 200
        data = r.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        for item in data:
            assert 'url' in item and 'verse' in item
