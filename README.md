# Homelab

Here's the ansible for my homelab.

It features:
- Auto-monitoring (By mail)
- Automated encrypted backups of important stuff (With restic on S3)
- DNS server
- NAS server
- Paperless (Managing your documents)
- Jellyfin (Media server)
- Gitea (Git server)
- Home Assistant (with zigbee2mqtt, nodered & mosquitto)
- JDownloader headless (for MyJdownloader)

## Usage

### Presetup

This guide expects you have a zfs pool with the following datasets: `nas_drives/sauvegarde`, `nas_drives/documents`, `nas_drives/shares`, `nas_drives/isos`

Here's how to create it. Note that once the drives are setup you must not do it again even if you reinstall your OS.

```
$ zpool create nas_drives mirror /dev/disk/by-id/disk1 /dev/disk/by-id/disk2
$ zpool create -o casesensitivity=mixed nas_drives/sauvegarde
$ zpool create -o casesensitivity=mixed nas_drives/documents
$ zpool create -o casesensitivity=mixed nas_drives/shares
$ zpool create -o casesensitivity=mixed nas_drives/isos
$ zfs set mountpoint=/mnt/sauvegarde nas_drives/sauvegarde
$ zfs set mountpoint=/mnt/documents nas_drives/documents
$ zfs set mountpoint=/mnt/shares nas_drives/shares
$ zfs set mountpoint=/mnt/isos nas_drives/isos
$ zfs export nas_drives
```

Note that they are case insensitive because we're making a samba share with them.

This also expects the ansible user is able to run root commands, on the server:
```
$ su -c "apt update && apt install sudo && /usr/sbin/usermod -aG sudo USERNAME"
```

Clone the repository on your computer, copy the `inventory.yaml.dist` to `inventory.yaml` and fill it accordingly.

You need to have a wildcard certificate for your hostname (home.lan in my case), please put it in the `files` folder so that you have `files/home.lan.crt` and `files/home.lan.key`. If you don't have one, see `docs/be-your-own-ca.md` to generate a CA and then a wildcard certificate. The CA private key should be stored in a secure location as it will be trusted on all of your machine. If it get stolen HTTPS BECOME USELESS ON YOUR MACHINES FOR ALL WEBSITES (You probably don't check the issuer of every cert of every website you visit) so be extra careful (REALLY IMPORTANT!).


### Setup

```
$ ansible-galaxy install -r requirements.yaml
$ ansible-galaxy collections install -r requirements.yaml
$ ansible-playbook --ask-become-pass -i inventory.yaml setup.yaml
```

### Usage

Now that everything is ready you can use the services with the following URLs, be sure to set your router's DNS server to the homelab's IP beforehand.

- https://play.home.lan => Jellyfin
- https://paper.home.lan => Paperless
- https://git.home.lan => Gitea

## License
> Copyright © 2023 Oxodao
> This work is free. You can redistribute it and/or modify it under the
> terms of the Do What The Fuck You Want To Public License, Version 2,
> as published by Sam Hocevar. See the COPYING file for more details.
