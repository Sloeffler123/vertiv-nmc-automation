import requests

def get_act_token(username, password, dhcp_ip_address, http_protocol):
    session = requests.Session()

    resp = session.get(
        f"{http_protocol}://{dhcp_ip_address}/session/unityLogin.htm",
        auth=(username, password),
        verify=False
    )
    sess_token = resp.text.split(";")[0][8:]
    return sess_token, session

class SessionToken:
    def __init__(
                self,
                nmc_device,
                site_id, 
                email_from, 
                email_custom_text, 
                ):
        self.sess_token, self.session = get_act_token(
            username=nmc_device.client_username, 
            password=nmc_device.client_password, 
            dhcp_ip_address=nmc_device.dhcp_address, 
            http_protocol=nmc_device.http_protocol
            )
        self.site_id = site_id
        self.email_from = email_from
        self.email_custom_text = email_custom_text
        self.nmc_device = nmc_device

    def get_serial_and_model(self):
        resp = self.session.get(
                f"{self.nmc_device.http_protocol}://{self.nmc_device.dhcp_address}/httpGetSet/httpGet.htm?devId=0&val4123_0\
                =vel~pnt~4123~0~0&val4333_0=vel~pnt~4333~0~0&val4240_0=vel~pnt~4240~0~0&val4335_0\
                =vel~pnt~4335~0~0&val4244_0=vel~pnt~4244~0~0&val4291_0=vel~pnt~4291~0~0&val6003_0\
                =vel~pnt~6003~0~0&val6199_0=vel~pnt~6199~0~0&val4168=vel~pnt~4168~0&val4122\
                =vel~pnt~4122~0&val4310=vel~pnt~4310~0&val6186=vel~pnt~6186~0&val6187\
                =vel~pnt~6187~0&val5588=vel~pnt~5588~0&val4823=vel~pnt~4823~0&val6254=vel~pnt~6254~0&val4295\
                =vel~pnt~4295~0&val4233=vel~pnt~4233~0&val4311=vel~pnt~4311~0&val4229\
                =vel~pnt~4229~0&val6453=vel~pnt~6453~0&val6454=vel~pnt~6454~0&enum5831\
                ={0}vel~pnt~5831~0&num4710=vel~pnt~4710~0~0&str4247=vel~pnt~4247~0&str4248\
                =vel~pnt~4248~0&str4329=vel~pnt~4329~0&enum6188={0}vel~pnt~6188~0&enum6720\
                ={0}vel~pnt~6720~0&num6721=vel~pnt~6721~0~0&enum6722={0}vel~pnt~6722~0&num6723\
                =vel~pnt~6723~0~0&enum6724={0}vel~pnt~6724~0&enum6725={0}vel~pnt~6725~0&enum6726\
                ={0}vel~pnt~6726~0&enum6727={0}vel~pnt~6727~0&sessACT={self.sess_token}",
                verify=False
        )
        system_info = resp.text.split(";")
        system_data = {}
        for item in system_info:
            val = item.split('=')
            system_data[val[0]] = val[1]
        model = system_data.get('val4240_0')
        serial = system_data.get('val4244_0')
        ups_name = system_data.get('str4247_0')
        site_identifier = system_data.get('str4329_0')
        return model, serial, ups_name, site_identifier

    def set_name_and_site_identifier(self):
        
        resp = self.session.post(
            f"{self.nmc_device.http_protocol}://{self.nmc_device.dhcp_address}/protected/httpSet.htm",
            data={
                "devId": "0",
                "begin": "http~set~begin",
                "str4247": f"vel~pnt~4247~0|val~str~{self.site_id}",
                "str4329": f"vel~pnt~4329~0|val~str~{self.nmc_device.ups_name}",
                "end": "http~set~end",
                "sessACT": self.sess_token,
            },
            verify=False
        )

    def set_email(self):
        resp = self.session.post(
            f"{self.nmc_device.http_protocol}://{self.nmc_device.dhcp_address}/protected/httpSet.htm",
            data={
                "devId": "4",
                "begin": "http~set~begin",
                "chkbx7312": "{0}vel~pnt~7312~0|val~num~1",
                "str7314": f"vel~pnt~7314~0|val~str~{self.email_from}",
                "str7315": "vel~pnt~7315~0|val~str~to_address",
                "enum7316": "{0}vel~pnt~7316~0|val~num~1",
                "st7317": f"vel~pnt~7317~0|val~str~{self.email_custom_text}",
                "str7318": "vel~pnt~7318~0|val~str~smtp_server.com", 
                "num7319": "vel~pnt~7319~0~0|val~num~25",
                "end": "http~set~end",
                "sessACT": self.sess_token,
            },
            verify=False
        )