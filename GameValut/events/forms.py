from django import forms
from .models import Event
from django.core.exceptions import ValidationError

# Form per la creazione/modifica di un Evento
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'location', 'start_date', 'end_date', 'max_participants']
        labels = {
            'title': 'Nome del Torneo/Evento',
            'location': 'Luogo (o Link Streaming)',
            'max_participants': 'Posti totali disponibili',
            'start_date': 'Data Inizio',
            'end_date': 'Data Fine'
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'start_date': forms.TextInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.TextInput(attrs={'type': 'datetime-local'}),
        }

    # Uso la classe form-control di Bootstrap per tutti i campi
    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    # Validazione date: la data di fine deve essere dopo la data di inizio
    def clean(self):
        # Recupero i dati puliti (già convertiti nei tipi corretti da Django)
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        # Verifica logica: se entrambe le date esistono, controlla l'ordine
        if start_date and end_date:
            if end_date < start_date:
                # Aggiungo un errore specifico al campo 'end_date'
                self.add_error('end_date', "La data di fine non può essere precedente alla data di inizio!")
        return cleaned_data