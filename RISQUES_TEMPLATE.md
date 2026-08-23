# Gestion des risques et dette technique : SunuSanté

**Nom / Groupe 1 : Mamadou Yassarou Diallo, Aliou Drame and Nafissatou Niang**

---

## 1. Classification du risque - données patients

**Le modèle Patient (et ses rendez-vous associés) contient-il un risque important, modéré ou faible au sens du chapitre 2 ?**  
**Important**
    
**Justification :**  
Le modèle `Patient` contient des données personnelles permettant d'identifier les patients, notamment le nom, le prénom et l'adresse email. De plus, il est directement associé aux rendez-vous, ce qui peut révéler qu'une personne fréquente une clinique ainsi que certains éléments sur sa prise en charge. Une fuite, une modification non autorisée ou une perte de ces données pourrait donc avoir un impact important sur la confidentialité des patients et sur la réputation de SunuSanté.

---

## 2. Matrice de risques (probabilité × impact)

### Matrice théorique

| Probabilité \ Impact | Faible | Modéré | Élevé |
|---|---|---|---|
| **Élevée** | Modérée | Critique | Critique |
| **Modérée** | Faible | Modérée | Critique |
| **Faible** | Faible | Faible | Modérée |

### Positionnement des risques

| Probabilité \ Impact | Faible | Modéré | Élevé |
|---|---|---|---|
| **Élevée** | | Absence HTTPS en cas d'accès à distance | |
| **Modérée** | | | - `SECRET_KEY` exposée<br>- `DEBUG=True` en production<br>- Dépendances vulnérables |
| **Faible** | | Absence de limite de tentatives admin | |

### Tableau récapitulatif des risques

| Risque identifié | Probabilité | Impact | Priorité résultante |
|---|---|---|---|
| `SECRET_KEY` directement présente dans `settings.py` | Modérée | Élevé | **Critique** |
| `DEBUG = True` potentiellement actif hors environnement de développement | Modérée | Élevé | **Critique** |
| Absence de HTTPS lors du lancement avec le serveur local | Élevée | Modéré | **Critique** |
| Dépendance Django en version fixe sans processus visible de suivi des mises à jour de sécurité | Modérée | Élevé | **Critique** |
| Absence de limitation des tentatives de connexion à l'administration Django | Faible | Modéré | **Faible** |

### Justification des risques

* **Risque 1 — `SECRET_KEY` présente directement dans le code :**  
  La clé secrète Django est actuellement écrite directement dans `settings.py`. Dans un contexte de TP local, cela est explicitement accepté, mais dans une véritable application, si le dépôt est partagé publiquement ou si le code est exposé, cette clé peut être récupérée par une personne non autorisée. Il faudrait donc, dans un environnement réel, stocker cette valeur dans une variable d'environnement ou dans un fichier `.env` non versionné.

* **Risque 2 — `DEBUG = True` :**  
  Le projet possède actuellement :
  ```python
  DEBUG = True
Ce paramètre est adapté au développement, mais il représente un risque si l'application est déployée avec cette configuration. En cas d'erreur, Django peut afficher des informations techniques détaillées sur l'application, son environnement et son fonctionnement interne. En production, DEBUG doit être désactivé.

* **Risque 3 — Absence de HTTPS en local :**

  Le projet est lancé avec :

  ```Bash
    ```python manage.py runserver```
et accessible en HTTP local. Les communications ne sont donc pas chiffrées dans une architecture classique de production. Dans une application de santé réelle, les informations échangées entre le navigateur et le serveur doivent être protégées par HTTPS afin de limiter les risques d'interception ou de modification des données pendant leur transport.

* **Risque 4 — Gestion des dépendances :**

Le fichier requirements.txt contient uniquement :

 ``` Django==5.0.6 ```
Le fait d'utiliser une version précise permet d'avoir un environnement reproductible, ce qui est positif. Cependant, aucune procédure de surveillance ou de mise à jour des vulnérabilités des dépendances n'est actuellement mise en évidence dans le projet. Une dépendance qui devient vulnérable sans être mise à jour peut introduire un risque de sécurité dans l'application.

* **Risque 5 — Absence de limitation des tentatives de connexion à l'administration :**

Le projet utilise l'administration Django, mais la configuration actuelle ne montre pas de mécanisme spécifique limitant les tentatives répétées de connexion. Un attaquant pourrait théoriquement effectuer de nombreuses tentatives de connexion sur les comptes administrateurs. Dans une application réelle, des mécanismes complémentaires tels que la limitation de débit, le blocage temporaire et la surveillance des tentatives devraient être envisagés.

## 3. Post-mortem blameless

Incident simulé :

Une simulation d'incident a été réalisée en utilisant volontairement un identifiant de patient inexistant lors de la consultation de sa facture. Dans la version initiale de la vue, le patient était récupéré avec :

 Python
       ```Patient.objects.get(id=patient_id)```
Lorsqu'aucun patient ne correspondait à l'identifiant fourni, une exception Patient.DoesNotExist était levée, empêchant l'affichage normal de la page de facture.

### Que s'est-il passé ?
Le serveur Django a été démarré localement, puis une requête a été effectuée pour consulter la facture d'un patient avec un identifiant inexistant. La récupération du patient a échoué et l'application a levé une exception Patient.DoesNotExist.

La requête n'a donc pas pu produire la réponse attendue. En environnement de développement, Django a affiché une page détaillée contenant les informations techniques relatives à l'erreur.

### Pourquoi cela s'est-il produit ?
La vue supposait que l'identifiant de patient reçu correspondait obligatoirement à un patient existant dans la base de données. Le code utilisait Patient.objects.get(id=patient_id) sans mécanisme spécifique de gestion du cas où aucun objet n'était trouvé.

Le problème ne provient donc pas d'une personne en particulier, mais d'une hypothèse insuffisamment prise en compte dans la conception : les données provenant d'une URL ou d'une requête HTTP peuvent être invalides, modifiées ou correspondre à des ressources qui n'existent plus.

### Qu'avons-nous appris ?
Cet incident montre que les cas limites et les entrées invalides doivent être pris en compte dès la conception de l'application. Même lorsqu'un identifiant est normalement généré par le système, il ne doit pas être considéré comme automatiquement valide.

L'incident rappelle également que la gestion des erreurs fait partie de la qualité du logiciel. Une application robuste doit pouvoir répondre correctement à une ressource inexistante plutôt que de produire une exception non gérée.

### Que changeons-nous ?
La récupération directe du patient est remplacée par le mécanisme Django suivant :

   Python
        ```patient = get_object_or_404(Patient, id=patient_id)```
Lorsqu'un identifiant inexistant est demandé, l'application renvoie désormais une réponse HTTP 404 Not Found plutôt qu'une exception Patient.DoesNotExist non gérée.
