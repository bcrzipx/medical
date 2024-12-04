from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Malade, Rendezvous
from datetime import datetime
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm


@login_required
def rendezvous(request):
    if request.method == 'POST':
        nom = request.POST['nom']
        prenom = request.POST['prenom']
        email = request.POST['email']
        date_rendez_vous_str = request.POST['dateR']
        date_rendez_vous = datetime.strptime(date_rendez_vous_str, '%Y-%m-%d').date()
        heure_rendez_vous_str = request.POST['heureR']
        heure_rendez_vous = datetime.strptime(heure_rendez_vous_str, '%H:%M').time()
        raison = request.POST['raisonR']
        sexe = request.POST['sexe']

        try:
            malade = Malade.objects.get(email=email)
        except Malade.DoesNotExist:
            return redirect('inscription')

        try:
            rendezvous = Rendezvous.objects.create(
                date=date_rendez_vous,
                heure=heure_rendez_vous,
                raison=raison,
                malade=malade
            )
            rendezvous.save()

            # Préparer le message de confirmation du rendez-vous
            message = f"Votre rendez-vous du {date_rendez_vous_str} à {heure_rendez_vous_str} a été confirmé avec succès."

            # Envoi de l'e-mail de confirmation au patient
            send_mail(
                'Confirmation de rendez-vous',
                message,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False
            )

            messages.success(request, "Le rendez-vous a été pris avec succès ! Un e-mail de confirmation vous a été envoyé.")
            return redirect('rendezvous')
        except ValidationError as e:
            messages.error(request, "Choisissez une autre date et heure pour le rendez-vous.")
            return redirect('rendezvous')

    return render(request, 'rendezvous/rendezvous.html')

def inscription(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        sexe = request.POST.get('sexe')
        date_naissance = request.POST.get('datenaissance')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')
        adresse = request.POST.get('adresse')

        malade = Malade.objects.create(
            nom=nom,
            prenom=prenom,
            sexe=sexe,
            date_naissance=date_naissance,
            email=email,
            telephone=telephone,
            adresse=adresse
        )
        malade.save()

        # Préparer le message de confirmation d'inscription
        message = 'Votre inscription a été enregistrée avec succès.'

        # Envoi de l'e-mail de confirmation d'inscription
        send_mail(
            'Confirmation d\'inscription',
            message,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False
        )

        messages.success(request, "L'inscription a été faite avec succès ! Prenez le rendez-vous une autre fois.")
        return redirect('rendezvous')

    else:
        form = UserCreationForm()

    return render(request, 'rendezvous/inscription.html')