# from django.test import TestCase

# TODO (TP2, étape 2) : une fois la logique de tarif extraite dans
# services.py (hors des vues), écrivez ici des tests unitaires pour cette
# nouvelle classe/fonction. Comparez avec solution/rendezvous/tests.py une
# fois votre refactoring terminé.


from datetime import date

from django.test import TestCase

from .services import TarifCalculator


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