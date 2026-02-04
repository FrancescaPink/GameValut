from django.shortcuts import render, redirect, get_object_or_404
from .models import Event, EventRegistration
from django.contrib.auth.decorators import login_required
from django.contrib import messages                     # Per usare i messaggi popup
from django.core.exceptions import PermissionDenied
from .forms import EventForm

# Funzione per creare un nuovo evento - accessibile solo agli utenti aziendali
@login_required
def create_event(request):
    # Solo gli utenti aziendali possono creare gli eventi
    if not request.user.is_company:
        raise PermissionDenied("Solo le aziende possono creare eventi.") 
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            return redirect('homepage')
    else:
        form = EventForm()
    return render(request, 'events/create_event.html', {'form': form})

# Dettaglio di un evento specifico, con possibilità di iscriversi o annullare l'iscrizione (la logica è gestita in POST)
def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    # Controllo se l'utente è già iscritto
    is_registered = False
    if request.user.is_authenticated:
        # Verifico se esiste già una registrazione per questo utente e evento con la logica di filter + exists con una query efficiente al db
        is_registered = event.registrations.filter(user=request.user).exists()
    # LOGICA DI PRENOTAZIONE (POST)
    if request.method == 'POST' and request.user.is_authenticated:
        if is_registered:
            # Se è già iscritto -> Annulla iscrizione
            event.registrations.filter(user=request.user).delete()
        else:
            # Se non è iscritto -> Iscriviti (se c'è posto)
            if event.available_spots() > 0:
                EventRegistration.objects.create(event=event, user=request.user)
            else:
                messages.error(request, "Posti esauriti!")
        return redirect('event_detail', pk=pk)
    context = {
        'event': event,
        'is_registered': is_registered,
    }
    return render(request, 'events/event_detail.html', context)

# Per visualizzare la lista di tutti gli eventi
def event_list(request):
    # Prendo tutti gli eventi, ordinati dal più vicino
    events = Event.objects.all().order_by('start_date')
    return render(request, 'events/event_list.html', {'events': events})

# Per cancellare un evento
@login_required
def delete_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    # Controllo di Sicurezza: Solo chi l'ha creato può cancellarlo
    if request.user != event.organizer:
        messages.error(request, "Non hai il permesso di cancellare questo evento!")
        return redirect('event_detail', pk=pk)
    if request.method == 'POST':
        event.delete()
        messages.success(request, "Evento cancellato con successo.")
        return redirect('event_list')
    # Se è una GET, mostra la pagina di conferma
    return render(request, 'events/event_confirm_delete.html', {'event': event})

# Per modificare un evento
@login_required
def update_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    # Solo l'organizzatore può modificare
    if request.user != event.organizer:
        messages.error(request, "Non puoi modificare eventi non tuoi!")
        return redirect('event_detail', pk=pk)
    # Gestione Form
    if request.method == 'POST':
        # instance=event serve per dire a Django che voglio modificare questo evento esistente, non crearne uno nuovo
        form = EventForm(request.POST, instance=event)         
        if form.is_valid():
            form.save()
            messages.success(request, "Evento aggiornato con successo!")
            return redirect('event_detail', pk=pk)
    else:
        form = EventForm(instance=event)                        # Pre-compila il form con i dati attuali
    return render(request, 'events/update_event.html', {'form': form, 'event': event})