# Backups

## Setup backups

Pour faire les backups, on va utiliser resticprofile.

Il permet d'avoir des fichiers de configuration pour restic.

### Setup restic

Restic à besoin d'un setup un peu particulier car on veut qu'il soit exécuté en root quoi qu'il arrive (Pas bien mais oh well).

On installe donc restic et on lui donne cette capacité:
```sh
$ sudo apt install restic
$ sudo setcap 'cap_dac_read_search=+ep' /usr/bin/restic
```

### Setup resticprofile

Ensuite on installe resticprofile, pour cela, récupérer l'url du latest sur [creativeprojects/resticprofile](https://github.com/creativeprojects/resticprofile):
```sh
$ wget -O /tmp/resticprofile.tar.gz https://xxxxxxx
$ tar -xvzf /opt/resticprofile.tar.gz -C /opt/
$ rm /opt/{LICENSE,README.md}
$ chmod +x /opt/resticprofile
$ sudo ln -s /opt/resticprofile /usr/bin/resticprofile
```

### Configuration

On ajoute notre fichier contenant le mot de passe de notre repository restic:

```sh
# echo "my_password" > /root/password.txt
# chmod 600 /root/password.txt
```

Une fois fait, on va pouvoir créer notre fichier de configuration dans `/etc/resticprofile/profiles.yaml:
```yaml
version: '1' # La version 2 n'est pas encore stable donc on reste sur la 1

groups:
  full: # On créé un groupe pour facilement tout lancer sans lancer le default qui est "abstrait"
    - my_app1
    - my_app2

# Le "default" est notre tâche abstraite qui va contenir la
# config principale réutilisée partout
default:
  repository: 's3:s3.eu-central-003.backblazeb2.com/BUCKET_NAME'
  password-file: '/root/password.txt'

  env:
    AWS_ACCESS_KEY_ID: 'my b2 access key'
    AWS_SECRET_ACCESS_KEY: 'my b2 secret key'

  # Pour la commande restic backup
  backup:
    # Avant toute chose
    run-before:
      # On envoit un message sur discord pour prévenir qu'on backup l'app
      - 'sn -l main_bot -m "Backing up $PROFILE_NAME"'
      # On l'éteint
      - 'cd ~oxodao/$RESTIC_APP && docker compose down'
    # Après que le backup soit fait
    run-after:
      # On envoit un message pour dire que tout s'est bien passé
      - 'sn -l main_bot -m "$PROFILE_NAME backed up!'
    # En cas d'erreur
    run-after-fail:
      - 'sn -l main_bot -m "Failed to backup $PROFILE_NAME: $ERROR_MESSAGE\n$ERROR_STDERR'
    # Et dans tous les cas, après
    run-finally:
      # On rallume l'app
      - 'cd ~oxodao/$RESTIC_APP && docker compose up -d'

# Pour chaque app qu'on veut faire, on peut alors définir sa config spécifique
my_app1:
  # On ré-utilise la config default
  inherit: 'default'

  # Le run-before de l'app est exécuté avant le run-before de la commande (backup)
  # On set une variable d'environnement pour qu'il sache dans quel dossier ça se passe
  run-before:
    - 'echo "RESTIC_APP=my_app1" > "{{env}}"'

  backup:
    source: ['/home/oxodao/jellyfin'] # Le dossier à backup
    tag: ['jellyfin'] # Le tag restic à afficher
    exclude: # La liste des fichiers à exclure du backup (cache, transcodes, etc...)
      - 'cache/'
      - 'transcodes/'

# Pour les app qui stockent leurs données sur le nas,
# On créé une autre config avec le suffix `_docs`
my_app1_docs:
  inherit: 'default'

  run_before:
    # On set la MÊME variable d'environnement
    # Car on veut toujours qu'il éteigne l'app avant de backup
    - 'echo "RESTIC_APP=my_app1" > "{{env}}"'

  backup:
    source: ['/mnt/myapp'] # On sélectionne le point de montage SMB
    tag: ['my_app1_docs'] # On lui donne aussi le suffix

    exclude:
      - 'my_excluded_dir/'

```

### Setup du cronjob

Afin de le lancer régulièrement, on va plannifier un cronjob qui fera le backup tous les lundis à minuit de la VM locale, et tous les lundis à 1h de la VM publique. Cela est fait pour éviter qu'on ait les messages mixés dans les logs sur discord.

Le tag "Ansible: " permet à ansible de retrouver quelle tâche correspond à quelle cronjob.

VM locale:
```sh
$ crontab -e
#Ansible: backup_job
0 0 * * 1 resticprofile --name "full" backup
```

VM publique:
```sh
$ crontab -e
#Ansible: backup_job
0 1 * * 1 resticprofile --name "full" backup
```

### Initialization du repository

Si on part d'un S3 vide qui n'est pas déjà un repository restic, il faut l'initialiser:
```sh
$ resticprofile --name "default" init
```

## Tags

- gitea: local:/home/oxodao/gitea
- gitea_docs: smb://NAS/git
- grafana: local:/home/oxodao/grafana
- homeassistant: local:/home/oxodao/homeassistant
- immich: local:/home/oxodao/immich
- immich_docs: smb://NAS/images
- jellyfin: public:/home/oxodao/jellyfin
- navidrome: public:/home/oxodao/navidrome # Pas de _docs pour l'instant
- paperless: local:/home/oxodao/paperless
- paperless_docs: smb://NAS/documents

## Utilisation de resticprofile

Resticprofile prends en paramètre un name permettant de spécifier la tache ou le groupe à utiliser, puis des commandes standard de restic.

Passer un paramètre AVANT la commande restic le passe à resticprofile, et après le passe à restic lui même.

Par exemple si on veut lister les backups:
```sh
# On peut se permettre d'utiliser default puisqu'il est suffisement configuré pour cet usage
# Les profiles spécifiques ne sont à utiliser que pour le backup
$ resticprofile --name "default" snapshots
2024/07/13 12:44:40 using configuration file: /etc/resticprofile/profiles.yaml
2024/07/13 12:44:40 profile 'default': starting 'snapshots'
repository 72394675 opened (repository version 2) successfully, password is correct
ID        Time                 Host           Tags        Paths
--------------------------------------------------------------------------------
9e609ecd  2024-07-09 21:41:03  rubeus-public  jellyfin    /home/oxodao/jellyfin
9824bc9d  2024-07-09 21:41:11  rubeus-public  navidrome   /home/oxodao/navidrome
914c2fb0  2024-07-13 11:15:05  rubeus-public  jellyfin    /home/oxodao/jellyfin
f99938cf  2024-07-13 11:15:10  rubeus-public  navidrome   /home/oxodao/navidrome
--------------------------------------------------------------------------------
```

## Restorer un backup

Restaurer une app nécessite de restaurer le tag standard ET le tag `_docs` datant du MÊME BACKUP.

D'abord on restaure sur le PC la/les snapshots en question, par exemple je veux restorer navidrome de l'exemple précédent:
```sh
$  AWS_ACCESS_KEY_ID='KEY_ID' AWS_SECRET_ACCESS_KEY='KEY_SECRET' restic -r s3:s3.eu-central-003.backblazeb2.com/BUCKET_NAME restore f99938cf --target .
```

> /!\ On met bien un ESPACE avant la commande
>
> Cela permet d'éviter qu'elle se stock dans l'historique du shell
>
> Car on a nos credentials dedans

Le restore se fait dans le dossier actuel du coup (`.`). On supprime les fichiers sur le serveur puis on les remplace par ceux restaurés.

[Page précédente](setup_firewall.md) / [Page suivante](setup_add_user_vpn.md)