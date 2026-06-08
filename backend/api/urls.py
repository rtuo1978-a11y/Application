from django.urls import path
from . import views

urlpatterns = [
    path('auth/login', views.login_view, name='login'),
    path('auth/logout', views.logout_view, name='logout'),
    path('auth/me', views.me_view, name='me'),
    path('tables', views.tables_view, name='tables'),
    path('tables/create', views.create_table_view, name='create_table'),
    path('menu', views.menu_view, name='menu'),
    path('menu/create', views.create_dish_view, name='create_dish'),
    path('guests/register', views.register_guest_view, name='register_guest'),
    path('guests/<str:guest_id>', views.guest_detail_view, name='guest_detail'),
    path('orders/create', views.create_order_view, name='create_order'),
    path('orders/<str:order_id>/update', views.update_order_view, name='update_order'),
    path('admin/results', views.admin_results_view, name='admin_results'),
    path('gallery', views.gallery_view, name='gallery'),
]
