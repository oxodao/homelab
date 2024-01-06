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
[x] Auto-setup samba
[ ] Setup firewall correctly - Nothing at all should be accessible except:
    - 80/443 (Web stuff)
    - 22 (Git SSH port)
    - 5792 (Main SSH port)
    - 25565-25665 (Minecraft servers, just in case, large range just to be safe if I want multiple ones running at the same time)


Wireguard should have 3 VPNs on 3 distinct ports with different credentials for each:
- Full LAN access + DNS
- Full LAN access + DNS + internet forwarding
- Jellyfin only (For family)