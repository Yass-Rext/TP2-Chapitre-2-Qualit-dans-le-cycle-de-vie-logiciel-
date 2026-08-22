from django import forms

from patients.models import Patient

from .models import TypeConsultation


class RendezVousForm(forms.Form):
    patient = forms.ModelChoiceField(
        queryset=Patient.objects.all(),
        empty_label="Sélectionnez un patient",
        label="Patient",
    )

    type_consultation = forms.ChoiceField(
        choices=TypeConsultation.choices,
        label="Type de consultation",
    )

    date = forms.DateField(
        label="Date",
        widget=forms.DateInput(
            attrs={"type": "date"}
        ),
    )