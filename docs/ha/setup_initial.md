# Setup initial

## HACS

HACS est un store custom pour HomeAssistant permettant d'ajouter pas mal d'intégrations supplémentaires.

Pour l'installer, se rendre dans le dossier du docker compose et lancer ces commandes:
```sh
$ docker compose exec app bash
$ wget -O - https://get.hacs.xyz | bash -
$ exit
$ docker compose restart app
```

Se diriger dans l'interface web de HA, Paramètres, Appareils et services, Ajouter une intégration, rechercher HACS et l'installer. Redémarrer HA.

Voici la liste des intégrations à installer depuis HACS:
- Mushroom
- mini-graph-card
- layout-card
- Battery State Card / Entity Row
- Banner Card
- Weather Card
- Node-RED Companion
- RGB Light Card
- Zigbee2mqtt Networkmap Card
- Light Entity Card
- Google Dark Theme
