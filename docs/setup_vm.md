# Setup des VMs

Nous allons créer deux VM, une pour les services accessibles par la famille et une pour les services accessibles uniquement en local.

## Ajouter le SR des iso sur xcp-ng

Sur XOA, allez dans `Home > Hosts > rubeus > Storage` puis cliquer sur `Add a storage`.

Donner un nom (`NAS - Iso`), une description `ISOs on the NAS` et choisir en type `SMB ISO`.

Pour le serveur renseigner `\\NAS-IP\iso` et en username/password le user dédié au partage du point de montage ISO.

Valider

## Création de la VM publique

Via XOA nous créons donc une VM `Public VM` avec 2 vCPU, 2Go de ram (A voir à l'usage si c'est suffisant) et 60Go de stockage (Overkill mais j'ai de la place).

Avant de lancer la VM, nous allons ajouter le passthrough pour le iGPU, sur l'host xcp-ng:
```sh
$ xe vm-param-set other-config:pci=0/0000:<ID iGPU (ex: 00:02.0)> uuid=<ID DE LA VM>
```

Effectuer une install de debian standard avec comme hostname `rubeus-public`, server name `public.lan`. Déselectionner l'environnement de bureau pour ne garder que "serveur SSH" et "Utilitaires usuels du système". Un user/password puis on installe le Management Agent de xcp-ng.

### Autoriser l'utilisateur à sudo
```sh
# apt update && apt install sudo vim
# EDITOR=vim visudo
```

S'assurer que cette ligne est bien présente:
```
# Allow members of group sudo to execute any command
%sudo   ALL=(ALL:ALL) ALL
```

Puis l'ajouter au groupe concerné:
```sh
# usermod -aG sudo oxodao
```

On note l'ip de la vm (Aussi visible dans XOA):
```sh
$ ip -br -c a
```

Enfin, se déconnecter du SSH et copier sa clé publique pour pouvoir se connecter avec.
```sh
$ ssh-copy-id oxodao@192.168.14.XX
```

## Création de la VM locale

Même chose que pour la VM publique avec exception:
- 12Go de ram
- 120Go de stockage
- Hostname à rubeus-local
- Pas de setup pour le iGPU

**Attention**, pour HomeAssistant il faut aussi autoriser le passthrough de l'adaptateur zigbee, se référer à la partie [HomeAssistant](setup_ha.md) avant de lancer le ansible !

[Page précédente](setup_xcp.md) / [Page suivante](setup_common.md)