# Dossier SDLC - SunuSanté

Nom / Groupe :

## 1. Planification & recueil des besoins

| Contrainte                                     | Réponse |
|------------------------------------------------|---|
| Budget                                         | |
| Juridique (RGPD - données de santé)            | |
| Technique (hébergement, base de données, etc.) | |
| Qualité & timing                               | |

### Exigences qualité & sécurité posées dès maintenant (Shift Left)

Listez au moins 3 exigences que vous posez **avant** de coder (pas après),
en vous inspirant de l'exemple du cours (standards de code, MFA/chiffrement
des données sensibles, conformité RGPD dès la planification).

1.
2.
3.

## 2. Conception (HLD / LLD)

### HLD - vue générale

Décrivez ou schématisez (texte, ASCII art, ou lien vers une image) les
grands blocs de SunuSanté et leurs interactions : navigateur, application
Django, base de données.

### LLD - détails du flux "prendre un rendez-vous"

Décrivez le déroulé précis : quelles données envoyées, quel format, quelles
étapes de validation, quelle réponse renvoyée.

## 3. Threat Modeling - méthode STRIDE

Flux étudié : **Navigateur → Django (API/vues) → Base de données**

Pour chaque famille de menace STRIDE, identifiez au moins une menace
plausible sur ce flux et une contre-mesure (déjà en place ou à prévoir).

| Menace STRIDE | Exemple concret sur SunuSanté | Contre-mesure |
|---|---|---|
| **S**poofing (usurpation) | | |
| **T**ampering (falsification) | | |
| **R**epudiation (répudiation) | | |
| **I**nformation disclosure (divulgation) | | |
| **D**enial of service (déni de service) | | |
| **E**levation of privilege (élévation de privilège) | | |

## 4. Tableau SSDLC - qualité et sécurité à chaque étape

Pour chaque étape du SDLC, notez l'action concrète que vous appliquez (ou
allez appliquer) dans SunuSanté.

| Étape | Action qualité/sécurité prévue |
|---|---|
| Planification | |
| Design | |
| Codage | |
| Tests | |
| Déploiement | |
