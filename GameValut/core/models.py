from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone

# GESTIONE UTENTI (Estensione del modello User predefinito di Django)
class User(AbstractUser):
    is_company = models.BooleanField(
        default=False, 
        help_text="Spunta questa casella se l'account appartiene a un'azienda/organizzatore."
    )
    def __str__(self):
        return self.username

# SEZIONE FORUM (Discussioni)
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    class Meta:
        verbose_name_plural = "Categories"
    def __str__(self):
        return self.name

# Modello per i tag dei thread
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name

# Modello per i thread del forum
class Thread(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="threads")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="threads", null=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name="threads")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # [cite_start]Campo per distinguere gli annunci ufficiali delle aziende [cite: 31]
    is_official_announcement = models.BooleanField(default=False) 
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followed_threads', blank=True)
    def __str__(self):
        return f"{self.title} (by {self.author})"

# Modello per i post nei thread del forum (i post sono le risposte ai thread)
class Post(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="posts")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Post by {self.author} in {self.thread}"
    
# SEZIONE ANNUNCI UFFICIALI (Official Announcements) - Solo per aziende
class Announcement(models.Model):
    title = models.CharField(max_length=200, verbose_name="Titolo Annuncio")
    content = models.TextField(verbose_name="Contenuto")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="announcements")
    created_at = models.DateTimeField(auto_now_add=True)
    # Campo per le statistiche
    views_count = models.PositiveIntegerField(default=0)
    class Meta:
        ordering = ['-created_at']                      # Metto i più recenti in alto
        verbose_name = "Annuncio Ufficiale"
        verbose_name_plural = "Annunci Ufficiali"
    def __str__(self):
        return self.title

# Modello per i commenti sugli annunci ufficiali
class AnnouncementComment(models.Model):
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(verbose_name="Commento")
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created_at']           # I più recenti prima (ordine cronologico)
    def __str__(self):
        return f"Commento di {self.author} su {self.announcement}"