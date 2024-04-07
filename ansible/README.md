# Homelab ansible

Pour utiliser cet ansible, il faut copier-coller le `inventory.yaml.dist` en `inventory.yaml` et le compléter en suivant les commentaires.

Installation des roles:
```sh
$ ansible-galaxy install -r requirements.yaml --force
$ ansible-galaxy collection install -r requirements.yaml --force
```

Exécution du playbook:
```sh
$ export ANSIBLE_BECOME_PASSWORD="MON MOT DE PASSE SUDO" # A exécuter une seule fois
$ ansible-playbook -i inventory.yaml setup.yaml
```

Si on souhaite exécuter seulement certaines parties, on peut limiter avec les tags, ou les hosts:
```sh
$ export ANSIBLE_BECOME_PASSWORD="MON MOT DE PASSE SUDO" # A exécuter une seule fois
$ ansible-playbook -i inventory.yaml setup.yaml --limit public -t dns
```

Pour une réinstallation future, chiffrer le `inventory.yaml` et le stocker dans un endroit sécurisé. Il suffira alors de le reprendre et modifier en cas de mise à jour sur la version git.

Pour cela, on peut utiliser `ansible-vault` pour utiliser un utilitaire tout-en-un:
```sh
$ ansible-vault encrypt --vault-id homelab@prompt inventory.yaml # Chiffrer
$ ansible-vault decrypt inventory.yaml # Déchiffrer
```