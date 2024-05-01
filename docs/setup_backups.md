# Backups

Pour faire les backups, on va utiliser autorestic.

Restaurer une app nécessite de restaurer le tag standard ET le tag `_data` datant du MÊME BACKUP.

Tags:
- gitea: /home/oxodao/gitea
- gitea_data: smb://NAS/Git