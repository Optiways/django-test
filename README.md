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

#############################################################################################################################################################


Ce projet est une application Django permettant de gérer des bus, des chauffeurs, des trajets (BusShift) et des arrêts (BusStop). L'application fournit une interface d'administration pour créer et gérer ces entités, en assurant la cohérence et la validation des données.

Ce rendu est réalisé dans le cadre du test technique pour mon entretien avec Padam Mobility.
Installation
Prérequis

    Python 3.6 ou supérieur
    Django 3.2.5
    pip (gestionnaire de paquets Python)
    Un environnement virtuel est recommandé pour isoler les dépendances du projet.

Étapes d'installation

    Cloner le dépôt :

    bash

git clone <URL-de-votre-référentiel>
cd <nom_du_dossier>

Créer et activer un environnement virtuel :

# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
# Sur Windows
venv\Scripts\activate
# Sur macOS/Linux
source venv/bin/activate

Installer les dépendances :

Assurez-vous que le fichier requirements.txt est présent à la racine du projet.

pip install -r requirements.txt

Appliquer les migrations :

python manage.py migrate

Créer un superutilisateur :

python manage.py createsuperuser

Suivez les instructions pour définir le nom d'utilisateur et le mot de passe.

Lancer le serveur de développement :

    python manage.py runserver

Créer des données via les scripts:

Des scripts sont à votre disposition pour vous permettre de rapidement créer de la donnée et de prendre le projet en main:

    create_data
    create_buses
    create_drivers
    create_places
    create_users

Par exemple:

python manage.py create_drivers -n 5



    Accéder à l'application :
        Application principale : http://127.0.0.1:8000/
        Interface d'administration : http://127.0.0.1:8000/admin/

Utilisation de l'application

    Connexion à l'interface d'administration :

    Accédez à http://127.0.0.1:8000/admin/ et connectez-vous avec le superutilisateur que vous avez créé précédemment.



    Création de Trajets (BusShift) :
        Lors de la création d'un trajet, sélectionnez le bus et le chauffeur affectés.

    Ajout d'Arrêts (BusStop) :
        Dans le formulaire de création/modification d'un trajet, ajoutez au moins deux arrêts.
        Spécifiez l'ordre, le lieu et l'heure de passage pour chaque arrêt.
        Assurez-vous que les heures de passage sont cohérentes avec l'ordre des arrêts.

Problèmes Rencontrés et Solutions Proposées

Bien que j'aie rencontré certains problèmes, je préfère les laisser tels quels pour le moment et je serais ravi de discuter des solutions possibles avec vous lors de notre entretien.

    Gestion des Arrêts Uniques :
        Problème : Lorsqu'il n'y a qu'un seul BusStop dans le formulaire d'ajout d'un BusShift, une erreur est levée, mais elle n'est pas correctement gérée dans le formulaire, contrairement aux autres cas.
        Explication : Le système exige qu'un trajet ait au moins deux arrêts pour être valide. Cependant, le message d'erreur correspondant n'est pas affiché correctement à l'utilisateur.

    Mise à Jour Automatique des Horaires de Départ et d'Arrivée :
        Problème : Les horaires de départ et d'arrivée du BusShift ne sont pas automatiquement mis à jour en fonction des BusStop associés. J'ai écrit une fonction qui tente de le faire, mais je n'ai pas réussi à la faire fonctionner correctement.
        Explication : Le problème est peut-être dû au fait que les heures de départ et d'arrivée sont sauvegardées avant que les BusStop ne soient créés, ce qui empêche la mise à jour automatique basée sur les horaires des arrêts.

Je serais heureux de discuter de ces problèmes et des solutions potentielles lors de notre entretien. Votre retour me sera très précieux pour améliorer cette application.
Remarques

    Cohérence des Données : Assurez-vous que les BusStop ont des heures de passage cohérentes avec leur ordre. L'heure de passage d'un arrêt doit être postérieure à celle de l'arrêt précédent.

    Nombre Minimum d'Arrêts : Un trajet doit comporter au moins deux arrêts. Cette contrainte est vérifiée lors de la sauvegarde, mais le message d'erreur pourrait être amélioré pour une meilleure expérience utilisateur.

    Extensions Possibles : Pour améliorer le projet, il serait envisageable de rendre les champs departure_time et arrival_time optionnels lors de la création initiale, puis obligatoires après la sauvegarde des BusStop, ou d'ajuster l'ordre des opérations de sauvegarde pour permettre la mise à jour automatique.

Contact

Pour toute question ou suggestion, n'hésitez pas à me contacter à l'adresse suivante : frederictamiazzo@example.com




