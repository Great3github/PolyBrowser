

from msg import cmdconfig, msgconfig
from dialog import CustomDialog
from browser_config import Config
from internal import pb_url
from time import sleep


from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QMessageBox, QDialog, QLabel,QDialogButtonBox
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl


import sys


class SimpleBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setGeometry(Config.windowDimensions[0], Config.windowDimensions[1], Config.windowDimensions[2], Config.windowDimensions[3])
        
        # Create browser widget
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl(Config.startingpage))
        if Config.runMode.lower() == "fullscreen": self.showFullScreen()
        if Config.runMode.lower() == "maximized": self.showMaximized()
        if Config.runMode.lower() == "minimized": self.showMinimized()
        if Config.runMode.lower() == "normal": self.showNormal()
        if Config.runMode.lower() not in ['normal', 'minimized', 'maximized', 'fullscreen']:
            CustomDialog.NewOkDialog("Error", msgconfig.ErrorMsg.invalidParamError)
            exit(1)
        # Create navigation bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigateToURL)
        self.url_bar.setDisabled(Config.urlBarDisabled)
        if Config.showHomeButton:
            self.go_btn = QPushButton(msgconfig.ButtonText.homeButton)
            self.go_btn.clicked.connect(self.navigate_to_home)
        if Config.showBackButton:
            self.back_btn = QPushButton(msgconfig.ButtonText.backButton)
            self.back_btn.clicked.connect(self.browser.back)
        if Config.showForwardButton:
            self.forward_btn = QPushButton(msgconfig.ButtonText.forwardButton)
            self.forward_btn.clicked.connect(self.browser.forward)
        if Config.showRefreshButton:
            self.refresh_btn = QPushButton(msgconfig.ButtonText.refreshButton)
            self.refresh_btn.clicked.connect(self.browser.reload)

        # Layout for navigation bar
        nav_layout = QHBoxLayout()
        if Config.showBackButton: nav_layout.addWidget(self.back_btn)
        if Config.showForwardButton: nav_layout.addWidget(self.forward_btn)
        if Config.showRefreshButton: nav_layout.addWidget(self.refresh_btn)
        nav_layout.addWidget(self.url_bar)
        if Config.showHomeButton: nav_layout.addWidget(self.go_btn)

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
        self.browser.loadStarted.connect(self.onLoadStarted)
        self.browser.loadFinished.connect(self.onLoadFinished)
    def navigateToURL(self):
        if self.url_bar.text().startswith("pb:") and Config.pbUrlsEnabled:
            if self.url_bar.text() == "pb:exit" and Config.exitURLEnabled: exit()
            elif self.url_bar.text() == "pb:exit": self.browser.setUrl(QUrl(""))
            if self.url_bar.text() == "pb:about" and Config.aboutURLEnabled: pb_url.ShowAbout()
            elif self.url_bar.text() == "pb:about": self.browser.setUrl(QUrl(""))
            if self.url_bar.text() == "pb:policy" and Config.policyURLEnabled: pb_url.ShowPolicy()
            elif self.url_bar.text() == "pb:policy": self.browser.setUrl(QUrl(""))

        for url in Config.url_blocklist:
            if url in self.url_bar.text():
                CustomDialog.NewOkDialog(msgconfig.ErrorMsg.siteBlockedError[0], msgconfig.ErrorMsg.siteBlockedError[1])
                self.url_bar.setText("")
                return
        if not self.url_bar.text().startswith(("https://", "http://")):
            self.url_bar.setText("http://" + self.url_bar.text())
        self.browser.setUrl(QUrl(self.url_bar.text()))

    def navigate_to_home(self):
        
        self.browser.setUrl(QUrl(Config.homepage))

    def update_url_bar(self, q):
        self.url_bar.setText(q.toString())
    def onLoadStarted(self):
        if Config.showRefreshButton:
            self.refresh_btn.setText("Loading...")
            self.refresh_btn.setDisabled(True)
        else:
            print("Started page loading...")
    def onLoadFinished(self):
        if Config.showRefreshButton:
            # self.refresh_btn.setText("Finished!")
            
            self.refresh_btn.setText("Refresh")
            self.refresh_btn.setDisabled(False)
        else:
            print("Finished page loading!")
        
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimpleBrowser()
    window.show()
    sys.exit(app.exec_())
