class NMCDevice:
    def __init__(self, dhcp_address, http_protocol, client_username, client_password, new_password, ups_name, route, prefix, ip_address):
        self.dhcp_address = dhcp_address
        self.http_protocol = http_protocol
        self.client_username = client_username
        self.client_password = client_password
        self.new_password = new_password
        self.ups_name = ups_name
        self.route = route
        self.prefix = prefix
        self.ip_address = ip_address