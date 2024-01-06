[x] Basic setup
[ ] ZFS import pools
[x] Setup dns server
[x] Install docker
[ ] Setup docker composes
    [x] Gitea
    [x] Jellyfin
    [ ] Home Assistant
    [x] Paperless
    [x] JDownloader
    [ ] Immich (?)
[x] Setup nginx
[x] Setup SMB server # More or less, still have to debug permissions and autosetup the default shares
[x] Setup wireguard server
[x] Setup internal email server (mailgun, to send monitoring emails, via msmtp ou dma)
[x] Setup hard drive monitoring
[ ] Setup app monitoring (Maybe? Really useful?)
[ ] Setup restic backups (Better setup than what I have currently)
[ ] Make a "Disaster recovery" guide in the readme AND TEST IT !!

@TODO:
Debug smb => Pas les permissions pour mettre des trucs dans le share depuis un windows => Pas les permissions sur le dossier monté, chmod 755 ?
Setup iptables with simple rules in ansible yaml
