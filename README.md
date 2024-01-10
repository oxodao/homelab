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
- JDownloader (Download manager)

## Usage

### Presetup

This guide expects you have a zfs pool with the following datasets: `nas_drives/sauvegarde`, `nas_drives/documents`, `nas_drives/shares`, `nas_drives/isos`

Here's how to create it. Note that once the drives are setup you must not do it again even if you reinstall your OS.

```
$ zpool create nas_drives mirror /dev/disk/by-id/disk1 /dev/disk/by-id/disk2
$ zfs create -o mountpoint=/mnt/sauvegarde -o casesensitivity=mixed nas_drives/sauvegarde
$ zfs create -o mountpoint=/mnt/documents -o casesensitivity=mixed nas_drives/documents
$ zfs create -o mountpoint=/mnt/images -o casesensitivity=mixed nas_drives/images
$ zfs create -o mountpoint=/mnt/shares -o casesensitivity=mixed nas_drives/shares
$ zfs create -o mountpoint=/mnt/isos -o casesensitivity=mixed nas_drives/isos
$ zfs export nas_drives
```

How this is organized:
- `sauvegarde` is my main NAS storage, where I put my files, SMB should have authed-only access
- `documents` is the Paperless' data folder, it should NOT be shared on SMB
- `images` is the Immich data folder, it should NOT be shared on SMB
- `shares` is where I put my movies, series, musics, ... It is SMB accessible in read-only for anonymous and read-write for authenticated
- `isos` is where I put my Windows / Linux ISOs to be used with VMs / real hardware. It should have the same permissions as `shares`

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
- https://dl.home.lan => JDownloader
- https://domo.home.lan => Home Assistant (Domotique = home automation in French)
- https://influx.home.lan => Influx DB (From HA)
- https://z2m.home.lan => Zigbee2mqtt (Only if enabled)
- https://nr.home.lan => Nodered

### Additional setup

#### Backups

The most important, you need to initialize your restic repo the first time.

```
$ AWS_ACCESS_KEY_ID=xxxxxxxx AWS_SECRET_ACCESS_KEY=xxxxxxxxxx restic -r s3:https://s3.eu-central-003.backblazeb2.com/xxxxxBUCKETxxxxx init
```

Put a reminder on your phone, once every ~3-6 months to TEST the backups. In order to do so, create a folder `test-backup` somewhere and restore EACH app in it. Stop the docker containers that are running and start them in the `test-backup` folder and verify everything is right (Config correctly restored, all data are present, ...). THIS IS AN EXTREMLY IMPORTANT THING TO DO. BAD BACKUPS = NO BACKUPS.

Optionally, use this time to export your s3 backup to a separate, external hard drive that you keep at one of your family member's house / a friend house to have a third backup to be extra safe. If for some reason you get kicked of your S3 account or the host catch fire (hi OVH).

#### Jellyfin

You need to do the initial setup of Jellyfin.

The media mount from the NAS (shares ZFS dataset) should contain your media. Create collections as you wish.

You also need to enable hardware acceleration, VA-API on the standard render node. For the `i3-10100` you can use the default decoders + `HEVC`, `VP8`, `MPEG2` and `VP9` (Don't trust google on this one, this list was obtained by `vainfo`. The quora answer is a liar).

You also need to setup the metadata folder and the transcodes folder to be `/metadata` and `/transcodes`. This is important as the data folder is backed up and you don't want those to be included in the backup process.

#### Gitea

Do the setup as you would do on a standard Gitea install. The only thing you have to change is the SSH port that should be `22` instead of `2222`.

Don't forget to create your admin account during the setup!

#### JDownloader

It should work out of the box. You might want to setup your MyJdownloader account though.

Keep in mind that the built-in UI is running under VNC server so you need to paste your clipboard in the box on the left so that it's forwarded to the app.

#### Paperless

You only have to setup your admin user, login to the homelab then:
```
$ cd /opt/docker-apps/paperless
$ dc exec app python3 manage.py createsuperuser
```

#### Home Assistant

This is a pain to setup so it's not fully automated.

You will need to setup influxdb, on the server:
```sh
$ cd /opt/docker-apps/homeassistant
$ docker compose exec influx influx setup --username "MY USERNAME" --password "MY PASSWORD" --token "MY_GENERATED_TOKEN" --retention 0 --org homelab --bucket homeassistant
```

In order to setup HomeAssistant you need to make it work with the reverse proxy:
```yaml
http:
  server_host: 127.0.0.1
  use_x_forwarded_for: true
  trusted_proxies: 127.0.0.1
```

in `/opt/docker-apps/homeassistant/config/configuration.yaml`.

You also need to configure the influx_db connection in this file:
```yaml
influxdb:
  api_version: 2
  ssl: false
  host: 127.0.0.1 # Note: HA is set up in network mode "host" so you can call directly 127.0.0.1
  port: 8086
  token: MY_GENERATED_TOKEN
  organization: homelab
  bucket: homeassistant
```

If you are using ESPHome you might also want to setup the token:
```yaml
api:
  encryption:
    key: "ESPHOME TOKEN"
```

Once this is done, you can `docker compose restart app`.

### Backup restoration

In order to see how to restore a backup, refer to [disaster recovery docs](/docs/disaster-recovery.md).

## License
```
Copyright © 2023 Oxodao
This work is free. You can redistribute it and/or modify it under the
terms of the Do What The Fuck You Want To Public License, Version 2,
as published by Sam Hocevar. See the COPYING file for more details.
```