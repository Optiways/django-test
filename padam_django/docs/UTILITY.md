# Notice d'utilisation

Cette note contient les éléments nécessaires à la prise en main de l'application

Note : la base de donnée n'a pas été vidée et est déjà peuplée

## Accessibilité

L'application s'appuie sur l'interface admin de django.

L'URL d'admin est : http://127.0.0.1:8000/admin/

Login :
- username : admin
- password : admin

## Utilisation

Un arrêt peut-être saisi dans l'onglet "BusStop" en renseignant :
- un lieu depuis la liste des lieux
- une heure de passage à l'arrêt. Le format recommandé est le suivant : hh:mm

Un trajet peut-être saisi dans l'onglet "BusShift" en renseignant :
- un bus depuis la liste des bus
- un chauffeur depuis la liste des chauffeurs
- un arrêt de départ
- un arrêt de fin


Il est possible d'ajouter des étapes au trajet en sélectionnant des arrêts dans la liste "steps".
Les heures de passages aux étapes doivent être comprises entre l'heure de départ et l'heure de fin du trajet.