# coding:utf-8

import sys
import psutil
import os

sys.path.append(os.path.abspath(r"Files_BurnWP\PyQt-Fluent-Widgets"))


from qfluentwidgets import qconfig
from Config_A import Config  
import Config_A
cfg = Config()
qconfig.load(r'Config/config.json', cfg)

from PyQt5.QtCore import Qt, QSize, QUrl, QPoint, QTimer
from PyQt5.QtGui import QIcon, QColor, QDesktopServices, QFont
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QFrame, QHBoxLayout, QVBoxLayout, QStackedWidget,
    QFileDialog, QFontDialog, QCompleter, QSpacerItem, QSizePolicy, QPushButton
)

from qfluentwidgets import (
    setTheme, Theme, FluentIcon as FIF, FluentWindow, MSFluentWindow, MSFluentTitleBar,
    NavigationItemPosition, NavigationAvatarWidget, qrouter, MessageBox, InfoBar,
    InfoBarIcon, InfoBarManager, InfoBarPosition, TabBar, TabCloseButtonDisplayMode,
    IconWidget, TransparentDropDownToolButton, TransparentToolButton, SwitchButton,
    isDarkTheme, ScrollArea, SubtitleLabel, CaptionLabel, MessageBoxBase,
    LineEdit, SearchLineEdit, PushButton, ComboBox, SettingCard, SettingCardGroup,
    ExpandLayout, RangeSettingCard, SwitchSettingCard, ComboBoxSettingCard,
    PushSettingCard, ProgressRing, SimpleCardWidget, SpinBox, IndeterminateProgressRing,
    setFont, FluentThemeColor, ToggleToolButton, StrongBodyLabel,
    CompactSpinBox, DoubleSpinBox, CompactDoubleSpinBox,
    DateTimeEdit, CompactDateTimeEdit, DateEdit, CompactDateEdit,
    TimeEdit, CompactTimeEdit
)

def Calc_Threader(max_default=50):
  
    cpu_count = os.cpu_count() or 1
    load_avg = psutil.getloadavg()[0] 

    if load_avg >= cpu_count * 0.9:
        multiplier = 1  
    elif load_avg <= cpu_count * 0.5:
        multiplier = 4  
    else:
        multiplier = 2  

    threads = cpu_count * multiplier
    return min(threads, max_default)

class CPU_Network(SimpleCardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.resize(180, 180)
        self.last_cpu_percent = -1
        self.last_net_percent = -1
        self.last_speed_text = ""
        self.last_sent = 0
        self.last_recv = 0

        fontTitle = QFont("Microsoft YaHei Light", 11)
        fontSpeed = QFont("Microsoft YaHei Light", 11)

        mainLayout = QHBoxLayout(self)
        mainLayout.setContentsMargins(10, 10, 10, 10)
        mainLayout.setSpacing(20)
        mainLayout.setAlignment(Qt.AlignCenter)

        cpuWidget = QWidget(self)
        cpuLayout = QVBoxLayout(cpuWidget)
        cpuLayout.setAlignment(Qt.AlignLeft)  
        cpuLayout.setSpacing(8)

        self.cpuRing = ProgressRing(self)
        self.cpuRing.setFixedSize(120, 120)
        self.cpuRing.setStrokeWidth(10)
        self.cpuRing.setTextVisible(True)
        cpuLayout.addWidget(self.cpuRing, alignment=Qt.AlignCenter)

        self.cpuLabel = QLabel("CPU Usage", self)
        self.cpuLabel.setFont(fontTitle)
        self.cpuLabel.setStyleSheet("color: white;")
        self.cpuLabel.setAlignment(Qt.AlignCenter)
        cpuLayout.addWidget(self.cpuLabel)

        # Internet widget
        netWidget = QWidget(self)
        netLayout = QVBoxLayout(netWidget)
        netLayout.setAlignment(Qt.AlignRight)  
        netLayout.setSpacing(8)

        self.netRing = ProgressRing(self)
        self.netRing.setFixedSize(120, 120)
        self.netRing.setStrokeWidth(10)
        self.netRing.setTextVisible(True)
        netLayout.addWidget(self.netRing, alignment=Qt.AlignCenter)

        self.netSpeedLabel = QLabel("Internet Usage", self)
        self.netSpeedLabel.setFont(fontSpeed)
        self.netSpeedLabel.setStyleSheet("color: white;")
        self.netSpeedLabel.setAlignment(Qt.AlignCenter)
        netLayout.addWidget(self.netSpeedLabel)

        
        mainLayout.addWidget(cpuWidget)
        mainLayout.addWidget(netWidget)

        # Initialize network counters
        net_counters = psutil.net_io_counters()
        self.last_sent = net_counters.bytes_sent
        self.last_recv = net_counters.bytes_recv

        # Update 
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateStats)
        self.timer.start(1000)
        self.updateStats()

    def updateStats(self):
        cpu_percent = int(psutil.cpu_percent())
        if cpu_percent != self.last_cpu_percent:
            self.cpuRing.setValue(cpu_percent)
            self.last_cpu_percent = cpu_percent

        current = psutil.net_io_counters()
        sent_diff = current.bytes_sent - self.last_sent
        recv_diff = current.bytes_recv - self.last_recv

        upload_kb = sent_diff / 1024
        download_kb = recv_diff / 1024
        total_kb = upload_kb + download_kb

        max_speed_kb = 10240
        usage_percent = min(100, int((total_kb / max_speed_kb) * 100))

        if usage_percent != self.last_net_percent:
            self.netRing.setValue(usage_percent)
            self.last_net_percent = usage_percent

        speed_text = f"Up: {upload_kb:.1f} KB/s, Down: {download_kb:.1f} KB/s"
        if speed_text != self.last_speed_text:
            self.netSpeedLabel.setText(speed_text)
            self.last_speed_text = speed_text

        self.last_sent = current.bytes_sent
        self.last_recv = current.bytes_recv



