# Gestion des risques et dette technique : SunuSanté

Nom / Groupe :

## 1. Classification du risque - données patients

Le modèle `Patient` (et ses rendez-vous associés) contient-il un risque
important, modéré ou faible au sens du chapitre 2 ? Entourez et justifiez
en 2-3 phrases.

**Important / Modéré / Faible**

Justification :

## 2. Matrice de risques (probabilité × impact)

Identifiez au moins 4 risques concrets dans le code actuel de SunuSanté
(exemples de pistes : gestion du secret Django, absence de HTTPS en local,
dépendances non maintenues, absence de limite de tentatives de connexion à
l'admin...). Placez chacun dans la matrice, puis dans le tableau.

```
              IMPACT →
              Faible      Modéré      Élevé
PROBABILITÉ
Élevée        modérée     critique    critique
Modérée       faible      modérée     critique
Faible        faible      faible      modérée
```

| Risque identifié | Probabilité | Impact | Priorité résultante |
|---|---|---|---|
| | | | |
| | | | |
| | | | |
| | | | |

## 3. Post-mortem blameless

Décrivez brièvement l'incident simulé (voir consigne du README), puis
répondez aux 4 questions du cours **sans chercher de coupable** : l'objectif
est de comprendre les causes systémiques.

**Incident simulé :**

### Que s'est-il passé ?

Chronologie factuelle, sans jugement.

### Pourquoi cela s'est-il produit ?

Analyse des causes racines (systèmes, processus - pas de noms de personnes).

### Qu'avons-nous appris ?

Ce que l'incident révèle sur SunuSanté.

### Que changeons-nous ?

Action(s) concrète(s), avec un responsable (vous) et une échéance
raisonnable pour ce TP.
