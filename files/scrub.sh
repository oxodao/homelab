#!/bin/sh -eu

# Stolen from https://svennd.be/setting-up-zpool-scrub-every-2-months/

# you can stop/pause a scrub
# using : zpool -p poolname

# report
logger "zfs" "cron scrub initiated"

# Scrub all healthy pools.
zpool list -H -o health,name 2>&1 | \
        awk 'BEGIN {FS="\t"} {if ($1 ~ /^ONLINE/) print $2}' | \
while read pool
do
        zpool scrub "$pool"
done