from dataclasses import dataclass

@dataclass
class UserInfo:
    dhcp_address: str
    client_username: str
    client_password: str
    ip_address: str
    prefix: str
    route: str
    new_password: str
    ups_name: str
    site_id: str 
    email_from_address: str 
    custom_email_subject: str
    http_protocol: str

def user_input():
    system_name = input("Enter system name ").strip()
    return UserInfo(
        dhcp_address = input("Enter current ip of UPS ").strip(),
        client_username = input("Enter client username ").strip(),
        client_password = input("Enter client password ").strip(),
        ip_address = input("Enter ip address ").strip(),
        prefix = int(input("Enter subnet mask prefix ")),
        route = input("Enter gateway ").strip(),
        new_password = input("Enter BIT password ").strip(),
        site_id = input("Enter site id ").strip(),
        email_from_address = f"{system_name}@alerts.bridgeheadit.com",
        custom_email_subject = f"{system_name}",
        ups_name = system_name,
        http_protocol = input("Enter current http protocol used in the ip ").strip()
    )