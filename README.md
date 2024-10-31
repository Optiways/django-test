
### Tester l'interface de gestion des trajets de bus

Une fois les migrations faites, il suffit de créer un super utilisateur pour pouvoir se connecter à l'admin Django:

```
python manage.py createsuperuser
```

Puis, il faut créer les données de base :

```
python manage.py create_data
```

- Et enfin, il faut lancer le serveur. 
- Si vous voulez, vous pouvez créer des bus stop directement dans l'interface de création des bus shifts.

**Note** : J'ai laissé de côté les tests unitaires.