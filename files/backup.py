#!/usr/bin/python3

import json
import requests
import os
from email.mime.text import MIMEText
import subprocess


if not os.path.exists('/etc/backups.json'):
    print('Failed to locate backup config (/etc/backups.json)')
    exit(1)

config = {}

with open('/etc/backups.json', 'r') as f:
    config = json.load(f)

DRY = config.get('dry_run', False)

LOG_TYPE = config.get('notification', {}).get('type', '').lower()
SERVER_CFG = config.get('server', {})

os.environ['AWS_ACCESS_KEY_ID'] = SERVER_CFG.get('access_key_id')
os.environ['AWS_SECRET_ACCESS_KEY'] = SERVER_CFG.get('access_key_secret')
os.environ['RESTIC_REPOSITORY'] = SERVER_CFG.get('endpoint')
os.environ['RESTIC_PASSWORD'] = SERVER_CFG.get('restic_password')

IS_LOG_DEFFERED = True if LOG_TYPE in ['email',] else False
DEFFERED_LOGS = []

def log(msg):
    print(msg)

    if LOG_TYPE == 'discord':
        requests.post(
            config.get('notification', {}).get('endpoint'),
            json={
                'username': config.get('notification', {}).get('username', 'Backup bot'),
                'content': msg,
            },
        )
    elif LOG_TYPE == 'email':
        DEFFERED_LOGS.append(msg)

def run(cmd):
    if DRY:
        log(f'>>> {cmd}')
        return 0

    return os.system("bash -c \"" + cmd + "\"")

def backup_folder(folder):
    if DRY:
        print(f'Backing up folder {folder["path"]} excluding {folder["exclude"]}')
        return

    if not folder.get('tag') and not folder.get('name'):
        log('NO TAG OR NAME FOR ' + folder['path'] + '. SKIPPING !')
        return

    tag = folder.get('tag', folder.get('name')).lower()

    exclusions = (' ' if len(folder.get('exclude', [])) > 0 else '') + ' '.join(['--exclude ' + os.path.join(folder.get('path') + excl) for excl in folder.get('exclude', [])])

    result = subprocess.run(['bash', '-c', f'restic --verbose backup --tag {tag}{exclusions} {folder.get("path")}'], capture_output=True, text=True)
    if result.returncode != 0:
        log(f'Failed to backup {tag}')
        log("STDOUT: \n" + (result.stdout if result.stdout else '-'))
        log("STDERR: \n" + (result.stderr if result.stderr else '-'))
        return

    log(f'- {tag} backed up')


log('Starting backup process' + ('' if not DRY else ' (DRY)'))

for folder in config.get('folders', []):
    try:
        is_docker = folder.get('is_docker_app', False)

        log('- Starting the backup of ' + folder.get('name', folder.get('path')))

        if is_docker:
            if DRY:
                print('Stopping docker container')
            else:
                status = run(f'cd {folder["path"]} && docker compose down')
                if status != 0:
                    log(f'Error while stopping {folder["path"]}. Skipping...')
                    continue

        backup_folder(folder)

        if is_docker:
            if DRY:
                print('Restarting docker container')
            else:
                status = run(f'cd {folder["path"]} && docker compose up -d')
                if status != 0:
                    log(f'Error while restarting {folder["path"]}. Skipping...')
                    continue
    except Exception as e:
        log(f'Something went really wrong: {str(e)}')

log('Backup process completed')


if IS_LOG_DEFFERED:
    if LOG_TYPE == 'email':
        email_from = config.get('notification', {}).get('from', '')
        email_to = config.get('notification', {}).get('to', '')

        if len(email_from) == 0 or len(email_to) == 0:
            print('Failed to send notification email: No from/to address')

        msg = "Backup report\n\n"
        for txt in DEFFERED_LOGS:
            msg += txt + "\n"

        msg = MIMEText("Here is the body of my message")
        msg["From"] = email_from
        msg["To"] = email_to
        msg["Subject"] = "Backup log report"
        p = subprocess.Popen(["/usr/sbin/sendmail", "-t", "-oi"], stdin=subprocess.PIPE)

        p.communicate(msg.as_bytes())