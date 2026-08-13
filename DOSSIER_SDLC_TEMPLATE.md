# Dossier SDLC - SunuSanté

## Nom / Groupe : Groupe 1: Mamadou Yassarou Diallo, Aliou Dramé and Nafissatou Niang

## 1. Planification & recueil des besoins

| Contrainte | Réponse |
|---|---|
| **Budget** | Maîtrisé / Académique (Open Source) : priorité au développement backend optimisé et à l'usage de briques éprouvées (Django). |
| **Juridique (RGPD - données de santé)** | Strict respect du traitement des PII (données personnelles) et données médicales : consentement explicite, chiffrement au repos/en transit, droit d'accès et à l'oubli. |
| **Technique (hébergement, BDD, etc.)** | Architecture Python 3.x / Django, base de données PostgreSQL en production, conteneurisation Docker et HTTPS obligatoire. |
| **Qualité & timing** | Approche Agile/Scrum avec livraisons itératives, intégration continue (CI/CD) et couverture de tests unitaires minimum de 80%. |

### Exigences qualité & sécurité posées dès maintenant (Shift Left)

1. **Chiffrement et minimisation des données (Privacy by Design)** : Chiffrement des données sensibles en base de données et transfert sous HTTPS/TLS 1.3.
2. **Gestion stricte des accès et RBAC** : Authentification renforcée pour le personnel médical avec séparation stricte des privilèges (ex: accès `/admin/` limité aux administrateurs).
3. **Analyse statique continue du code (SAST)** : Intégration de linters (`Flake8`, `Black`) et d'outils de détection de vulnérabilités (`Bandit`, `pip-audit`) dès l'étape de développement.

---



## 2. Conception (HLD / LLD)

### HLD - vue générale

```mermaid
graph TD
    A["<b>Navigateur Web</b><br/>(Client/User)"]
    
    subgraph Django ["<b>Serveur Web / Django</b>"]
        direction TB
        B1["Middlewares (Auth, CSRF, Security)"]
        B2["Vues (Request/Response)"]
        B3["Couche Service (RendezVousService)"]
    end
    
    C[("<b>Base de Données Relationale</b><br/>(PostgreSQL / SQLite)")]

    A <-->|"HTTPS"| Django
    Django -->|"ORM Django"| C

    classDef client fill:#f9f9f9,stroke:#333,stroke-width:2px;
    classDef db fill:#e1f5fe,stroke:#0288d1,stroke-width:2px;
    class A client;
    class C db;
```

### LLD - détails du flux "prendre un rendez-vous"

1. **Requête HTTP POST** : Le navigateur envoie `patient_id`, `date_heure` et `motif` via HTTPS à `/rendezvous/`.
2. **Validation (`RendezVousForm`)** : Django valide le type des données, le jeton CSRF et vérifie l'existence du patient.
3. **Traitement Métier (`RendezVousService`)** : 
   - Appelle `TarifCalculator` pour appliquer les règles métiers (tarif de base, majoration weekend, réduction VIP).
   - Instancie et sauvegarde l'objet `RendezVous` en BDD avec son prix définitif calculé.
4. **Réponse HTTP** : Django renvoie une redirection HTTP 302 vers la facture ou effectue un rendu de la page de confirmation.

---

## 3. Threat Modeling - méthode STRIDE

Flux étudié : **Navigateur → Django (API/vues) → Base de données**

| Menace STRIDE | Exemple concret sur SunuSanté | Contre-mesure |
|---|---|---|
| **S**poofing (usurpation) | Usurpation de session d'un médecin ou d'un patient. | Jetons de session sécurisés (`HttpOnly`, `SameSite=Lax`, `Secure`), HTTPS obligatoire. |
| **T**ampering (falsification) | Modification du montant du RDV ou injection SQL dans le formulaire. | Utilisation exclusive de l'ORM Django (requêtes préparées) et calcul impératif du prix côté serveur. |
| **R**epudiation (répudiation) | Un utilisateur nie avoir annulé ou créé un rendez-vous. | Journalisation (logging) centralisée et infalsifiable des événements majeurs avec horodatage UTC. |
| **I**nformation disclosure (divulgation) | Fuite d'informations médicales via une exception brute affichée à l'écran. | `DEBUG=False` en production et pages d'erreurs 404/500 personnalisées. |
| **D**enial of service (déni de service) | Soumission en masse du formulaire de prise de rendez-vous pour saturer la BDD. | Implémentation d'un Rate Limiting sur les endpoints sensibles (ex: `django-ratelimit`). |
| **E**levation of privilege (élévation) | Un patient tente d'accéder aux vues réservées à l'administration (`/admin/`). | Contrôle d'accès basé sur les rôles (`@staff_member_required`, `PermissionRequiredMixin`). |

---

## 4. Tableau SSDLC - qualité et sécurité à chaque étape

| Étape | Action qualité/sécurité prévue |
|---|---|
| **Planification** | Analyse d'impact sur la vie privée (PIA/RGPD) et définition des exigences de sécurité (Shift Left). |
| **Design** | Modélisation des menaces (STRIDE) et architecture modulaire à faible couplage. |
| **Codage** | Application des principes SOLID, revues de code systématiques (Pull Requests) et analyse statique SAST (`Bandit`). |
| **Tests** | Tests unitaires automatisés, tests d'intégration du service tarifaire et vérification des failles OWASP Top 10. |
| **Déploiement** | Hardening du serveur, désactivation du mode Debug (`DEBUG=False`) et gestion des secrets via variables d'environnement (`.env`). |
