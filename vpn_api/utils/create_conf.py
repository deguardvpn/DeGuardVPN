import base64
import os
import subprocess

import requests

from config import *

path_to_wg = '/config'


def get_serv_conf():
    try:
        with open(f"{path_to_wg}/wg_confs/wg0.conf", 'r') as f:
            serv_conf = f.read()

        return serv_conf
    except Exception as e:
        raise e


def find_configs(serv_conf):
    return serv_conf.count('#NP')


def generate_wireguard_keys():
    private_key = subprocess.check_output(
        "wg genkey", shell=True).decode("utf-8").strip()
    pubkey_key = subprocess.check_output(
        f"echo '{private_key}' | wg pubkey", shell=True).decode("utf-8").strip()
    return private_key, pubkey_key


def increment_act(ip):

    if int(ip[2]) == 0 and int(ip[3]) < 252:
        ip[3] = str(int(ip[-1]) + 1)
        return '.'.join(ip)
    elif int(ip[2]) == 0 and int(ip[3]) >= 252:
        return '10.0.1.0'

    if int(ip[2]) == 1 and int(ip[3]) <= 252:
        ip[3] = str(int(ip[-1]) + 1)
        return '.'.join(ip)
    elif int(ip[2]) == 1 and int(ip[3]) >= 252:
        return '10.0.2.0'

    if int(ip[2]) == 2 and int(ip[3]) <= 252:
        ip[3] = str(int(ip[-1]) + 1)
        return '.'.join(ip)
    elif int(ip[2]) == 2 and int(ip[3]) >= 252:
        return '10.0.3.0'

    if int(ip[2]) == 3 and int(ip[3]) <= 252:
        ip[3] = str(int(ip[-1]) + 1)
        return '.'.join(ip)
    elif int(ip[2]) == 3 and int(ip[3]) >= 252:
        return '10.0.4.0'

    if int(ip[2]) == 4 and int(ip[3]) <= 252:
        ip[3] = str(int(ip[-1]) + 1)
        return '.'.join(ip)
    elif int(ip[2]) == 4 and int(ip[3]) >= 252:
        return '10.0.5.0'

    if int(ip[2]) == 5 and int(ip[3]) <= 252:
        ip[3] = str(int(ip[-1]) + 1)
        return '.'.join(ip)


def main(user_id: str):
    client_priv_key, client_pub_key = generate_wireguard_keys()
    serv_conf = get_serv_conf()

    with open(f"{path_to_wg}/.donoteditthisfile", 'r') as f:
        server_ip = f.read()

    server_ip = server_ip.split('\n')[0].split('"')[1]

    if find_configs(serv_conf) == 0:
        allow_ip = '10.0.0.2'
    else:
        last_ip = serv_conf.split('\n')[-4].split()[-1].split('.')
        print(last_ip)

        last_ip[-1] = last_ip[-1].split('/')[0]
        print(last_ip)

        allow_ip = increment_act(last_ip)
        

    with open(f'{path_to_wg}/server/publickey-server', 'r') as f:
        server_pub_key = f.read()

    urs_peer = (f"""
#NP {user_id}
[Peer]
PublicKey = {client_pub_key}
AllowedIPs = {allow_ip}/32
# {user_id}

""")

    with open(f"{path_to_wg}/wg_confs/wg0.conf", "a") as f:
        f.write(urs_peer)

    user_config = f"""[Interface]
PrivateKey = {client_priv_key}
Address = {allow_ip}/32
DNS = 8.8.8.8

[Peer]
PublicKey = {server_pub_key.strip()}
Endpoint = {server_ip}:{WG_PORT}
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 20
"""


    r = requests.get("http://192.168.240.2:8001/api/sync_configs")

    return base64.b64encode(user_config.encode('ascii')).decode('ascii')
