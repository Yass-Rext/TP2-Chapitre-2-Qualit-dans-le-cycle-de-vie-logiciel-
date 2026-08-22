# from django.test import TestCase

# TODO (TP2, étape 2) : une fois la logique de tarif extraite dans
# services.py (hors des vues), écrivez ici des tests unitaires pour cette
# nouvelle classe/fonction. Comparez avec solution/rendezvous/tests.py une
# fois votre refactoring terminé.


from datetime import date
from django.test import TestCase
from .services import TarifCalculator, RendezVousService
from .models import RendezVous, TypeConsultation
from patients.models import Patient
from decimal import Decimal



class TarifCalculatorTest(TestCase):

    def setUp(self):
        self.calculator = TarifCalculator()

    def test_tarif_base_generaliste(self):
        prix = self.calculator.tarif_base("GENERALISTE")

        self.assertEqual(prix, 5000)

    def test_tarif_base_specialiste(self):
        prix = self.calculator.tarif_base("SPECIALISTE")

        self.assertEqual(prix, 10000)

    def test_tarif_base_urgence(self):
        prix = self.calculator.tarif_base("URGENCE")

        self.assertEqual(prix, 15000)

    def test_tarif_base_type_inconnu(self):
        with self.assertRaises(ValueError):
            self.calculator.tarif_base("CARDIOLOGUE")

    def test_majoration_weekend(self):
        prix = self.calculator.appliquer_majoration_weekend(
            10000,
            date(2026, 7, 25)
        )

        self.assertEqual(prix, 12000)

    def test_pas_de_majoration_en_semaine(self):
        prix = self.calculator.appliquer_majoration_weekend(
            10000,
            date(2026, 7, 21)
        )

        self.assertEqual(prix, 10000)

    def test_reduction_vip(self):
        prix = self.calculator.appliquer_reduction_vip(
            10000,
            True
        )

        self.assertEqual(prix, 9000)

    def test_pas_de_reduction_non_vip(self):
        prix = self.calculator.appliquer_reduction_vip(
            10000,
            False
        )

        self.assertEqual(prix, 10000)

    def test_cumul_weekend_et_vip(self):
        prix = self.calculator.calculer(
            "URGENCE",
            date(2026, 7, 25),
            True
        )

        self.assertEqual(prix, 16200)

    def test_calcul_generaliste_semaine_non_vip(self):
        prix = self.calculator.calculer(
            "GENERALISTE",
            date(2026, 7, 21),
            False
        )

        self.assertEqual(prix, 5000)
        
        
class RendezVousServiceTest(TestCase):

    def setUp(self):
        self.patient = Patient.objects.create(
            nom="Ndiaye",
            prenom="Awa",
            email="awa@example.com",
            est_vip=False
        )

        self.service = RendezVousService()

    def test_creer_rendez_vous(self):
        rdv = self.service.creer_rendez_vous(
            patient=self.patient,
            type_consultation=TypeConsultation.GENERALISTE,
            date_consultation=date(2026, 7, 21)
        )

        self.assertIsNotNone(rdv.pk)
        self.assertEqual(rdv.patient, self.patient)
        self.assertEqual(
            rdv.type_consultation,
            TypeConsultation.GENERALISTE
        )
        self.assertEqual(
            rdv.date,
            date(2026, 7, 21)
        )
        self.assertEqual(rdv.prix, Decimal("5000"))

    def test_creer_rendez_vous_patient_vip_weekend(self):
        patient_vip = Patient.objects.create(
            nom="Fall",
            prenom="Moussa",
            email="moussa@example.com",
            est_vip=True
        )

        rdv = self.service.creer_rendez_vous(
            patient=patient_vip,
            type_consultation=TypeConsultation.URGENCE,
            date_consultation=date(2026, 7, 25)
        )

        self.assertEqual(rdv.prix, Decimal("16200"))

    def test_facturer_patient(self):
        self.service.creer_rendez_vous(
            patient=self.patient,
            type_consultation=TypeConsultation.GENERALISTE,
            date_consultation=date(2026, 7, 21)
        )

        self.service.creer_rendez_vous(
            patient=self.patient,
            type_consultation=TypeConsultation.SPECIALISTE,
            date_consultation=date(2026, 7, 21)
        )

        total = self.service.facturer_patient(self.patient)

        self.assertEqual(total, Decimal("15000"))

    def test_facturer_patient_ne_prend_que_ses_rendez_vous(self):
        autre_patient = Patient.objects.create(
            nom="Diop",
            prenom="Fatou",
            email="fatou@example.com",
            est_vip=False
        )

        self.service.creer_rendez_vous(
            patient=self.patient,
            type_consultation=TypeConsultation.GENERALISTE,
            date_consultation=date(2026, 7, 21)
        )

        self.service.creer_rendez_vous(
            patient=autre_patient,
            type_consultation=TypeConsultation.URGENCE,
            date_consultation=date(2026, 7, 21)
        )

        total = self.service.facturer_patient(self.patient)

        self.assertEqual(total, Decimal("5000"))