# Dossier SDLC - SunuSanté

## Nom / Groupe : Groupe 1: Mamadou Yassarou Diallo, Aliou Dramé and Nafissatou Niang

## 1. Planification & recueil des besoins

| Contrainte | Réponse |
|---|---|
| **Budget** | Budget maîtrisé dans un contexte académique : priorité aux technologies Open Source et aux solutions éprouvées afin de limiter les coûts de licence, de développement et de maintenance. Django est retenu comme framework principal car il fournit de nombreux mécanismes intégrés pour le développement web et la sécurité. |
| **Juridique (RGPD - données de santé)** | SunuSanté manipule des données personnelles et potentiellement sensibles liées aux patients. Le système doit donc respecter les principes de protection des données : minimisation des données collectées, contrôle des accès, authentification des utilisateurs autorisés, protection des données en transit et au repos, traçabilité des actions sensibles et gestion des droits des personnes. |
| **Technique (hébergement, BDD, etc.)** | Architecture web basée sur Python et Django. SQLite est acceptable pour le développement et le TP, mais une base de données adaptée à la production, comme PostgreSQL, devra être envisagée. Le déploiement devra utiliser HTTPS, une gestion sécurisée des secrets via des variables d'environnement et une configuration séparée entre les environnements de développement et de production. |
| **Qualité & sécurité (Shift Left)** | Les exigences de qualité et de sécurité doivent être définies dès la planification et non ajoutées uniquement à la fin du projet. Elles incluent notamment : validation des données, gestion des erreurs, séparation des responsabilités, tests automatisés, objectif de couverture sur la logique métier, revue de code, analyse des dépendances et identification des risques de sécurité avant le développement. |
| **Qualité & timing** | Approche itérative inspirée d'Agile/Scrum avec des livraisons fréquentes. Chaque fonctionnalité doit être accompagnée de tests et validée avant intégration. Une intégration continue peut exécuter automatiquement les tests et contrôles de qualité à chaque modification. Un objectif de couverture de 70 à 80 % minimum peut être visé pour la logique métier, tout en privilégiant la pertinence des tests plutôt que la recherche artificielle de 100 % de couverture. |

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
