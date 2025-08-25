# Setup Koel

**VM VPS**

> A faire même en cas de ansible
>
> => Post-setup Koel

## Ajout du montage SMB

Même setup que Jellyfin, et on utilise le point de montage `Music`.

## Setup de Koel

En tant qu'utilisateur non-root, on créé les dossiers utiles:
```sh
$ mkdir -p /home/oxodao/koel/{search_index,pg_data}
```

On ajoute ensuite le `compose.yaml` dans `/home/oxodao/koel`:
```yaml

```

Puis on le lance:
```sh
$ cd /home/oxodao/koel
$ docker compose up -d
```

## Post Setup Koel

Il faut initialiser le soft visiblement et c'est pas expliqué dans leur doc.

```sh
$ docker compose exec app php artisan key:generate
$ docker compose exec app php artisan koel:init
```

[Page précédente](setup_paperless.md) / [Page suivante](setup_immich.md)