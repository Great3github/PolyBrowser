
import subprocess
from msg import cmdconfig, msgconfig
from dialog import CustomDialog
import browser_config
from internal import pb_url
from subprocess import DEVNULL, STDOUT
try:
    subprocess.run(cmdconfig.installcmd, stdout=DEVNULL, stderr=DEVNULL)
    from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QMessageBox, QDialog, QLabel,QDialogButtonBox
    from PyQt5.QtWebEngineWidgets import QWebEngineView
    from PyQt5.QtCore import QUrl
except ImportError as e:
    CustomDialog.NewOkDialog("Error", msgconfig.ErrorMsg.importErrorMsg(e))
    exit(1)
import sys


class SimpleBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setGeometry(browser_config.windowDimensions[0], browser_config.windowDimensions[1], browser_config.windowDimensions[2], browser_config.windowDimensions[3])
        
        # Create browser widget
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl(browser_config.startingpage))
        if browser_config.runMode.lower() == "fullscreen": self.showFullScreen()
        if browser_config.runMode.lower() == "maximized": self.showMaximized()
        if browser_config.runMode.lower() == "minimized": self.showMinimized()
        if browser_config.runMode.lower() == "normal": self.showNormal()
        if browser_config.runMode.lower() not in ['normal', 'minimized', 'maximized', 'fullscreen']:
            CustomDialog.NewOkDialog("Error", msgconfig.ErrorMsg.invalidParamError)
            exit(1)
        # Create navigation bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigateToURL)
        self.url_bar.setDisabled(browser_config.urlBarDisabled)
        if browser_config.showHomeButton:
            self.go_btn = QPushButton(msgconfig.ButtonText.homeButton)
            self.go_btn.clicked.connect(self.navigate_to_home)
        if browser_config.showBackButton:
            self.back_btn = QPushButton(msgconfig.ButtonText.backButton)
            self.back_btn.clicked.connect(self.browser.back)
        if browser_config.showForwardButton:
            self.forward_btn = QPushButton(msgconfig.ButtonText.forwardButton)
            self.forward_btn.clicked.connect(self.browser.forward)
        if browser_config.showRefreshButton:
            self.refresh_btn = QPushButton(msgconfig.ButtonText.refreshButton)
            self.refresh_btn.clicked.connect(self.browser.reload)

        # Layout for navigation bar
        nav_layout = QHBoxLayout()
        if browser_config.showBackButton: nav_layout.addWidget(self.back_btn)
        if browser_config.showForwardButton: nav_layout.addWidget(self.forward_btn)
        if browser_config.showRefreshButton: nav_layout.addWidget(self.refresh_btn)
        nav_layout.addWidget(self.url_bar)
        if browser_config.showHomeButton: nav_layout.addWidget(self.go_btn)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(nav_layout)
        main_layout.addWidget(self.browser)

        # Main widget
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Update URL bar when URL changes
        self.browser.urlChanged.connect(self.update_url_bar)
    def navigateToURL(self):
        if self.url_bar.text().startswith("pb:") and browser_config.pbUrlsEnabled:
            if self.url_bar.text() == "pb:exit" and browser_config.exitURLEnabled: exit()
            elif self.url_bar.text() == "pb:exit": self.browser.setUrl(QUrl(""))
            if self.url_bar.text() == "pb:about" and browser_config.aboutURLEnabled: pb_url.ShowAbout()
            elif self.url_bar.text() == "pb:about": self.browser.setUrl(QUrl(""))
            if self.url_bar.text() == "pb:policy" and browser_config.policyURLEnabled: pb_url.ShowPolicy()

        for url in browser_config.url_blocklist:
            if url in self.url_bar.text():
                CustomDialog.NewOkDialog(msgconfig.ErrorMsg.siteBlockedError[0], msgconfig.ErrorMsg.siteBlockedError[1])
                self.url_bar.setText("")
                return
        if not self.url_bar.text().startswith(("https://", "http://")):
            self.url_bar.setText("http://" + self.url_bar.text())
        self.browser.setUrl(QUrl(self.url_bar.text()))

    def navigate_to_home(self):
        
        self.browser.setUrl(QUrl(browser_config.homepage))

    def update_url_bar(self, q):
        self.url_bar.setText(q.toString())
        
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimpleBrowser()
    window.show()
    sys.exit(app.exec_())
