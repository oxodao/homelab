# Setup de SimpleNotifier

**VM LOCAL & PUBLIC**

[Soft](https://github.com/oxodao/simple-notifier) que j'ai créé moi même pour simplifier l'envoi de notifications sur Discord.

## Setup de SimpleNotifier

En tant qu'utilisateur root, on télécharge la dernière release présente sur le Github et on la met dans le bon dossier en ajoutant les droits
```sh
$ wget https://github.com/oxodao/simple-notifier/XXXXXXXXXXXX
$ mv sn-vX.X.X-linux-amd64 /usr/bin/sn
$ chmod +x /usr/bin/sn
```

Puis on ajoute la config:
`/etc/simple_notifier.yaml`
```yaml
locations:
  main_bot:
    type: discord
    bot_name: 'Backup bot'
    webhook: 'URL DE WEBHOOK DE DISCORD'
```

Enfin on test que ça marche bien:
```sh
$ sn -l main_bot -m "Test message"
```

[Page précédente](setup_xoa.md) / [Page suivante](setup_jellyfin.md)