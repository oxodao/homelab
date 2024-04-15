# Setup Immich

**VM LOCALE**

> A faire même en cas de ansible
>
> => Post-setup Immich

## Ajout du montage SMB

Même setup que Jellyfin, et on utilise le point de montage `Images`.

## Setup de Immich

En tant qu'utilisateur non-root, on créé les dossiers utiles:
```sh
$ mkdir -p /home/oxodao/immich/pgdata
```

On ajoute ensuite le `docker-compose.yaml` dans `/home/oxodao/immich`:
```yaml
services:
  immich-server:
    container_name: immich_server
    image: 'ghcr.io/immich-app/immich-server:${IMMICH_VERSION:-release}'
    command: ['start.sh', 'immich']
    volumes:
      - '${UPLOAD_LOCATION}:/usr/src/app/upload'
      - /etc/localtime:/etc/localtime:ro
    env_file:
      - .env
    ports:
      - "127.0.0.1:2283:3001"
    depends_on:
      - redis
      - database
    restart: always

  immich-microservices:
    container_name: immich_microservices
    image: 'ghcr.io/immich-app/immich-server:${IMMICH_VERSION:-release}'
    extends: # uncomment this section for hardware acceleration - see https://immich.app/docs/features/hardware-transcoding
      file: hwaccel.transcoding.yml
      service: vaapi # set to one of [nvenc, quicksync, rkmpp, vaapi, vaapi-wsl] for accelerated transcoding
    command: ['start.sh', 'microservices']
    volumes:
      - '${UPLOAD_LOCATION}:/usr/src/app/upload'
      - /etc/localtime:/etc/localtime:ro
      - /dev/dri:/dev/dri
    env_file:
      - .env
    depends_on:
      - redis
      - database
    restart: always

  immich-machine-learning:
    container_name: immich_machine_learning
    # For hardware acceleration, add one of -[armnn, cuda, openvino] to the image tag.
    # Example tag: '${IMMICH_VERSION:-release}-cuda'
    image: 'ghcr.io/immich-app/immich-machine-learning:${IMMICH_VERSION:-release}'
    # extends: # uncomment this section for hardware acceleration - see https://immich.app/docs/features/ml-hardware-acceleration
    #   file: hwaccel.ml.yml
    #   service: cpu # set to one of [armnn, cuda, openvino, openvino-wsl] for accelerated inference - use the `-wsl` version for WSL2 where applicable
    volumes:
      - model-cache:/cache
    env_file:
      - .env
    restart: always

  redis:
    container_name: immich_redis
    image: registry.hub.docker.com/library/redis:6.2-alpine@sha256:51d6c56749a4243096327e3fb964a48ed92254357108449cb6e23999c37773c5
    restart: always

  database:
    container_name: immich_postgres
    image: registry.hub.docker.com/tensorchord/pgvecto-rs:pg14-v0.2.0@sha256:90724186f0a3517cf6914295b5ab410db9ce23190a2d9d0b9dd6463e3fa298f0
    environment:
      POSTGRES_PASSWORD: '${DB_PASSWORD}'
      POSTGRES_USER: '${DB_USERNAME}'
      POSTGRES_DB: '${DB_DATABASE_NAME}'
    volumes:
      - "./pgdata:/var/lib/postgresql/data"
    restart: always

volumes:
  model-cache:
```

Il faut aussi ajouter le `.env`:
```sh
# You can find documentation for all the supported env variables at https://immich.app/docs/install/environment-variables

# The location where your uploaded files are stored
UPLOAD_LOCATION=/media/images

# The Immich version to use. You can pin this to a specific version like "v1.71.0"
IMMICH_VERSION=v1.99.0

# Connection secret for postgres. You should change it to a random password
DB_PASSWORD=immich

# The values below this line do not need to be changed
###################################################################################
DB_HOSTNAME=immich_postgres
DB_USERNAME=immich
DB_DATABASE_NAME=immich

REDIS_HOSTNAME=immich_redis
```

Puis on le lance:
```sh
$ cd /home/oxodao/immich
$ docker compose up -d
```

Ensuite on setup le nginx, dans `/etc/nginx/sites-available/immich.conf`:
```
server {
    listen      80;
    server_name i.home.lan;
    return 307 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name i.home.lan;

    include snippets/ssl.conf;

    # Useful for uploading videos
    client_max_body_size 4096M;

    location / {
        proxy_pass http://localhost:2283;
        include snippets/reverse_proxy.conf;
    }
}
```

On fait le petit symlink qui va bien et on relance nginx:
```sh
$ sudo ln -s /etc/nginx/sites-available/immich.conf /etc/nginx/sites-enabled/immich.conf
$ sudo systemctl restart nginx
```

On test que tout marche bien en allant sur [https://i.home.lan](https://i.home.lan).

Attention aux DNS, si c'est pas encore configuré dans la freebox on n'y aura pas accès, on peut temporairement mettre ça dans `/etc/hosts` sur son PC:
```
192.168.14.59 i.home.lan
```

## Post-setup Immich

Aller sur l'interafce Web et créer son compte Admin.

Immich est prêt à usage.

[Page précédente](setup_gitea.md) / [Page suivante](setup_jdownloader.md)