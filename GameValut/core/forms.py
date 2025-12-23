from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from .models import Thread, Thread, User, Post

class CustomUserCreationForm(UserCreationForm):
    # Aggiungiamo una checkbox per chiedere se è un'azienda
    is_company = forms.BooleanField(
        required=False, 
        label="Registrati come Azienda/Organizzatore",
        help_text="Spunta questa casella se vuoi organizzare eventi e tornei."
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'is_company') # Campi visibili nel form

    def save(self, commit=True):
        # 1. Salviamo l'utente creato dal form
        user = super().save(commit=False)
        
        # Impostiamo il flag is_company in base alla checkbox
        user.is_company = self.cleaned_data['is_company']
        
        if commit:
            user.save()
            # 2. SE è un'azienda, lo aggiungiamo subito al gruppo 'Enterprises'
            if user.is_company:
                try:
                    # Usa il nome esatto del gruppo che hai creato nello screenshot
                    group = Group.objects.get(name='Enterprises') 
                    user.groups.add(group)
                except Group.DoesNotExist:
                    pass # Se il gruppo non esiste, non fa nulla (evita crash)
                    
        return user
    
# Classe per creare nuovi thread nel forum    
class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['title', 'category', 'content'] # L'utente sceglie solo questi
        labels = {
            'title': 'Titolo della discussione',
            'category': 'Categoria',
            'content': 'Messaggio'
        }
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Scrivi qui il tuo messaggio...'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'})
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']
        labels = {'content': 'Rispondi alla discussione'}
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Scrivi la tua risposta qui...'}),
        }
    