# SunuSanté - TP2 : Qualité dans le cycle de vie (Django)

## Contexte

SunuSanté grandit : après le module Java du TP1, la clinique veut une vraie
application web. On vous confie un squelette Django déjà fonctionnel : deux
apps, `patients` et `rendezvous` avec un formulaire de prise de
rendez-vous qui marche. Comme au TP1, "ça marche" ne veut pas dire "c'est
bien conçu".

## Installation

```bash
python -m venv venv
# Windows : venv\Scripts\activate   |   macOS/Linux : source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser   # pour ajouter des patients via /admin/
python manage.py runserver
```

- Formulaire de prise de rendez-vous : http://127.0.0.1:8000/rendezvous/
- Gestion des patients : http://127.0.0.1:8000/admin/

Ajoutez au moins 2 patients (dont un `est_vip=True`) avant de tester.

---

## Partie 1 - SDLC et SSDLC

Ouvrez `DOSSIER_SDLC_TEMPLATE.md` et complétez-le dans l'ordre :

1. **Planification** : budget, contraintes juridiques (RGPD - SunuSanté
   manipule des données de santé), contraintes techniques, et surtout les
   **exigences qualité & sécurité** à poser dès maintenant (Shift Left,
   chapitre 2) plutôt qu'en fin de projet.
2. **Conception (HLD/LLD)** : un schéma HLD (les blocs : navigateur, Django,
   base de données) et un LLD sur le flux de prise de rendez-vous.
3. **Threat modeling STRIDE** : pour le flux Navigateur → Django → Base de
   données, remplissez le tableau STRIDE fourni. Posez-vous la question du
   cours pour chaque flèche : *qui pourrait l'intercepter, la falsifier, ou
   la bloquer ?*
4. **Tableau SSDLC** : pour chaque étape (Planification, Design, Codage,
   Tests, Déploiement), notez l'action qualité/sécurité concrète que vous
   allez appliquer dans SunuSanté.

## Partie 2 - Refactoring SOLID / DRY / KISS / YAGNI

Lisez `rendezvous/views.py`. Les deux fonctions marchent, mais :

- Chacune mélange lecture de la requête HTTP, validation, calcul du tarif,
  accès à la base de données et (pour la première) une "notification"
  console. C'est une violation du **principe de responsabilité unique**
  (SRP).
- La logique de tarif (tarif de base, majoration weekend, réduction VIP)
  est recopiée à l'identique dans les deux fonctions, et `facture_patient`
  **recalcule** le prix au lieu de relire `rdv.prix` déjà stocké en base.
  C'est une violation **DRY**.
- La constante `MODE_EXPERIMENTAL` n'est utilisée nulle part : c'est du
  code mort ajouté "au cas où". C'est une violation **YAGNI**.

**Votre travail**, dans cet ordre :

1. Créez `rendezvous/services.py` avec une classe `TarifCalculator` qui
   centralise le calcul du tarif (une méthode par règle : tarif de base,
   majoration weekend, réduction VIP. Chaque méthode ne doit avoir qu'une
   seule décision, comme au TP1).
2. Créez une classe `RendezVousService` qui orchestre validation métier +
   appel à `TarifCalculator` + création du `RendezVous` en base. Les vues
   ne doivent plus jamais recalculer un prix : elles lisent `rdv.prix`.
3. Créez `rendezvous/forms.py` avec un `RendezVousForm` (`forms.Form`) qui
   remplace toutes les vérifications manuelles (`if not patient_id: ...`)
   par la validation native de Django.
4. Réécrivez `prendre_rendez_vous` et `facture_patient` dans `views.py`
   pour qu'elles ne fassent plus que : lire la requête, appeler le
   form/service, choisir un template. Aucune règle métier ne doit rester
   dans les vues.
5. Supprimez `MODE_EXPERIMENTAL`.
6. Écrivez des tests unitaires Django dans `rendezvous/tests.py` pour
   `TarifCalculator` (au moins : tarif de base, majoration weekend,
   réduction VIP, cumul des deux) et `RendezVousService`
   (`creer_rendez_vous`, `facturer_patient`).

*Petit rappel de cohésion/couplage (chapitre 2)* : à la fin, `services.py`
doit être **fortement cohérent** (tout y concerne la tarification/les
rendez-vous) et **faiblement couplé** à Django lui-même : c'est ce qui rend
`TarifCalculator` testable sans base de données ni requête HTTP, comme vous
l'avez fait au TP1 en Java.

## Partie 3 - Gestion des risques et dette technique

1. Ouvrez `RISQUES_TEMPLATE.md`. Classez le risque associé aux données du
   modèle `Patient` (important / modéré / faible) et justifiez.
2. Identifiez au moins 4 risques concrets dans le code actuel de SunuSanté
   (indice : regardez `settings.py`, la façon dont le projet est lancé en
   local, les dépendances dans `requirements.txt`...). Placez-les dans la
   matrice probabilité × impact.
3. **Simulation d'incident** : coupez volontairement le service (par
   exemple, arrêtez le serveur en pleine démonstration, ou introduisez puis
   observez un bug simple comme une exception `Patient.DoesNotExist` sur un
   ID invalide dans `facture_patient`). Rédigez un post-mortem blameless en
   suivant les 4 questions du template : que s'est-il passé, pourquoi,
   qu'avons-nous appris, que changeons-nous.

## Rendu attendu

- Dépôt Git avec historique de commits lisible (idéalement : un commit par
  étape de refactoring)
- `DOSSIER_SDLC_TEMPLATE.md` et `RISQUES_TEMPLATE.md` complétés
- `rendezvous/services.py`, `rendezvous/forms.py`, `rendezvous/views.py`
  refactorés
- `rendezvous/tests.py` avec les tests unitaires, tous verts
  (`python manage.py test`)
