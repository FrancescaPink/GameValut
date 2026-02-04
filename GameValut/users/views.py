from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.models import Announcement
from events.models import Event, EventRegistration  
from .forms import UserUpdateForm, ProfileUpdateForm
from .models import Profile

# View per la gestione del profilo utente e della dashboard
@login_required(login_url='/admin/login/')      # Protegge la view richiedendo il login, se non loggato reindirizza alla pagina di login admin
def profile(request):
    # Gestione profilo (creazione se non esiste)
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)
    # Gestione Form (POST/GET)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Il tuo profilo è stato aggiornato!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    # DATI PER LA DASHBOARD
    organized_events = []
    company_announcements = []
    my_registrations = []
    # Aggiungo il controllo per utenti aziendali
    if request.user.is_company:
        # Recupero i tornei organizzati
        organized_events = Event.objects.filter(organizer=request.user)
        # Recupero gli annunci pubblicati (per le statistiche)
        company_announcements = Announcement.objects.filter(author=request.user)
    else:
        # Recupero le iscrizioni per i giocatori normali
        my_registrations = EventRegistration.objects.filter(user=request.user)
    # Preparazione del contesto, ovvero i dati da passare al template
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'organized_events': organized_events, 
        'my_registrations': my_registrations,  
        'company_announcements': company_announcements,
    }
    return render(request, 'users/profile.html', context)