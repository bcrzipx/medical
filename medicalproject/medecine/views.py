from django.shortcuts import render, redirect
from .models import Malade, Rendezvous
from datetime import datetime
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings
from django.db import IntegrityError


def rendezvous(request):
    if request.method == 'POST':
        try:
            nom = request.POST.get('nom', '').strip()
            prenom = request.POST.get('prenom', '').strip()
            email = request.POST.get('email', '').strip().lower()
            date_rendez_vous_str = request.POST.get('dateR', '')
            heure_rendez_vous_str = request.POST.get('heureR', '')
            raison = request.POST.get('raisonR', '').strip()
            sexe = request.POST.get('sexe', '')

            # Validation des champs requis
            if not all([nom, prenom, email, date_rendez_vous_str, heure_rendez_vous_str, raison, sexe]):
                messages.error(request, "Veuillez remplir tous les champs requis.")
                return render(request, 'rendezvous/rendezvous.html')

            # Conversion des dates
            try:
                date_rendez_vous = datetime.strptime(date_rendez_vous_str, '%Y-%m-%d').date()
                heure_rendez_vous = datetime.strptime(heure_rendez_vous_str, '%H:%M').time()
            except ValueError:
                messages.error(request, "Format de date ou d'heure invalide.")
                return render(request, 'rendezvous/rendezvous.html')

            # Vérifier si le patient existe
            try:
                malade = Malade.objects.get(email=email)
                # Vérifier que les informations correspondent
                if malade.nom.lower() != nom.lower() or malade.prenom.lower() != prenom.lower():
                    messages.error(request, "Les informations ne correspondent pas à votre compte. Veuillez vous inscrire d'abord.")
                    return redirect('inscription')
            except Malade.DoesNotExist:
                messages.warning(request, "Vous devez d'abord vous inscrire avant de prendre un rendez-vous.")
                return redirect('inscription')

            # Créer le rendez-vous avec validation
            try:
                rendezvous_obj = Rendezvous(
                    date=date_rendez_vous,
                    heure=heure_rendez_vous,
                    raison=raison,
                    malade=malade
                )
                rendezvous_obj.full_clean()  # Appelle clean() et valide tous les champs
                rendezvous_obj.save()

                # Préparer le message de confirmation du rendez-vous
                message = f"""Bonjour {prenom} {nom},

Votre rendez-vous du {date_rendez_vous_str} à {heure_rendez_vous_str} a été confirmé avec succès.

Raison: {raison}

Merci de votre confiance.
Cabinet Dr Asmaa Abidine"""

                # Envoi de l'e-mail de confirmation au patient
                try:
                    send_mail(
                        'Confirmation de rendez-vous',
                        message,
                        settings.EMAIL_HOST_USER,
                        [email],
                        fail_silently=False
                    )
                except Exception as e:
                    # L'email n'a pas pu être envoyé mais le rendez-vous est enregistré
                    messages.warning(request, "Le rendez-vous a été pris mais l'email de confirmation n'a pas pu être envoyé.")

                messages.success(request, "Le rendez-vous a été pris avec succès ! Un e-mail de confirmation vous a été envoyé.")
                return redirect('rendezvous')
            except ValidationError as e:
                error_message = str(e)
                if "date" in error_message.lower():
                    messages.error(request, "La date ne peut pas être dans le passé.")
                elif "heure" in error_message.lower():
                    messages.error(request, "L'heure doit être entre 09:00 et 16:00, ou cette heure est déjà prise.")
                else:
                    messages.error(request, f"Erreur de validation: {error_message}")
                return render(request, 'rendezvous/rendezvous.html')
            except IntegrityError:
                messages.error(request, "Ce rendez-vous existe déjà. Veuillez choisir une autre date et heure.")
                return render(request, 'rendezvous/rendezvous.html')

        except Exception as e:
            messages.error(request, "Une erreur est survenue. Veuillez réessayer.")
            return render(request, 'rendezvous/rendezvous.html')

    return render(request, 'rendezvous/rendezvous.html')

def inscription(request):
    if request.method == 'POST':
        try:
            nom = request.POST.get('nom', '').strip()
            prenom = request.POST.get('prenom', '').strip()
            sexe = request.POST.get('sexe', '')
            date_naissance_str = request.POST.get('datenaissance', '')
            email = request.POST.get('email', '').strip().lower()
            telephone = request.POST.get('telephone', '').strip()
            adresse = request.POST.get('adresse', '').strip()

            # Validation des champs requis
            if not all([nom, prenom, sexe, date_naissance_str, email, telephone, adresse]):
                messages.error(request, "Veuillez remplir tous les champs requis.")
                return render(request, 'rendezvous/inscription.html')

            # Validation du sexe
            if sexe not in ['femme', 'homme']:
                messages.error(request, "Veuillez sélectionner un sexe valide.")
                return render(request, 'rendezvous/inscription.html')

            # Conversion de la date
            try:
                date_naissance = datetime.strptime(date_naissance_str, '%Y-%m-%d').date()
                # Vérifier que la date de naissance est valide (pas dans le futur)
                from django.utils import timezone
                if date_naissance > timezone.now().date():
                    messages.error(request, "La date de naissance ne peut pas être dans le futur.")
                    return render(request, 'rendezvous/inscription.html')
            except ValueError:
                messages.error(request, "Format de date invalide.")
                return render(request, 'rendezvous/inscription.html')

            # Vérifier si l'email existe déjà
            if Malade.objects.filter(email=email).exists():
                messages.warning(request, "Cet email est déjà inscrit. Vous pouvez maintenant prendre un rendez-vous.")
                return redirect('rendezvous')

            # Créer le patient
            try:
                malade = Malade.objects.create(
                    nom=nom,
                    prenom=prenom,
                    sexe=sexe,
                    date_naissance=date_naissance,
                    email=email,
                    telephone=telephone,
                    adresse=adresse
                )

                # Préparer le message de confirmation d'inscription
                message = f"""Bonjour {prenom} {nom},

Votre inscription a été enregistrée avec succès.

Vous pouvez maintenant prendre un rendez-vous sur notre site.

Merci de votre confiance.
Cabinet Dr Asmaa Abidine"""

                # Envoi de l'e-mail de confirmation d'inscription
                try:
                    send_mail(
                        'Confirmation d\'inscription',
                        message,
                        settings.EMAIL_HOST_USER,
                        [email],
                        fail_silently=False
                    )
                except Exception as e:
                    messages.warning(request, "L'inscription a été enregistrée mais l'email de confirmation n'a pas pu être envoyé.")

                messages.success(request, "L'inscription a été faite avec succès ! Vous pouvez maintenant prendre un rendez-vous.")
                return redirect('rendezvous')
            except IntegrityError:
                messages.error(request, "Cet email est déjà utilisé. Veuillez utiliser un autre email.")
                return render(request, 'rendezvous/inscription.html')
            except Exception as e:
                messages.error(request, f"Une erreur est survenue lors de l'inscription: {str(e)}")
                return render(request, 'rendezvous/inscription.html')

        except Exception as e:
            messages.error(request, "Une erreur est survenue. Veuillez réessayer.")
            return render(request, 'rendezvous/inscription.html')

    return render(request, 'rendezvous/inscription.html')