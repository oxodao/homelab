# Setup Nextcloud

**VM PUBLIC**

> A faire même en cas de ansible
>
> => Post-setup Nextcloud

## Ajout du montage SMB

Même setup que Jellyfin, et on utilise le point de montage `cloud`.

Attention il faut cependant forcer les permissions user/group pour `33` (www-data) et les permissions d'accès en `0770` sur le montage.

## Setup de Nextcloud

En tant qu'utilisateur non-root, on créé les dossiers utiles:
```sh
$ mkdir -p /home/oxodao/nextcloud/{pg_data,nc_data}
```

On ajoute ensuite le `docker-compose.yaml` dans `/home/oxodao/nextcloud`:
```yaml
services:
  db:
    image: 'postgres'
    restart: 'unless-stopped'
    volumes:
      - './pg_data:/var/lib/postgresql/data'
    environment:
      POSTGRES_DB: 'nextcloud'
      POSTGRES_USER: 'nextcloud'
      POSTGRES_PASSWORD: 'nextcloud'
      PGDATA: '/var/lib/postgresql/data/pgdata'
    healthcheck:
      test: ['CMD-SHELL', 'pg_isready']
      interval: '10s'
      timeout: '5s'
      retries: 5

  redis:
    image: 'redis:7'
    healthcheck:
      test: [ 'CMD', 'redis-cli', '--raw', 'incr', 'ping' ]
      interval: '10s'
      timeout: '5s'
      retries: 5

  app:
    image: 'nextcloud'
    restart: 'unless-stopped'
    ports:
      - '127.0.0.1:8012:80'
    volumes:
      - './nc_data:/var/www/html'
      - '/mnt/cloud:/data'
    depends_on:
      db:
        condition: 'service_healthy'
      redis:
        condition: 'service_healthy'
    environment:
      POSTGRES_HOST: 'db'
      POSTGRES_DB: 'nextcloud'
      POSTGRES_USER: 'nextcloud'
      POSTGRES_PASSWORD: 'nextcloud'
      NEXTCLOUD_DATA_DIR: '/data'
      REDIS_HOST: 'redis'
      PHP_UPLOAD_LIMIT: '8G'
      # Remplir les champs suivant
      SMTP_HOST: ''
      SMTP_SECURE: 'tls'
      SMTP_PORT: ''
      SMTP_NAME: ''
      SMTP_PASSWORD: ''
      MAIL_FROM_ADDRESS: ''
      MAIL_DOMAIN: ''
```

Puis on le lance:
```sh
$ cd /home/oxodao/nextcloud
$ docker compose up -d
```

Ensuite on setup le nginx, dans `/etc/nginx/sites-available/nextcloud.conf`:
```
server {
    listen      80;
    server_name cloud.public.lan;
    return 307 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name cloud.public.lan;

    include snippets/ssl.conf;

    location / {
        proxy_pass http://localhost:8012;
        include snippets/reverse_proxy.conf;
    }
}
```

On fait le petit symlink qui va bien et on relance nginx:
```sh
$ sudo ln -s /etc/nginx/sites-available/nextcloud.conf /etc/nginx/sites-enabled/nextcloud.conf
$ sudo systemctl restart nginx
```

On test que tout marche bien en allant sur [https://cloud.public.lan](https://cloud.public.lan).

Attention aux DNS, si c'est pas encore configuré dans la freebox on n'y aura pas accès, on peut temporairement mettre ça dans `/etc/hosts` sur son PC:
```
192.168.14.59 cloud.public.lan
```

## Post-setup Nextcloud

Le post-setup de Nextcloud se fait dans le navigateur.

Créer le compte utilisateur.

@TODO: Normalement on peut setup ça avec des env-var au premier démarrage, à vérifier

Il faut autoriser le reverse-proxy, pour cela il faut éditer le fichier `nc_data/config/config.php` pour ajouter la ligne suivante:
```php
  'trusted_proxies' => ['172.31.0.1'],
```
**PAS SUR QUE ÇA RESTE LA MÊME, A VOIR CMT FAIRE !!**

Il faut aussi dire à Nextcloud qu'il peut utiliser le https:
```php
  'overwrite.cli.url' => 'https://cloud.public.lan',
```

Vérifier et corriger les problèmes dans [la page des issues](https://cloud.public.lan/settings/admin/overview).

[Page précédente](setup_xoa.md) / [Page suivante](setup_paperless.md)