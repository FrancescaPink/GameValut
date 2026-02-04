from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from .models import Announcement, AnnouncementComment, Thread, Thread, User, Post

# Classe per il form di registrazione utente personalizzato - estende UserCreationForm di Django, che già gestisce password e validazioni
class CustomUserCreationForm(UserCreationForm):
    # Aggiungo una checkbox per chiedere se è un'azienda
    is_company = forms.BooleanField(
        required=False, 
        label="Registrati come Azienda/Organizzatore",
        help_text="Spunta questa casella se vuoi organizzare eventi e tornei."
    )
    class Meta:
        model = User
        fields = ('username', 'email', 'is_company')    # Campi visibili nel form

    def save(self, commit=True):
        # Salvo l'utente creato dal form
        user = super().save(commit=False)
        # Imposto il flag is_company in base alla checkbox
        user.is_company = self.cleaned_data['is_company']
        if commit:
            user.save()
            # Se è un'azienda, lo aggiungo al gruppo 'Enterprises'
            if user.is_company:
                try:
                    group = Group.objects.get(name='Enterprises') 
                    user.groups.add(group)
                except Group.DoesNotExist:
                    pass                        # Se il gruppo non esiste, non fa nulla (evita crash)        
        return user
    
# Classe per creare nuovi thread nel forum - estende forms.ModelForm di Django, che semplifica la creazione di form basati su modelli
class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['title', 'category', 'tags', 'content']       # L'utente sceglie solo questi
        labels = {
            'title': 'Titolo della discussione',
            'category': 'Categoria',
            'tags': 'Tag',
            'content': 'Messaggio'
        }
        # I widgets personalizzano l'aspetto dei campi nel form
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Scrivi qui il tuo messaggio...'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

# Classe per rispondere ai thread nel forum - segue lo stesso schema di ThreadForm
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']
        labels = {'content': 'Rispondi alla discussione'}
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Scrivi la tua risposta qui...'}),
        }
    
# Classe per creare annunci ufficiali - usata dalle aziende/organizzatori
class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Es: Lancio ufficiale nuovi server...'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 6, 
                'placeholder': 'Scrivi qui il contenuto del comunicato...'
            }),
        }
        # Le labels personalizzano i nomi dei campi nel form
        labels = {
            'title': 'Titolo della News',
            'content': 'Testo dell\'Annuncio'
        }

# Classe per commentare gli annunci ufficiali - usata principalmente dagli utenti
class AnnouncementCommentForm(forms.ModelForm):
    class Meta:
        model = AnnouncementComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Scrivi un commento ufficiale...'
            }),
        }
        labels = {
            'content': ''       # Nascondo l'etichetta per pulizia
        }