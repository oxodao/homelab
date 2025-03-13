##### Config
DNS_SERVER_IP = '1' # The IP on the WG network of the DNS server
# DNS_SERVER_IP = None
##############

from pathlib import Path

try:
    import yaml
except ImportError:
    print('This script requires the pyyaml package')
    print('In a venv you can install it with `pip install pyyaml`')
    print("It is also available in debian's standard repo under the name python3-yaml")
    exit(1)

try:
    from jinja2 import Template, Environment
except ImportError:
    print('This script requires the jinja2 package')
    print('In a venv you can install it with `pip install jinja2`')
    exit(1)

TEMPLATE = Template("""# Wireguard config for {{ machine.hostname }}
[Interface]
PrivateKey = {{ machine.private_key }}
# PublicKey = {{ machine.public_key }}
Address = {{ server.ip_prefix }}{{ machine.ip }}/24
{% if dns_server is not none %}DNS = {{ server.ip_prefix }}{{ dns_server }}
{% endif %}
[Peer]
PublicKey = {{ server.public_key }}
AllowedIPs = {{ server.allowed_ips }}
Endpoint = {{ server.public_ip }}:{{ server.port }}
""")

inventory = Path('./inventory.yaml')

if not inventory.exists():
    print('The inventory.yaml file does not exist!')
    exit(1)

inventory = yaml.safe_load(inventory.read_text(encoding='utf-8'))

basepath = Path('./00_WIREGUARD_CLIENTS')
basepath.mkdir(parents=True, exist_ok=True)

for group_name, group in inventory.items():
    group_path = basepath.joinpath(group_name)
    group_path.mkdir(parents=True, exist_ok=True)

    for hostname, host in group['hosts'].items():
        if 'wireguard' not in host:
            print(f'No wireguard config for host {hostname}')
            continue

        wg = host['wireguard']

        if 'machines' not in wg:
            print(f'No machines in wireguard config for {hostname}')
            continue

        for machine in wg['machines']:
            out_file = group_path.joinpath(machine['hostname'] + '.conf')

            config = TEMPLATE.render(
                server=wg,
                machine=machine,
                dns_server=DNS_SERVER_IP,
            )

            out_file.write_text(config, 'utf-8')