@InfoBarManager.register('Custom')
class CustomInfoBarManager(InfoBarManager):
    def _pos(self, infoBar: InfoBar, parentSize=None):
        p = infoBar.parent()
        parentSize = parentSize or p.size()
        x = (parentSize.width() - infoBar.width()) // 2
        y = (parentSize.height() - infoBar.height()) // 2
        index = self.infoBars[p].index(infoBar)
        for bar in self.infoBars[p][0:index]:
            y += (bar.height() + self.spacing)
        return QPoint(x, y)

    def _slideStartPos(self, infoBar: InfoBar):
        pos = self._pos(infoBar)
        return QPoint(pos.x(), pos.y() - 16)
    
    
class ProxyTargetInputCard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(200, 200)

        fontTitle = QFont("Microsoft YaHei Light", 11)

        layout = ExpandLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        self.urlLabel = QLabel("Domain Test_Proxy", self)
        self.urlLabel.setFont(fontTitle)
        self.urlLabel.setStyleSheet("color: white;")
        self.urlInput = LineEdit(self)
        #self.urlInput.setPlaceholderText("http://example.com")
        if cfg.CFG_TEST_URL.value:
            self.urlInput.setText(cfg.CFG_TEST_URL.value)
        else:
            self.urlInput.setPlaceholderText("http://example.com")

        self.urlInput.setClearButtonEnabled(True)

        self.keyLabel = QLabel("Key_Found", self)
        self.keyLabel.setFont(fontTitle)
        self.keyLabel.setStyleSheet("color: white;")
        self.keyInput = LineEdit(self)
        #self.keyInput.setPlaceholderText("title>Example Domain")
        
        if cfg.CFG_TEST_KEY.value:
            self.keyInput.setText(cfg.CFG_TEST_KEY.value)
        else:
            self.keyInput.setPlaceholderText("title>Example Domain")

        self.keyInput.setClearButtonEnabled(True)


        self.urlInput.textChanged.connect(lambda text: self.on_value_changed(cfg.CFG_TEST_URL, text))
        self.keyInput.textChanged.connect(lambda text: self.on_value_changed(cfg.CFG_TEST_KEY, text))

        layout.addWidget(self.urlLabel)
        layout.addWidget(self.urlInput)
        layout.addWidget(self.keyLabel)
        layout.addWidget(self.keyInput)

        self.setLayout(layout)

    def on_value_changed(self, config_item, value):
        config_item.value = value
        Config_A.save_config()

