from datetime import date

from .models import RendezVous


class TarifCalculator:

    def tarif_base(self, type_consultation):
        tarifs = {
            "GENERALISTE": 5000,
            "SPECIALISTE": 10000,
            "URGENCE": 15000,
        }

        if type_consultation not in tarifs:
            raise ValueError(
                f"Type de consultation inconnu : {type_consultation}"
            )

        return tarifs[type_consultation]

    def appliquer_majoration_weekend(self, prix, date_consultation):
        if date_consultation.weekday() >= 5:
            return prix * 1.20

        return prix

    def appliquer_reduction_vip(self, prix, est_vip):
        if est_vip:
            return prix * 0.90

        return prix

    def calculer(self, type_consultation, date_consultation, est_vip):
        prix = self.tarif_base(type_consultation)
        prix = self.appliquer_majoration_weekend(
            prix,
            date_consultation
        )
        prix = self.appliquer_reduction_vip(
            prix,
            est_vip
        )

        return prix
    

class RendezVousService:

    def __init__(self):
        self.tarif_calculator = TarifCalculator()

    def creer_rendez_vous(
        self,
        patient,
        type_consultation,
        date_consultation
    ):
        prix = self.tarif_calculator.calculer(
            type_consultation,
            date_consultation,
            patient.est_vip
        )

        return RendezVous.objects.create(
            patient=patient,
            type_consultation=type_consultation,
            date=date_consultation,
            prix=prix,
        )
        
    def facturer_patient(self, patient):
        rendez_vous = RendezVous.objects.filter(
            patient=patient
        )

        return sum(rdv.prix for rdv in rendez_vous)