# Projet Médical - Cabinet Dr Asmaa Abidine

Application web Django pour la gestion d'un cabinet médical, permettant aux patients de prendre des rendez-vous en ligne et au personnel médical de gérer les consultations et ordonnances.

## 🚀 Fonctionnalités

### Pour les Patients
- **Inscription** : Création de compte patient avec informations personnelles
- **Prise de rendez-vous** : Réservation en ligne avec validation automatique
- **Confirmation par email** : Réception automatique d'emails de confirmation

### Pour le Personnel Médical
- **Interface d'administration Django** : Gestion complète des patients, rendez-vous, consultations et ordonnances
- **Gestion des consultations** : Enregistrement des examens et mesures
- **Gestion des ordonnances** : Création et suivi des prescriptions

## 📋 Prérequis

- Python 3.10 ou supérieur
- pip (gestionnaire de paquets Python)
- Virtualenv (recommandé)

## 🛠️ Installation

1. **Cloner le projet** (ou télécharger les fichiers)

2. **Créer un environnement virtuel** :
```bash
python -m venv venv
```

3. **Activer l'environnement virtuel** :
   - Sur Linux/Mac : `source venv/bin/activate`
   - Sur Windows : `venv\Scripts\activate`

4. **Installer les dépendances** :
```bash
pip install -r requirements.txt
```

5. **Configurer les variables d'environnement** :
   - Copier `.env.example` vers `.env`
   - Éditer `.env` avec vos propres valeurs :
```env
SECRET_KEY=votre-secret-key-genere-aleatoirement
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=votre-email@gmail.com
EMAIL_HOST_PASSWORD=votre-mot-de-passe-application
```

6. **Appliquer les migrations** :
```bash
cd medicalproject
python manage.py migrate
```

7. **Créer un superutilisateur** (pour accéder à l'admin) :
```bash
python manage.py createsuperuser
```

8. **Lancer le serveur de développement** :
```bash
python manage.py runserver
```

9. **Accéder à l'application** :
   - Site web : http://127.0.0.1:8000/
   - Administration : http://127.0.0.1:8000/admin/

## 🐳 Déploiement avec Docker

1. **Construire l'image** :
```bash
docker-compose build
```

2. **Lancer les conteneurs** :
```bash
docker-compose up -d
```

3. **Appliquer les migrations** :
```bash
docker-compose exec web python manage.py migrate
```

4. **Créer un superutilisateur** :
```bash
docker-compose exec web python manage.py createsuperuser
```

## 📁 Structure du Projet

```
medicalproject/
├── firstpage/           # Application pour la page d'accueil
├── medecine/            # Application principale (gestion médicale)
│   ├── models.py        # Modèles de données (Malade, Rendezvous, Consultation, Ordonnance)
│   ├── views.py         # Vues (inscription, rendez-vous)
│   ├── admin.py         # Configuration de l'interface d'administration
│   └── urls.py          # Routes de l'application
├── medicalproject/      # Configuration principale du projet
│   ├── settings.py      # Paramètres Django
│   ├── urls.py          # Routes principales
│   └── wsgi.py          # Configuration WSGI
├── templates/           # Templates HTML
│   ├── firstpage/       # Page d'accueil
│   └── rendezvous/      # Pages d'inscription et rendez-vous
└── static/              # Fichiers statiques (CSS, JS, images)
```

## 🗄️ Modèles de Données

### Malade (Patient)
- Informations personnelles (nom, prénom, sexe, date de naissance)
- Coordonnées (email unique, téléphone, adresse)

### Rendezvous
- Date et heure (validation : entre 09:00 et 16:00)
- Raison de la consultation
- Lien vers le patient

### Consultation
- Informations médicales (état hydrodynamique, respiratoire, échographie)
- Mesures (poids, tension, fièvre)
- Lien OneToOne vers un rendez-vous

### Ordonnance
- Contenu de la prescription
- Lien vers une consultation

## 🔒 Sécurité

- ✅ Variables d'environnement pour les informations sensibles
- ✅ Validation des données côté serveur
- ✅ Protection CSRF activée
- ✅ Validation des rendez-vous (horaires, dates, disponibilités)

## ⚙️ Configuration Email (Gmail)

Pour utiliser Gmail comme service d'envoi d'emails :

1. Activer l'authentification à deux facteurs sur votre compte Gmail
2. Générer un mot de passe d'application :
   - Aller dans : Paramètres Google → Sécurité → Validation en 2 étapes → Mots de passe des applications
   - Créer un nouveau mot de passe d'application
   - Utiliser ce mot de passe dans `EMAIL_HOST_PASSWORD`

## 🐛 Dépannage

### Erreur de migration
```bash
python manage.py makemigrations
python manage.py migrate
```

### Erreur de static files
```bash
python manage.py collectstatic
```

### Email ne fonctionne pas
- Vérifier que les variables d'environnement EMAIL sont correctement configurées
- Pour Gmail, utiliser un mot de passe d'application (pas le mot de passe du compte)
- Vérifier que `EMAIL_HOST_USER` et `EMAIL_HOST_PASSWORD` sont corrects

## 📝 Notes

- Le projet utilise SQLite par défaut (idéal pour le développement)
- Pour la production, configurer une base de données PostgreSQL ou MySQL
- Assurez-vous de changer `DEBUG=False` et de configurer `ALLOWED_HOSTS` pour la production

## 👨‍💻 Développement

Pour contribuer au projet :
1. Créer une branche pour votre fonctionnalité
2. Faire vos modifications
3. Tester localement
4. Créer une pull request

## 📄 Licence

Ce projet est développé pour le Cabinet Dr Asmaa Abidine.

## 📞 Support

Pour toute question ou problème, contactez l'administrateur du système.
