# Setup Gitea

**VM LOCALE**

> A faire même en cas de ansible
>
> => Post-setup Gitea

## Ajout du montage SMB

Même setup que Jellyfin, et on utilise le point de montage `git`.

## Setup de Gitea

En tant qu'utilisateur non-root, on créé les dossiers utiles:
```sh
$ mkdir -p /home/oxodao/gitea/config
```

On ajoute ensuite le `docker-compose.yaml` dans `/home/oxodao/gitea`:
```yaml
services:
  app:
    image: 'gitea/gitea:latest-rootless'
    restart: 'unless-stopped'
    environment:
      USER: 'oxodao'
      USER_UID: 1000
      USER_GID: 1000
    volumes:
      - './config:/etc/gitea'
      - '/etc/timezone:/etc/timezone:ro'
      - '/etc/localtime:/etc/localtime:ro'
      - '/mnt/git:/var/lib/gitea'
    ports:
      - '127.0.0.1:3000:3000'
      - '22:22'
```

Puis on le lance:
```sh
$ cd /home/oxodao/gitea
$ docker compose up -d
```

Ensuite on setup le nginx, dans `/etc/nginx/sites-available/gitea.conf`:
```
server {
    listen      80;
    server_name git.home.lan;
    return 307 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name git.home.lan;

    include snippets/ssl.conf;

    # Lets you use LFS
    client_max_body_size 10000M;

    location / {
        proxy_pass http://localhost:3000;
        include snippets/reverse_proxy.conf;
    }
}
```

On fait le petit symlink qui va bien et on relance nginx:
```sh
$ sudo ln -s /etc/nginx/sites-available/gitea.conf /etc/nginx/sites-enabled/gitea.conf
$ sudo systemctl restart nginx
```

On test que tout marche bien en allant sur [https://git.home.lan](https://git.home.lan).

Attention aux DNS, si c'est pas encore configuré dans la freebox on n'y aura pas accès, on peut temporairement mettre ça dans `/etc/hosts` sur son PC:
```
192.168.14.59 git.home.lan
```

## Post-setup Gitea

**Note**: On met la BD de gitea dans `/etc` car l'endroit par défaut est sur le montage SMB et SQLite n'aime VRAIMENT pas être sur le smb.

Aller sur l'interface web, une page de configuration initale sera affichée.

Choisir:
- SQLite 3
- Stocker la BD dans `/etc/gitea/gitea.db`
- Titre du site: "Oxodao's Git"
- S'assurer que Domaine du serveur = "git.home.lan"
- Port du serveur SSH: 22
- S'assurer que URL de base de Gitea = "https://git.home.lan/"
- Activer la vérification de MaJ

Paramètres de messagerie:
- Remplir avec la config Mailgun
- Activer les notifications par courriel

Paramètres de serveur et tierce parties:
- Activer le mode hors-ligne
- Désactiver le formulaire d'inscription
- Exiger la connexion à un compte pour afficher les pages

Paramètres de compte administrateur:
- Créer son compte admin


[Page précédente](setup_paperless.md) / [Page suivante](setup_immich.md)