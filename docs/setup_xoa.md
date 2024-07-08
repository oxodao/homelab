# Setup XenOrchestra

**VM LOCALE**

XOA est en général déployé sur une VM à part. Cela prends des perfs pour rien donc je préfère le lancer dans un container sur une des VM que j'utilise déjà.

> A faire même en cas de ansible
>
> => Post-setup XOA

## Setup de XOA

En tant qu'utilisateur non-root, on créé les dossiers utiles:
```sh
$ mkdir -p /home/oxodao/jellyfin/{xoa_data,redis_data}
```

On ajoute ensuite le `docker-compose.yaml` dans `/home/oxodao/xoa`:
```yaml
services:
  app:
    image: linuxserver/jellyfin:latest
    restart: 'unless-stopped'
    environment:
      PUID: 1000
      PGID: 1000
      TZ: 'Europe/Paris'
      JELLYFIN_PublishedServerUrl: 'https://play.public.lan'
    volumes:
      - './config:/config'
      - './cache:/cache'
      - './transcodes:/transcodes'
      - './metadata:/metadata'
      - '/mnt/shares:/shares'
    devices:
      - '/dev/dri/renderD128:/dev/dri/renderD128'
      - '/dev/dri/card0:/dev/dri/card0'
    ports:
      - '127.0.0.1:8096:8096'
      - '7359:7359' # Autodiscovery
      - '1900:1900' # Autodiscovery
```

Puis on le lance:
```sh
$ cd /home/oxodao/xoa
$ docker compose up -d
```

Ensuite on setup le nginx, dans `/etc/nginx/sites-available/xoa.conf`:
```
server {
    listen      80;
    server_name xoa.home.lan;

}

server {
    listen 443 ssl http2;
    server_name xoa.home.lan;

    include snippets/ssl.conf;

    location / {
        proxy_pass http://localhost:8037;
        include snippets/reverse_proxy.conf;
    }
}
```

On fait le petit symlink qui va bien et on relance nginx:
```sh
$ sudo ln -s /etc/nginx/sites-available/xoa.conf /etc/nginx/sites-enabled/xoa.conf
$ sudo systemctl restart nginx
```

On test que tout marche bien en allant sur [https://xoa.home.lan](https://xoa.home.lan).

Attention aux DNS, si c'est pas encore configuré dans la freebox on n'y aura pas accès, on peut temporairement mettre ça dans `/etc/hosts` sur son PC:
```
192.168.14.59 xoa.home.lan
```

## Post-setup XOA

Il faut setup le compte admin. Pour cela, se connecter avec le compte par défaut (`admin@admin.net:admin`).

Ensuite direction Settings > Users pour changer l'adresse mail ainsi que le mot de passe. On peut en profiter aussi pour activer dans son profile le MFA / OTP.

Ensuite il faut ajouter son serveur, dans Settings > Servers il faut se connecter sur le host XCP-NG:

- Nom: `rubeus`
- Host: `192.168.14.253`
- Username: `root`
- Password: `Root password`

Attention, après avoir cliqué sur connect il faut bien valider l'utilisation du certificat SSL self-signed.

[Page précédente](setup_reverseproxy.md) / [Page suivante](setup_simple_notifier.md)