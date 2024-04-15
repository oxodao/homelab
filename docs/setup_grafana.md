# Setup Grafana

**VM LOCALE**

> A faire même en cas de ansible
>
> => Post-setup Grafana

## Setup de Grafana

En tant qu'utilisateur non-root, on créé les dossiers utiles:
```sh
$ mkdir -p /home/oxodao/grafana/data
```

On ajoute ensuite le `docker-compose.yaml` dans `/home/oxodao/grafana`:
```yaml
services:
  app:
    image: 'grafana/grafana-oss'
    restart: 'unless-stopped'
    user: 1000:1000
    environment:
      GF_SERVER_ROOT_URL: 'https://grafana.home.lan'
    volumes:
      - './data:/var/lib/grafana'
    ports:
      - '127.0.0.1:5492:3000'
    extra_hosts:
      - 'host.docker.internal:host-gateway'
```

Puis on le lance:
```sh
$ cd /home/oxodao/grafana
$ docker compose up -d
```

Ensuite on setup le nginx, dans `/etc/nginx/sites-available/grafana.conf`:
```
server {
    listen      80;
    server_name grafana.home.lan;
    return 307 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name grafana.home.lan;

    include snippets/ssl.conf;

    location / {
        proxy_pass http://localhost:5492;
        include snippets/reverse_proxy.conf;
    }
}
```

On fait le petit symlink qui va bien et on relance nginx:
```sh
$ sudo ln -s /etc/nginx/sites-available/grafana.conf /etc/nginx/sites-enabled/grafana.conf
$ sudo systemctl restart nginx
```

On test que tout marche bien en allant sur [https://grafana.home.lan](https://grafana.home.lan).

Attention aux DNS, si c'est pas encore configuré dans la freebox on n'y aura pas accès, on peut temporairement mettre ça dans `/etc/hosts` sur son PC:
```
192.168.14.59 grafana.home.lan
```

## Post-setup Grafana

On se connecte avec le compte `admin:admin` puis on choisi un nouveau mot de passe.

On va changer son username / email / display name.

Puis dans Connection > Data sources on va ajouter InfluxDB:
- Name: `Home Assistant - InfluxDB`
- Query Language: `Flux`
- URL: `http://host.docker.internal:8086`
- InfluxDB details > Organization: `homelab`
- InfluxDB details > Token: `LE TOKEN`

>>> ça marche pas @TODO !!

[Page précédente](setup_ha.md) / [Page suivante](setup_vpn.md)