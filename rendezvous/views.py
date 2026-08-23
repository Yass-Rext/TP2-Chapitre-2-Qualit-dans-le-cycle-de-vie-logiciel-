"""
TP2 - Vues refactorées.

Les vues gèrent uniquement la couche HTTP :
lecture de la requête, validation via formulaire,
appel aux services et choix de la réponse.
"""

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from patients.models import Patient

from .forms import RendezVousForm
# from .models import TypeConsultation
from .services import RendezVousService


def prendre_rendez_vous(request):
    if request.method == "POST":
        form = RendezVousForm(request.POST)

        if form.is_valid():
            service = RendezVousService()

            rdv = service.creer_rendez_vous(
                patient=form.cleaned_data["patient"],
                type_consultation=form.cleaned_data["type_consultation"],
                date_consultation=form.cleaned_data["date"],
            )

            messages.success(
                request,
                f"Rendez-vous confirmé - {rdv.prix} FCFA"
            )

            return redirect("rendezvous:prendre")

        messages.error(
            request,
            "Veuillez corriger les erreurs du formulaire"
        )

    else:
        form = RendezVousForm()

    return render(
        request,
        "rendezvous/formulaire.html",
        {
            "form": form,
        },
    )


def facture_patient(request, patient_id):
    patient = get_object_or_404(
        Patient,
        id=patient_id
    )

    service = RendezVousService()

    total = service.facturer_patient(patient)

    return render(
        request,
        "rendezvous/facture.html",
        {
            "patient": patient,
            "total": total,
        },
    )