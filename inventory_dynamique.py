#!/usr/bin/env python3
import json
import docker

client = docker.from_env()

inventory = {"_meta": {"hostvars": {}}}

# On crée un groupe pour les conteneurs Docker
inventory["docker"] = {"hosts": [], "vars": {}}

for container in client.containers.list():
    ports = container.attrs['NetworkSettings']['Ports']
    ssh_port = None
    if '22/tcp' in ports and ports['22/tcp']:
        ssh_port = ports['22/tcp'][0]['HostPort']
    
    if ssh_port:
        name = container.name
        inventory["docker"]["hosts"].append(name)
        inventory["_meta"]["hostvars"][name] = {
            "ansible_host": "127.0.0.1",
            "ansible_port": int(ssh_port),
            "ansible_user": "ansible",
            "ansible_password": "ansible",
            "ansible_connection": "ssh",
            "ansible_ssh_common_args": "-o StrictHostKeyChecking=no"
        }

print(json.dumps(inventory, indent=2))
