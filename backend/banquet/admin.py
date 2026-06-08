"""Enregistrement des modèles dans l'interface admin Django."""
from django.contrib import admin
from .models import Table, Dish, Guest, Order


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('table_number', 'places', 'created_at')
    ordering = ('table_number',)


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name',)


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'table', 'registration_time')
    list_filter = ('table',)
    search_fields = ('name', 'email')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('guest', 'dish', 'created_at', 'is_locked')
    list_filter = ('dish',)
