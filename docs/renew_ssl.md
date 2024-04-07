# Renouveller un certificat SSL

Le guide pour générer les certificats génère un CA d'une durée de vie de 5 ans. Passé cette date il faudra re-créer un CA entièrement et trust son nouveau certificat sur tous les appareils qui l'utilisent.

Pour les certificats SSL simples, leurs durée de vie est de un an. Cela signifie qu'une fois par an il faut générer un nouveau certificat pour la VM public et la VM locale, les ajouter dans le `inventory.yaml` de ansible et relancer l'exécution complète pour qu'il mette à jour les certificats sur les VMs et redémarre nginx.

Alternativement, on peut simplement scp les certificats dans `/opt/ssl/cert.key` et `/opt/ssl/cert.crt` de chaque VM et redémarrer nginx manuellement.

Mettre à jour les certificats simple ne demande pas de faire le tour de chaque appareils se connectant au homelab puisqu'ils sont signé par le même CA.


**Note**: Il peut être intéressant de se mettre un rappel régulier sur son Google Agenda pour être notifié avant que le certificat expire pour prévoir et éviter l'interruption de service. Aucun processus d'alerting n'est mis en place.

[Page précédente](add_user_vpn.md) / [Page suivante](disaster_recovery.md)