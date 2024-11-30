# Setup des serveurs VPNs

J'utilise Wireguard comme serveur VPN.

Deux VPNs sont créés:
- Un VPN pour moi uniquement me permettant d'accéder à tout le réseau local
- Un VPN pour ma famille permettant d'accéder à la machine `rubeus-public`

Il faut donc faire le setup sur les deux machines puisqu'un firewall bloque l'accès au réseau local à la machine `rubeus-public` qui n'a alors accès qu'au NAS.

**Note**: Lien utile => https://gist.github.com/qdm12/4e0e4f9d1a34db9cf63ebb0997827d0d, https://www.developpez.net/forums/d1275817/systemes/linux/securite/iptables-forward-drop/

> Aucun setup hors ansible
>
> Sauf si ajout d'utilisateurs

## Installation de Wireguard

Il faut tout d'abord installer deux packages:
```sh
$ sudo apt install wireguard wireguard-tools
```

On s'assure que l'ip forwarding est activée:
```sh
$ cat /etc/sysctl.conf
# Si ce n'est pas le cas, ajouter la ligne suivante dans ce fichier:
net.ipv4.ip_forward=1
# Puis appliquer
$ sudo sysctl -p
```

## Configuration de Wireguard

On va tout d'abord générer une clé publique et une clé privée pour le serveur, en tant que root:
```sh
$ cd /etc/wireguard
$ umask 077
$ wg genkey | tee private.key | wg pubkey > public.key
```

Puis on créé le fichier de configuration `/etc/wireguard/wg0.conf:
```
[Interface]
Address = 192.168.XX.1/24
ListenPort = <PORT DE WIREGUARD>
PrivateKey = <Contenu du fichier private.key>

# Clients
```

### IPTables

Dans la section interface il va falloir rajouter deux configurations, `PostUp` et `PostDown`. Il s'agit des commandes exécutées par wireguard à ces moments permettant de router les packets correctement via iptables.

Pour le serveur local il faut utiliser les lignes suivantes:
```
# On autorise le transit des packets en provenance de l'interface wg0 à destination de tout autre interface
PostUp = iptables -A FORWARD -i %i -j ACCEPT
# On autorise le transit des packets à destination de l'interface wg0 peu importe leur source
PostUp = iptables -A FORWARD -o %i -j ACCEPT
# Permet de faire passer les packets du VPN sur le réseau local (Ils sont transformé pour avoir l'ip du serveur en source sur l'interface de sortie)
PostUp = iptables -t nat -A POSTROUTING -o enp2s0f0 -j MASQUERADE

# On supprime les règles précédemment créées
PostDown = iptables -D FORWARD -i %i -j ACCEPT
PostDown = iptables -D FORWARD -o %i -j ACCEPT
PostDown = iptables -t nat -D POSTROUTING -o enp2s0f0 -j MASQUERADE
```

Pour le serveur public il faut utiliser les lignes suivantes:
```
# On refuse le transit des packets en provenance de l'interface wg0 à destination de tout autre interface
PostUp = iptables -A FORWARD -i %i -j DROP
# On refuse le transit des packets à destination de l'interface wg0 peu importe leur source
PostUp = iptables -A FORWARD -o %i -j DROP

# On supprime les règles précédemment créées
PostDown = iptables -D FORWARD -i %i -j DROP
PostDown = iptables -D FORWARD -o %i -j DROP
```

## Ajout de clients

Pour ajouter des utilisateurs (Générer des clés privées) il faut suivre [le guide correspondant](add_user_vpn.md) dans ce dépôt.

## Activation

Il faut ensuite allumer le serveur pour le tester:
```sh
$ sudo wg-quick up wg0
# Vérifier que tout marche bien avec
$ sudo wg show
```

Si tout est bon, on peu l'activer au démarrage de la machine:
```sh
$ sudo systemctl enable --now wg-quick@wg0
```

Il faut peut-être dans certains cas charger le module du kernel:
```sh
$ sudo modprobe wireguard
```

[Page précédente](setup_grafana.md) / [Page suivante](setup_firewall.md)