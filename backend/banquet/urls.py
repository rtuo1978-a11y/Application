"""Configuration des URLs pour l'application Apotheosis ACE."""
from django.urls import path
from . import views

urlpatterns = [
    # ===== Pages publiques =====
    path('', views.welcome_view, name='welcome'),
    path('register/', views.register_guest_view, name='register'),
    path('menu/<int:guest_id>/', views.dish_selection_view, name='dish_selection'),
    path('api/order/<int:order_id>/status/', views.order_status_api, name='order_status_api'),
    
    # ===== Vote présidentiel ACE =====
    path('vote/', views.vote_view, name='vote'),
    path('vote/cast/', views.cast_vote_view, name='cast_vote'),
    
    # ===== Espace administrateur =====
    path('admin-panel/login/', views.admin_login_view, name='admin_login'),
    path('admin-panel/logout/', views.admin_logout_view, name='admin_logout'),
    path('admin-panel/dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('admin-panel/tables/', views.admin_tables_view, name='admin_tables'),
    path('admin-panel/tables/delete/<int:table_id>/', views.admin_delete_table_view, name='admin_delete_table'),
    path('admin-panel/menu/', views.admin_menu_view, name='admin_menu'),
    path('admin-panel/menu/delete/<int:dish_id>/', views.admin_delete_dish_view, name='admin_delete_dish'),
    path('admin-panel/results/', views.admin_results_view, name='admin_results'),
    path('admin-panel/candidates/', views.admin_candidates_view, name='admin_candidates'),
    path('admin-panel/candidates/delete/<int:candidate_id>/', views.admin_delete_candidate_view, name='admin_delete_candidate'),
    path('admin-panel/vote-results/', views.admin_vote_results_view, name='admin_vote_results'),
]
