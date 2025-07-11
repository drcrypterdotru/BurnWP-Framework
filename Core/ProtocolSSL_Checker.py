import socket
import urllib
from requests.exceptions import ConnectionError, Timeout, HTTPError, RequestException
from urllib.parse import urlparse
import requests
import importlib


NO_USED = None 

Core_Helper = importlib.import_module('Core.Core_Helper')
def Clean_Protocol(url: str) -> str:
    return url.strip().lower().replace("https://", "").replace("http://", "")
class Magic_ProtocolSSL:
    
    def __init__(self, host, timeout=30, Proxies=NO_USED, Config_AU=NO_USED):
        # if not host.startswith(('http://', 'https://')):
        #     host = 'http://' + host
        # self.parsed = urlparse(host)
        # self.domain = self.parsed.hostname   
        self.domain = Clean_Protocol(host)
        self.timeout = timeout
        self.UA_ = Config_AU
        self.Proxies_ON = Proxies
        self.RESP_INF = {}

    def Pro_Checker(self, port=443):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(self.timeout)
                result = sock.connect_ex((self.domain, port)) 
                return result == 0
        except Exception:
            return False
            
    def Domain_Requestor(self): 

        
        HTTP_V1 = f'http://{self.domain}'
        HTTPS_V2 = f'https://{self.domain}'

        #Step 1 requests if site https and requests useful can know website down or up if site down no need go to check port 443 its ready its down reduce our scan 
        try:
            
            response = requests.get(HTTPS_V2, 
                                    headers=self.UA_, 
                                    timeout=self.timeout, 
                                    allow_redirects=True, 
                                    verify=False,
                                    proxies=self.Proxies_ON)
            if response.status_code < 452:
                
                #print(f'[+] HTTPS : {HTTPS_V2}')
                self.RESP_INF = { 'protocol': HTTPS_V2, 
                                 'r_saved': response }
                return self.RESP_INF
                
        except Exception as e:
            self.RESP_INF = {'protocol': None, 'r_saved': None, 'err': str(e)} 
        # 2. Check Port 443
        # port_443_open = self.Pro_Checker(443)
        # if port_443_open:
        #     #print(f'[+] 443 == HTTPS : {HTTPS_V2}')
        #     self.RESP_INF = {'protocol': HTTPS_V2,
        #                     'r_saved': response}
        #     return self.RESP_INF

        try:
            response = requests.get(
                HTTP_V1,
                headers=self.UA_,
                timeout=self.timeout,
                allow_redirects=True,
                proxies=self.Proxies_ON, 
                verify=False
                
            )
            if response.status_code < 452:
                
                self.RESP_INF = {'protocol': HTTP_V1, 
                                 'r_saved': response}
                return self.RESP_INF
        except Exception as er: 

            self.RESP_INF = {'protocol': None,
                            'r_saved': None,
                            'err': str(er),
                            }
            return self.RESP_INF
            
        