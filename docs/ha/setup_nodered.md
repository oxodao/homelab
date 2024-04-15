# NodeRED

## Connexion Home Assistant

Après avoir setup HACS, dans intégrations, activer l'intégration NodeRED.

Dans la page de l'utilisateur, activer le mode avancé puis dans l'onglet sécurité générer un token longue durée.

Dans NodeRED aller dans le menu hamburger puis "Gérer la palette" et installer la node `node-red-contrib-home-assistant-websocket`.

Dropper n'importe où dans l'interface une node Home assistant puis dans sa configuration ajouter un serveur.

- Base URL: `https://domo.home.lan`
- Access Token: Celui généré dans HA
- Accept Unauthorized SSL Certificates: `true`
- Enable global context store: `true`

Sauvegarder.


NodeRED est maintenant connecté à HomeAssistant.

## Connexion MQTT

Ajouter une node MQTT puis la configurer, ajouter un serveur et remplir:
- Serveur: `mosquitto`
- Port: `1883`
- Client ID: `nodered`
- Onglet sécurité: credentials de mosquitto

Sauvegarder.

NodeRED est maintenant connecté à MQTT.
