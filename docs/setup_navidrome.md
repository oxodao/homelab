# Setup Navidrome

**VM PUBLIC**

> A faire même en cas de ansible
>
> => Post-setup Navidrome

## Ajout du montage SMB

Même setup que Jellyfin, et on utilise le même point de montage.

## Setup de Navidrome

En tant qu'utilisateur non-root, on créé les dossiers utiles:
```sh
$ mkdir -p /home/oxodao/navidrome/data
```

On ajoute ensuite le `docker-compose.yaml` dans `/home/oxodao/navidrome`:
```yaml
services:
  app:
    image: 'deluan/navidrome:latest'
    restart: 'unless-stopped'
    user: 1000:1000
    environment:
      ND_SCANSCHEDULE: '1h'
      ND_LOGLEVEL: 'info'
      ND_SESSIONTIMEOUT: '24h'
      ND_CACHEFOLDER: '/cache'
      ND_MUSICFOLDER: '/shares/Music'
      ND_AUTHWINDOWLENGTH: '60s'
      ND_DEFAULTLANGUAGE: 'fr'
      ND_IMAGECACHESIZE: '1024MB'
      ND_SPOTIFY_ID: 'SPOTIFY APP ID'
      ND_SPOTIFY_SECRET: 'SPOTIFY APP SECRET'
      ND_TRANSCODINGCACHESIZE: '1024MB'
      ND_BASEURL: "" # @TODO: ? c'est dans leur doc comme ça, a voir si ça a un impact
    volumes:
      - './data:/data'
      - './cache:/cache'
      - '/mnt/shares:/shares:ro'
    ports:
      - '127.0.0.1:4533:4533'
```

Puis on le lance:
```sh
$ cd /home/oxodao/navidrome
$ docker compose up -d
```

Ensuite on setup le nginx, dans `/etc/nginx/sites-available/navidrome.conf`:
```
server {
    listen      80;
    server_name m.public.lan;
    return 307 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name m.public.lan;

    include snippets/ssl.conf;

    location / {
        proxy_pass http://localhost:4533;
        include snippets/reverse_proxy.conf;
    }
}
```

On fait le petit symlink qui va bien et on relance nginx:
```sh
$ sudo ln -s /etc/nginx/sites-available/navidrome.conf /etc/nginx/sites-enabled/navidrome.conf
$ sudo systemctl restart nginx
```

On test que tout marche bien en allant sur [https://m.public.lan](https://m.public.lan).

Attention aux DNS, si c'est pas encore configuré dans la freebox on n'y aura pas accès, on peut temporairement mettre ça dans `/etc/hosts` sur son PC:
```
192.168.14.59 m.public.lan
```

## Post-setup Navidrome

Le post-setup de Jellyfin se fait dans le navigateur.

Créer le compte utilisateur.

Le setup de Navidrome est terminé.

[Page précédente](setup_xoa.md) / [Page suivante](setup_paperless.md)