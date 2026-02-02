from django.test import TestCase, Client
from django.urls import reverse
from .models import User, Thread, Category, Tag

class ForumLogicTest(TestCase):
    # REQ 1: Testare codice applicativo (Logica Backend). Oggetto: Creazione Thread e gestione Tag.
    def setUp(self):
        # Vado a creare dati di base per i test
        self.user = User.objects.create_user(username='tester', password='pw')
        self.category = Category.objects.create(name='News')
        self.tag = Tag.objects.create(name='Urgente')

    def test_thread_creation_logic(self):
        # CASO VALIDO: Creazione corretta di un thread e associazione dati.
        # Creazione del thread
        thread = Thread.objects.create(
            title="Nuovo Gioco",
            content="Recensione completa...",
            author=self.user,
            category=self.category
        )
        # Aggiunta di un tag (relazione ManyToMany)
        thread.tags.add(self.tag)
        # Verifiche di logica (Asserts)
        self.assertEqual(thread.author.username, 'tester')                  # L'autore è corretto?
        self.assertEqual(thread.category.name, 'News')                      # La categoria è corretta?
        self.assertTrue(thread.tags.filter(name='Urgente').exists())        # Il tag è stato aggiunto?
        print("\n✅ Test Logica 1: Creazione Thread e Tag -> OK")

    def test_thread_string_representation(self):
        #CASO LOGICO: Verifica che il metodo __str__ restituisca il titolo e l'autore.
        thread = Thread.objects.create(
            title="Test Titolo",
            author=self.user,
            category=self.category
        )
        expected_string = f"Test Titolo (by {self.user.username})"
        self.assertEqual(str(thread), expected_string)
        print("✅ Test Logica 2: Rappresentazione Stringa (__str__) -> OK")

class HomepageViewTest(TestCase):
    # REQ 2: Testare una 'vista' (pagina) utente. Oggetto: Home Page con Filtri di Ricerca.
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='visitatore', password='pw')
        # Dati per il test della vista
        self.cat_ps = Category.objects.create(name='Playstation')
        self.cat_xbox = Category.objects.create(name='Xbox')
        # Creo due thread per vedere se il filtro li distingue
        self.thread_ps = Thread.objects.create(title='God of War', author=self.user, category=self.cat_ps, content='Testo')
        self.thread_xbox = Thread.objects.create(title='Halo Infinite', author=self.user, category=self.cat_xbox, content='Testo')

    def test_homepage_status_code(self):
        # Verifica Base: La pagina risponde correttamente (HTTP 200).
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)
        print("✅ Test Vista 1: Caricamento Pagina (Status 200) -> OK")

    def test_homepage_search_filter_valid(self):
        # Verifica Black-Box (Input Valido): Cerco 'Halo'. Risultato atteso: Vedo 'Halo', NON 'God of War'.
        response = self.client.get(reverse('homepage'), {'q': 'Halo'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Halo Infinite')      # Deve esserci
        self.assertNotContains(response, 'God of War')      # NON deve esserci
        print("✅ Test Vista 2: Filtro Ricerca Funzionante -> OK")

    def test_homepage_search_no_results(self):
        # Verifica Black-Box (Input Valido ma senza risultati): Cerco 'Super Mario'. Risultato atteso: Nessun thread trovato.
        response = self.client.get(reverse('homepage'), {'q': 'Super Mario'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Halo Infinite')
        self.assertNotContains(response, 'God of War')
        # Verifica che appaia il messaggio "Nessuna discussione trovata" (o simile, controlla il tuo HTML)
        self.assertContains(response, 'Nessuna discussione') 
        print("✅ Test Vista 3: Ricerca senza risultati -> OK")