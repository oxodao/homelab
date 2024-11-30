# Setup Manyfold

**VM LOCALE**

> A faire même en cas de ansible
>
> => Post-setup Manyfold

## Setup de Manyfold

En tant qu'utilisateur non-root, on créé les dossiers utiles:
```sh
$ mkdir -p /home/oxodao/manyfold/{data,db_data}
```

On ajoute ensuite le `compose.yaml` dans `/home/oxodao/manyfold`:
```yaml
services:
  app:
    image: 'ghcr.io/manyfold3d/manyfold:latest'
    restart: 'unless-stopped'
    environment:
      DATABASE_ADAPTER: 'postgresql'
      DATABASE_HOST: 'database'
      DATABASE_PORT: 5432
      DATABASE_NAME: 'manyfold'
      DATABASE_USER: 'manyfold'
      DATABASE_PASSWORD: 'manyfold'
      SECRET_KEY_BASE: 'SOME LONG RANDOM STRING'
      REDIS_URL: 'redis://valkey:6379/1'
      PUID: 1000
      PGID: 1000
    depends_on:
      database:
        condition: 'service_healthy'
      valkey:
        condition: 'service_healthy'
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - 'ALL'
    cap_add:
      - 'CHOWN'
      - 'DAC_OVERRIDE'
      - 'SETUID'
      - 'SETGID'
    volumes:
      - './data:/libraries'
    ports:
      - '127.0.0.1:3214:3214'

  database:
    image: 'postgres:16-alpine'
    restart: 'unless-stopped'
    environment:
      POSTGRES_DB: 'manyfold'
      POSTGRES_PASSWORD: 'manyfold'
      POSTGRES_USER: 'manyfold'
      PGDATA: '/var/lib/postgresql/data/pgdata'
    volumes:
      - './db_data:/var/lib/postgresql/data'
    healthcheck:
      test: ["CMD", "pg_isready", "-d", "manyfold", "-U", "manyfold"]
      timeout: '5s'
      start_period: '60s'
      retries: 5

  valkey:
    image: 'valkey/valkey:8.0.1-bookworm'
    restart: 'unless-stopped'
    healthcheck:
      test: [ "CMD", "redis-cli", "--raw", "incr", "ping" ]
      timeout: '5s'
      start_period: '60s'
      retries: 5
```

Puis on le lance:
```sh
$ cd /home/oxodao/manyfold
$ docker compose up -d
```

Ensuite on setup le nginx, dans `/etc/nginx/sites-available/manyfold.conf`:
```
server {
    listen      80;
    server_name 3d.home.lan;
    return 307 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name 3d.home.lan;

    include snippets/ssl.conf;

    # Useful for uploading videos
    client_max_body_size 4096M;

    location / {
        proxy_pass http://localhost:3214;
        include snippets/reverse_proxy.conf;
    }
}
```

On fait le petit symlink qui va bien et on relance nginx:
```sh
$ sudo ln -s /etc/nginx/sites-available/manyfold.conf /etc/nginx/sites-enabled/manyfold.conf
$ sudo systemctl restart nginx
```

On test que tout marche bien en allant sur [https://3d.home.lan](https://3d.home.lan).

Attention aux DNS, si c'est pas encore configuré dans la freebox on n'y aura pas accès, on peut temporairement mettre ça dans `/etc/hosts` sur son PC:
```
192.168.14.59 3d.home.lan
```

## Post-setup Manyfold

Aller sur l'interafce Web et créer son compte Admin.

Manyfold est prêt à usage.

[Page précédente](setup_immich.md) / [Page suivante](setup_jdownloader.md)