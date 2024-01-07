# Oh no. Shit happened

## How to recover

In order to recover from backup, first shut down the impacted app (`docker compose down` for docker apps).

Then look at your available backups:
```
$ AWS_ACCESS_KEY_ID=xxxxx AWS_SECRET_ACCESS_KEY=xxxxx restic -r s3:https://s3.eu-central-003.backblazeb2.com/xxxxxBUCKETxxxxx snapshots
```

You can filter on tags with `--tag jellyfin`, tags are either in the `tag` key or the lower cased version of the `name` key in the `backups.json`. Note that if you have a specific file to get you can `restic find file.txt`.

You want to restore both the container (the `docker-compose.yaml` + settings it has) and the app files (when it have some, e.g. Paperless or Immich) to the latest working version (Both from the same backup!).

Now you found the ID for the backup you want to restore, simply use the following command:
```
$ AWS_ACCESS_KEY_ID=xxxxx AWS_SECRET_ACCESS_KEY=xxxxx restic -r s3:https://s3.eu-central-003.backblazeb2.com/xxxxxBUCKETxxxxx restore xxxxBACKUP_IDxxxx
```

You can also us the `--target /some/path` to restore to a specific path if you want to do stuff with the files first.

Once the restoration is successful, you can restart the docker containers and you're good to go!