
import importlib
import requests
import time
import urllib3
from concurrent.futures import ThreadPoolExecutor, as_completed
import os 
NO_USED = None


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"


Core_Helper = importlib.import_module('Core.Core_Helper')

class ProxyChecker:
    def __init__(self, 
                tgt_url, 
                tgt_keyword, 
                timeout, 
                max_retry,
                tgt_good_proxies,
                tgt_bad_proxies,
                tgt_mark_good,
                tgt_mark_bad,
                max_tasker):
        
        self.TARGET_TEST = tgt_url
        self.KEYWORD = tgt_keyword
        self.TIMEOUT = timeout
        self.MAX_RETRY = max_retry
        self.good_proxies = tgt_good_proxies
        self.bad_proxies = tgt_bad_proxies
        self.mark_good = tgt_mark_good
        self.mark_bad = tgt_mark_bad
        self.MAX_HUMAN = max_tasker
        
    def check_proxy(self, proxy_raw):
        
        #proxy_url = f"{proxy_type}://{proxy_raw.strip()}"
        #proxies = {"http": proxy_raw, "https": proxy_raw}

        for i in range(self.MAX_RETRY + 1):
            try:
                response = requests.get(self.TARGET_TEST, proxies={"http": proxy_raw, "https": proxy_raw}, timeout=self.TIMEOUT, verify=False)
            
                
                if self.KEYWORD in str(response.text):
                    #Found Key 
                    if proxy_raw not in self.good_proxies: #IF proxy new not yet add to good proxy
                        #Check IF not yet Add  
                        self.good_proxies.append(proxy_raw) 
                        #print(f"{GREEN}[OK]{RESET} {proxy_raw} => {self.TARGET_TEST}")

                    self.mark_bad.discard(proxy_raw)  
                    """    
                    safe remove (no error IF not in set) IF we use dot_remove will be crash like KeyError etc.. 
                    so use discard better and without error smoothly 
                    
                    """
                    self.mark_good.add(proxy_raw) #now move from bad to good by way add mark_good
                    return True
                else:
                    break  #Miss keyword == useless than break up 
            except Exception:
                #Finally with no repeat bad_proxies
                if i == self.MAX_RETRY: 
                    if proxy_raw not in self.bad_proxies:  #duplicate
                        self.bad_proxies.append(proxy_raw) 
                        #print(f"{RED}[FAIL]{RESET} {proxy_raw}")

                    
                    if proxy_raw in self.mark_good: 
                        self.mark_good.discard(proxy_raw)   #discard is safe even if not in set
                        #print(f"{RED}[GOOD KICK]{RESET} {proxy_raw}")
                    
                    self.mark_bad.add(proxy_raw)  

        return False


    def Loader_Proxies(self, ptype, folder):
        path_txt = os.path.join(folder, f"{str(ptype).upper()}_Proxies.txt")
        try:
            with open(path_txt, "r", encoding='utf-8') as f:
                proxies = f.read().splitlines()
                return proxies
        except FileNotFoundError:
            return []



    def Autodetect_Proxies(self, folder=r"Config/Type_Proxies"):
        types = ["http", "https", "socks4", "socks5"]
        for p_type in types:
            proxies = self.Loader_Proxies(p_type, folder)
            if proxies: #if allow read file also type is matched 
                return p_type, proxies
        return None, []



    def MAN_THREADER(self):
        proxy_type, proxy_lists = self.Autodetect_Proxies()
        #start_time = time.time()  # Start timer
        with ThreadPoolExecutor(max_workers=self.MAX_HUMAN) as executor:
            futures = []
            for proxy in proxy_lists:
                proxy_url = f"{proxy_type}://{proxy.strip()}"
                futures.append(executor.submit(self.check_proxy, proxy_url))

            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"[ERROR] {e}")