# Setup Firefly III

**VM LOCALE**

> A faire même en cas de ansible
>
> => Post-setup Firefly

## Ajout du montage SMB

Même setup que Jellyfin, et on utilise le point de montage `documents`.

## Setup de Nextcloud

En tant qu'utilisateur non-root, on créé les dossiers utiles:
```sh
$ mkdir -p /home/oxodao/firefly/pg_data
```

On ajoute ensuite le `docker-compose.yaml` dans `/home/oxodao/firefly`:
```yaml
services:
  app:
    image: 'fireflyiii/core:latest'
    restart: 'unless-stopped'
    volumes:
      - "/mnt/documents/firefly:/var/www/html/storage/upload"
    environment:
      # More info in their .env
      # https://raw.githubusercontent.com/firefly-iii/firefly-iii/main/.env.example
      SITE_OWNER: 'EMAIL DE L OWNER'
      APP_KEY: 'APPKEY RANDOM DE 32 CHARS'
      STATIC_CRON_TOKEN: 'CRON TOKEN RANDOM DE 32 CHARS'
      APP_ENV: 'production'
      MAIL_MAILER: 'smtp'
      MAIL_HOST: 'smtp.mailgun.org'
      MAIL_PORT: '587'
      MAIL_FROM: 'EMAIL FROM'
      MAIL_USERNAME: 'SMTP USERNAME'
      MAIL_PASSWORD: 'SMTP PASSWORD'
      MAIL_ENCRYPTION: 'tls'
      MAP_DEFAULT_LAT: 'LONGITUDE DE OU ON EST'
      MAP_DEFAULT_LONG: 'LATITUDE DE OU ON EST'
      APP_URL: 'https://compta.home.lan'
      # Default stuff
      APP_DEBUG: 'false'
      DEFAULT_LANGUAGE: 'fr_FR'
      DEFAULT_LOCALE: 'equal'
      TZ: 'Europe/Paris'
      TRUSTED_PROXIES: '**'
      LOG_CHANNEL: 'stack'
      APP_LOG_LEVEL: 'notice'
      AUDIT_LOG_LEVEL: 'emergency'
      DB_CONNECTION: 'pgsql'
      DB_HOST: 'db'
      DB_USERNAME: 'firefly'
      DB_PASSWORD: 'firefly'
      DB_DATABASE: 'firefly'
      PG_SCHEMA: 'public'
      CACHE_DRIVER: 'file' # Maybe switch to redis later
      SESSION_DRIVER: 'file'
      COOKIE_PATH: '"/"'
      COOKIE_SECURE: 'false'
      COOKIE_SAMESITE: 'lax'
      SEND_ERROR_MESSAGE: 'true'
      SEND_REPORT_JOURNALS: 'true'
      ENABLE_EXTERNAL_MAP: 'false'
      ENABLE_EXCHANGE_RATES: 'true'
      MAP_DEFAULT_ZOOM: '6'
      AUTHENTICATION_GUARD: 'web' # Useful for oauth & such
      AUTHENTICATION_GUARD_HEADER: 'REMOTE_USER'
      DISABLE_FRAME_HEADER: 'false'
      DISABLE_CSP_HEADER: 'false'
      ALLOW_WEBHOOKS: 'false'
      DKR_BUILD_LOCALE: 'false'
      DKR_CHECK_SQLITE: 'true'
      DKR_RUN_MIGRATION: 'true'
      DKR_RUN_UPGRADE: 'true'
      DKR_RUN_VERIFY: 'true'
      DKR_RUN_REPORT: 'true'
      DKR_RUN_PASSPORT_INSTALL: 'true'
      APP_NAME: 'FireflyIII'
      BROADCAST_DRIVER: 'log'
      QUEUE_DRIVER: 'sync'
      CACHE_PREFIX: 'firefly'
      FIREFLY_III_LAYOUT: 'v1'
    depends_on:
      db:
        condition: 'service_healthy'
    ports:
      - '127.0.0.1:7385:8080'

  db:
    image: 'postgres'
    restart: 'unless-stopped'
    volumes:
      - './pg_data:/var/lib/postgresql/data'
    environment:
      POSTGRES_DB: 'firefly'
      POSTGRES_USER: 'firefly'
      POSTGRES_PASSWORD: 'firefly'
      PGDATA: '/var/lib/postgresql/data/pgdata'
    healthcheck:
      test: ['CMD-SHELL', 'pg_isready']
      interval: '10s'
      timeout: '5s'
      retries: 5

  cron:
    image: 'alpine'
    restart: 'unless-stopped'
    command: 'sh -c "echo \"0 3 * * * wget -qO- http://app:8080/api/v1/cron/<STATIC TOKEN DU ENV>\" | crontab - && crond -f -L /dev/stdout"'
    depends_on:
      db:
        condition: 'service_healthy'
```

Puis on le lance:
```sh
$ cd /home/oxodao/firefly
$ docker compose up -d
```

Ensuite on setup le nginx, dans `/etc/nginx/sites-available/firefly.conf`:
```
server {
    listen      80;
    server_name compta.public.lan;
    return 307 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name compta.public.lan;

    include snippets/ssl.conf;
    client_max_body_size 200M;

    location / {
        proxy_pass http://localhost:7385;
        include snippets/reverse_proxy.conf;
    }
}
```

On fait le petit symlink qui va bien et on relance nginx:
```sh
$ sudo ln -s /etc/nginx/sites-available/firefly.conf /etc/nginx/sites-enabled/firefly.conf
$ sudo systemctl restart nginx
```

On test que tout marche bien en allant sur [https://firefly.public.lan](https://compta.public.lan).

Attention aux DNS, si c'est pas encore configuré dans la freebox on n'y aura pas accès, on peut temporairement mettre ça dans `/etc/hosts` sur son PC:
```
192.168.14.59 compta.public.lan
```

## Post-setup Firefly

@TODO

[Page précédente](setup_nextcloud.md) / [Page suivante](setup_vpn.md)