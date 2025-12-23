from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone

# 1. GESTIONE UTENTI (User Custom)
class User(AbstractUser):
    is_company = models.BooleanField(
        default=False, 
        help_text="Spunta questa casella se l'account appartiene a un'azienda/organizzatore."
    )
    def __str__(self):
        return self.username

# 2. SEZIONE FORUM (Discussioni)
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    class Meta:
        verbose_name_plural = "Categories"
    def __str__(self):
        return self.name

class Thread(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="threads")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # [cite_start]Campo per distinguere gli annunci ufficiali delle aziende [cite: 31]
    is_official_announcement = models.BooleanField(default=False) 
    def __str__(self):
        return f"{self.title} (by {self.author})"

class Post(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="posts")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Post by {self.author} in {self.thread}"

# 3. SEZIONE EVENTI E TORNEI (Prenotazioni)
class Event(models.Model):
    # Solo le aziende possono organizzare eventi
    organizer = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        limit_choices_to={'is_company': True}, 
        related_name="organized_events"
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200, help_text="Link o indirizzo fisico")
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    # Gestione capienza
    max_participants = models.PositiveIntegerField(default=20)
    created_at = models.DateTimeField(auto_now_add=True)
    def available_spots(self):
        # Totale posti meno gli iscritti attuali
        return self.max_participants - self.registrations.count()
    def __str__(self):
        return self.title

class EventRegistration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="registrations")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="event_registrations")
    registered_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        # Impedisce allo stesso utente di iscriversi due volte allo stesso evento
        unique_together = ('event', 'user')
    def __str__(self):
        return f"{self.user.username} -> {self.event.title}"