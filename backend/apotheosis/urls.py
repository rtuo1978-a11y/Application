"""URLs principales du projet Apotheosis ACE."""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('', include('banquet.urls')),
]
