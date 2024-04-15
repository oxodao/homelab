# Setup JDownloader

**VM LOCALE**

> A faire même en cas de ansible
>
> => Post-setup JDownloader

## Ajout du montage SMB

Même setup que Jellyfin, et on utilise le même point de montage`.

## Setup de JDownloader

En tant qu'utilisateur non-root, on créé les dossiers utiles:
```sh
$ mkdir -p /home/oxodao/jdownloader/config
```

On ajoute ensuite le `docker-compose.yaml` dans `/home/oxodao/jdownloader`:
```yaml
services:
  app:
    image: 'antlafarge/jdownloader:latest'
    restart: 'unless-stopped'
    user: 1000:1000
    volumes:
        - './config:/jdownloader/cfg'
        - '/mnt/shares/downloads:/jdownloader/downloads'
    environment:
        JD_EMAIL: 'MYJD EMAIL'
        JD_PASSWORD: 'MYJD PASSWORD'
        JD_DEVICENAME: 'homelab'
```

Puis on le lance:
```sh
$ cd /home/oxodao/jdownloader
$ docker compose up -d
```

## Post-setup JDownloader

Aller sur [MyJdownloader](https://my.jdownloader.org) et vérifier que la machine apparait bien.

En profiter pour ajouter les comptes sur les différents hosts.

[Page précédente](setup_immich.md) / [Page suivante](setup_ha.md)