class ProxyControlCard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(60, 60)

        fontTitle = QFont("Microsoft YaHei Light", 11)

        layout = QHBoxLayout(self)
      
        self.threadsLabel = QLabel("Threads:", self)
        self.threadsLabel.setFont(fontTitle)
        self.threadsLabel.setStyleSheet("color: white;")

        self.threadsSpin = SpinBox(self)
        self.threadsSpin.setRange(1, 256)
        self.threadsSpin.setValue(cfg.PROXY_THREADS.value)

        self.retryLabel = QLabel("Retry:", self)
        self.retryLabel.setFont(fontTitle)
        self.retryLabel.setStyleSheet("color: white;")

        self.retrySpin = SpinBox(self)
        self.retrySpin.setRange(1, 10)
        self.retrySpin.setValue(cfg.PROXY_RETRY.value)

        self.timeoutLabel = QLabel("Timeout (s):", self)
        self.timeoutLabel.setFont(fontTitle)
        self.timeoutLabel.setStyleSheet("color: white;")

        self.timeoutSpin = SpinBox(self)
        self.timeoutSpin.setRange(1, 60)
        self.timeoutSpin.setValue(cfg.PROXY_TIMEOUT.value)


        self.threadsSpin.valueChanged.connect(lambda val: self.on_value_changed(cfg.PROXY_THREADS, val))
        self.retrySpin.valueChanged.connect(lambda val: self.on_value_changed(cfg.PROXY_RETRY, val))
        self.timeoutSpin.valueChanged.connect(lambda val: self.on_value_changed(cfg.PROXY_TIMEOUT, val))

        layout.addWidget(self.threadsLabel)
        layout.addWidget(self.threadsSpin)
        layout.addWidget(self.retryLabel)
        layout.addWidget(self.retrySpin)
        layout.addWidget(self.timeoutLabel)
        layout.addWidget(self.timeoutSpin)

        self.setLayout(layout)

    def on_value_changed(self, config_item, value):
        config_item.value = value
        Config_A.save_config()

class ProxySettingsCard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(380, 380)

        layout = ExpandLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        self.targetCard = ProxyTargetInputCard(self)
        self.controlCard = ProxyControlCard(self)

        layout.addWidget(self.targetCard)
        layout.addWidget(self.controlCard)

        self.setLayout(layout)

    
