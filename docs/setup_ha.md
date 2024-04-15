# Setup de HomeAssistant

**VM LOCALE / DOM0**

> A faire même en cas de ansible
>
> => Installation de zigbee2mqtt, Post-setup HomeAssistant


Cette étape est un peu plus complexe que les autres car:
- Nécessite plusieurs dépendances (Mosquitto, influxdb, nodered)
- Nécessite d'installer zigbee2mqtt sur dom0

Cela est plus compliqué uniquement car j'utilise une VM dans XCP-ng, sinon le setup standard est tout aussi simple.

## Setup de HomeAssistant

En tant qu'utilisateur non-root, on créé les dossiers utiles:
```sh
$ mkdir -p /home/oxodao/homeassistant/{mosquitto/data,mosquitto/logs,config,influxdb,nodered_data,zigbee2mqtt_data}
```

On ajoute ensuite le `docker-compose.yaml` dans `/home/oxodao/homeassistant`:
```yaml
services:
  app:
    image: 'ghcr.io/home-assistant/home-assistant:stable'
    restart: 'unless-stopped'
    volumes:
      - './config:/config'
      - '/etc/localtime:/etc/localtime:ro'
    privileged: true
    network_mode: 'host'

  mosquitto:
    image: 'eclipse-mosquitto:latest'
    restart: 'unless-stopped'
    volumes:
      - './mosquitto.conf:/mosquitto/config/mosquitto.conf'
      - './mosquitto_users:/mosquitto/config/users'
      - './mosquitto/data:/mosquitto/data'
      - './mosquitto/logs:/mosquitto/log'
      - '/var/run/docker.sock:/var/run/docker.sock'
    extra_hosts:
      - 'host.docker.internal:host-gateway'
    ports:
      - '1883:1883'
      - '9001:9001'

  influx:
    image: 'influxdb:alpine'
    restart: 'unless-stopped'
    volumes:
      - './influxdb:/var/lib/influxdb2'
    extra_hosts:
      - 'host.docker.internal:host-gateway'
    ports:
      - '127.0.0.1:8086:8086'

  nodered:
    image: 'nodered/node-red'
    restart: 'unless-stopped'
    environment:
      TZ: 'Europe/Paris'
    extra_hosts:
      - 'domo.home.lan:host-gateway'
    volumes:
      - './nodered_data:/data'
    ports:
      - '127.0.0.1:1880:1880'
```

On ajoute la configuration de mosquitto dans `/home/oxodao/homeassistant/mosquitto.conf`:
```
listener 1883

allow_anonymous false
password_file /mosquitto/config/users

persistence true
persistence_location /mosquitto/data/
log_dest file /mosquitto/log/mosquitto.log
log_dest stdout
```

Puis on créé le fichier de users:
```sh
$
```

**Note**: Si le `/dev/serial/by-id` n'existe pas, se référer à [ce post](https://www.reddit.com/r/debian/comments/1331wlr/devserialbyid_suddenly_missing/) sur Reddit.

Use the nginx file present in the template folder for homeassistant and replace the template for `{{domain}}` to `home.lan` to `/etc/nginx/sites-available/homeassistant.conf`.

On fait le petit symlink qui va bien et on relance nginx:
```sh
$ sudo ln -s /etc/nginx/sites-available/homeassistant.conf /etc/nginx/sites-enabled/homeassistant.conf
$ sudo systemctl restart nginx
```

