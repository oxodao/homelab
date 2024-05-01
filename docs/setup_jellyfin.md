# Setup Jellyfin

**VM PUBLIC**

Pour Jellyfin, nous allons avoir besoin tout d'abord de monter le partage samba qui contient la collection de vidéos puis nous le passerons via Docker.

> A faire même en cas de ansible
>
> => Post-setup Jellyfin

## Ajout du montage SMB

On s'assure que `cifs-utils` est bien installé:
```sh
$ sudo apt install cifs-utils
```

On créé le dossier dans lequel le montage sera effectué:
```sh
$ sudo mkdir /mnt/shares
```

On ajoute l'entrée dans `/etc/fstab`:
```
[...]
//[IP_DU_NAS]/shares /mnt/shares cifs username=homelab_shares,password=[HOMELAB_SHARES_PASSWORD] 0 0
```

Enfin, on demande le montage et on vérifie que tout s'est bien passé:
```sh
$ sudo mount -a
$ ls /mnt/shares
```

Optionnellement, on peut stocker le mot de passe dans un fichier comme ceci:

`/etc/fstab`:
```
//[IP_DU_NAS]/shares /mnt/shares cifs credentials=/root/smb_shares_credentials 0 0
```

`/root/smb_shares_credentials`:
```
user=homelab_shares
password=[HOMELAB_SHARES_PASSWORD]
```

## Setup de Jellyfin

En tant qu'utilisateur non-root, on créé les dossiers utiles:
```sh
$ mkdir -p /home/oxodao/jellyfin/{cache,config,metadata,transcodes}
```

On ajoute ensuite le `docker-compose.yaml` dans `/home/oxodao/jellyfin`:
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
$ cd /home/oxodao/jellyfin
$ docker compose up -d
```

Ensuite on setup le nginx, dans `/etc/nginx/sites-available/jellyfin.conf`:
```
server {
    listen      80;
    server_name play.public.lan;

    # No redirecting to https version
    # Because the android app sucks
    # And won't allow self-signed certs
    location / {
        proxy_pass http://localhost:8096;
        include snippets/reverse_proxy.conf;
    }
}

server {
    listen 443 ssl http2;
    server_name play.public.lan;

    include snippets/ssl.conf;

    location / {
        proxy_pass http://localhost:8096;
        include snippets/reverse_proxy.conf;
    }
}
```

On fait le petit symlink qui va bien et on relance nginx:
```sh
$ sudo ln -s /etc/nginx/sites-available/jellyfin.conf /etc/nginx/sites-enabled/jellyfin.conf
$ sudo systemctl restart nginx
```

On test que tout marche bien en allant sur [https://play.public.lan](https://play.public.lan).

Attention aux DNS, si c'est pas encore configuré dans la freebox on n'y aura pas accès, on peut temporairement mettre ça dans `/etc/hosts` sur son PC:
```
192.168.14.59 play.public.lan
```

## Post-setup Jellyfin

Le post-setup de Jellyfin se fait dans le navigateur.

Le setup commence par la langue, sélectionner Français.

Créer le compte utilisateur.

Ajouter ensuite les médiatèques suivantes, laisser la config par défaut:
- Type: Films, Dossiers: /shares/Films, Nom: Films
- Type: Émissions, Dossiers: /shares/Series, Nom: Séries
- Type: Émissions, Dossiers: /shares/TV, Nom: TV
- Type: Clips musicaux, Dossiers: /shares/Concerts, Nom: Concerts

Langue de métadonnées: FR, Pays FR.

Accès à distance: laisser la config par défaut

Se connecter après le setup puis aller dans les paramètres d'administrations.

Optionnellement, créer les autres comptes utilisateurs nécessaires (Tant qu'on a pas d'AD)

Aller dans l'onglet "Lecture" pour configurer le hardware transcoding:
- Accélération matérielle: "Video Acceleration API (VAAPI)"
- Appareil VA-API: "/dev/dri/renderD128"
- Activer le décodage matériel pour: h264, HEVC, VC1, VP9, AV1
- Activer l'encodage matériel
- @TODO: Tester avec l'encoder basse conso h264
- Laisser le reste par défaut

Attention ces settings sont faites pour le i3-10100, cela peu changer si on change de matériel.

Pour vérifier que le transcoding marche, lancer un film dans un autre onglet puis choisir une résolution différente de la native du fichier, puis dans l'onglet admin aller dans "Tableau de bord", dans "Appareils actifs" cliquer sur le "i". Si le transcodage fonctionne la pop-up devrait afficher "@TODO".

Le setup de Jellyfin est terminé.

[Page précédente](setup_apprise.md) / [Page suivante](setup_navidrome.md)