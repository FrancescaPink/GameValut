# 🎮 GameValut - Gaming Forum & Events Platform

**GameValut** è una piattaforma web sviluppata con **Django** progettata per creare una community di appassionati di videogiochi. Il sistema permette la gestione di discussioni, l'organizzazione di tornei e la pubblicazione di annunci ufficiali da parte delle aziende.

## ✨ Funzionalità Principali

* **Gestione Utenti Avanzata:**
    * Distinzione tra **Giocatori** e **Aziende** (Account verificati).
    * Profili utente personalizzabili con Avatar e Bio.
* **Forum di Discussione:**
    * Creazione di Thread con supporto per **Categorie** e **Tag** multipli.
    * Sistema di risposte (Post) e possibilità di seguire le discussioni.
    * Ricerca avanzata con filtri dinamici (Titolo, Autore, Categoria, Tag).
* **Eventi e Tornei:**
    * Calendario eventi futuri.
    * Sistema di iscrizione agli eventi con gestione dei posti disponibili (logica *sold-out*).
* **Annunci Ufficiali:**
    * Sezione dedicata alle notizie pubblicate solo da account Aziendali/Staff.
    * Conteggio visualizzazioni per ogni annuncio.
* **Interfaccia Responsiva:**
    * Utilizzo di **Bootstrap 5** con personalizzazione CSS (Dark/Light mode ibrida).
* **Qualità del Codice:**
    * Unit Testing completo su logica applicativa e viste.

## 🛠️ Tecnologie Utilizzate

* **Python 3.x**
* **Django 5.x** (Framework Backend)
* **SQLite** (Database di default)
* **Bootstrap 5** (Frontend)
* **Pillow** (Gestione immagini)


## 🚀 Guida all'Installazione

Segui questi passaggi per avviare il progetto in locale.

### 1. Clona la repository
```bash
git clone https://github.com/FrancescaPink/GameValut.git
cd GameValut
```

### 2. Configura l'ambiente virtuale
È consigliato creare un ambiente virtuale per isolare le dipendenze.

Su Windows:
```bash
python -m venv venv
.\venv\Scripts\activate
```
Su Mac/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```
### 3. Installa le dipendenze
Il progetto è leggero e richiede solo Django e la libreria per le immagini

```bash
pip install django pillow
```

### 4. Configurazione Database
Esegui le migrazioni per generare il database SQLite.

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Crea un Superuser (Amministratore)
Necessario per accedere al pannello di controllo e creare le prime Categorie/Tag.

```bash
python manage.py createsuperuser
(Inserisci username, email e password quando richiesto)
```

### 6. Avvia il Server
```bash
python manage.py runserver
```

---

### ⚙️ Configurazione Iniziale (Importante!)
Per far funzionare correttamente i filtri e la creazione delle discussioni, dopo il primo avvio accedi al pannello di amministrazione su http://127.0.0.1:8000/admin/ e crea i dati base:
* Categorie: Aggiungi voci come PC, PlayStation, Xbox, Nintendo, Mobile.
* Tag: Aggiungi voci come News, Recensione, Rumor, FPS, RPG, Guida.

---

### 🧪 Testing
Il progetto include una suite di Unit Test che verifica la logica applicativa (es. iscrizione eventi, permessi) e il funzionamento delle viste.
Per eseguire i test automatizzati:
```bash
python manage.py test core
```
