# Setup du serveur DNS

Le serveur DNS se charge de traduire les domaines en `.lan` vers l'ip de la machine correspondante sur le réseau. Les autres TLD ne sont pas pris en compte et sont cherchés via les serveurs DNS [OpenNIC](https://www.opennic.org/).

> Toute la config est gérée dans le ansible.
>
> Rien est à faire à la main.


## Installation de dnsmasq
```sh
$ sudo apt install dnsmasq
```

> @TODO
>
> Vérifier que la config marche avec deux VMs.
>
> Voir comment faire marche l'IPv6 dans xcp-ng pour
> les androids qui veulent pas d'un DNS ipv4.

Ajouter la configuration dans `/etc/dnsmasq.conf`:
```
domain-needed # Ne transmet pas à OpenNIC les requête qui ne sont pas des noms de domaines complets
bogus-priv
no-resolv # N'utilise pas le fichier resolv.conf de la vm
no-hosts # N'utilise pas le fichier hosts de la vm

# Serveur DNS forwardé (Ce qui n'est pas résolu par le serveur local)
# Il peut y en avoir plusieurs
server={{ IP_DNS_OPENNIC }}

local=/lan/

domain=public.lan

# Addresses de mes VM
address=/.public.lan/192.168.14.59  # rubeus-public
address=/.home.lan/192.168.14.1  # rubeus-local

# Ces config sont des IPs fictives car flemme de les retrouver
# Il en manque aussi beaucoup surement
# Se référer au ansible pour avoir la liste complète
address=/severusdesk.lan/192.168.14.10  # PC de bureau
address=/severuspad.lan/192.168.14.11  # PC portable
address=/mediacenter.lan/192.168.14.20  # PC Media center
address=/switch.lan/192.168.14.30  # Nintendo Switch
```

Enfin on active ou redémarre le service
```sh
$ sudo systemctl enable --now dnsmasq
$ sudo systemctl restart dnsmasq
```

[Page précédente](setup_common.md) / [Page suivante](setup_reverseproxy.md)