On test que tout marche bien en allant sur [https://domo.home.lan](https://domo.home.lan) et [https://nr.home.lan](https://nr.home.lan).

Attention aux DNS, si c'est pas encore configuré dans la freebox on n'y aura pas accès, on peut temporairement mettre ça dans `/etc/hosts` sur son PC:
```
192.168.14.59 domo.home.lan
192.168.14.59 nr.home.lan
```

## Installation de zigbee2mqtt

Le passthrough USB est à chier sur XCP-NG, la solution un peu recipe for disaster que j'ai trouvé et qui à l'air de marcher est de setup zigbee2mqtt sur dom0 puisque le dongle est automatiquement attaché sur dom0.

Cependant, z2m nécessite NodeJS 18+ qui n'est pas compatible CentOS 7 (XCP-NG).

On va donc trouver une [unofficial build](https://unofficial-builds.nodejs.org/download/release/v20.12.1/) de NodeJS compatible, la télécharger et l'extraire dans `/opt` et faire un setup vite-fais.

```sh
$ cd /opt
$ wget https://unofficial-builds.nodejs.org/download/release/v20.12.1/node-v20.12.1-linux-x64-glibc-217.tar.gz
$ tar -xvzf node-v20.12.1-linux-x64-glibc-217.tar.gz
$ rm node-v20.12.1-linux-x64-glibc-217.tar.gz
$ mv node-v20.12.1-linux-x64-glibc-217 nodejs
$ ln -s /opt/nodejs/bin/node /usr/bin/node
$ ln -s /opt/nodejs/bin/npm /usr/bin/npm
$ ln -s /opt/nodejs/bin/npx /usr/bin/npx
```

Une fois ceci fait, on va en profiter pour installer `pm2` car pour une raison inconnue, systemd freeze sur le démarrage du service si on l'utilise directement...

```sh
$ npm install -f pm2
$ npx pm2 startup # On l'active au démarrage
```

On va ensuite setup zigbee2mqtt:
```sh
$ git clone --depth 1 https://github.com/Koenkk/zigbee2mqtt.git /opt/zigbee2mqtt
$ cd /opt/zigbee2mqtt
$ npm ci
```

Avant de le lancer, on va setup la config dans `/opt/zigbee2mqtt/data/configuration.yaml`
```yaml
homeassistant: true
permit_join: false
mqtt:
  base_topic: zigbee2mqtt
  server: mqtt://192.168.14.2
  user: iot
  password: MOT DE PASSE MQTT
frontend:
  port: 8080
  host: 0.0.0.0
[...]
```

On peut le lancer.

```sh
$ npx pm2 start index.js
$ npx pm2 save
```

Plus qu'à configurer tous les appareils zigbee dans z2m !

Petite subtilité, dom0 à un firewall de configuré. Plutôt que de toucher à ça, on va juste faire un forwarding via SSH:
```
Host dom0
        Hostname 192.168.14.253
        Port 22
        User root
        LocalForward 8080 localhost:8080
```

## Post-setup HomeAssistant

Celui la est un peu plus compliqué au vu de tous les services.

Tout d'abord, HA va se plaindre que notre requête vient d'un reverse-proxy mais qu'il n'est pas configuré pour.

Dans `configuration.yaml` il faut ajouter:
```
http:
  server_host: 127.0.0.1
  use_x_forwarded_for: true
  trusted_proxies: 127.0.0.1
```

On relance le docker et on va sur [l'interface web](https://domo.home.lan). On créé son compte utilisateur.

On va ensuite ajouter l'intégration InfluxDB.

RDV sur [l'interface web](https://influx.home.lan), on créé son compte avec comme organisation "homelab" et comme bucket "homeassistant".

On pense à garder dans le gestionnaire de mot de passes le token généré. Puis dans le dossier `homeassistant`:
```sh
$ docker compose exec influx influx auth create --token API_TOKEN --org homelab  --read-buckets --write-buckets
```

On ajoute dans la config homeassistant:
```yaml
influxdb:
  api_version: 2
  ssl: false
  host: 127.0.0.1
  port: 8086
  token: <TOKEN INFLUX>
  organization: homelab
  bucket: homeassistant
```

Pour les thermomètre avec MijiaBridge, la clé de chiffrement est à ajouter lors de l'ajout dans HA et non plus dans la config.

Se référer au guide HA séparé pour toutes les info de setup.

[Page précédente](setup_jdownloader.md) / [Page suivante](setup_grafana.md)