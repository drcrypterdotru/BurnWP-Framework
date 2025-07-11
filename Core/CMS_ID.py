import importlib
NO_USED = None
FUC_SAVE = importlib.import_module('main')
SmokeCore = importlib.import_module('Core.Core_Helper')  
ProtocolSSL = importlib.import_module('Core.ProtocolSSL_Checker')


class DetectCMS_Class:
    def __init__(self, CFG_DOMAIN, CFG_TIMEOUT, CFG_USERAGENT, CFG_DELAY_ATTACK, SET_REDIRECT, CFG_Proxy, MULTI_CMS, User_Agent):
        self.CFG_Target = CFG_DOMAIN
        self.CFG_timeout = CFG_TIMEOUT
        self.CFG_Useragent = CFG_USERAGENT
        self.CFG_Delay = CFG_DELAY_ATTACK 
        self.Set_Redirect = SET_REDIRECT
        self.Proxies_ON = CFG_Proxy
        self.MULTI_CMS = MULTI_CMS
        self.Config_UA = {'User-Agent': User_Agent}
        #print(self.Config_UA)
    def Clean_Protocol(self, url: str) -> str:
        return url.strip().lower().replace("https://", "").replace("http://", "")
    
    def CMS_Run(self):
        try:
            WPNonce_code = None
            self.CFG_Target = self.Clean_Protocol(self.CFG_Target)
            
            HTTP_ = 'http://' + self.CFG_Target
            
            Protocol_Check = ProtocolSSL.Magic_ProtocolSSL(self.CFG_Target, 8, self.Proxies_ON, self.Config_UA)
            RES_PROT = Protocol_Check.Domain_Requestor()
            if not RES_PROT['protocol']:
                SmokeCore.Printed_Value.Log_Info(HTTP_, f'[CMS:Timeout]')
                FUC_SAVE.Saved_Result(r'DB_Results\Domain_Technology\Domain_Timeout.txt', f'{self.CFG_Target}\n')
                return None, None, None
            

            if RES_PROT['protocol']:
            
                FUC_SAVE.Saved_Result(r"DB_Results\Domain_Technology\Wordpress.txt", f"{RES_PROT['protocol']}\n")
                WPNonce_Found = SmokeCore.Extract_WPNonce(RES_PROT['r_saved'].text)
                if WPNonce_Found:
                    WPNonce_code = WPNonce_Found
                
                if WPNonce_Found:
                    FUC_SAVE.Saved_Result(r"DB_Results\Domain_Technology\Wordpress_Vuln_WPNonce.txt", f"{RES_PROT['protocol']}|{WPNonce_Found}\n")

                #Check raw page to find the key 
                RAW_Source = str(RES_PROT['r_saved'].text).lower()

                Header_RES = str(RES_PROT['r_saved'].headers).lower()
                
                if 'wp-content' in RAW_Source or 'wordpress' in RAW_Source or 'wp-' in RAW_Source:

                    FUC_SAVE.Saved_Result(r'DB_Results\Domain_Technology\Wordpress.txt', f'{RES_PROT['protocol']}\n')   
                    return RES_PROT['protocol'], 'WORDPRESS', WPNonce_code
                
                if self.MULTI_CMS:
                    if 'joomla' in RAW_Source or 'index.php?option=' in RAW_Source \
                        or 'com_content' in RAW_Source or 'com_users' in RAW_Source \
                        or 'components/com_' in RAW_Source or ('mod_login' in RAW_Source and 'mod_menu' in RAW_Source):
                        FUC_SAVE.Saved_Result(r'DB_Results\Domain_Technology\Joomla.txt', f'{RES_PROT['protocol']}\n')
                        return RES_PROT['protocol'], 'JOOMLA', None

                    if 'drupal' in RAW_Source or '/?q=' in RAW_Source or '/sites/default/' in RAW_Source or '/user/login' in RAW_Source:
                        FUC_SAVE.Saved_Result(r'DB_Results\Domain_Technology\Drupal.txt', f'{RES_PROT['protocol']}\n')
                        return RES_PROT['protocol'], 'DRUPAL', None

                    if 'opencart' in RAW_Source or 'index.php?route=' in RAW_Source \
                        or 'catalog/view/theme' in RAW_Source or 'controller/common' in RAW_Source or 'common/footer' in RAW_Source:
                        FUC_SAVE.Saved_Result(r'DB_Results\Domain_Technology\OpenCart.txt', f'{RES_PROT['protocol']}\n')
                        return RES_PROT['protocol'], 'OPENCART', None

                    if 'magento' in RAW_Source or 'skin/frontend' in RAW_Source \
                        or 'static/frontend' in RAW_Source or 'checkout/cart' in RAW_Source or 'customer/account' in RAW_Source:
                        FUC_SAVE.Saved_Result(r'DB_Results\Domain_Technology\Magento.txt', f'{RES_PROT['protocol']}\n')
                        return RES_PROT['protocol'], 'MAGENTO', None 
                        
                    if 'wordpress' in Header_RES or 'wp-' in Header_RES:
                        FUC_SAVE.Saved_Result(r'DB_Results\Domain_Technology\Wordpress.txt', f'{RES_PROT['protocol']}\n')
                        return RES_PROT['protocol'], 'WORDPRESS', WPNonce_code 
                    
                    if 'apache' in Header_RES or 'httpd' in Header_RES or 'mod_security' in Header_RES or 'mod_ssl' in Header_RES:
                        FUC_SAVE.Saved_Result(r'DB_Results\Domain_Technology\Apache.txt', f'{RES_PROT['protocol']}\n')
                        return RES_PROT['protocol'], 'APACHE', None 
                    

                    if 'nginx' in Header_RES:
                        FUC_SAVE.Saved_Result(r'DB_Results\Domain_Technology\Nginx.txt', f'{RES_PROT['protocol']}\n')
                        return RES_PROT['protocol'], 'NGINX', None 

                    if 'laravel' in Header_RES:
                        FUC_SAVE.Saved_Result(r'DB_Results\Domain_Technology\Laravel.txt', f'{RES_PROT['protocol']}\n')
                        return RES_PROT['protocol'], 'LARAVEL', None 

                    if 'php/' in Header_RES or '.php' in Header_RES:
                        FUC_SAVE.Saved_Result(r'DB_Results\Domain_Technology\PHP.txt', f'{RES_PROT['protocol']}\n')
                        return RES_PROT['protocol'], 'PHP', None 
            
                
            if RES_PROT['protocol']:    
                GET_XMLRPC = SmokeCore.Threaded_GET(
                                                    CFG_DOMAIN=RES_PROT['protocol'], 
                                                    CFG_VULN='xmlrpc.php', 
                                                    CFG_TIMEOUT=self.CFG_timeout, 
                                                    CFG_USERAGENT=self.Config_UA['User-Agent'], 
                                                    CFG_POSTDATA=NO_USED,
                                                    CFG_DELAY_ATTACK=self.CFG_Delay, 
                                                    SET_REDIRECT=self.Set_Redirect,
                                                    SET_MODE='req_get',
                                                    CFG_PROXIES=self.Proxies_ON,
                                                    Mem_Sess=NO_USED,
                                                    )
                
                RET_XMLRPC = GET_XMLRPC.run()
                XMLRPC_RES = [RET_XMLRPC[vuln_path] for vuln_path in RET_XMLRPC][0]

                if RES_PROT['protocol'] and XMLRPC_RES['resp']: #No both domain are dead
                    xmlrpc_text = str(XMLRPC_RES['resp'].text)
                    if 'XML-RPC server accepts POST requests only' in xmlrpc_text:
                        FUC_SAVE.Saved_Result(r'DB_Results\Domain_Technology\Wordpress_XMLRPC.txt', f'{RES_PROT['protocol']}\n')
                        
                        return RES_PROT['protocol'], 'WORDPRESS-XMLRPC', WPNonce_code
                    
            if RES_PROT['protocol']:   
                return RES_PROT['protocol'], 'Unknown_ID', None
            

            return None, None, None
            
        except:
            SmokeCore.Printed_Value.Log_Info(HTTP_, f'[CMS:Error]')
            FUC_SAVE.Saved_Result(r'DB_Results\Domain_Technology\Domain_Error.txt', f'{self.CFG_Target}\n')
            return None, None, None