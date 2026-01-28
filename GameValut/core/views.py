from django.utils import timezone
from django.shortcuts import render, redirect
from .models import Category, Thread
from events.models import Event
from .forms import CustomUserCreationForm, Thread, ThreadForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required           # Importante per proteggere la vista
from django.shortcuts import get_object_or_404
from .forms import PostForm

def homepage(request):
    # Prendiamo tutti i thread, ordinati dal più recente
    threads = Thread.objects.all().order_by('-created_at')[:5]
    categories = Category.objects.all()
    # Eventi Generali (Prossimi 3 in arrivo)
    upcoming_events = Event.objects.filter(start_date__gte=timezone.now()).order_by('start_date')[:3]
    # NUOVA LOGICA: Eventi a cui sono iscritto
    my_events = []
    if request.user.is_authenticated:
        # Prendi gli eventi dove esiste una registrazione collegata al mio utente
        my_events = Event.objects.filter(registrations__user=request.user)

    context = {
        'threads': threads,
        'categories': categories,
        'events': upcoming_events, # Quelli generici nella sidebar
        'my_events': my_events,    # <--- Quelli miei personali
    }
    return render(request, 'core/homepage.html', context)

# Funzione per la registrazione
def registration(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Logga l'utente subito dopo la registrazione
            return redirect('homepage') # Lo rimanda alla home
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/registration.html', {'form': form})

@login_required                 # Blocca l'accesso se non sei loggato
def create_thread(request):
    if request.method == 'POST':
        form = ThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)        # Non salvare ancora nel DB
            # Assegna l'autore automaticamente (l'utente loggato)
            thread.author = request.user 
            # Se l'utente è un'azienda, segna il thread come Ufficiale
            if request.user.is_company:
                thread.is_official_announcement = True
            thread.save()                           # Ora salva tutto definitivamente
            return redirect('homepage')
    else:
        form = ThreadForm()
    return render(request, 'core/create_thread.html', {'form': form})

# Permette la visualizzazione dettagliata di un singolo thread
def thread_detail(request, pk):
    # Cerca il thread con quell'ID (pk), se non esiste da Errore 404
    thread = get_object_or_404(Thread, pk=pk)
    # Recupera tutte le risposte (Post) associate a questo thread
    posts = thread.posts.all().order_by('created_at')
    # Logica per aggiungere una nuova risposta
    if request.method == 'POST' and request.user.is_authenticated:
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.thread = thread
            post.author = request.user
            post.save()
            # Ricarica la pagina per vedere il nuovo messaggio
            return redirect('thread_detail', pk=pk)
    else:
        form = PostForm()
    context = {
        'thread': thread,
        'posts': posts,
        'form': form
    }
    return render(request, 'core/thread_detail.html', context)

# Funzione per eliminare un thread
@login_required
def delete_thread(request, pk):
    thread = get_object_or_404(Thread, pk=pk)
    # Controlla se l'utente loggato è l'autore del thread
    if request.user == thread.author:
        if request.method == 'POST':
            thread.delete()
            return redirect('homepage')
    return redirect('thread_detail', pk=pk)

# L'admin può sempre eliminare qualsiasi thread tramite l'admin di Django. Non è necessario creare una vista separata per questo scopo.