import sys, os 
sys.path.append(os.path.abspath(r"Files_BurnWP/PyQt-Fluent-Widgets"))

from qfluentwidgets import qconfig
from qfluentwidgets import (
    QConfig, ConfigItem, BoolValidator,
    RangeConfigItem, RangeValidator,
    OptionsConfigItem, OptionsValidator
)




class Config(QConfig):

    #TECHNOLOGIA
    CFG_CVE_EXPLOITER = ConfigItem("TECHNOLOGY", "CVE_Exploiter", False, BoolValidator())
    CFG_PLUGIN_OFFON = ConfigItem("TECHNOLOGY", "Plugin_Exploiter", False, BoolValidator())
    CFG_LFI_SCANNER = ConfigItem("TECHNOLOGY", "LFI_Scanner", False, BoolValidator())
    # CFG_DETECT_MULTI_CMS = ConfigItem("TECHNOLOGY", "Detect_All_CMS", False, BoolValidator())
    CFG_USERAGENT = ConfigItem("TECHNOLOGY", "User_Agent", False, BoolValidator())
    CFG_WP_PHPUNIT = ConfigItem("TECHNOLOGY", "WP_PHPUnit", False, BoolValidator())
    CFG_PHPMYADMIN_CHECKER = ConfigItem("TECHNOLOGY", "PhpMyAdmin", False, BoolValidator())
    CFG_PROXIES_OFFON = ConfigItem("TECHNOLOGY", "Proxies", False, BoolValidator())

    CFG_TECH_WORDPRESS = ConfigItem("TECHNOLOGY", "WordPress", False, BoolValidator())
    CFG_TECH_WPXMLRPC = ConfigItem("TECHNOLOGY", "WP_XMLRPC Brute", False, BoolValidator())
    CFG_TECH_JOOMLA = ConfigItem("TECHNOLOGY", "Joomla", False, BoolValidator())
    CFG_TECH_JOOMLABRUTE = ConfigItem("TECHNOLOGY", "Joomla Brute", False, BoolValidator())

    CFG_TECH_LARAVEL = ConfigItem("TECHNOLOGY", "Laravel", False, BoolValidator())
    CFG_TECH_GIT_CONFIG = ConfigItem("TECHNOLOGY", "Git_Config", False, BoolValidator())
    CFG_PHP = ConfigItem("TECHNOLOGY", "PHP", False, BoolValidator())
    
   

    # URLs
    CFG_RFI_WEBSHELL = ConfigItem("URLs", "RFI_WebShell", "", None)
    CFG_HOSTSHELL = ConfigItem("URLs", "HOST_WebShell", "", None)

    # Threads
    MAX_THREADS = RangeConfigItem("Core", "maxThreads", 4, RangeValidator(1, 30))

    # User Agent
    CUSTOM_DEVICE = OptionsConfigItem(
        "Core", "userAgent", "pc_chrome",
        OptionsValidator([
            'pc_chrome', 'pc_firefox', 'pc_edge', 'pc_safari',
            'phone_chrome', 'phone_safari', 'phone_firefox',
        ])
    )

    PROXY_THREADS = RangeConfigItem("Proxy_Config", "THREADS", 10, RangeValidator(1, 30))
    PROXY_RETRY = RangeConfigItem("Proxy_Config", "RETRY", 1, RangeValidator(1, 10))
    PROXY_TIMEOUT = RangeConfigItem("Proxy_Config", "TIMEOUT", 10, RangeValidator(1, 60))

    CFG_TEST_URL = ConfigItem("Proxy_Config", "TEST_URL", "", None)
    CFG_TEST_KEY = ConfigItem("Proxy_Config", "TEST_KEY", "", None)


cfg = Config()


def load_config(path='Config/config.json'):
    try:
        qconfig.load(path, cfg)  
        #print(f"Config loaded from {path}")
    except:pass 
        #print(f"Failed to load Config: {e}")

def save_config():
    try:
        qconfig.save()  
        #print("Config saved")
    except:pass 
        #print(f"Failed to save Config: {e}")