class HomePage(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.max_threads = Calc_Threader() // 6


        self.scrollWidget = QWidget(self)
        self.expandLayout = ExpandLayout(self.scrollWidget) 

        self.Proxy_Group = SettingCardGroup(self.tr("Proxy Config"), self.scrollWidget)
         
        
        self.Main_Panel = SettingCardGroup(self.tr('Statistics - BurnWP Framework'), self.scrollWidget)
        self.Basic_Settings = SettingCardGroup(self.tr("Basic Configs"), self.scrollWidget)
        self.Technology_Setting = SettingCardGroup(self.tr("Technology Configs"), self.scrollWidget)

        self.proxySettingsCard= ProxyTargetInputCard(self)
        self.Proxy_Group.addSettingCard(self.proxySettingsCard)

        self.proxySettingsCard2 = ProxyControlCard(self)
        self.Proxy_Group.addSettingCard(self.proxySettingsCard2)
        

        self.cpu_Card = CPU_Network(self)
        self.Main_Panel.addSettingCard(self.cpu_Card)

        # -------- WEBSHELL LINK ---------------

        self.HOST_WebShell = LineEdit(self)
        #self.HOST_WebShell.setPlaceholderText("")
        if cfg.CFG_HOSTSHELL.value:
            self.HOST_WebShell.setText(cfg.CFG_HOSTSHELL.value)            
        else:
            self.HOST_WebShell.setText('HOST WebShell (Pastebin)')

    
        # ------- WEBSHELL RCE --------------

        self.RFI_WebShell = LineEdit(self)
        #self.RFI_WebShell.setPlaceholderText("")

        if cfg.CFG_RFI_WEBSHELL.value:
            self.RFI_WebShell.setText(cfg.CFG_RFI_WEBSHELL.value)
        else:
            self.RFI_WebShell.setText('HOST RFI_WebShell (LINK RAW)')


        self.HOST_WebShell.textChanged.connect(self.WEBSHELL_HOST_ADDED)
        self.RFI_WebShell.textChanged.connect(self.RFI_HOST_ADDED)

        # ---- RangeSettingCard for MAX_THREADS ----

        self.maxThreadsCard = RangeSettingCard(
        cfg.MAX_THREADS,
            FIF.SPEED_HIGH,
            self.tr('Max Threads'),
            parent=self.Basic_Settings
        )

        self.Basic_Settings.addSettingCard(self.maxThreadsCard)

          # ---- COMBO USERAGENT  ------
        self.comboBox_Card = ComboBoxSettingCard(
            cfg.CUSTOM_DEVICE,
            FIF.ROBOT,
            self.tr('Custom User-Agent'),
            #self.tr('Select a default User-Agent'),
            texts=[
                'pc_chrome', 'pc_firefox', 'pc_edge', 'pc_safari',
                'phone_chrome', 'phone_safari', 'phone_firefox',
            ],
            parent=self.Basic_Settings
        )
        self.Basic_Settings.addSettingCard(self.comboBox_Card)


        def on_toggled(checked, config_item):
            config_item.value = checked
            Config_A.save_config()


        # TECHNO_LISTS = [
        #                 ("WordPress", cfg.CFG_TECH_WORDPRESS),
        #                 ("WP_XMLRPC Brute", cfg.CFG_TECH_WPXMLRPC),
        #                 ("Joomla", cfg.CFG_TECH_JOOMLA),
        #                 ("Joomla Brute", cfg.CFG_TECH_JOOMLABRUTE),
        #                 ("PHP", cfg.CFG_PHP),
        #                 ("Laravel", cfg.CFG_TECH_LARAVEL),
        #                 ("Git Config", cfg.CFG_TECH_GIT_CONFIG),
                
        #             ]
        
        LIST_FEATURES = [
                        ("CVE Exploiter", cfg.CFG_CVE_EXPLOITER),
                        ("Plugin Exploiter", cfg.CFG_PLUGIN_OFFON),
                        # ("Laravel", cfg.CFG_LARAVEL),
                        # ("Git Config", cfg.CFG_GIT_CONFIG),
                        ("LFI [WP-Config] Scanner", cfg.CFG_LFI_SCANNER),
                        ("WP PHPUnit", cfg.CFG_WP_PHPUNIT),
                        # ("WP XMLRPC Brute", cfg.CFG_WP_XMLRPC),
                        ("phpMyAdmin [LFI]", cfg.CFG_PHPMYADMIN_CHECKER),
                        # ("Detect ALL CMS", cfg.CFG_DETECT_MULTI_CMS),
                        ("Proxies", cfg.CFG_PROXIES_OFFON),
                        ("WordPress [Plugin]", cfg.CFG_TECH_WORDPRESS),
                      
                    ]
        
        

        LIST_LOCKED = [

                        ("WP_XMLRPC Brute [Plugin]", cfg.CFG_TECH_WPXMLRPC),
                        ("Joomla [Plugin]", cfg.CFG_TECH_JOOMLA),
                        ("Joomla Brute [Plugin]", cfg.CFG_TECH_JOOMLABRUTE),
                        ("PHP [Plugin]", cfg.CFG_PHP),
                        ("Laravel [Plugin]", cfg.CFG_TECH_LARAVEL),
                        ("Git_Config [Plugin]", cfg.CFG_TECH_GIT_CONFIG),
        ]



        for label_, config_item in LIST_FEATURES:
            card = SwitchSettingCard(
                icon=FIF.SETTING,
                title=self.tr(label_),
                content=None,
                configItem=config_item,
                parent=self.Technology_Setting
            )
            card.switchButton.setChecked(config_item.value)
            card.switchButton.checkedChanged.connect(lambda checked, item=config_item: on_toggled(checked, item))
            self.Technology_Setting.addSettingCard(card)



        for label_, config_item in LIST_LOCKED:
            card = SwitchSettingCard(
                icon=FIF.SETTING,
                title=self.tr(label_),
                content=None,
                configItem=config_item,
                parent=self.Technology_Setting  
            )
            card.switchButton.setChecked(config_item.value)
            card.switchButton.setEnabled(False)  # Disable toggle
            #card.switchButton.checkedChanged.connect(lambda checked, item=config_item: on_toggled(checked, item))
            self.Technology_Setting.addSettingCard(card)
     
     

        self.expandLayout.addWidget(self.Main_Panel)
        self.expandLayout.addWidget(self.Basic_Settings)
        
        self.Basic_Settings.addSettingCard(self.HOST_WebShell)
        self.Basic_Settings.addSettingCard(self.RFI_WebShell)
        
        self.expandLayout.addWidget(self.Technology_Setting)

        self.expandLayout.addWidget(self.Proxy_Group)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_threaded_order)
        self.timer.start(1000)  

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.ForceUser_Enable_PluginCMS)
        self.timer.start(1000)  # 1000 milliseconds = 1 second
        

    def showCustomInfoBar(self, INFO_TT, INFO_CC):
        bar = InfoBar.new(
            icon=FIF.INFO,
            title=INFO_TT,
            content=INFO_CC,
            orient=Qt.Horizontal,
            isClosable=True,
            duration=2000,
            position=InfoBarPosition.BOTTOM_RIGHT,   
            parent=self
        )
        bar.setCustomBackgroundColor('#FFF3CD', "#CB9B0B") 
        bar.show()

    def ForceUser_Enable_PluginCMS(self):
        if cfg.CFG_PLUGIN_OFFON.value and not cfg.CFG_TECH_WORDPRESS.value or cfg.CFG_TECH_WORDPRESS.value and not cfg.CFG_PLUGIN_OFFON.value:
            
            self.showCustomInfoBar(INFO_TT='Warning: Plugin Exploiter will Skip', INFO_CC='You must enable the WordPress Plugin because the Plugin Exploiter checks\n which CMS plugins are Enabled before launching any Exploiter.')


    def WEBSHELL_HOST_ADDED(self, text):
        cfg.HOST_WebShell.value = text
        Config_A.save_config()

    def RFI_HOST_ADDED(self, text):
        cfg.RFI_WebShell.value = text
        Config_A.save_config()

    def check_threaded_order(self):
        # print(self.maxThreadsCard.slider.value())
        if self.maxThreadsCard.slider.value() > self.max_threads:
            #print('too much reached')  
            self.showCustomInfoBar(INFO_TT='Warning: Maximum Threads Reached', INFO_CC='Increase More Threads will be Crash while Working')
        
        

        
        self.__initWidget()

    def __initWidget(self):
        self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)

        #initialize layout
        self.__setQss()
 
    def __setQss(self):
        try:
            theme = 'dark' if isDarkTheme() else 'light'

            # Dark
            if theme == 'dark':
                qss = """
                #scrollWidget {
                    background-color: rgb(39, 39, 39);
                }

                QScrollArea {
                    border: none;
                    background-color: rgb(39, 39, 39);
                }

                /* 标签 */
                QLabel#settingLabel {
                    font: 33px 'Microsoft YaHei Light';
                    background-color: transparent;
                    color: white;
                }
                """
            else:
                # Light
                qss = """
                #scrollWidget {
                    background-color: rgb(255, 255, 255);
                }

                QScrollArea {
                    border: none;
                    background-color: rgb(255, 255, 255);
                }

                QLabel#settingLabel {
                    font: 33px 'Microsoft YaHei Light';
                    background-color: transparent;
                    color: black;
                }
                """

            self.scrollWidget.setObjectName('scrollWidget')
            self.setStyleSheet(qss)
        except Exception as er:
            print(er)

