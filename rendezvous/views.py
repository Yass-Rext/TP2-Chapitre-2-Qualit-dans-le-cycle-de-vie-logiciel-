"""
TP2 - Vues fournies aux étudiants.

Ce module FONCTIONNE : on peut prendre un rendez-vous et consulter la
facture d'un patient. Mais il mélange tout dans les vues : lecture de la
requête, validation, calcul du tarif, persistance, "notification" et
préparation de l'affichage (violation du principe de responsabilité
unique, chapitre 2). Le calcul du tarif est en plus recopié à l'identique
entre les deux vues (violation DRY) au lieu de réutiliser rdv.prix déjà
stocké en base.

NE MODIFIEZ PAS CE FICHIER avant d'avoir lu le README de ce dossier.
"""
from datetime import date as date_cls

from django.contrib import messages
from django.shortcuts import redirect, render

from patients.models import Patient

from .models import RendezVous, TypeConsultation

# TODO (YAGNI, chapitre 2) : ce flag n'est utilisé nulle part dans le code.
# Un développeur l'a ajouté "au cas où on ait besoin d'un mode bêta plus
# tard". Que faut-il en faire ?
MODE_EXPERIMENTAL = False


def prendre_rendez_vous(request):
    if request.method == "POST":
        patient_id = request.POST.get("patient_id")
        type_consultation = request.POST.get("type_consultation")
        date_str = request.POST.get("date")

        if not patient_id:
            messages.error(request, "Le patient est obligatoire")
            return redirect("rendezvous:prendre")
        if not date_str:
            messages.error(request, "La date est obligatoire")
            return redirect("rendezvous:prendre")

        patient = Patient.objects.get(id=patient_id)
        rdv_date = date_cls.fromisoformat(date_str)

        if type_consultation == TypeConsultation.GENERALISTE:
            prix = 5000
        elif type_consultation == TypeConsultation.SPECIALISTE:
            prix = 10000
        elif type_consultation == TypeConsultation.URGENCE:
            prix = 15000
        else:
            messages.error(request, "Type de consultation inconnu")
            return redirect("rendezvous:prendre")

        if rdv_date.weekday() >= 5:  # 5 = samedi, 6 = dimanche
            if type_consultation == TypeConsultation.GENERALISTE:
                prix = prix + prix * 0.2
            elif type_consultation == TypeConsultation.SPECIALISTE:
                prix = prix + prix * 0.2
            elif type_consultation == TypeConsultation.URGENCE:
                prix = prix + prix * 0.2

        if patient.est_vip:
            if type_consultation == TypeConsultation.GENERALISTE:
                prix = prix - prix * 0.1
            elif type_consultation == TypeConsultation.SPECIALISTE:
                prix = prix - prix * 0.1
            elif type_consultation == TypeConsultation.URGENCE:
                prix = prix - prix * 0.1

        RendezVous.objects.create(
            patient=patient,
            type_consultation=type_consultation,
            date=rdv_date,
            prix=prix,
        )

        # "Notification" simulée : dans la vraie vie, ce serait un email/SMS.
        print(f"[notification] Rendez-vous confirmé pour {patient} le {rdv_date} - {prix} FCFA")

        messages.success(request, f"Rendez-vous confirmé - {prix} FCFA")
        return redirect("rendezvous:prendre")

    patients = Patient.objects.all()
    return render(
        request,
        "rendezvous/formulaire.html",
        {"patients": patients, "types": TypeConsultation.choices},
    )


def facture_patient(request, patient_id):
    patient = Patient.objects.get(id=patient_id)
    total = 0

    for rdv in RendezVous.objects.filter(patient=patient):
        type_consultation = rdv.type_consultation

        # Recalcul intégral du prix au lieu de réutiliser rdv.prix déjà
        # stocké : c'est la duplication à repérer (chapitre 2, DRY).
        if type_consultation == TypeConsultation.GENERALISTE:
            prix = 5000
        elif type_consultation == TypeConsultation.SPECIALISTE:
            prix = 10000
        elif type_consultation == TypeConsultation.URGENCE:
            prix = 15000
        else:
            prix = 0

        if rdv.date.weekday() >= 5:
            if type_consultation == TypeConsultation.GENERALISTE:
                prix = prix + prix * 0.2
            elif type_consultation == TypeConsultation.SPECIALISTE:
                prix = prix + prix * 0.2
            elif type_consultation == TypeConsultation.URGENCE:
                prix = prix + prix * 0.2

        if patient.est_vip:
            if type_consultation == TypeConsultation.GENERALISTE:
                prix = prix - prix * 0.1
            elif type_consultation == TypeConsultation.SPECIALISTE:
                prix = prix - prix * 0.1
            elif type_consultation == TypeConsultation.URGENCE:
                prix = prix - prix * 0.1

        total = total + prix

    return render(request, "rendezvous/facture.html", {"patient": patient, "total": total})
