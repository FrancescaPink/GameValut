from django import forms
from django.contrib.auth import get_user_model # <--- Importiamo questo
from .models import Profile

# Recupero il modello utente corretto
User = get_user_model()

# Definizione del modulo per l'aggiornamento dell'utente e del profilo
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email']

# Definizione del modulo per l'aggiornamento del profilo
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'bio']