# Setup XCP-NG

XCP-NG est l'hyperviseur que j'ai choisi pour mon homelab. Ce dernier est consitué d'un seul host.

## Installation

Rien de spécifique pour l'installation, télécharger l'iso [via le site officiel](https://xcp-ng.org/#easy-to-install) et suivre les instructions de base.

## Post-install

Après l'installation, on va ajouter le terminfo pour `tmux-256color` sinon ça va être relou.
```sh
$ curl -LO https://invisible-island.net/datafiles/current/terminfo.src.gz && gunzip terminfo.src.gz
$ tic -xe tmux-256color terminfo.src
$ rm terminfo.src terminfo.src.gz
```

Déco-reco du ssh pour que ça prenne effet.

Ensuite, il faut préparer le iGPU à être utilisé en passthrough pour la VM qui proposera Jellyfin.

[Doc officielle](https://docs.xcp-ng.org/compute/#pci-passthrough)

```shell
$ lspci | grep VGA
00:02.0 VGA compatible controller: Intel Corporation CometLake-S GT2 [UHD Graphics 630] (rev 03)
```

On prends note du device id (00:02.0) puis on l'exclu de `dom0`:
```shell
# /opt/xensource/libexec/xen-cmdline --set-dom0 "xen-pciback.hide=(0000:00:02.0)"
```

On reboot le host puis on vérifie que le iGPU est bien disponible:
```shell
# xl pci-assignable-list
0000:00:02.0
```

Une fois cela fait, on est prêt à créer nos VMs.

[Page suivante](setup_vm.md)