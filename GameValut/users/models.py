from django.db import models
from django.conf import settings

# Modello per il profilo utente con immagine e biografia
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics', null=True, blank=True)
    bio = models.TextField(blank=True, null=True, verbose_name="Biografia")
    # Aggiungo la possibilità di seguire altri utenti
    following = models.ManyToManyField("self", symmetrical=False, related_name="followers", blank=True)
    def __str__(self):
        return f'{self.user.username} Profile'