# Setup du serveur DNS

Le serveur DNS se charge de traduire les domaines en `.lan` vers l'ip de la machine correspondante sur le réseau. Les autres TLD ne sont pas pris en compte et sont cherchés via les serveurs DNS [OpenNIC](https://www.opennic.org/).

> Toute la config est gérée dans le ansible.
>
> Rien est à faire à la main.


## Installation de dnsmasq
```sh
$ sudo apt install dnsmasq
```

Ajouter la configuration dans `/etc/dnsmasq.conf`:
```
# Never forward plain names (without a dot or domain part)
domain-needed

# Never forward addresses in the non-routed address spaces.
bogus-priv

# Don't read /etc/resolv.conf or any other file.
no-resolv

# Don't read /etc/hosts file
no-hosts

# Don't poll changes from external files (like /etc/resolv.conf)
no-poll

# Force the upstream servers to be used in order
strict-order

# Don't store in cache the invalid resolutions
no-negcache

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