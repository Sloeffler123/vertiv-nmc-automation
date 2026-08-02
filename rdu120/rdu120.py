import requests
from Network_management_cards.nmc_device import NMCDevice

def rdu120_get_token(client_username, client_password, dhcp_address, http_protocol):
    url = f"{http_protocol}://{dhcp_address}/api/auth/user/{client_username}"
    commands = {
        "cmd": "login",
        "username": client_username,
        "password": client_password
    }
    req = requests.post(url, json=commands, verify=False).json()
    print(req)
    token = req["data"]["token"]
    return token

class RDU120(NMCDevice):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.token = rdu120_get_token(
            self.client_username, 
            self.client_password, 
            self.dhcp_address, 
            self.http_protocol
            ) 

    def add_user(self):
        url = f"{self.http_protocol}://{self.dhcp_address}/api/auth/user"
        data = {
        "token": self.token,
        "cmd": "add",
        "data": {
            "id": "new_user",
            "password": self.new_password,
            "scope": None,
            "enabled": True,
            "language": "en",
            "publicKey": [],
            "privilege": "administrator"
                }
            }
        resp = requests.post(url=url, json=data, verify=False).json()
        print(resp)

    def send_email_test(self):
        url = f"{self.http_protocol}://{self.dhcp_address}/api/conf/email/target/1"
        data = {
            "cmd": "sendTest",
            "token": self.token
        }
        resp = requests.post(url=url, json=data, verify=False).json()
    
    def set_up_email(self):
        url = f"{self.http_protocol}://{self.dhcp_address}/api/conf/email"
        data = {
            "token": self.token,
            "cmd": "set",
            "data": {
                "server": "smtp_server",
                "port": 25,
                "sender": f"{self.ups_name}@alerts.com",
                "subjectPrefix": self.ups_name
            }
        }
        url_2 = f"{self.http_protocol}://{self.dhcp_address}/api/conf/email/target"
        data_2 = {
            "token": self.token,
            "cmd": "add",
            "data": {
                "id": "0",
                "name": "sender_address"
            }
        }

        resp = requests.post(url=url, json=data, verify=False).json()
        resp_2 = requests.post(url=url_2, json=data_2, verify=False).json()
        print(resp)
        print(resp_2)

    def set_network(self):
        url_dns = f"{self.http_protocol}://{self.dhcp_address}/api/conf/network/dns"
        data_dns = {
            "token": self.token,
            "cmd": "add",
            "data": {
                "address": "8.8.8.8"
            }
        }
        url_route = f"{self.http_protocol}://{self.dhcp_address}/api/conf/network/route"
        data_route = {
            "token": self.token,
            "cmd": "add",
            "destination": "0.0.0.0",
            "prefix": 0,
            "gateway": self.route,
            "interface": "all"
        }
        url_ip_address = f"{self.http_protocol}://{self.dhcp_address}/api/conf/network/interface/lan/address"
        data_lan = {
            "token": self.token,
            "cmd": "add",
            "mutable": False,
            "prefix": self.prefix,
            "address": self.ip_address
        }
        url_dhcp_false = f"{self.http_protocol}://{self.dhcp_address}/api/conf/network/interface/lan"
        data_dhcp_false = {
            "token": self.token,
            "cmd": "set",
            "data": {
                "dhcpEnabled":False,
            }
        }
        url_set_static = f"{self.http_protocol}://{self.dhcp_address}/api/conf/network"
        data_static = {
            "token": self.token,
            "cmd": "set",
            "data": {
                "ipV4BootMode": "STATIC"
            }
        }
        resp_set_static = requests.post (url=url_set_static, json=data_static, verify=False).json()
        resp_dhcp_false = requests.post (url=url_dhcp_false, json=data_dhcp_false, verify=False).json()
        resp_dns = requests.post(url=url_dns, json=data_dns, verify=False).json()
        resp_route = requests.post(url=url_route, json=data_route, verify=False).json()
        resp_lan = requests.post(url=url_ip_address, json=data_lan, verify=False).json()

        print(f"DNS = {resp_dns}\n", f"Route =  {resp_route}\n" f"IP = {resp_lan}\n")

    def set_system_info(self):
        url = f"{self.http_protocol}://{self.dhcp_address}/api/conf/system"
        data = {
            "token": self.token,
            "cmd": "set",
            "data": {
                "contact": "contact",
                "description": "UPS for networking equipment",
                "label": self.ups_name,
                "location": "IT room"
            }
        }
        resp = requests.post(url=url, json=data, verify=False).json()
        print(resp)

    def set_time(self):
        url = f"{self.http_protocol}://{self.dhcp_address}/api/conf/time"
        data = {
            "token": self.token,
            "cmd": "set",
            "data": {
                "mode": "automatic",
                "zone": "America/Chicago",
                "ntpServer1": "pool.ntp.org",
                "ntpServer2": ""
            }
        }
        resp = requests.post(url=url, json=data, verify=False).json()
        print(resp)