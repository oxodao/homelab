# Ajouter des utilisateurs sur les VPNs

La procédure est la même pour les deux VPNs.

Il faut tout d'abord leur générer une clé privée et une clé publique:
```sh
$ wg genkey | tee private.key | wg pubkey > public.key
$ cat private.key public.key
```

On défini ensuite une IP sur laquelle il sera assigné, e.g. `192.168.66.123`.

Puis on l'ajoute au fichier `/etc/wireguard/wg0.conf`:
```
[...]

[Peer] # Nom pour savoir qui c'est
PublicKey = <Contenu du fichier public.key>
AllowedIPs = 192.168.66.123/32
```

On relance le serveur:
```sh
$ sudo systemctl restart wg-quick@wg0
```

Il suffit ensuite de lui créer un fichier d'authentification:
```
[Interface]
Address = 192.168.66.123/24
PrivateKey = <Contenu du fichier private.key>
DNS = 192.168.66.1

[Peer]
PublicKey = <Clé publique du serveur>
AllowedIPs = 192.168.66.0/24,192.168.14.0/24
Endpoint = <IP PUBLIC DE LA BOX:PORT WIREGUARD>
PersistentKeepalive = 25
```

Le `AllowedIPs` de `Peer` permet au client wireguard de savoir ce qu'il doit router vers le VPN.

Sur `rubeus-local` on peut laisser cette config car il a accès à tout le réseau local et aux autres clients du VPN.

Sur `rubeus-public` on doit lui dire qu'il n'a accès qu'au serveur: `192.168.70.1/32`.

On copie ce fichier sur le PC / Téléphone choisi puis on l'importe dans le client wireguard.

On vérifie que ça marche.

[Page précédente](setup_backups.md) / [Page suivante](renew_ssl.md)