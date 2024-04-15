# Setup Paperless-ngx

**VM LOCALE**

> A faire même en cas de ansible
>
> => Post-setup Paperless-ngx

## Ajout du montage SMB

Même setup que Jellyfin, et on utilise le point de montage `documents`.

Pré-créez les dossiers suivants:
```sh
$ mkdir /mnt/documents/{medias,ingress}
```

## Setup de Paperless-ngx

En tant qu'utilisateur non-root, on créé les dossiers utiles:
```sh
$ mkdir -p /home/oxodao/paperless/{data,export}
```

On ajoute ensuite le `docker-compose.yaml` dans `/home/oxodao/paperless`:
```yaml
services:
  broker:
    image: 'redis:7.0'
    restart: 'unless-stopped'

  app:
    image: 'ghcr.io/paperless-ngx/paperless-ngx:latest'
    restart: 'unless-stopped'
    user: 1000:1000
    environment:
      USERMAP_UID: 1000
      USERMAP_GID: 1000
      PAPERLESS_REDIS: 'redis://broker:6379'
      PAPERLESS_URL: 'https://paper.home.lan'
      PAPERLESS_TIME_ZONE: 'Europe/Paris'
      PAPERLESS_OCR_LANGUAGE: 'fra'
      PAPERLESS_CONSUMER_POLLING: 30
    volumes:
      - './data:/usr/src/paperless/data'
      - './export:/usr/src/paperless/export'
      - '/mnt/documents/medias:/usr/src/paperless/media'
      - '/mnt/documents/ingress:/usr/src/paperless/consume'
    depends_on:
      - broker
    ports:
      - '127.0.0.1:8000:8000'
```

Puis on le lance:
```sh
$ cd /home/oxodao/paperless
$ docker compose up -d
```

Ensuite on setup le nginx, dans `/etc/nginx/sites-available/paperless.conf`:
```
server {
    listen      80;
    server_name paper.home.lan;
    return 307 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name paper.home.lan;

    include snippets/ssl.conf;

    # Lets you upload large docs
    client_max_body_size 200M;

    location / {
        proxy_pass http://localhost:8000;
        include snippets/reverse_proxy.conf;
    }
}
```

On fait le petit symlink qui va bien et on relance nginx:
```sh
$ sudo ln -s /etc/nginx/sites-available/paperless.conf /etc/nginx/sites-enabled/paperless.conf
$ sudo systemctl restart nginx
```

On test que tout marche bien en allant sur [https://paper.home.lan](https://paper.home.lan).

Attention aux DNS, si c'est pas encore configuré dans la freebox on n'y aura pas accès, on peut temporairement mettre ça dans `/etc/hosts` sur son PC:
```
192.168.14.59 paper.home.lan
```

## Post-setup Paperless-ngx

On créé le compte super-user:
```sh
$ docker compose run --rm app createsuperuser
```

Le setup de Paperless-ngx est terminé.

**Note**: Pour ajouter des documents, simplement les coller dans le montage smb: `\\NAS\documents\ingress`.
Sous 30s ils seront ingérés par Paperless puis supprimés de ce dossier.

[Page précédente](setup_navidrome.md) / [Page suivante](setup_gitea.md)