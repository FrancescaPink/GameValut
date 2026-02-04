from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from .models import Announcement, Category, Thread, Tag, AnnouncementComment
from events.models import Event
from .forms import CustomUserCreationForm, Thread, ThreadForm, AnnouncementForm, AnnouncementCommentForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from django.db.models import Q
from django.contrib.auth.decorators import login_required           # Importante per proteggere la vista
from .forms import PostForm

# Funzione per la homepage - mostra i thread del forum e filtri di ricerca, oltre agli eventi e i filtri
def homepage(request):
    # Prendo tutti i thread, ordinati dal più recente
    threads = Thread.objects.all().order_by('-created_at')
    # Prendo tutte le categorie e i tag per i filtri
    categories = Category.objects.all()
    tags = Tag.objects.all()
    # Eventi Generali (Prossimi 3 in arrivo)
    upcoming_events = Event.objects.filter(start_date__gte=timezone.now()).order_by('start_date')[:3]
    # Filtro Titolo - dentro c'è q perché è il nome del parametro nella barra di ricerca
    title_query = request.GET.get('q')
    if title_query:
        threads = threads.filter(title__icontains=title_query)
    # Filtro Categoria
    category_id = request.GET.get('category')
    if category_id:
        threads = threads.filter(category__id=category_id)
    # Filtro Tag
    tag_id = request.GET.get('tag')
    if tag_id:
        threads = threads.filter(tags__id=tag_id)
    # Filtro Autore
    author_name = request.GET.get('author')
    if author_name:
        threads = threads.filter(author__username__icontains=author_name)
    # Logica per eventi a cui l'utente è registrato
    my_events = []
    if request.user.is_authenticated:
        # Prendo gli eventi dove esiste una registrazione collegata al mio utente
        my_events = Event.objects.filter(registrations__user=request.user)
    context = {
        'threads': threads,
        'categories': categories,
        'tags': tags,
        'events': upcoming_events,          # Quelli generici nella sidebar
        'my_events': my_events,             # Quelli miei personali
    }
    # Rendo il template con il contesto
    return render(request, 'core/homepage.html', context)

# Funzione per la registrazione
def registration(request):
    # Se il metodo è POST, significa che l'utente ha inviato il form
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)         # Uso la classe CustomUserCreationForm definita in forms.py
        if form.is_valid():
            user = form.save()
            login(request, user)                # Logga l'utente subito dopo la registrazione
            return redirect('homepage')         # Lo rimanda alla home
    else:
        form = CustomUserCreationForm()         # Se request.method non è POST, mostra il form vuoto
    return render(request, 'core/registration.html', {'form': form})

# Funzione per creare un nuovo thread nel forum
@login_required                             # Decoratore che blocca l'accesso se non sei loggato
def create_thread(request):
    if request.method == 'POST':
        form = ThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)            # Non va a salvare ancora nel DB
            # Assegna l'autore automaticamente (l'utente loggato)
            thread.author = request.user 
            # Se l'utente è un'azienda, segna il thread come Ufficiale
            if request.user.is_company:
                thread.is_official_announcement = True
            thread.save()                               # Ora salva tutto definitivamente
            form.save_m2m()                             # Salva i ManyToMany (es. tags)
            return redirect('homepage')
    else:
        form = ThreadForm()
    return render(request, 'core/create_thread.html', {'form': form})

# Per la visualizzazione dettagliata di un singolo thread
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
        form = PostForm()       # Se non è POST o non sei loggato, rimani con il form vuoto
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

# LISTA ANNUNCI (Pagina "News")
def announcement_list(request):
    news = Announcement.objects.all()
    return render(request, 'core/announcement_list.html', {'news': news})

# CREAZIONE ANNUNCI (Solo Aziende)
@login_required
def create_announcement(request):
    # Se non sei azienda o staff, ti butta fuori
    if not (request.user.is_staff or getattr(request.user, 'is_company', False)):
        return redirect('homepage')
    # Gestione del form
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.author = request.user
            announcement.save()
            return redirect('announcement_detail', pk=announcement.pk) 
    else:
        form = AnnouncementForm()
    # Rende il template con il form
    return render(request, 'core/create_announcement.html', {'form': form})

# DETTAGLIO ANNUNCI(+ Contatore Views)
def announcement_detail(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    # Gestione Conteggio Visualizzazioni - uso le sessioni per evitare conteggi multipli dallo stesso utente
    session_key = f'viewed_announcement_{pk}'
    # Se l'utente non ha ancora visto questo annuncio, incremento il contatore
    if not request.session.get(session_key, False):
        announcement.views_count += 1
        announcement.save()
        request.session[session_key] = True
    # Gestione Commenti
    comments = announcement.comments.all()
    # Aggiunta Commento
    if request.method == 'POST' and request.user.is_authenticated:
        form = AnnouncementCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.announcement = announcement
            comment.author = request.user
            comment.save()
            return redirect('announcement_detail', pk=pk)
    else:
        form = AnnouncementCommentForm()
    # Rende il template con i dettagli e i commenti
    return render(request, 'core/announcement_detail.html', {
        'announcement': announcement,
        'comments': comments,
        'form': form
    })

# MODIFICA ANNUNCIO
@login_required
def edit_announcement(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    # SICUREZZA: Solo l'autore (o un admin) può modificare
    if request.user != announcement.author and not request.user.is_superuser:
        return redirect('announcement_detail', pk=pk)
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            form.save()
            return redirect('announcement_detail', pk=pk)
    else:
        form = AnnouncementForm(instance=announcement)
    return render(request, 'core/edit_announcement.html', {'form': form, 'announcement': announcement})

# CANCELLA ANNUNCIO
@login_required
def delete_announcement(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    # SICUREZZA: Solo l'autore può cancellare
    if request.user == announcement.author or request.user.is_superuser:
        if request.method == 'POST':
            announcement.delete()
            return redirect('profile')              # Torna al profilo dopo la cancellazione
    return redirect('announcement_detail', pk=pk)

# Funzione per seguire o smettere di seguire un thread
@login_required
def toggle_follow_thread(request, pk):
    thread = get_object_or_404(Thread, pk=pk)
    # Controlla se l'utente sta già seguendo il thread
    if thread.followers.filter(id=request.user.id).exists():
        thread.followers.remove(request.user) # Smetti di seguire
    else:
        thread.followers.add(request.user)    # Inizia a seguire
    return redirect('thread_detail', pk=pk)