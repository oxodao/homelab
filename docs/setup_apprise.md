# Setup Firefly III

**VM LOCALE**

> A faire même en cas de ansible
>
> => Post-setup Apprise

## Setup de Apprise

En tant qu'utilisateur non-root, on créé les dossiers utiles:
```sh
$ mkdir -p /home/oxodao/apprise/config
$ sudo chmod 777 /home/oxodao/apprise
```

On ajoute ensuite le `docker-compose.yaml` dans `/home/oxodao/apprise`:
```yaml
services:
  app:
    image: 'caronc/apprise'
    restart: 'unless-stopped'
    volumes:
      - './config:/config'
    ports:
      - '127.0.0.1:3231:8000'
```

Puis on le lance:
```sh
$ cd /home/oxodao/apprise
$ docker compose up -d
```

Ensuite on setup le nginx, dans `/etc/nginx/sites-available/apprise.conf`:
```
server {
    listen      80;
    server_name notif.public.lan;
    return 307 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name notif.public.lan;

    include snippets/ssl.conf;

    location / {
        proxy_pass http://localhost:3231;

        # Apprise did weird thing with their config
        # Using the reverse proxy config will cause an error "Contradictory scheme headers"
        # I don't have the patience to fix this properly
        #include snippets/reverse_proxy.conf;
    }
}
```

On fait le petit symlink qui va bien et on relance nginx:
```sh
$ sudo ln -s /etc/nginx/sites-available/apprise.conf /etc/nginx/sites-enabled/apprise.conf
$ sudo systemctl restart nginx
```

On test que tout marche bien en allant sur [https://notif.public.lan](https://notif.public.lan).

Attention aux DNS, si c'est pas encore configuré dans la freebox on n'y aura pas accès, on peut temporairement mettre ça dans `/etc/hosts` sur son PC:
```
192.168.14.59 notif.public.lan
```

## Post-setup Apprise

Aller sur la page web et configurer les canaux de notification en suivant les infos présentes sur [leur wiki](https://github.com/caronc/apprise/wiki#notification-services).

[Page précédente](setup_xoa.md) / [Page suivante](setup_jellyfin.md)