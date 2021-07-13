# Test technique Django / Backend

L'objectif de l'exercice ci-dessous est de modéliser une base de données à partir de spécifications métiers et de 
concevoir une interface simple de gestion de trajets de bus, en utilisant l'admin de Django.

Pour réaliser le test, pensez à fork ce repository. Idéalement, ouvrir une PR à la fin.

## Critères d'évaluation

- Documentation et clarté du code
- Modélisation de la base de donnée
- Maîtrise du framework Django

## Stack Technique

| Nom    | Version |
| ------ | ------- |
| Python | 3.7     |
| Django | 3.2.5   |

 - Le projet à été réalisé en utilisant Python 3.7. Vous êtes libre d'utiliser une autre version mais c'est celle que 
 nous vous conseillons.
 - La base de donnée est au choix. Le projet est configuré pour utiliser `sqlite` par défaut.

### Démarrer le projet

*Depuis votre virtualenv Python 3.7*:

```
make install
make migrate
make run
```

Des scripts sont à votre disposition pour vous permettre de rapidement créer de la donnée et de prendre le projet en 
main:

 - `create_data`
 - `create_buses`
 - `create_drivers`
 - `create_places`
 - `create_users`

Par exemple:

```
python manage.py create_drivers -n 5
```

## Sujet

### Description

Un trajet en bus (`BusShift`) est composé des éléments suivants:

- Un bus: (`Bus`).
- Un chauffeur: (`Driver`).
- Entre 2 et une infinité d'arrêts (`BusStop`).
- L'heure de départ est déterminée par l'heure de passage au premier arrêt.
- L'heure d'arrivée est déterminée par l'heure de passage au dernier arrêt.
- Il est possible de déduire le temps total nécessaire pour effectuer le trajet depuis l'heure de départ et l'heure d'arrivée.

La structure de projet qui vous est proposée comprends déjà les models suivants:
 - `Bus`
 - `Driver`
 - `Place`
 - `User` (étends le model [AbstractUser de Django](https://docs.djangoproject.com/en/3.2/topics/auth/customizing/#substituting-a-custom-user-model))

### Objectifs

#### Implémenter les modèles `BusShift` and `BusStop` à la base de code existante

L'implémentation de ces deux modèles est libre et laissée à votre appréciation. Les contraintes métiers suivantes 
doivent être respectées:

 - Un même bus ne peut être assigné, en même temps, à plusieurs trajets dont les heures de début et fin se 
 chevaucheraient.
 - Il en va de même pour les chauffeurs.

#### Fournir une interface de gestion des trajets de bus

Il doit être possible, pour un utilisateur, de créer ou de modifier des trajets de bus (`BusShift`) en utilisant l'admin
de django.

**Note**: Il existe plusieurs solutions pour concevoir cette fonctionnalité. Certaines seront peut être plus couteuse
en temps que d'autres ... 

### Conseils

 - Ne passez pas plus de 4 heures sur un sujet (le but est d'évaluer vos compétences, pas de réduire votre temps libre à néant ;-))
 - Privilégier la qualité et les bonnes pratiques.
 - Vous pouvez réduire le périmètre du projet si vous manquez de temps. Une ébauche de réponse est déjà une bonne chose.
 - Soyez prêt à présenter le sujet, à justifier vos choix et à parler de comment vous auriez fait les parties que vous avez laisser de côté.