class Widget(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = SubtitleLabel(text, self)
        self.hBoxLayout = QHBoxLayout(self)

        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignCenter)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)
        self.setObjectName(text.replace(' ', '-'))

class TabInterface(QFrame):
    """ Tab interface """

    def __init__(self, text: str, icon, objectName, parent=None):
        super().__init__(parent=parent)
        self.iconWidget = IconWidget(icon, self)
        self.label = SubtitleLabel(text, self)
        self.iconWidget.setFixedSize(120, 120)

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setAlignment(Qt.AlignCenter)
        self.vBoxLayout.setSpacing(30)
        self.vBoxLayout.addWidget(self.iconWidget, 0, Qt.AlignCenter)
        self.vBoxLayout.addWidget(self.label, 0, Qt.AlignCenter)
        setFont(self.label, 24)

        self.setObjectName(objectName)

class Window(FluentWindow):

    def __init__(self):
        super().__init__()
        
        # create sub interface
        self.homeInterface = QStackedWidget(self, objectName='homeInterface')

        self.homePage = HomePage(self)
        self.homePage.setObjectName("homePage")

        self.initNavigation()
        self.initWindow()

    
    def onCheckedChanged(self, isChecked: bool):
        text = 'On' if isChecked else 'Off'
        self.switchButton.setText(text)

    def initNavigation(self):
        self.addSubInterface(self.homePage, FIF.HOME, "home")

        self.navigationInterface.addSeparator()

    def onTabChanged(self, index: int):
        objectName = self.tabBar.currentTab().routeKey()
        self.homeInterface.setCurrentWidget(self.findChild(TabInterface, objectName))
        self.stackedWidget.setCurrentWidget(self.homeInterface)



    def initWindow(self):
        self.resize(1000, 800)
        
        #Logo on Top with ICON
        # BASE_DIR = os.path.dirname(__file__)
        # icon_path = os.path.join(BASE_DIR, "Files_BurnWP", "wordpress.svg")
        self.setWindowIcon(QIcon(r'Files_BurnWP/wordpress.svg'))
        self.setWindowTitle('  BurnWP Framework - Config')

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)


def UI_Frame():
    try:
        QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

        setTheme(Theme.DARK)
        # LIGHT = "Light"
        # DARK = "Dark"
        # AUTO = "Auto"

        # setTheme(Theme.WHITE)
        
        app = QApplication(sys.argv)
        w = Window()
        w.show()
        app.exec_()
    except Exception as er:
        print(er, 'Error UI')