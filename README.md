# Test technique Django / React

L'objectif de l'exercice ci-dessous est de concevoir une interface simple de gestion de trajets de bus.
Pour réaliser le test, penser à fork ce repository. Idéalement, ouvrir une PR à la fin.

## Critères d'évaluation

- Compréhension de la modélisation
- Clarté du code
- Maîtrise des framework Django et React

## Stack Technique

| Nom    | Version |
|--------|---------|
| Python | 3.7     |
| Django | 3.2.5   |
| React  | 18.2.0  |


### Démarrer le projet

*Depuis votre virtualenv*:

```
make install
make migrate
make run
```

Des scripts sont à votre disposition pour vous permettre de rapidement créer des données et de prendre le projet en 
main:

 - `create_data`
 - `create_buses`
 - `create_drivers`
 - `create_places`
 - `create_users`
 - `create_busshifts`

Par exemple:

```
python manage.py create_busshifts -n 5
```

## Sujet

### Description

Un trajet en bus (`BusShift`) est composé des éléments suivants:

- Un bus: (`Bus`).
- Un chauffeur: (`Driver`).
- Entre 2 et une infinité d'arrêts (`BusStop`).
- L'heure de départ est déterminée par l'heure de passage au premier arrêt.
- L'heure d'arrivée est déterminée par l'heure de passage au dernier arrêt.
- Un même bus ne peut être assigné, en même temps, à plusieurs trajets dont les heures de début et fin se 
chevaucheraient.
- Il en va de même pour les chauffeurs.

La structure de projet qui vous est proposée comprend déjà les models suivants:
 - `Bus`
 - `Driver`
 - `Place` 
 - `BusShift`
 - `BusStop`
 - `User` (étend le model [AbstractUser de Django](https://docs.djangoproject.com/en/3.2/topics/auth/customizing/#substituting-a-custom-user-model))

### Objectifs

#### Fournir une interface de gestion des trajets de bus

Il doit être possible de créer ou de modifier des trajets de bus (`BusShift`) en utilisant l'app React.
Les potentielles erreurs lors de la création ou la modification doivent être affichées à l'utilisateur. 

### Conseils

 - Ne passez pas plus de 2 heures sur un sujet (le but est d'évaluer vos compétences, pas de réduire votre temps libre à néant ;-))
 - Privilégiez la qualité et les bonnes pratiques.
 - Vous pouvez réduire le périmètre du projet si vous manquez de temps.
 - Soyez prêt à présenter le sujet, à justifier vos choix et à parler de comment vous auriez fait les parties que vous avez laissées de côté.
