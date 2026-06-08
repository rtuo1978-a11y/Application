"""
Modèles de données pour l'application Apotheosis ACE.
Utilise la base de données SQLite intégrée à Django.
"""
from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.conf import settings


class Table(models.Model):
    """Modèle représentant une table du banquet."""
    table_number = models.IntegerField(unique=True, verbose_name='Numéro de table')
    places = models.IntegerField(default=1, verbose_name='Nombre de places')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Date de création')

    class Meta:
        ordering = ['table_number']
        verbose_name = 'Table'
        verbose_name_plural = 'Tables'

    def __str__(self):
        return f'Table {self.table_number} ({self.places} places)'


class Dish(models.Model):
    """Modèle représentant un plat du menu."""
    name = models.CharField(max_length=200, verbose_name='Nom du plat')
    description = models.TextField(blank=True, verbose_name='Description')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Plat'
        verbose_name_plural = 'Plats'

    def __str__(self):
        return self.name


class Guest(models.Model):
    """Modèle représentant un invité inscrit au banquet."""
    name = models.CharField(max_length=200, verbose_name='Nom complet')
    email = models.EmailField(blank=True, verbose_name='Email')
    table = models.ForeignKey(
        Table,
        on_delete=models.CASCADE,
        related_name='guests',
        verbose_name='Table'
    )
    registration_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['table__table_number', 'name']
        verbose_name = 'Invité'
        verbose_name_plural = 'Invités'

    def __str__(self):
        return f'{self.name} - Table {self.table.table_number}'


class Order(models.Model):
    """Modèle représentant une commande de plat par un invité.
    
    La commande peut être modifiée pendant 2 minutes après sa création,
    après quoi elle est verrouillée définitivement.
    """
    guest = models.OneToOneField(
        Guest,
        on_delete=models.CASCADE,
        related_name='order',
        verbose_name='Invité'
    )
    dish = models.ForeignKey(
        Dish,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Plat'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Commande'
        verbose_name_plural = 'Commandes'

    @property
    def lock_time(self):
        """Retourne l'heure de verrouillage de la commande."""
        return self.created_at + timedelta(seconds=settings.ORDER_LOCK_SECONDS)

    @property
    def is_locked(self):
        """Retourne True si la commande est verrouillée (> 2 minutes)."""
        return timezone.now() >= self.lock_time

    @property
    def seconds_remaining(self):
        """Retourne le nombre de secondes restantes avant verrouillage."""
        diff = self.lock_time - timezone.now()
        return max(0, int(diff.total_seconds()))

    def __str__(self):
        return f'{self.guest.name} - {self.dish.name}'


class Candidate(models.Model):
    """Modèle représentant un candidat à l'élection du leader ACE."""
    name = models.CharField(max_length=200, verbose_name='Nom du candidat')
    photo = models.ImageField(
        upload_to='candidates/',
        verbose_name='Photo'
    )
    description = models.TextField(blank=True, verbose_name='Description / Programme')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Candidat'
        verbose_name_plural = 'Candidats'

    def __str__(self):
        return self.name

    @property
    def vote_count(self):
        """Retourne le nombre total de votes reçus."""
        return self.votes.count()


class Vote(models.Model):
    """Modèle représentant un vote pour un candidat.
    
    Identifié par session_key pour empêcher les votes multiples
    depuis le même navigateur.
    """
    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE,
        related_name='votes',
        verbose_name='Candidat'
    )
    session_key = models.CharField(max_length=40, unique=True, verbose_name='Clé de session')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Vote'
        verbose_name_plural = 'Votes'

    def __str__(self):
        return f'Vote pour {self.candidate.name}'
