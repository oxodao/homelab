# Setup reverse-proxy

Pour le reverse-proxy, j'utilise `nginx`. Puisque j'ai un certificat CA privé, cela nécessite une petite configuration en plus.

> Attention
>
> L'étape "Créer son CA" n'est pas inclue dans le ansible
>
> Il faut le faire à la main et placer les certificats au bon endroit dans ansible !

**Note**: Pour la suite de ce guide, si il n'est pas précisé sur quelle VM effectuer les actions, il faut le faire sur les deux.

## Créer son CA

Se référer au guide [be your own CA](be_your_own_ca.md) pour créer son certificat CA ainsi que des certificats pour des noms de domaines.

Créer un certificat `public.lan` / `*.public.lan` et `home.lan` / `*.home.lan`.

*Ansible se charge de la suite*

Sur les deux VMs créer le dossier `/opt/ssl`

Copier via scp les certificats sur les bonnes VMs:
```sh
$ scp home.lan.crt oxodao@rubeus-local:/opt/ssl/home.lan.crt
$ scp home.lan.key oxodao@rubeus-local:/opt/ssl/home.lan.key
$ scp public.lan.crt oxodao@rubeus-public:/opt/ssl/public.lan.crt
$ scp public.lan.key oxodao@rubeus-public:/opt/ssl/public.lan.key
```

S'assurer que les owner des fichiers `.key` soient en `root:root` avec les permissions `600`.

Les permissions des clés publiques ne sont pas importantes.

## Installer nginx

```sh
$ sudo apt install nginx openssl
```

## Configuration de nginx

### Création du dhparm

Exécuter les commandes suivantes:
```sh
$ cd /opt/ssl
$ openssl dhparam -out dhparam.pem 2048
```

### Configuration du nginx

Nous allons faire un système modulaire à la `apache2`, la configuration de nginx importera les sites depuis le dossier `sites-enabled`.

Tout d'abord nous allons créer le fichier `/etc/nginx/nginx.conf` qui sera très simple et se contentera d'importer les sites:
```nginx
worker_processes  1;

events {
    worker_connections  1024;
}


http {
    include       mime.types;
    default_type  application/octet-stream;
    sendfile        on;
    keepalive_timeout  65;

    include sites-enabled/*;
}
```

Ensuite, nous allons créer les dossiers importants pour la configuration:
```sh
$ sudo mkdir -p /etc/nginx/{sites-available,sites-enabled,snippets}
```

- **sites-available**: Dossier dans lequel nous mettrons la configuration des sites
- **sites-enabled**: Dossier qui contiendra des liens symboliques vers les applications actuellements utilisées
- **snippets**: Dossier qui contiendra des helpers pour les configurations des diverses applis


### Snippets

Nous allons créer un snippet pour la configuration SSL qui sera réutilisée par les sites.

Cette config est à titre d'exemple, il convient d'utiliser le [generateur de config de mozilla](https://ssl-config.mozilla.org/) pour générer une config à jour puis de récupérer les différentes portions liées au SSL.


```
ssl_session_timeout 1d;
ssl_session_cache shared:MozSSL:10m;  # about 40000 sessions
ssl_session_tickets off;

# curl https://ssl-config.mozilla.org/ffdhe2048.txt > /path/to/dhparam
ssl_dhparam /opt/ssl/dhparam.pem;

# intermediate configuration
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384:DHE-RSA-CHACHA20-POLY1305;
ssl_prefer_server_ciphers off;

# HSTS (ngx_http_headers_module is required) (63072000 seconds)
add_header Strict-Transport-Security "max-age=63072000" always;

ssl_certificate /opt/ssl/{HOSTNAME}.lan.crt;
ssl_certificate_key /opt/ssl/{HOSTNAME}.lan.key;
```

## Lancement de nginx
```sh
$ sudo systemctl enable --now nginx
```

## Ajout d'applications

Pour ajouter une application, on utilise la config standard suivante.

Attention elle est à personnaliser en fonction de l'appli et peut avoir des cas d'usage spécifique.

Cette config prends en compte les websockets et devrait donc marcher dans la plupart des cas.

```
server {
    listen      80;
    server_name {SUBDOMAIN}.{HOSTNAME}.lan;

    # Using 307 ensure that the client will follow the redirection on POST requests
    # Cf. https://softwareengineering.stackexchange.com/questions/99894/why-doesnt-http-have-post-redirect
    return 307 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name {SUBDOMAIN}.{HOSTNAME}.lan;

    include snippets/ssl.conf;

    location / {
        proxy_pass http://localhost:{PORT};
        proxy_http_version 1.1;
        proxy_redirect off;
        proxy_buffering off;
        proxy_pass_request_headers on;

        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $remote_addr;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Protocol $scheme;
        proxy_set_header X-Forwarded-Host $http_host;
    }
}
```

Elle est à placer dans `/etc/nginx/sites-available/{APP_NAME}.conf` puis à symlink:
```sh
$ sudo ln -s /etc/nginx/sites-available/{APP_NAME}.conf /etc/nginx/sites-enabled/{APP_NAME}.conf
```

Enfin, on redémarre le serveur nginx pour prendre en compte la nouvelle config:
```sh
$ sudo systemctl restart nginx
```

Si on souhaite tester la config avant de redémarrer le serveur et potentiellement tout casser, on peut utiliser l'argument suivant:
```sh
$ sudo /usr/sbin/nginx -t
```

[Page précédente](setup_dns.md) / [Page suivante](setup_jellyfin.md)