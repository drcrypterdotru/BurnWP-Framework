import os,sys 
import time
import importlib.util
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from sys import platform
from concurrent.futures import ThreadPoolExecutor, as_completed

VALID_EXTENSIONS = [".py"]
NO_USED = None

PCore = importlib.import_module('Core.Core_Helper')
PMain = importlib.import_module('main')


class PluginManager:
    def __init__(self, plugin_folder=NO_USED, cfg_plugin=NO_USED):
        
        self.plugin_functions = {} 
        self.Target = NO_USED
        self.WPNonce = NO_USED
        self.Proxies = NO_USED 
        self.Sess = NO_USED
        self.User_Agent = NO_USED
        self.Cfg_Technologia = NO_USED
        
        self.plugin_folder = plugin_folder
        self.plugin_filename = cfg_plugin
        self.plugin_funct = 'Plugin_BurnWP'
      
        self.loaded_plugins_set = set()
        self.invalid_plugins_set = set()
        self.modified_plugin_names = set()
        self.plugin_names = set()
        self.new_plugins = 0
        self.deleted_plugins = 0
        self.modified_plugins = 0
        os.makedirs(self.plugin_folder, exist_ok=True) 
        
 
    def Plugin_Selected(self, Target_Lists, User_Agent, PLUGIN_CONTROL_SYSTEM, MAX_THREADED, Plugin_Named=NO_USED):
        DIRECT_PLUGIN = False
        PCore.Printed_Value.Log_Success('MAX Threaded :', MAX_THREADED)
        plugin_files = []
        if Plugin_Named:
            DIRECT_PLUGIN = True
            
    
        for filename in os.listdir(self.plugin_folder):
            full_path = os.path.join(self.plugin_folder, filename) 
            if os.path.isfile(full_path) and filename.endswith(".py") and not filename.startswith("__"):
                
                plugin_files.append((filename, full_path))

        if not plugin_files:
            PCore.Printed_Value.Log_Error("Plugin_Manager", "No plugins found.")
            return
        PCore.Printed_Value.Log_Success("Plugin_Manager\n\n", "LIST Plugins was Listening....")
        print('\n')
        

        if DIRECT_PLUGIN:
            self.Loading_Plugin(Plugin_Named+'.py')
        else:
        
            try:
                for idx, (name, _) in enumerate(plugin_files):
                    without_ex = str(name).replace('.py', '')
                    print(f"[{idx}] {without_ex}")

                print("\n\n[999] Exit")

                selection = int(input("\n\nSelect plugin number to run: ")) 
                if selection == 999: 
                    print("\nExecuted ==> Exit\n")
                    sys.exit()
                _, p_selected = plugin_files[selection]
                
                #print(_, p_selected) WP_Bricks_RCE_196.py Plugins_Exploiter\WP_Bricks_RCE_196.py
                
                self.Loading_Plugin(p_selected)

            except Exception as er:
                PCore.Printed_Value.Log_Error("Plugin_Manager", f"Error Invalid Selection : {er}")
     
    
        def Per_ScanTGT(i):
            try:
                PRO_TARGET, WPNONCE, P_SESS, PROXIES, FOUND_CMS = PMain.Scan_Plugin(i)
                # print(PRO_TARGET, WPNONCE, P_SESS, PROXIES, FOUND_CMS )
                if PRO_TARGET:

                    self.Run_Plugin(PRO_TARGET, PROXIES, WPNONCE, P_SESS, User_Agent, PLUGIN_CONTROL_SYSTEM, FOUND_CMS)
            except:
                pass 

        with ThreadPoolExecutor(max_workers=MAX_THREADED) as executor:  
            futures = [executor.submit(Per_ScanTGT, target) for target in Target_Lists]

            for future in as_completed(futures):
                try:
                    future.result()  
                except Exception as e:
                    PCore.Printed_Value.Log_Error("Plugin_Manager", f"Error Plugin Selected : {e}")


    
    def Loading_Plugin(self, path): #Loading per Plugin
        
        # Valid .py extension if not valid 

        # pattern = r"\.py$|\.plugin\.py$"
        # if not re.search(pattern, path):
        #     self.invalid_plugins_set.add(path)
        #     self.print_status("Invalid Plugin", path, 'ERROR')
        
        if not path.endswith(tuple(VALID_EXTENSIONS)):
            self.invalid_plugins_set.add(path)
            PCore.Printed_Value.Log_Error("Plugin_Manager", f"Invalid plugin: {path}")
            return

        plugin_name = os.path.splitext(os.path.basename(path))[0].lower()
       
        self.loaded_plugins_set.discard(plugin_name)
        self.invalid_plugins_set.discard(plugin_name)
        

        spec = importlib.util.spec_from_file_location(plugin_name, path)
        if spec is NO_USED or spec.loader is NO_USED: 
            self.invalid_plugins_set.add(plugin_name)
            PCore.Printed_Value.Log_Error("Plugin_Manager", f"Spec load failed: {path}")
            return

        module = importlib.util.module_from_spec(spec) 
        try:
            
            # Execute module
            spec.loader.exec_module(module) 
            plugin_function = module.__dict__.get(self.plugin_funct)
            #print(plugin_function)

            if plugin_function:
                self.plugin_functions[plugin_name] = plugin_function
            
                self.loaded_plugins_set.add(plugin_name)
                self.plugin_names.add(plugin_name)
                #PCore.Printed_Value.Log_Success("Plugin_Manager", f"Plugin executed: {plugin_name}")
            else:
                self.invalid_plugins_set.add(plugin_name)
                PCore.Printed_Value.Log_Error("Plugin_Manager", f"Missing Function {self.plugin_funct} in {path}")
        except Exception as e:
            self.invalid_plugins_set.add(plugin_name)
            #self.print_status(f"Execution Error: {e}", path, 'ERROR')
            PCore.Printed_Value.Log_Error("Plugin_Manager", f"Execution Error: {e} in {path}")

    
    def Persistenced_Plugin(self): #Persistenced_Plugin only once and then run them without recalling the again.
        for filename in os.listdir(self.plugin_folder):
            full_path = os.path.join(self.plugin_folder, filename) 
            if os.path.isfile(full_path):
                self.Loading_Plugin(full_path)

    def Run_Plugin(self, TGT_, Proxies, WP_Code, req_SESS, User_Agent, PLUGIN_CONTROL_SYSTEM, FOUND_CMS):
        
        #(self.TARGET, self.Proxies_ON, self.WPNonce, self.Sessions, self.UA_, self.PLUGIN_CONTROL_SYSTEM, self.FOUND_CMS)
        
        try:
            
            for plugin_name in self.plugin_functions:
                #PCore.Printed_Value.Log_Info("Plugin_Manager", f"Running plugin: {plugin_name}")
                #print(TGT_, Proxies, WP_Code, req_SESS)
                self.plugin_functions[plugin_name](TGT_, Proxies, req_SESS, WP_Code, User_Agent, PLUGIN_CONTROL_SYSTEM, FOUND_CMS)
        except Exception as e:
            
            PCore.Printed_Value.Log_Error("Plugin_Manager", f"Error running plugin '{plugin_name}': {e}")

    def Plugin_Watcher(self):
        event_handler = PluginEventHandler(self)
        observer = Observer()
        observer.schedule(event_handler, path=self.plugin_folder, recursive=False) 
        observer.start()

        try:
            while True:
                #Set watching every a sec
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        
        observer.join()
        
    def Printed_MSG(self):
        os.system('cls' if platform == 'win32' else 'clear')
        
        total = len(self.loaded_plugins_set | self.invalid_plugins_set)
        s_plugins = f'+{self.new_plugins}' if self.new_plugins > 0 else '0'
      
        print(
            f"\033[36mTotal Plugins: {total}\033[0m | "
            f"\033[34mValid Plugins: {len(self.loaded_plugins_set)}\033[0m   | "
            f"\033[31mError Plugins: {len(self.invalid_plugins_set)}\033[0m  \n"
            f"\033[32mNew Plugins: {s_plugins}\033[0m   | "
            f"\033[33mDeleted Plugins: {self.deleted_plugins}\033[0m | "
            f"\033[35mModified Plugins: {self.modified_plugins // 4}\033[0m"
        )
        print(f'\n{"-" * 60}\n')
        PCore.Printed_Value.Log_Info("Plugin_Manager", "Watching Plugin Folder for Real-Time Updates...")

    def _color_text(self, text, color):
        codes = {
            'green': '\033[32m',
            'red': '\033[31m',
            'blue': '\033[34m',
            'yellow': '\033[33m',
            'magenta': '\033[35m',
            'reset': '\033[0m'
        }
        return f"{codes[color]}{text}{codes['reset']}"

