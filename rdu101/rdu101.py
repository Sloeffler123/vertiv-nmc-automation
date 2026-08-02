import requests
from networkmangementcards.nmc_device import NMCDevice

def rdu101_get_token(client_username, client_password, dhcp_ip_address, http_protocol):
    url = f"{http_protocol}://{dhcp_ip_address}/api/auth/{client_username}"
    commands = {
        "cmd": "login",
        "data": {
            "password": client_password
        },
    }
    req = requests.post(url, json=commands, verify=False).json()
    token = req["data"]["token"]
    return token

class RDU101(NMCDevice):
    def __init__(self, **kwargs):
       super().__init__(**kwargs)
       self.token = rdu101_get_token(
           self.client_username, 
           self.client_password, 
           self.dhcp_address, 
           self.http_protocol
           ) 
    
    def add_user(self):
        url = f"{self.http_protocol}://{self.dhcp_ip_address}/api/auth"
        commands = {
            "token": self.token,
            "cmd": "add",
            "data": {
                "username": "new_user",
                "password": self.new_password,
                "language": "en",
                "enabled": True,
                "control": True,
                "admin": True
            }
        }
        resp = requests.post(url, json=commands, verify=False).json()
        print(resp)
    
    def set_nmc_name(self):
        url = f"{self.http_protocol}://{self.dhcp_ip_address}/api/conf/system"
        data = {
            "token": self.token,
            "cmd": "set",
            "data": {
                "label": self.system_name
            }
        }
        resp = requests.post(url, json=data, verify=False).json()
        print(resp)

    def set_contact_info(self):
        url = f"{self.http_protocol}://{self.dhcp_ip_address}/api/conf/contact"
        data = {
            "token": self.token,
            "cmd": "set",
            "data": {
                "location": "IT room",
                "description": "UPS for networking equipment",
                "contactInfo": "contact"
            }
        }
        resp = requests.post(url, json=data, verify=False).json()
        print(resp)

    def set_ntp(self):
        url = f"{self.http_protocol}://{self.dhcp_ip_address}/api/conf/time"
        data = {
            "token": self.token,
            "cmd": "set",
            "data": {
                "mode": "ntp",
                "zone": "(UTC-06:00) Central Time (US and Canada)",
                "ntpServer1": "ntp.pool.org"
            }
        }
        resp = requests.post(url, json=data, verify=False).json()
        print(resp)

    def set_networking(self):
        url_ethernet = f"{self.http_protocol}://{self.dhcp_ip_address}/api/conf/network/ethernet"
        data = {
            "token": self.token,
            "cmd": "set",
            "data": {
                "dhcpOn": False,
                "address": {
                    "0": {
                        "prefix": self.prefix,
                        "address": self.ip_address
                    }
                }
            }
        }
        resp = requests.post(url_ethernet, json=data, verify=False).json()
        print(resp)

    def set_dns(self):
        url_ethernet = f"{self.http_protocol}://{self.dhcp_ip_address}/api/conf/network/ethernet/dns"
        data = {
            "token": self.token,
            "cmd": "add",
            "data": {
                "address": "8.8.8.8"
            }
        }
        resp = requests.post(url_ethernet, json=data, verify=False).json()
        print(resp)

    def set_route(self):
        url_ethernet = f"{self.http_protocol}://{self.dhcp_ip_address}/api/conf/network/ethernet/route"
        data = {
            "token": self.token,
            "cmd": "set",
            "data": {
                "0": {
                    "gateway": self.default_gateway
                }
            }
        }
        resp = requests.post(url_ethernet, json=data, verify=False).json()
        print(resp)
