"""
Formulaires Django pour l'application Apotheosis ACE.
"""
from django import forms
from .models import Table, Dish, Guest, Candidate


class TableForm(forms.ModelForm):
    """Formulaire pour créer ou modifier une table."""
    class Meta:
        model = Table
        fields = ['table_number', 'places']
        widgets = {
            'table_number': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Ex: 1',
                'min': '1',
                'data-testid': 'table-number-input'
            }),
            'places': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Ex: 8',
                'min': '1',
                'data-testid': 'table-places-input'
            }),
        }
        labels = {
            'table_number': 'Numéro de table',
            'places': 'Nombre de places',
        }


class DishForm(forms.ModelForm):
    """Formulaire pour créer ou modifier un plat."""
    class Meta:
        model = Dish
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Ex: Agneau rôti aux herbes',
                'data-testid': 'dish-name-input'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Description du plat...',
                'rows': 3,
                'data-testid': 'dish-description-input'
            }),
        }
        labels = {
            'name': 'Nom du plat',
            'description': 'Description (optionnel)',
        }


class GuestForm(forms.ModelForm):
    """Formulaire d'inscription pour un invité."""
    class Meta:
        model = Guest
        fields = ['name', 'email', 'table']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Votre nom',
                'data-testid': 'guest-name-input'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'votre@email.com (optionnel)',
                'data-testid': 'guest-email-input'
            }),
            'table': forms.Select(attrs={
                'class': 'form-input',
                'data-testid': 'guest-table-select'
            }),
        }
        labels = {
            'name': 'Nom complet',
            'email': 'Email (optionnel)',
            'table': 'Numéro de table',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['table'].queryset = Table.objects.all().order_by('table_number')
        self.fields['table'].empty_label = 'Sélectionnez votre table'


class LoginForm(forms.Form):
    """Formulaire de connexion administrateur."""
    username = forms.CharField(
        label='Nom d\'utilisateur',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'admin',
            'data-testid': 'admin-username-input'
        })
    )
    password = forms.CharField(
        label='Mot de passe',
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': '••••••••',
            'data-testid': 'admin-password-input'
        })
    )


class CandidateForm(forms.ModelForm):
    """Formulaire pour ajouter un candidat à l'élection ACE."""
    class Meta:
        model = Candidate
        fields = ['name', 'photo', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Nom complet du candidat',
                'data-testid': 'candidate-name-input'
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-input',
                'accept': 'image/*',
                'data-testid': 'candidate-photo-input'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Présentation du candidat (programme, parcours...)',
                'rows': 3,
                'data-testid': 'candidate-description-input'
            }),
        }
        labels = {
            'name': 'Nom du candidat',
            'photo': 'Photo (JPG, PNG)',
            'description': 'Description / Programme (optionnel)',
        }
