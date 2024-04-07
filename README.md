# Oxodao's Homelab

Documentation de mon homelab

## Architecture

Mon homelab est composé de trois machines:
- Un NAS Synology pour le stockage (Actuellement 2x2TB WDC WD20EFRX-68EUZN0)
- Un PC "multimédia" qui est utilisé sur la TV (Thinkcentre m75q / Athlon 300GE)
- Un PC serveur (i3-10100 / 24Gb DDR4 / 1to nvme)
- Un router TP Link Archer C6 (AC1200) sous OpenWRT (Pas encore mis en place)

Le serveur est un host XCP-NG (hostname `rubeus`) avec deux VM principales, une dédiée aux services accessible en publique, l'autre avec les services accessible uniquement sur le réseau interne.

Note: le serveur n'a pas de VM pour XenOrchestra, j'utilise sur mon PC une VM sur laquelle j'ai installé XOA via [XenOrchestraInstallerUpdater](https://github.com/ronivay/XenOrchestraInstallerUpdater), cela permet d'économiser de la RAM / du CPU utilisé pour autre chose.

Le NAS Synology possède toutes les data et expose plusieurs montage samba:
- sauvegarde (Mon espace de stockage générique ou je met un peu tout)
- iso (Mon SR d'iso pour xcp-ng)
- shares (Espace pour stocker mes films / séries / musiques / ...)
- documents (Montage utilisé pour Paperless)
- images (Montage utilisé pour Immich)

Pour la gestion des droits, j'ai mon utilisateur perso pour la connexion depuis mes machines, et des utilisateurs scopés en RO sur iso et shares pour les différents services ansi qu'un utilisateur RW pour Paperless, chacun n'ayant accès qu'aux shares qu'ils ont besoin.

Enfin le PC multimédia est un simple debian 12 qui accèdes aux services hébergés sur le serveur.

Ce guide note particulièrement le setup du serveur puisque le reste est basique et ne nécessite rien de spécial.

## Sommaire

1. [Setup XCP-NG](docs/setup_xcp.md)
2. [Setup basique des VMs](docs/setup_vm.md)

> A partir de ce point la, les divers ansible
> vont setup tout ça.
>
> Il faut tout de même suivre chaque page pour s'assurer
> la config des logiciels est complète car tout n'est
> pas fait dans ansible pour l'instant (e.g. config
> interne de Jellyfin, création de compte utilisateur, etc...)

3. [Setup des utilitaires communs](docs/setup_common.md)
4. [Setup serveur DNS](docs/setup_dns.md)
5. [Setup reverse-proxy](docs/setup_reverseproxy.md)

-- Setup des apps --

6. [Setup Jellyfin](docs/setup_jellyfin.md)
7. [Setup Navidrome](docs/setup_navidrome.md)
8. [Setup Paperless](docs/setup_paperless.md)
9. [Setup Gitea](docs/setup_gitea.md)
10. [Setup Immich](docs/setup_immich.md)
11. [Setup JDownloader](docs/setup_jdownloader.md)
12. [Setup HomeAssistant](docs/setup_ha.md)

-- Setup sécu --

13. [Setup serveurs VPN](docs/setup_vpn.md)
14. [Setup firewall](docs/setup_firewall.md)
15. [Setup cloudflared](docs/setup_cloudflared.md)
16. [Setup backups](docs/setup_backups.md)

> A partir de ce point la, il s'agît d'informations sur
> l'utilisation usuelle des VMs et du serveur ainsi que
> comment faire du disaster recovery.

17. [Ajouter un utilisateur sur le VPN](docs/add_user_vpn.md)
18. [Renouveller les certificats SSL](docs/renew_ssl.md)
19. [Restorer un backup](docs/disaster_recovery.md)
20. [Backup day](docs/backup_day.md)

## Roadmap

Chose que je vais potentiellement ajouter après que tout soit fonctionnel

- Authentik / Authelia: Active Directory / OAuth
    - [Gitea](https://docs.gitea.com/usage/authentication): LDAP
    - [Jellyfin](https://github.com/jellyfin/jellyfin-plugin-ldapauth): LDAP
    - [Immich](https://www.reddit.com/r/selfhosted/comments/zrkokx/immich_and_ldap/): OAuth
    - [Paperless](https://github.com/paperless-ngx/paperless-ngx/pull/100): Ils ont pas l'air de vouloir ni ldap ni oauth
    - [Navidrome](https://github.com/navidrome/navidrome/pull/590): huuuh ça à pas l'air très fun non plus
    - JDownloader: Accès externe donc via LEUR login, à voir pour dev un client self-hosted mais API non documentée
