#!/usr/bin/env python3

import json
import re

DEFAULT_SOCKS_PORT = 10808


def read_env_file(filename):
    """Read the .env file and return its content."""
    with open(filename, 'r') as file:
        return file.read()

def extract_values(env_content):
    """Extract PROXY_LINK and WG_PORT from the .env content."""
    proxy_link_match = re.search(r'PROXY_LINK=(vless://[^\n]+)', env_content)
    wg_port_match = re.search(r'WG_PORT=(\d+)', env_content)
    socks_port_match = re.search(r'SOCKS_PORT=(\d+)', env_content)

    if not proxy_link_match:
        raise ValueError("PROXY_LINK not found")
    if not wg_port_match:
        raise ValueError("WG_PORT not found")
    return proxy_link_match.group(1), int(wg_port_match.group(1)), int(socks_port_match.group(1)) or DEFAULT_SOCKS_PORT

def parse_proxy_link(proxy_link):
    """Parse the PROXY_LINK to extract details."""
    proxy_pattern = re.compile(
        r'vless://(?P<client_uuid>[^@]+)@(?P<host_server>[^:]+):(?P<host_port>\d+).*pbk=(?P<public_key>[^&]+).*sni=(?P<sni_server>[^&]+)'
    )
    proxy_match = proxy_pattern.search(proxy_link)

    if not proxy_match:
        raise ValueError("PROXY_LINK is not in the expected format")

    return {
        "client_uuid": proxy_match.group('client_uuid'),
        "host_server": proxy_match.group('host_server'),
        "host_port": int(proxy_match.group('host_port')),
        "public_key": proxy_match.group('public_key'),
        "sni_server": proxy_match.group('sni_server')
    }

def generate_config(proxy_details, wg_port, socks_port):
    """Generate the configuration dictionary."""
    return {
        "log": {
            "loglevel": "debug"
        },
        "inbounds": [
            {
                "listen": "127.0.0.1",
                "port": socks_port,
                "protocol": "socks",
                "settings": {
                    "udp": True
                },
                "sniffing": {
                    "enabled": True,
                    "destOverride": [
                        "http",
                        "tls",
                        "quic"
                    ],
                    "routeOnly": True
                }
            },
            {
                "listen": "127.0.0.1",
                "tag": "wireguard",
                "port": wg_port,
                "protocol": "dokodemo-door",
                "settings": {
                    "address": proxy_details["host_server"],
                    "port": wg_port,
                    "network": "udp"
                }
            }
        ],
        "outbounds": [
            {
                "protocol": "vless",
                "settings": {
                    "vnext": [
                        {
                            "address": proxy_details["host_server"],
                            "port": proxy_details["host_port"],
                            "users": [
                                {
                                    "id": proxy_details["client_uuid"],
                                    "encryption": "none",
                                    "flow": "xtls-rprx-vision"
                                }
                            ]
                        }
                    ]
                },
                "streamSettings": {
                    "network": "tcp",
                    "security": "reality",
                    "realitySettings": {
                        "fingerprint": "chrome",
                        "serverName": proxy_details["sni_server"],
                        "publicKey": proxy_details["public_key"],
                        "spiderX": "",
                        "shortId": ""
                    }
                },
                "tag": "proxy"
            }
        ]
    }

def write_config_to_file(config, filename):
    """Write the configuration dictionary to a JSON file."""
    with open(filename, 'w') as json_file:
        json.dump(config, json_file, indent=4)

def main():
    env_content = read_env_file('.env')
    proxy_link, wg_port, socks_port = extract_values(env_content)
    proxy_details = parse_proxy_link(proxy_link)
    config = generate_config(proxy_details, wg_port, socks_port)
    write_config_to_file(config, 'config_client.json')
    print("config_client.json has been generated.")

if __name__ == "__main__":
    main()
