import urllib3
from networkmangementcards.nmc_device import RDU101
from networkmangementcards.nmc_user_input import user_input
from networkmangementcards.session_token import SessionToken

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def main():
    data = user_input()
    nmc_device = RDU101(
        dhcp_address = data.dhcp_address, 
        http_protocol = data.http_protocol, 
        client_username = data.client_username, 
        client_password = data.client_password, 
        new_password = data.new_password, 
        ups_name = data.ups_name, 
        route = data.route, 
        prefix = data.prefix, 
        ip_address = data.ip_address
        )
    session_token = SessionToken(
        nmc_device=nmc_device,
        site_id=data.site_id, 
        email_from=data.email_from_address, 
        email_custom_text=data.custom_email_subject
        )
    session_token.set_name_and_site_identifier()
    session_token.set_email()
    nmc_device.set_contact_info()
    nmc_device.set_nmc_name()
    nmc_device.set_contact_info()
    nmc_device.set_ntp()
    nmc_device.set_networking()
    nmc_device.set_dns()
    nmc_device.set_route()
    nmc_device.add_user()
main()