# File Watching Handler
class PluginEventHandler(FileSystemEventHandler):
    def __init__(self, plugin_manager):
        self.plugin_manager = plugin_manager

    def On_Created(self, event):
        if not event.is_directory:
            plugin_name = os.path.splitext(os.path.basename(event.src_path))[0].lower().replace(" ", "_") # type: ignore
            
            if plugin_name not in self.plugin_manager.plugin_names:
                self.plugin_manager.new_plugins += 1
            self.plugin_manager.Loading_Plugin(event.src_path)
            PCore.Printed_Value.Log_Info("Plugin_Manager", f"Plugin Created: {plugin_name}")
            self.plugin_manager.Printed_MSG()

    def On_Modified(self, event):
        if not event.is_directory:
            plugin_name = os.path.splitext(os.path.basename(event.src_path))[0].lower()

            self.plugin_manager.modified_plugins += 1  # Always count
            self.plugin_manager.modified_plugin_names.add(plugin_name)  # Optional: for list of modified plugins

            self.plugin_manager.Loading_Plugin(event.src_path)
            PCore.Printed_Value.Log_Info("Plugin_Manager", f"Plugin Modified: {plugin_name}")
            self.plugin_manager.Printed_MSG()

    def On_Deleted(self, event):
        if not event.is_directory:
            plugin_name = os.path.splitext(os.path.basename(event.src_path))[0].lower()
            #print(plugin_name)
            self.plugin_manager.plugin_names.discard(plugin_name)
            self.plugin_manager.loaded_plugins_set.discard(plugin_name)
            self.plugin_manager.invalid_plugins_set.discard(plugin_name)
            self.plugin_manager.deleted_plugins += 1
            PCore.Printed_Value.Log_Fail("Plugin_Manager", f"Plugin Deleted: {plugin_name}")
            self.plugin_manager.Printed_MSG()
