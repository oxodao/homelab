# Autorestic

Cheatsheet autorestic

## Config file
```yaml
version: 2

backends:
  local_backblaze:
    type: 's3'
    path: 's3.REGION.backblazeb2.com/BUCKET'
    key: 'CLE DE CHIFFREMENT'
    env:
      AWS_ACCESS_KEY_ID: 'ACCESS ID'
      AWS_SECRET_ACCESS_KEY: 'ACCESS SECRET'

locations:
  gitea:
    from: '/home/oxodao/gitea'
    to: ['local_backblaze']
    options:
      backup:
        tag: ['gitea']
        exclude:
            - 'List of file'
            - 'or pattern'
            - 'to ignore'
    hooks:
      before:
        - 'curl -k -X POST -F "body=Backing up Gitea" -F "tags=all" https://notif.home.lan/notify/apprise'
        - 'cd /home/oxodao/gitea && docker compose down'
      after:
        - 'cd /home/oxodao/gitea && docker compose up -d'
        - 'curl -k -X POST -F "body=Gitea backed up" -F "tags=all" https://notif.home.lan/notify/apprise'
```

## Initialiser le bucket

Lors de la création du bucket on doit initialiser le repo restic, pour cela utiliser cette commande
```sh
$ autorestic exec -a init
```

## Variables d'environnement restic
```sh
$ export AWS_ACCESS_KEY_ID='ACCESS KEY ID'
$ export AWS_SECRET_ACCESS_ID='SECRET KEY ID'
$ export RESTIC_REPOSITORY='s3:s3.REGION.backblazeb2.com/BUCKET'
$ export RESTIC_PASSWORD='restic repository password'
```

## Lancer un backup
```sh
$ autorestic backup -a
```

## Restaurer un backup
```sh
$ restic snapshots # Lister les snapshots
$ restic restore <snapshot hash> --target . # Restaurer une snapshot dans le dossier actuel
```