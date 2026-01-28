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