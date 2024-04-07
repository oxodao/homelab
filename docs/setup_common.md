# Setup des utilitaires communs

> Toute la config est gérée dans le ansible.
>
> Rien est à faire à la main.

# SSH

Avant toute chose, le playbook ansible se charge de:
- Tester si on peut accéder en SSH sur le port custom
- Si c'est le cas il continue le playbook
- Si ça n'est pas le cas il désactive l'authentification par mot de passe, change le port et relance le service

Cela est fait en modifiant le fichier `/etc/ssh/sshd_config`:
```
Port 57982
PasswordAuthentication no
```

Cela permet de ne pas laisser le serveur SSH sur le port par défaut afin de ne pas avoir de conflit avec Gitea.

Accessoirement, cela permet de diminuer la quantité de requêtes faites sur son serveur par les scanner d'internet (Dans le cas d'un homelab ça ne sert pas puisque non exposé sur internet).


## Setup des mises à jour automatiques

Je n'ai pas creusé le fonctionnement, j'utilise un [playbook existant](https://github.com/hifis-net/ansible-role-unattended-upgrades).

Il se base sur le projet [unattended-upgrades](https://launchpad.net/unattended-upgrades).

## Setup du NTP

Permet d'avoir une horloge à l'heure automatiquement, pareil qu'au dessus, cela se base sur le playbook [ntp de geerlingguy](https://github.com/geerlingguy/ansible-role-ntp) que je n'ai pas creusé.

## Installation des utilitaires usuels du système

Installation des outils utils en plus sur le système:
```sh
sudo apt install zip unzip fuse zsh rsync sqlite3 iptables vim git exa direnv
```

> Note: exa est utilisé à la place de eza car il n'est pas dans les repos debian
> Et que je l'ai toujours pas changé sur mon PC

## Activation de fuse
```sh
$ sudo modprobe fuse
$ echo fuse | sudo tee -a /etc/modules
```

## Installation de docker

Suivre le guide officiel sur le [site de docker](https://docs.docker.com/engine/install/debian/).

Ansible utilise le [role de guerlingguy](https://github.com/geerlingguy/ansible-role-docker)

Penser à ajouter l'utilisateur dans le groupe docker
```sh
$ sudo /usr/sbin/usermod -aG docker oxodao
```

## Configuration basique

Il s'agît la d'ajouter de la configuration pour les utilitaires installés dans l'étape 2. Principalement la configuration zsh ainsi que celle de vim.

Installation de `oh-my-zsh` depuis le script officiel:
```shell
$ sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

Clone de mes dotfiles:
```shell
$ rm -rf $HOME/.config # Attention ! S'assurer que c'est bien ce qu'on veut
$ rm $HOME/.zshrc
$ cd /opt
$ git clone https://github.com/oxodao/dotfiles
$ cd dotfiles
$ ln -s $PWD/config $HOME/.config
$ ln -s $PWD/zshrc $HOME/.zshrc
$ ln -s $PWD/gitconfig $HOME/.gitconfig
$ touch $HOME/.memo $HOME/.zshrc.custom
```

[Page précédente](setup_vm.md) / [Page suivante](setup_dns.md)