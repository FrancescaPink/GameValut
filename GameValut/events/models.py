from django.db import models
from django.conf import settings
from django.utils import timezone

# SEZIONE EVENTI E TORNEI 
class Event(models.Model):
    # Solo le aziende possono organizzare eventi - metto un ForeignKey al modello User con limitazione per is_company=True
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'is_company': True}, 
        related_name="organized_events"     # Se elimino un'azienda, elimino anche i suoi eventi (on_delete=models.CASCADE)
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200, help_text="Link o indirizzo fisico")
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    if end_date < start_date:
        raise ValueError("La data di fine non può essere precedente alla data di inizio.")
    # Gestione capienza
    max_participants = models.PositiveIntegerField(default=20)
    created_at = models.DateTimeField(auto_now_add=True)
    # Posti disponibili: totale posti meno gli iscritti attuali
    def available_spots(self):
        return self.max_participants - self.registrations.count()
    # Rappresentazione testuale dell'evento (utile per l'admin e per debug)
    def __str__(self):
        return self.title

# Modello per le iscrizioni agli eventi - ogni iscrizione lega un utente a un evento specifico
class EventRegistration(models.Model):
    # Event e User sono collegati tramite ForeignKey, con on_delete=CASCADE per eliminare le iscrizioni se l'evento/l'utente viene cancellato
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="registrations")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="event_registrations")
    registered_at = models.DateTimeField(auto_now_add=True)
    # Impedisce allo stesso utente di iscriversi due volte allo stesso evento
    class Meta:
        unique_together = ('event', 'user')         # Rende unica la combinazione evento-utente, evitando doppie iscrizioni
    # Rappresentazione testuale dell'iscrizione (utile per l'admin e per debug)
    def __str__(self):
        return f"{self.user.username} -> {self.event.title}"