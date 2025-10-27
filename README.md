📚 LitReview
Une plateforme communautaire permettant de demander et publier des critiques de livres.
📋 Description
LitReview est une application web développée avec Django qui permet aux utilisateurs de :

Demander des critiques de livres en créant des tickets
Publier des critiques en réponse à des tickets ou de manière indépendante
Suivre d'autres utilisateurs pour créer un flux personnalisé
Gérer leurs propres publications (modification, suppression)

✨ Fonctionnalités
Authentification

✅ Inscription avec validation
✅ Connexion / Déconnexion sécurisée
✅ Protection des pages avec @login_required

Gestion des Tickets

✅ Créer une demande de critique (avec image optionnelle)
✅ Modifier ses propres tickets
✅ Supprimer ses tickets avec confirmation

Gestion des Critiques

✅ Créer une critique en réponse à un ticket
✅ Créer un ticket et une critique simultanément
✅ Système de notation de 0 à 5 étoiles
✅ Modifier et supprimer ses critiques
✅ Empêcher les critiques multiples sur le même ticket

Système d'Abonnements

✅ Suivre d'autres utilisateurs
✅ Se désabonner
✅ Voir la liste de ses abonnements et abonnés
✅ Flux personnalisé (uniquement les posts des utilisateurs suivis + les siens)

Interface

✅ Design moderne et épuré
✅ Messages de confirmation/erreur
✅ Navigation intuitive
✅ Affichage responsive des images

🛠️ Technologies utilisées

Backend: Django 5.2.7
Base de données: SQLite3
Frontend: HTML5, CSS3
Gestion d'images: Pillow
Langage: Python 3.11

📦 Installation
Prérequis

Python 3.11 ou supérieur
pip

Étapes d'installation

Cloner le repository

bashgit clone https://github.com/votre-username/litreview.git
cd litreview

Créer un environnement virtuel

bashpython -m venv env

Activer l'environnement virtuel


Windows:

bashenv\Scripts\activate

macOS/Linux:

bashsource env/bin/activate

Installer les dépendances

bashpip install -r requirements.txt

Effectuer les migrations

bashpython manage.py makemigrations
python manage.py migrate

Créer un superutilisateur (optionnel)

bashpython manage.py createsuperuser

Lancer le serveur

bashpython manage.py runserver

Accéder à l'application

Ouvrez votre navigateur et allez sur http://127.0.0.1:8000/
📁 Structure du projet
litrevu/
├── authentication/          # Application d'authentification
│   ├── templates/
│   │   └── authentication/
│   │       ├── login.html
│   │       └── signup.html
│   ├── views.py
│   └── urls.py
├── reviews/                 # Application principale
│   ├── templates/
│   │   └── reviews/
│   │       ├── base.html
│   │       ├── home.html
│   │       ├── create_ticket.html
│   │       ├── create_review.html
│   │       ├── edit_ticket.html
│   │       ├── delete_ticket.html
│   │       ├── user_posts.html
│   │       └── subscriptions.html
│   ├── models.py           # Ticket, Review, UserFollows
│   ├── views.py            # Logique métier
│   ├── forms.py            # Formulaires
│   └── urls.py
├── media/                  # Fichiers uploadés
│   └── tickets/
├── litrevu/                # Configuration Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── db.sqlite3              # Base de données
├── manage.py
└── requirements.txt
🗄️ Modèles de données
Ticket

title: Titre du livre/article
description: Description de la demande
user: Auteur du ticket (ForeignKey vers User)
image: Image de couverture (optionnelle)
time_created: Date de création

Review

ticket: Ticket associé (ForeignKey)
rating: Note de 0 à 5
headline: Titre de la critique
body: Contenu de la critique
user: Auteur de la critique (ForeignKey vers User)
time_created: Date de création

UserFollows

user: Utilisateur qui suit
followed_user: Utilisateur suivi
Contrainte: unique_together pour éviter les doublons

🔐 Sécurité

Protection CSRF sur tous les formulaires
Authentification requise pour toutes les actions sensibles
Validation des formulaires côté serveur
Vérification de propriété (un utilisateur ne peut modifier que ses propres posts)
Échappement automatique du HTML (protection XSS)
